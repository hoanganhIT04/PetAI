import pandas as pd
import os

# Thư mục gốc chứa dữ liệu
base_dir = r"A:\NCKH_Web\PetAI\ai\data"

# Danh sách chính xác 3 file kết quả bạn đã tải về từ Colab
files_to_merge = [
    os.path.join(base_dir, "result_metadata_part1.csv"),
    os.path.join(base_dir, "result_metadata_part2.csv"),
    os.path.join(base_dir, "result_metadata_part3.csv")
]

print("🚀 Bắt đầu gộp 3 file dữ liệu...")

try:
    # Đọc và gộp cả 3 file lại với nhau
    df_list = [pd.read_csv(file) for file in files_to_merge]
    final_df = pd.concat(df_list, ignore_index=True)

    # Đường dẫn file kết quả cuối cùng
    output_file = os.path.join(base_dir, "metadata_scored_final.csv")

    # Xuất ra file CSV (chuẩn utf-8-sig để không bị lỗi font tiếng Việt)
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"✅ Hợp nhất thành công! Tổng số dòng hiện có: {len(final_df)}")
    print(f"📁 File tổng được lưu tại: {output_file}")

except FileNotFoundError as e:
    print(f"❌ Lỗi: Không tìm thấy file. Hãy kiểm tra xem bạn đã copy đủ 3 file result_metadata_part(1,2,3).csv vào đúng thư mục chưa nhé.")
    print(f"Chi tiết lỗi: {e}")
except Exception as e:
    print(f"❌ Lỗi không xác định: {e}")