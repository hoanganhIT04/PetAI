import pandas as pd
import numpy as np
import os

# Đường dẫn đầy đủ đến file gốc
input_file = r"A:\NCKH_Web\PetAI\ai\data\metadata.csv"

# Kiểm tra xem file có tồn tại không trước khi đọc
if not os.path.exists(input_file):
    print(f"❌ Không tìm thấy file tại: {input_file}")
    print("👉 Hãy kiểm tra lại xem file có đúng ở thư mục 'ai/data/' không nhé!")
else:
    # Đọc dữ liệu
    df = pd.read_csv(input_file)

    # Chia làm 3 phần
    # Lưu ý: Với pandas mới, dùng np.array_split là chuẩn nhất
    df_parts = np.array_split(df, 3)

    # Lưu 3 file vào cùng folder 'ai/data/'
    output_dir = os.path.dirname(input_file)
    for i, part in enumerate(df_parts):
        part_name = f"metadata_part{i+1}.csv"
        full_output_path = os.path.join(output_dir, part_name)
        part.to_csv(full_output_path, index=False, encoding='utf-8-sig')
        print(f"✅ Đã tạo: {full_output_path}")