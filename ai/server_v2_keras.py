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

# ===== FASTAPI =====
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 cho test local luôn
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

# ===== STATIC =====
app.mount("/assets", StaticFiles(directory=ASSETS_PATH), name="assets")

# ===== LOAD MODELS =====
model_binary = tf.keras.models.load_model(MODEL_BINARY_PATH)
model = tf.keras.models.load_model(MODEL_PATH)

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

# ===== MODEL 1: BINARY =====
def check_animal(img):
    pred = model_binary.predict(img)[0][0]
    return pred  # >0.5 = non_animal

# ===== API =====
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        img = preprocess_image(image_bytes)

       # Model 1
        binary_pred = float(check_animal(img))

        if binary_pred > 0.5:
            return {
                "success": False,
                "message": "Ảnh không hợp lệ (không phải động vật)",
                "confidence": round(binary_pred * 100, 2)
            }

        # Model 2
        preds = model.predict(img)[0]
        max_conf = float(np.max(preds))   
        idx = int(np.argmax(preds))

        label = LABELS[str(idx)] if isinstance(LABELS, dict) else LABELS[idx]

        CONFIDENCE_THRESHOLD = 0.35
        # ===== RULE 1: confidence thấp =====
        if max_conf < CONFIDENCE_THRESHOLD:
            return {
                "success": False,
                "message": "Ảnh không hợp lệ (độ tin cậy thấp)",
                "confidence": round(max_conf * 100, 2)
            }

        # unknown 
        if label.lower() == "unknown":
            return {
                "success": False,
                "message": "Ảnh không hợp lệ (không xác định)",
                "confidence": round(max_conf * 100, 2)
            }

        # success
        return {
            "success": True,
            "class_id": idx,
            "breed": label,
            "confidence": round(max_conf * 100, 2)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ===== RUN =====
if __name__ == "__main__":
    uvicorn.run(
        "server_v2_keras:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )