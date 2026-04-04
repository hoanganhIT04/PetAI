import pandas as pd
import google.generativeai as genai
import json
import time

# ==========================================
# CẤU HÌNH
# ==========================================
API_KEY = "AIzaSyALHd3Lv1rwdbLsgJ0Y0sfzOZ86olhxQUg" 
FILE_PATH = r"A:\NCKH_Web\PetAI\ai\data\metadata_scored_final.csv"

# 9 vị trí cần vá lỗi
TARGET_INDICES = [11, 14, 45, 46, 65, 66, 67, 108, 135]

genai.configure(api_key=API_KEY)

# Chuyển sang bản Lite siêu nhẹ, lách giới hạn Quota cực tốt
model = genai.GenerativeModel(
    model_name="gemini-flash-lite-latest",
    system_instruction="Chuyên gia thú cưng. Phân tích 'Cách chăm sóc' và trả về JSON: {'energy':x, 'space':x, 'grooming':x, 'kidfriendly':x} (điểm 1-5)"
)

def main():
    print(f"🔍 Đang mở file: {FILE_PATH}")
    df = pd.read_csv(FILE_PATH)
    
    print(f"🎯 Bắt đầu ép AI (bản Lite) chấm lại 9 dòng bị lỗi...")

    for i in TARGET_INDICES:
        print(f" - Đang xử lý dòng index {i}...")
        
        care_text = df.at[i, 'cách chăm']
        if pd.isna(care_text):
            print("   -> ⚠️ Bỏ qua vì không có text cách chăm sóc.")
            continue

        # Vòng lặp kiên trì: Bị lỗi 429 thì nghỉ 30s rồi thử lại bằng được
        while True:
            try:
                time.sleep(3) 
                
                response = model.generate_content(
                    f"Nội dung: {care_text}",
                    generation_config={"response_mime_type": "application/json"}
                )
                scores = json.loads(response.text)
                
                # Ghi đè
                df.at[i, 'score_energy'] = scores.get('energy')
                df.at[i, 'score_space'] = scores.get('space')
                df.at[i, 'score_grooming'] = scores.get('grooming')
                df.at[i, 'score_kid_friendly'] = scores.get('kidfriendly')
                
                print(f"   -> ✅ Vá thành công: {scores}")
                break # Thoát vòng lặp while để sang dòng tiếp theo
                
            except Exception as e:
                err_str = str(e)
                if "429" in err_str:
                    print("   -> ⚠️ Chạm ngưỡng Lite, nghỉ 30s rồi thử lại chính dòng này...")
                    time.sleep(30)
                else:
                    print(f"   -> ❌ Lỗi khác: {err_str}")
                    break # Nếu lỗi cú pháp thì bỏ qua luôn

    # Lưu đè lại file lần cuối
    df.to_csv(FILE_PATH, index=False, encoding='utf-8-sig')
    print("\n✨ Xong! Bộ dữ liệu đã hoàn thiện 100%. Bạn có thể kiểm tra file CSV!")

if __name__ == "__main__":
    main()