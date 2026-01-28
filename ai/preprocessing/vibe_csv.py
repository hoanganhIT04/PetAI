import pandas as pd
import os
import re

# ==========================================
# CONSTANTS & SCORING HEURISTICS
# ==========================================

ENERGY_KEYWORDS = {
    1: ["ít vận động", "đi dạo ngắn", "nằm", "lười", "thụ động", "ngủ nhiều", "hiền", "nhút nhát"],
    2: ["vận động nhẹ", "đi bộ", "trong nhà", "bình tĩnh"],
    3: ["hoạt bát", "trung bình", "nhanh nhẹn", "vui vẻ"],
    4: ["năng lượng cao", "chạy nhảy", "thể thao", "săn bắt", "kéo xe"],
    5: ["rất hiếu động", "không mệt mỏi", "cường độ cao", "bền bỉ", "vận động liên tục"]
}

SPACE_KEYWORDS = {
    1: ["căn hộ", "chung cư", "phòng nhỏ", "nhà nhỏ", "trong nhà"],
    2: ["nhà phố", "sân nhỏ"],
    3: ["sân vườn", "nhà rộng", "không gian thoáng"],
    4: ["sân rộng", "vườn lớn", "chạy nhảy"],
    5: ["trang trại", "đồng cỏ", "chuồng", "rất rộng"]
}

GROOMING_KEYWORDS = {
    1: ["lông ngắn", "dễ chăm sóc", "ít rụng"],
    2: ["chải hàng tuần", "rụng vừa"],
    3: ["lông trung bình", "chải thường xuyên"],
    4: ["lông dài", "rụng nhiều", "chải hàng ngày"],
    5: ["lông rất dài", "2 lớp lông", "spa thường xuyên", "rất khó chăm"]
}

# 1 = rất phù hợp trẻ em | 5 = không phù hợp
KID_KEYWORDS = {
    1: ["rất thân thiện", "yêu trẻ", "nhẹ nhàng", "hiền", "bảo mẫu"],
    2: ["thân thiện", "hòa đồng", "chơi cùng trẻ"],
    3: ["trung lập", "cần giám sát"],
    4: ["cảnh giác", "khó tính", "không thích bị trêu"],
    5: ["nguy hiểm", "dữ", "tấn công", "không phù hợp trẻ nhỏ"]
}

# ==========================================
# UTILS
# ==========================================

def normalize_text(text):
    if pd.isna(text):
        return ""
    return str(text).lower().strip()

def calculate_score(text, keyword_dict, default=3):
    norm = normalize_text(text)
    for score in [5, 4, 3, 2, 1]:
        for kw in keyword_dict.get(score, []):
            if kw in norm:
                return score
    return default
def parse_avg_range(text):
    if pd.isna(text):
        return None

    nums = re.findall(r"\d+\.?\d*", str(text))
    nums = [float(n) for n in nums]

    if len(nums) == 0:
        return None
    if len(nums) == 1:
        return nums[0]
    return sum(nums) / len(nums)
def calculate_size_index(weight, height, length,
                         avg_weight, avg_height, avg_length):
    if not all([weight, height, length, avg_weight, avg_height, avg_length]):
        return None

    w_ratio = weight / avg_weight
    h_ratio = height / avg_height
    l_ratio = length / avg_length

    # Trọng số: cân nặng > chiều cao > chiều dài
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

def process_csv(input_path, output_path):
    print(f"Reading {input_path} ...")

    df = pd.read_csv(input_path, header=0)

    # Drop dòng header phụ Excel
    df = df[df['STT'].notna()]
    df = df[df['tên giống loài'].notna()]

    desc_col = 'cách chăm'

    # ---------- SCORING ----------
    df['score_energy'] = df[desc_col].apply(lambda x: calculate_score(x, ENERGY_KEYWORDS))
    df['score_space'] = df[desc_col].apply(lambda x: calculate_score(x, SPACE_KEYWORDS))
    df['score_grooming'] = df[desc_col].apply(lambda x: calculate_score(x, GROOMING_KEYWORDS))
    df['score_kid_friendly'] = df[desc_col].apply(
        lambda x: calculate_score(x, KID_KEYWORDS, default=3)
    )

    # ---------- SIZE SCORING ----------
    df['avg_weight'] = df['cân nặng trung bình'].apply(parse_avg_range)
    df['avg_height'] = df['chiều cao trung bình'].apply(parse_avg_range)
    df['avg_length'] = df['chiều dài trung bình'].apply(parse_avg_range)

    # Trung bình toàn dataset làm chuẩn
    breed_avg_weight = df['avg_weight'].mean()
    breed_avg_height = df['avg_height'].mean()
    breed_avg_length = df['avg_length'].mean()

    df['size_index'] = df.apply(
        lambda r: calculate_size_index(
            r['avg_weight'],
            r['avg_height'],
            r['avg_length'],
            breed_avg_weight,
            breed_avg_height,
            breed_avg_length
        ),
        axis=1
    )

    df['score_size'] = df['size_index'].apply(map_size)


    # ---------- PRICE COLUMN FIX ----------
    cols = df.columns.tolist()
    if "giá cả trung bình" in cols:
        idx = cols.index("giá cả trung bình")
        if idx + 2 < len(cols):
            df.rename(columns={
                cols[idx]: 'giá có giấy tờ',
                cols[idx+1]: 'giá không giấy tờ',
                cols[idx+2]: 'giá quốc tế'
            }, inplace=True)

    # ---------- FINAL COLUMNS ----------
    final_cols = [
        'STT',
        'type',
        'tên giống loài',
        'tuổi thọ trung bình',
        'cân nặng trung bình',
        'chiều cao trung bình',
        'chiều dài trung bình',
        'cách chăm',
        'giá có giấy tờ',
        'giá không giấy tờ',
        'giá quốc tế',
        'score_energy',
        'score_space',
        'score_grooming',
        'score_kid_friendly',
        'score_size',
        'size_index'
    ]


    # tạo cột trống nếu thiếu
    for c in final_cols:
        if c not in df.columns:
            df[c] = ""

    df_final = df[final_cols]

    df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("Done ✔")

# ==========================================
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "metadata.csv")

    if os.path.exists(csv_path):
        process_csv(csv_path, csv_path)
    else:
        print("❌ metadata.csv not found")
