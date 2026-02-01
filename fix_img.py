import json
import os

FILE_PATH = r"frontend\src\data\pets_data.json"

# Load JSON
with open(FILE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Process data
for item in data:
    # 1. Capitalize first letter of each word in name
    if "name" in item and isinstance(item["name"], str):
        item["name"] = item["name"].title()

    # 2. Replace '-' with '_' in image_path
    if "image_path" in item and isinstance(item["image_path"], str):
        item["image_path"] = item["image_path"].replace("-", "_")

# Save back to file
with open(FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Đã cập nhật pets_data.json:")
print("- Name: Viết hoa chữ cái đầu")
print("- image_path: '-' → '_'")
