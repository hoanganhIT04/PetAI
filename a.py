import json
import os

# Đường dẫn file JSON
JSON_PATH = r"A:\NCKH_Web\PetAI\frontend\src\data\pets_data.json"

# Prefix mới cho image_path
NEW_PREFIX = "/assets/dog_images/"

def normalize_image_path(old_path: str) -> str:
    """
    Chuyển mọi kiểu path về:
    /assets/dog_images/xxx/yyy.jpg
    """
    if not old_path:
        return old_path

    # Chuẩn hóa dấu /
    path = old_path.replace("\\", "/")

    # Lấy phần sau dog_images/
    if "dog_images/" in path:
        relative = path.split("dog_images/")[-1]
        return NEW_PREFIX + relative

    # Trường hợp path chỉ là filename
    return NEW_PREFIX + path.lstrip("/")


with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Hỗ trợ cả list lẫn dict
if isinstance(data, list):
    items = data
elif isinstance(data, dict):
    items = data.values()
else:
    raise ValueError("JSON format không hợp lệ")

changed = 0

for pet in items:
    if "image_path" in pet:
        old = pet["image_path"]
        new = normalize_image_path(old)
        pet["image_path"] = new
        if old != new:
            changed += 1

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Đã cập nhật {changed} image_path")
