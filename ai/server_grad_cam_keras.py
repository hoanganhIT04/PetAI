from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io
import os
import cv2
import uuid

# ===== FASTAPI =====
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_BINARY_PATH = os.path.join(BASE_DIR, "model", "3", "model1", "model_binary.keras")
MODEL_PATH = os.path.join(BASE_DIR, "model", "3", "model2", "model_v2.keras")
LABEL_PATH = os.path.join(BASE_DIR, "label", "label_v2_keras.json")
ASSETS_PATH = os.path.join(BASE_DIR, "..", "frontend", "public", "assets")

os.makedirs(ASSETS_PATH, exist_ok=True)

# ===== STATIC =====
app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="assets")

# ===== LOAD MODEL =====
model_binary = tf.keras.models.load_model(MODEL_BINARY_PATH)
model = tf.keras.models.load_model(MODEL_PATH)

# 🔥 BUILD MODEL (FIX LỖI CHÍNH)
dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
# model.predict(dummy)

# ===== LOAD LABEL =====
with open(LABEL_PATH, "r", encoding="utf-8") as f:
    LABELS = json.load(f)

CONFIDENCE_THRESHOLD = 0.35

# ===== PREPROCESS =====
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ===== MODEL 1 =====
def check_animal(img):
    return model_binary.predict(img)[0][0]

# ===== GRAD-CAM =====
def make_gradcam_heatmap(img_array, model):
    base_model = model.layers[0]

    # 🔥 tìm conv layer cuối
    last_conv_layer = None
    for layer in reversed(base_model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv_layer = layer
            break

    if last_conv_layer is None:
        raise Exception("Không tìm thấy Conv layer")

    print("🔥 Grad-CAM using:", last_conv_layer.name)

    # 🔥 model chỉ lấy feature từ base_model
    grad_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=[last_conv_layer.output, base_model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, features = grad_model(img_array)

        # 🔥 forward qua classifier head
        x = features
        for layer in model.layers[1:]:
            x = layer(x)

        pred_index = tf.argmax(x[0])
        class_channel = x[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0)
    max_val = tf.reduce_max(heatmap)

    if max_val == 0:
        return None

    heatmap /= max_val
    return heatmap.numpy()

# ===== SAVE =====
def save_and_overlay_gradcam(original_bytes, heatmap):
    if heatmap is None:
        return None

    img = Image.open(io.BytesIO(original_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img)

    heatmap = cv2.resize(heatmap, (224, 224))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    filename = f"gradcam_{uuid.uuid4().hex}.jpg"
    save_path = os.path.join(ASSETS_PATH, filename)

    cv2.imwrite(save_path, superimposed)

    return f"/assets/{filename}"

# ===== API =====
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        img = preprocess_image(image_bytes)

        # STEP 1
        binary_pred = float(check_animal(img))
        if binary_pred > 0.5:
            return {
                "success": False,
                "message": "Không phải động vật",
                "confidence": round(binary_pred * 100, 2)
            }

        # STEP 2
        preds = model.predict(img)[0]
        max_conf = float(np.max(preds))
        idx = int(np.argmax(preds))

        label = LABELS[str(idx)] if isinstance(LABELS, dict) else LABELS[idx]

        if max_conf < CONFIDENCE_THRESHOLD:
            return {
                "success": False,
                "message": "Độ tin cậy thấp",
                "confidence": round(max_conf * 100, 2)
            }

        if label.lower() == "unknown":
            return {
                "success": False,
                "message": "Không xác định",
                "confidence": round(max_conf * 100, 2)
            }

        # ===== GRAD-CAM =====
        heatmap_url = None
        try:
            heatmap = make_gradcam_heatmap(img, model)
            heatmap_url = save_and_overlay_gradcam(image_bytes, heatmap)
        except Exception as e:
            print("⚠️ Grad-CAM lỗi:", e)

        return {
            "success": True,
            "class_id": idx,
            "breed": label,
            "confidence": round(max_conf * 100, 2),
            "heatmap": heatmap_url
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ===== RUN =====
if __name__ == "__main__":
    uvicorn.run(
        "server_grad_cam_keras:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )