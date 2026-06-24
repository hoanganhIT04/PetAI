import pandas as pd
import google.generativeai as genai
import json
import time
import os
from tqdm import tqdm

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "AIzaSyC3OaMzL4W2lp0oydeEnv7i_gm_MiXVjkY" 
INPUT_FILE = r"ai/data/metadata.csv"
OUTPUT_FILE = r"ai/data/metadata_scored.csv"

genai.configure(api_key=API_KEY)

# Kiểm tra danh sách model khả dụng và chọn cái tốt nhất
print("🔍 Đang kiểm tra các model bạn có quyền truy cập...")
available_models = [m.name.split('/')[-1] for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# Ưu tiên các bản đời mới (2.5 -> 2.0 -> 1.5)
if "gemini-2.5-flash" in available_models:
    MODEL_NAME = "gemini-2.5-flash"
    SAFE_SLEEP = 13 # Hạn mức 5 RPM (60/5 = 12s + 1s dự phòng)
elif "gemini-2.0-flash" in available_models:
    MODEL_NAME = "gemini-2.0-flash"
    SAFE_SLEEP = 13
elif "gemini-1.5-flash" in available_models:
    MODEL_NAME = "gemini-1.5-flash"
    SAFE_SLEEP = 5 # Hạn mức 15 RPM
else:
    MODEL_NAME = available_models[0]
    SAFE_SLEEP = 15

print(f"🎯 Đã chọn model: {MODEL_NAME} | Độ trễ an toàn: {SAFE_SLEEP}s")

SYSTEM_PROMPT = """
Bạn là chuyên gia hành vi động vật. Phân tích "Cách chăm sóc" và chấm điểm 1-5 cho:
- energy (1:Lười, 5:Năng động)
- space (1:Nhà nhỏ, 5:Sân vườn)
- grooming (1:Dễ chăm, 5:Cần spa)
- kidfriendly (1:Hiền, 5:Cảnh giác)
TRẢ VỀ DUY NHẤT JSON: {"energy":x, "space":x, "grooming":x, "kidfriendly":x}
"""

model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)

def get_scores_with_retry(care_text):
    if not care_text or pd.isna(care_text): return None

    while True:
        try:
            response = model.generate_content(
                f"Nội dung: {care_text}",
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            err_str = str(e)
            if "429" in err_str:
                print(f"\n⚠️ Chạm ngưỡng giới hạn quota. Nghỉ 70s để reset...")
                time.sleep(70)
                continue 
            else:
                print(f"\n❌ Lỗi API: {err_str}")
                return None

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Không tìm thấy file: {INPUT_FILE}")
        return
    
    df = pd.read_csv(INPUT_FILE)

    # Khởi tạo cột mới nếu chưa có
    for col in ['score_energy', 'score_space', 'score_grooming', 'score_kid_friendly']:
        if col not in df.columns: df[col] = None

    mask = df['cách chăm'].notna()
    indices = df[mask].index

    print(f"🚀 Bắt đầu xử lý {len(indices)} loài vật...")

    for i in tqdm(indices, desc="Standardizing"):
        # Nghỉ trước khi gọi request (để đảm bảo không bị 429 ngay lập tức)
        time.sleep(SAFE_SLEEP)
        
        scores = get_scores_with_retry(df.at[i, 'cách chăm'])

        if scores:
            df.at[i, 'score_energy'] = scores.get('energy')
            df.at[i, 'score_space'] = scores.get('space')
            df.at[i, 'score_grooming'] = scores.get('grooming')
            df.at[i, 'score_kid_friendly'] = scores.get('kidfriendly')

        # Lưu checkpoint thường xuyên
        if i % 2 == 0:
            df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n✨ Xong! Dữ liệu đã được chuẩn hóa AI tại: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()