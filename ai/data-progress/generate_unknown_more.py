import os
import random
import re
from PIL import Image

# 1. Đường dẫn thư mục nguồn (dạng list vì có 2 thư mục)
src_dirs = [
    r"D:\MyCode\nghienCuuKhoaHoc\PetAI\frontend\public\assets\data\data_model_1\animal\dog",
    r"D:\MyCode\nghienCuuKhoaHoc\PetAI\frontend\public\assets\data\data_model_1\animal\cat"
]

# Thư mục đích
dst_dir = r"D:\MyCode\nghienCuuKhoaHoc\PetAI\frontend\public\assets\data\data_model_2\unknown"

os.makedirs(dst_dir, exist_ok=True)

# 2. Tìm toàn bộ ảnh hợp lệ trong cả 2 thư mục
all_images = []
for src_dir in src_dirs:
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                all_images.append(os.path.join(root, file))

if not all_images:
    print("Không tìm thấy ảnh nào trong các thư mục nguồn!")
    exit()

print(f"Đã tìm thấy {len(all_images)} ảnh gốc từ thư mục dog và cat.")

# 3. Tìm index lớn nhất hiện có trong thư mục unknown để nối tiếp
existing_files = os.listdir(dst_dir)
max_idx = 0
for f in existing_files:
    # Tìm các file có định dạng unknown_XXXX.jpg
    match = re.search(r'unknown_(\d+)\.jpg', f)
    if match:
        idx = int(match.group(1))
        if idx > max_idx:
            max_idx = idx

print(f"Số thứ tự file lớn nhất hiện tại là {max_idx}. Sẽ bắt đầu lưu từ {max_idx + 1}...")

# 4. Thông số crop
total_needed = 400
TARGET_SIZE = 224
count = 0
current_idx = max_idx + 1

while count < total_needed:
    img_path = random.choice(all_images)
    
    try:
        with Image.open(img_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            width, height = img.size
            min_edge = min(width, height)
            
            if min_edge < 100:
                continue
                
            # Random kích thước khung cắt: 20% đến 50%
            crop_size = int(min_edge * random.uniform(0.2, 0.5))
            
            # Random tọa độ cắt
            x = random.randint(0, width - crop_size)
            y = random.randint(0, height - crop_size)
            
            # Cắt và Resize về 224x224
            cropped_img = img.crop((x, y, x + crop_size, y + crop_size))
            final_img = cropped_img.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
            
            # Lưu file với index mới
            save_name = f"copy_{current_idx:04d}.jpg"
            save_path = os.path.join(dst_dir, save_name)
            final_img.save(save_path, "JPEG", quality=95)
            
            count += 1
            current_idx += 1
            
            if count % 100 == 0:
                print(f"Đã tạo {count}/{total_needed} ảnh...")
                
    except Exception as e:
        # Bỏ qua nếu gặp file ảnh lỗi
        pass

print(f"Hoàn thành! Đã bổ sung thêm {total_needed} ảnh vào {dst_dir}.")
print(f"Tổng số ảnh trong thư mục unknown hiện tại là: {len(os.listdir(dst_dir))} ảnh.")