import pandas as pd
import numpy as np
import os

def process_pet_metadata(input_file, output_file):
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Helper function to normalize text
    def normalize_text(text):
        if pd.isna(text):
            return ""
        return str(text).lower()

    # Keyword lists for Heuristic Scoring
    energy_low = ["ít vận động", "đi dạo ngắn", "trong nhà"]
    energy_high = ["năng lượng cao", "chạy bộ", "hoạt bát", "làm việc"]

    space_apt = ["căn hộ", "nhà nhỏ", "chung cư"]
    space_garden = ["sân vườn", "không gian rộng", "trang trại"]

    grooming_easy = ["lông ngắn", "dễ chăm sóc"]
    grooming_hard = ["lông dài", "rụng nhiều", "chải lông thường xuyên"]

    kid_caution = ["không phù hợp trẻ nhỏ", "cảnh giác", "dữ"]
    kid_friendly = ["thân thiện", "quấn chủ", "hiền lành"]

    # --- Scoring Functions ---

    def get_score_energy(text):
        """
        Score 1 (Low): contains "ít vận động", "đi dạo ngắn", "trong nhà"
        Score 3 (High): contains "năng lượng cao", "chạy bộ", "hoạt bát", "làm việc"
        Default: 2
        """
        norm_text = normalize_text(text)
        # Prioritize high/specific matches if needed. 
        # Logic: If both exist, specific domain logic applies, but usually checking for 'High' traits implies high energy.
        # Let's check High first (3), then Low (1), else 2.
        for kw in energy_high:
            if kw in norm_text:
                return 3
        for kw in energy_low:
            if kw in norm_text:
                return 1
        return 2

    def get_score_space(text):
        """
        Score 1 (Apartment): contains "căn hộ", "nhà nhỏ", "chung cư"
        Score 3 (Garden): contains "sân vườn", "không gian rộng", "trang trại"
        Default: 2
        """
        norm_text = normalize_text(text)
        for kw in space_garden:
            if kw in norm_text:
                return 3
        for kw in space_apt:
            if kw in norm_text:
                return 1
        return 2

    def get_score_grooming(text):
        """
        Score 1 (Easy): contains "lông ngắn", "dễ chăm sóc"
        Score 3 (Hard): contains "lông dài", "rụng nhiều", "chải lông thường xuyên"
        Default: 2
        """
        norm_text = normalize_text(text)
        for kw in grooming_hard:
            if kw in norm_text:
                return 3
        for kw in grooming_easy:
            if kw in norm_text:
                return 1
        return 2

    def get_score_kid_friendly(text):
        """
        Score 0 (Caution): contains "không phù hợp trẻ nhỏ", "cảnh giác", "dữ"
        Score 1 (Friendly): contains "thân thiện", "quấn chủ", "hiền lành"
        Default: 1
        """
        norm_text = normalize_text(text)
        # If caution found -> 0
        for kw in kid_caution:
            if kw in norm_text:
                return 0
        # If friendly found -> 1, but default is also 1, so effectively returns 1.
        return 1

    def get_is_cat(row):
        """
        1: If 'tên giống loài' or description contains "Mèo"
        0: Else
        """
        breed = normalize_text(row.get('tên giống loài', ''))
        # Using 'cách chăm' as description source or if there is another description column.
        # Assuming 'cách chăm' acts as description based on context, or use available cols.
        # We will scan 'cách chăm' as well.
        desc = normalize_text(row.get('cách chăm', ''))
        
        if "mèo" in breed or "mèo" in desc:
            return 1
        return 0

    print("Processing columns...")
    
    # We expect 'cách chăm' mainly.
    if 'cách chăm' not in df.columns:
        print(f"Error: Column 'cách chăm' not found in {df.columns.tolist()}")
        # Check for similar names?
        return

    # Apply functions
    print("Calculating score_energy...")
    df['score_energy'] = df['cách chăm'].apply(get_score_energy)
    
    print("Calculating score_space...")
    df['score_space'] = df['cách chăm'].apply(get_score_space)
    
    print("Calculating score_grooming...")
    df['score_grooming'] = df['cách chăm'].apply(get_score_grooming)
    
    print("Calculating score_kid_friendly...")
    df['score_kid_friendly'] = df['cách chăm'].apply(get_score_kid_friendly)
    
    print("Determining is_cat...")
    df['is_cat'] = df.apply(get_is_cat, axis=1)

    print(f"Exporting to {output_file}...")
    # Use utf-8-sig for Vietnamese characters to display correctly in Excel
    df.to_csv(output_file, index=False, encoding='utf-8-sig') 
    print("Done!")

if __name__ == "__main__":
    # Default paths but allowing for local execution context
    input_path = os.path.join(os.getcwd(), "metadata.xlsx")
    output_path = os.path.join(os.getcwd(), "metadata_processed.csv")
    
    # Override if user specified A: absolute path and we are running elsewhere? 
    # Provided path: A:\NCKH_Web\PetAI\metadata.xlsx
    # We will prioritize current directory if it exists, else try the absolute path.
    
    target_input = "A:\\NCKH_Web\\PetAI\\metadata.xlsx"
    target_output = "A:\\NCKH_Web\\PetAI\\metadata_processed.csv"
    
    if os.path.exists(target_input):
        process_pet_metadata(target_input, target_output)
    elif os.path.exists("metadata.xlsx"):
        process_pet_metadata("metadata.xlsx", "metadata_processed.csv")
    else:
        print(f"File not found: {target_input} or metadata.xlsx in current dir.")
