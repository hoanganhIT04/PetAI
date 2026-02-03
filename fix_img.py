import os
import re

FOLDER_PATH = r"A:\NCKH_Web\PetAI\frontend\public\assets\data\data_model_1\non_animal\electronic"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

pattern = re.compile(r"^electronic_\d+\.(jpg|jpeg|png|webp|bmp)$", re.IGNORECASE)

files = [
    f for f in os.listdir(FOLDER_PATH)
    if f.lower().endswith(IMAGE_EXTENSIONS) and not pattern.match(f)
]

files.sort()

# Tìm index lớn nhất hiện có
existing_indexes = []
for f in os.listdir(FOLDER_PATH):
    m = re.match(r"electronic_(\d+)\.", f, re.IGNORECASE)
    if m:
        existing_indexes.append(int(m.group(1)))

start_index = max(existing_indexes) + 1 if existing_indexes else 1

for idx, filename in enumerate(files, start=start_index):
    ext = os.path.splitext(filename)[1]
    new_name = f"electronic_{idx:03d}{ext}"

    old_path = os.path.join(FOLDER_PATH, filename)
    new_path = os.path.join(FOLDER_PATH, new_name)

    os.rename(old_path, new_path)

print(f"Đã đổi tên {len(files)} ảnh (không ghi đè).")
