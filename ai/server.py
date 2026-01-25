from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io
import os

# ===== PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dog.h5")
LABEL_PATH = os.path.join(BASE_DIR, "dog_label.json")

# ===== LOAD MODEL =====
model = tf.keras.models.load_model(MODEL_PATH)

# ===== LOAD LABEL =====
with open(LABEL_PATH, "r", encoding="utf-8") as f:
    LABELS = json.load(f)

# ===== FASTAPI =====
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== IMAGE PREPROCESS =====
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))  # PHẢI đúng size lúc train
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

CONFIDENCE_THRESHOLD = 0.35  # 35%
# ===== API =====
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        img = preprocess_image(image_bytes)

        preds = model.predict(img)[0]
        max_conf = float(np.max(preds))
        idx = int(np.argmax(preds))

        if max_conf < CONFIDENCE_THRESHOLD:
            return {
                "success": False,
                "message": "Ảnh không hợp lệ",
                "confidence": round(max_conf * 100, 2)
            }

        label = LABELS[str(idx)] if isinstance(LABELS, dict) else LABELS[idx]

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
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
