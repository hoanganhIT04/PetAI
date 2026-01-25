import pandas as pd
import numpy as np
import os
import re

# ==========================================
# CONSTANTS & SCORING HEURISTICS
# ==========================================

# 1. SCORE_ENERGY (1=Lazy -> 5=Hyperactive)
ENERGY_KEYWORDS = {
    1: ["ít vận động", "đi dạo ngắn", "nằm", "lười", "thụ động", "ngủ nhiều"],
    2: ["vận động nhẹ", "đi bộ", "trong nhà", "bình tĩnh"],
    3: ["hoạt bát", "trung bình", "nhanh nhẹn", "vui vẻ"],
    4: ["năng lượng cao", "chạy nhảy", "thể thao", "săn bắt", "kéo xe"],
    5: ["rất hiếu động", "không mệt mỏi", "cường độ cao", "bền bỉ", "vận động liên tục"]
}

# 2. SCORE_SPACE (1=Apartment -> 5=Farm/Huge)
SPACE_KEYWORDS = {
    1: ["căn hộ", "chung cư", "phòng nhỏ", "nhà nhỏ", "trong nhà"],
    2: ["nhà phố", "sân nhỏ", "trong nhà có sân"],
    3: ["sân vườn", "nhà rộng", "không gian thoáng"],
    4: ["sân rộng", "vườn lớn", "chạy nhảy"],
    5: ["trang trại", "đồng cỏ", "rất rộng", "bầy đàn"]
}

# 3. SCORE_GROOMING (1=Easy -> 5=Hard/Daily)
GROOMING_KEYWORDS = {
    1: ["lông ngắn", "dễ chăm sóc", "ít rụng", "thỉnh thoảng chải"],
    2: ["chải hàng tuần", "rụng vừa", "lông sát"],
    3: ["lông trung bình", "chải thường xuyên", "cắt tỉa định kỳ"],
    4: ["lông dài", "rụng nhiều", "chải hàng ngày", "dễ rối"],
    5: ["lông rất dài", "2 lớp lông", "nhu cầu cao", "spa thường xuyên", "rất khó chăm"]
}

# 4. SCORE_KID_FRIENDLY (1=Safe/Friendly -> 5=Risk/Unsuitable)
# Note: 1 = Highly suitable, 5 = Not suitable
KID_KEYWORDS = {
    1: ["rất thân thiện", "yêu trẻ", "nhẹ nhàng", "bảo mẫu", "cực kỳ hiền"],
    2: ["thân thiện", "hòa đồng", "dễ gần", "chơi cùng trẻ"],
    3: ["trung lập", "cần giám sát", "người lớn", "bình thường"],
    4: ["cảnh giác", "khó tính", "không thích bị trêu", "dễ cáu"],
    5: ["nguy hiểm", "không phù hợp trẻ nhỏ", "dữ dằn", "tấn công", "không nên nuôi cùng trẻ"]
}

def normalize_text(text):
    if pd.isna(text):
        return ""
    return str(text).lower().strip()

def calculate_score(text, keyword_dict, default=3):
    """
    Scans text for keywords in specific priority (5 -> 1 or 1 -> 5?).
    Usually assume 'extreme' keywords carry more weight.
    We will match from 5 down to 1 (or specific order).
    Let's check 5, then 4, then 1, then 2. 3 is usually fallback.
    """
    norm_text = normalize_text(text)
    
    # Priority check: Extreme values first
    for score in [5, 4, 1, 2]:
        for kw in keyword_dict[score]:
            if kw in norm_text:
                return score
    return default

def get_is_cat(row):
    """
    Determines if it is a cat based on 'type' or 'tên giống loài'.
    """
    # Explicit type column available?
    if 'type' in row and not pd.isna(row['type']):
        t = str(row['type']).lower()
        if 'cat' in t or 'mèo' in t:
            return 1
        return 0
    
    # Fallback to name/desc check
    name = normalize_text(row.get('tên giống loài', ''))
    desc = normalize_text(row.get('cách chăm', ''))
    if "mèo" in name or "mèo" in desc:
        return 1
    return 0

