import os
from PIL import Image
from pathlib import Path


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
DATA_DIR = FRONTEND_DIR / "public/assets/data"

BASE_DIR = DATA_DIR / "data_model_1/animal"
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

for folder_name in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.isdir(folder_path):
        continue

    images = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(IMAGE_EXTS)
    ]

    images.sort()

    # ===== PHASE 1: đổi tên tạm =====
    temp_files = []
    for i, img_name in enumerate(images):
        old_path = os.path.join(folder_path, img_name)
        temp_name = f"__tmp__{i}{os.path.splitext(img_name)[1]}"
        temp_path = os.path.join(folder_path, temp_name)
        os.rename(old_path, temp_path)
        temp_files.append(temp_path)

    # ===== PHASE 2: đổi tên chuẩn + convert =====
    for idx, temp_path in enumerate(temp_files, start=1):
        new_name = f"{folder_name}_{idx:03d}.jpg"
        new_path = os.path.join(folder_path, new_name)

        ext = os.path.splitext(temp_path)[1].lower()

        try:
            if ext == ".jpg":
                os.rename(temp_path, new_path)
            else:
                img = Image.open(temp_path).convert("RGB")
                img.save(new_path, "JPEG", quality=95)
                os.remove(temp_path)

            print(f"✅ {os.path.basename(new_path)}")

        except Exception as e:
            print(f"❌ Lỗi {temp_path}: {e}")

    print(f"🔥 DONE folder {folder_name} ({len(temp_files)} ảnh)")
