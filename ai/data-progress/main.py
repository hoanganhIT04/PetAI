import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PetAI Data Progress API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== CONFIG ==================
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

# ===== PATH CONFIG =====
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] / "frontend"

MODEL_1_ANIMAL = BASE_DIR / "public/assets/data/data_model_1/animal"
MODEL_1_NON_ANIMAL = BASE_DIR / "public/assets/data/data_model_1/non_animal"
MODEL_2_BASE = BASE_DIR / "public/assets/data/data_model_2"



# ================== HELPERS ==================
def count_images(folder_path: str) -> int:
    """Count all image files (recursive)"""
    if not os.path.exists(folder_path):
        return 0

    total = 0
    for root, _, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith(IMAGE_EXTS):
                total += 1
    return total


def count_detail_by_folder(base_path: str):
    """Count images per sub-folder"""
    detail = []
    total = 0

    if not os.path.exists(base_path):
        return {"total": 0, "detail": []}

    for name in sorted(os.listdir(base_path)):
        folder_path = os.path.join(base_path, name)

        if not os.path.isdir(folder_path):
            continue

        count = count_images(folder_path)
        total += count

        detail.append({
            "name": name,
            "count": count
        })

    return {
        "total": total,
        "detail": detail
    }


def count_model_2():
    """Count breed classes & unknown"""
    breed_total = 0
    unknown_total = 0
    breed_folders = 0
    breed_detail = []

    if not os.path.exists(MODEL_2_BASE):
        return {
            "breed_total": 0,
            "breed_folders": 0,
            "unknown": 0,
            "breed_detail": []
        }

    for name in sorted(os.listdir(MODEL_2_BASE)):
        folder_path = os.path.join(MODEL_2_BASE, name)

        if not os.path.isdir(folder_path):
            continue

        count = count_images(folder_path)

        if name.lower() == "unknown":
            unknown_total = count
        else:
            breed_total += count
            breed_folders += 1
            breed_detail.append({
                "name": name,
                "count": count
            })

    return {
        "breed_total": breed_total,
        "breed_folders": breed_folders,
        "unknown": unknown_total,
        "breed_detail": breed_detail
    }


# ================== API ==================
@app.get("/data-progress")
def data_progress():
    model_1_animal = count_detail_by_folder(MODEL_1_ANIMAL)
    model_1_non_animal = count_detail_by_folder(MODEL_1_NON_ANIMAL)
    model_2 = count_model_2()

    return {
        "model_1": {
            "animal": {
                "current": model_1_animal["total"],
                "target": 2000,
                "detail": model_1_animal["detail"]
            },
            "non_animal": {
                "current": model_1_non_animal["total"],
                "target": 2000,
                "detail": model_1_non_animal["detail"]
            }
        },
        "model_2": {
            "breed": {
                "current": model_2["breed_total"],
                "target": 25000,
                "num_classes": model_2["breed_folders"],
                "detail": model_2["breed_detail"]
            },
            "unknown": {
                "current": model_2["unknown"],
                "target": 3000
            }
        }
    }
