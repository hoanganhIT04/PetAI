import pandas as pd

# Đường dẫn file
file_goc = r"A:\NCKH_Web\PetAI\ai\data\metadata.csv"
file_new = r"A:\NCKH_Web\PetAI\ai\data\metadata_scored_final.csv"

df_goc = pd.read_csv(file_goc)
df_new = pd.read_csv(file_new)

# Các cột điểm cần so sánh
score_cols = ['score_energy', 'score_space', 'score_grooming', 'score_kid_friendly']

print("🔍 ĐANG SO SÁNH SỰ THAY ĐỔI ĐIỂM SỐ GIỮA 2 FILE...\n")

# Tạo một danh sách để chứa các dòng có sự thay đổi
diff_rows = []

for i in range(len(df_new)):
    changes = {}
    has_change = False
    
    for col in score_cols:
        val_goc = df_goc.at[i, col] if col in df_goc.columns else "N/A"
        val_new = df_new.at[i, col]
        
        # Nếu giá trị khác nhau (hoặc từ N/A thành có số)
        if str(val_goc) != str(val_new):
            changes[col] = f"{val_goc} -> {val_new}"
            has_change = True
            
    if has_change:
        # Lấy tên loài để dễ nhận diện
        breed_name = df_new.at[i, 'loài'] if 'loài' in df_new.columns else f"Dòng {i}"
        changes['Loài'] = breed_name
        changes['Index'] = i
        diff_rows.append(changes)

# Hiển thị kết quả dưới dạng bảng
if diff_rows:
    df_diff = pd.DataFrame(diff_rows)
    # Sắp xếp cột cho dễ nhìn
    cols = ['Index', 'Loài'] + [c for c in score_cols if c in df_diff.columns]
    print(df_diff[cols].to_string(index=False))
    print(f"\n=> Tổng cộng có {len(diff_rows)} dòng đã được cập nhật điểm mới.")
else:
    print("✅ Không có sự khác biệt nào giữa 2 file.")