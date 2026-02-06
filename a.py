import os

FOLDER_PATH = r"A:\NCKH_Web\PetAI\frontend\public\assets\data\data_model_2\lykoi"
PREFIX = "lykoi"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

files = [
    f for f in os.listdir(FOLDER_PATH)
    if f.lower().endswith(IMAGE_EXTENSIONS)
]

files.sort()  # giữ thứ tự ổn định

for idx, filename in enumerate(files, start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"{PREFIX}_{idx}{ext}"

    old_path = os.path.join(FOLDER_PATH, filename)
    new_path = os.path.join(FOLDER_PATH, new_name)

    os.rename(old_path, new_path)

print(f"Đã đổi tên {len(files)} ảnh trong folder {PREFIX}.")
