import pandas as pd
import os
import re

# ==========================================
# UTILS (Lấy từ vibe_csv.py)
# ==========================================

def parse_avg_range(text):
    if pd.isna(text):
        return None
    # Tìm tất cả các số (bao gồm cả số thập phân)
    nums = re.findall(r"\d+\.?\d*", str(text))
    nums = [float(n) for n in nums]

    if len(nums) == 0:
        return None
    if len(nums) == 1:
        return nums[0]
    # Trả về trung bình cộng của khoảng (ví dụ: "1.5 - 3 kg" -> 2.25)
    return sum(nums) / len(nums)

def calculate_size_index(weight, height, length, 
                         avg_weight_dataset, avg_height_dataset, avg_length_dataset):
    if not all([weight, height, length, avg_weight_dataset, avg_height_dataset, avg_length_dataset]):
        return None

    # Tính tỷ lệ so với trung bình của cả tập dữ liệu
    w_ratio = weight / avg_weight_dataset
    h_ratio = height / avg_height_dataset
    l_ratio = length / avg_length_dataset

    # Trọng số: cân nặng (40%), chiều cao (30%), chiều dài (30%)
    return 0.4 * w_ratio + 0.3 * h_ratio + 0.3 * l_ratio

def map_size(index):
    if index is None:
        return ""
    if index < 0.85:
        return "small"
    elif index <= 1.15:
        return "medium"
    else:
        return "large"

# ==========================================
# MAIN PROCESS
# ==========================================

def update_size_scores(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return

    print(f"Reading {file_path} ...")
    df = pd.read_csv(file_path)

    # Đảm bảo các dòng dữ liệu hợp lệ
    df = df[df['tên giống loài'].notna()].copy()

    # 1. Tính toán giá trị trung bình thô cho từng dòng để làm cơ sở tính toán
    temp_weight = df['cân nặng trung bình'].apply(parse_avg_range)
    temp_height = df['chiều cao trung bình'].apply(parse_avg_range)
    temp_length = df['chiều dài trung bình'].apply(parse_avg_range)

    # 2. Tính trung bình của toàn bộ dataset để làm mốc chuẩn (baseline)
    breed_avg_weight = temp_weight.mean()
    breed_avg_height = temp_height.mean()
    breed_avg_length = temp_length.mean()

    print(f"Dataset Averages -> Weight: {breed_avg_weight:.2f}, Height: {breed_avg_height:.2f}, Length: {breed_avg_length:.2f}")

    # 3. Tính size_index cho từng loài
    df['size_index'] = df.apply(
        lambda r: calculate_size_index(
            parse_avg_range(r['cân nặng trung bình']),
            parse_avg_range(r['chiều cao trung bình']),
            parse_avg_range(r['chiều dài trung bình']),
            breed_avg_weight,
            breed_avg_height,
            breed_avg_length
        ),
        axis=1
    )

    # 4. Gán nhãn score_size (small/medium/large) dựa trên index
    df['score_size'] = df['size_index'].apply(map_size)

    # Lưu lại file (giữ nguyên các cột score khác đã có)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Done ✔ Đã cập nhật size_index và score_size vào {file_path}")

if __name__ == "__main__":
    # Xác định đường dẫn file metadata_scored_final.csv
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir) # Vào thư mục ai
    target_csv = os.path.join(project_root, "data", "metadata_scored_final.csv")

    update_size_scores(target_csv)