def process_csv(input_path, output_path):
    print(f"Reading {input_path}...")
    
    try:
        # Read with header=0 to get the first row as columns, but we know row 2 (index 1) is trash.
        # Actually in user's file:
        # Line 1: STT, tên giống loài... (Header)
        # Line 2: ,,,, có giấy tờ... (Subheader)
        # Line 3: Data...
        
        # We read header=0.
        df = pd.read_csv(input_path, header=0)
        
        # Drop the row with index 0 (which corresponds to line 2 in file, the subheader junk)
        # Check if row 0 is indeed the subheader (starts with NaN or empty)
        # Actually let's just filter.
        
        # We need to standardize columns.
        cols = df.columns.tolist()
        print(f"Original columns: {cols}")
        
        # Remove the junk row if it exists (usually row 0 if header=0)
        # We inspect the 'STT' column. If it's NaN or empty, drop.
        df = df[df['STT'].notna()]
        # Also drop rows where 'tiếng giống loài' is NaN
        df = df[df['tên giống loài'].notna()]
        
        # Ensure we don't drop valid data. 
        # The subheader often has NaNs in STT.
        
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Processing {len(df)} rows...")

    # --- SCORING ---
    desc_col = 'cách chăm'
    
    df['score_energy'] = df[desc_col].apply(lambda x: calculate_score(x, ENERGY_KEYWORDS, default=3))
    df['score_space'] = df[desc_col].apply(lambda x: calculate_score(x, SPACE_KEYWORDS, default=3))
    df['score_grooming'] = df[desc_col].apply(lambda x: calculate_score(x, GROOMING_KEYWORDS, default=3))
    df['score_kid_friendly'] = df[desc_col].apply(lambda x: calculate_score(x, KID_KEYWORDS, default=1)) # Default 1 (Friendly) if unspecified? Or 3? Let's use 3 (Neutral) safe. User said 1=Very Friendly. Let's default 2 or 3.
    # User said: "1 = very low / very easy / highly suitable".
    # If no keywords found, "2" (Friendly) is a reasonable safe guess for most dogs/cats unless specified otherwise.
    # Actually, let's stick to 3 (Neutral) to be scientifically safe.
    
    # Fix 'is_cat' logic
    # Check if 'type' column exists, if not create/infer
    if 'type' not in df.columns:
        df['type'] = 'Dog' # Default
        
    # Re-evaluate is_cat ensuring correctness
    df['is_cat'] = df.apply(get_is_cat, axis=1)
    
    # Update 'type' column to be explicit 'Cat' or 'Dog' based on is_cat
    df['type'] = df['is_cat'].apply(lambda x: 'Cat' if x == 1 else 'Dog')

    # --- COLUMN ORDERING ---
    # Required: STT, type, tên giống loài, tuổi thọ trung bình, cách chăm, giá có giấy tờ, giá không giấy tờ, giá quốc tế, 
    # score_energy, score_space, score_grooming, score_kid_friendly, is_cat
    
    # We need to map existing price columns.
    # The original CSV header might be:
    # STT, tên giống loài, tuổi thọ trung bình, cách chăm, giá cả trung bình, Unnamed: 5, Unnamed: 6...
    # Because of the merged header row in Excel/CSV conversion.
    # We need to be careful with column mapping.
    
    # Let's check typical column indices if names are messed up.
    # Assuming the user provided `convert_pets.js` logic was working, the columns were 0,1,2,3,4,5,6...
    # 0: STT
    # 1: Name
    # 2: Lifespan
    # 3: Care
    # 4: Price Paper (was "giá cả trung bình" in header but data is in col 4)
    # 5: Price No Paper (Unnamed 5)
    # 6: Price Intl (Unnamed 6)
    
    # Let's rename columns safely if they exist by index range
    if len(df.columns) >= 7:
        # Create a clean map
        # We'll just assign the array back carefully.
        # But we added score cols.
        pass

    # Ensure required columns exist, fill if missing
    required_map = {
        'STT': 'STT',
        'type': 'type',
        'tên giống loài': 'tên giống loài',
        'tuổi thọ trung bình': 'tuổi thọ trung bình',
        'cách chăm': 'cách chăm',
        # Prices are tricky, relying on index might be safer if headers are messed up
    }
    
    # HACK: If headers are "giá cả trung bình", "Unnamed: 5", "Unnamed: 6"
    # Rename them explicitly
    cols = df.columns.tolist()
    if "giá cả trung bình" in cols:
        idx = cols.index("giá cả trung bình")
        df.rename(columns={
            cols[idx]: 'giá có giấy tờ',
            cols[idx+1]: 'giá không giấy tờ',
            cols[idx+2]: 'giá quốc tế'
        }, inplace=True)
    
    # Select and Reorder
    final_cols = [
        'STT', 'type', 'tên giống loài', 'tuổi thọ trung bình', 'cách chăm',
        'giá có giấy tờ', 'giá không giấy tờ', 'giá quốc tế',
        'score_energy', 'score_space', 'score_grooming', 'score_kid_friendly',
        'is_cat'
    ]
    
    # Create missing columns with empty/default
    for c in final_cols:
        if c not in df.columns:
            df[c] = ""
            
    df_final = df[final_cols]
    
    # Clean STT to be integer
    # df_final['STT'] = range(1, len(df_final) + 1)
    
    print(f"Exporting to {output_path}...")
    df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(current_dir, "dog.csv")
    
    if os.path.exists(input_csv):
        process_csv(input_csv, input_csv) # Overwrite
    else:
        print("dog.csv not found in current directory.")
