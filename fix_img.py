import os
import re

FOLDER_PATH = r"A:\NCKH_Web\PetAI\frontend\public\assets\data\data_model_1\animal\cat"  # Thay đổi đường dẫn đến thư mục chứa ảnh của bạn
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

# Format chuẩn cần đạt: unknown_1.jpg
pattern = re.compile(r"^cat_\d+\.(jpg|jpeg|png|webp|bmp)$", re.IGNORECASE)

# Lấy tất cả file ảnh CHƯA đúng format
files = [
    f for f in os.listdir(FOLDER_PATH)
    if f.lower().endswith(IMAGE_EXTENSIONS) and not pattern.match(f)
]

files.sort()

# Lấy index đã tồn tại (theo format mới)
existing_indexes = []
for f in os.listdir(FOLDER_PATH):
    m = re.match(r"cat_(\d+)\.", f, re.IGNORECASE)
    if m:
        existing_indexes.append(int(m.group(1)))

start_index = max(existing_indexes) + 1 if existing_indexes else 1

# Rename
for idx, filename in enumerate(files, start=start_index):
    ext = os.path.splitext(filename)[1].lower()
    new_name = f"cat_{idx}{ext}"

    old_path = os.path.join(FOLDER_PATH, filename)
    new_path = os.path.join(FOLDER_PATH, new_name)

    os.rename(old_path, new_path)

print(f"Đã đổi tên {len(files)} ảnh → format cat_x.jpg")