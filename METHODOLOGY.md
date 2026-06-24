# BÁO CÁO PHƯƠNG PHÁP XÂY DỰNG BỘ CHỈ SỐ ĐẶC TÍNH THÚ CƯNG (METHODOLOGY)

## 1. Tổng quan phương pháp luận
Trong dự án **PetAI**, để chuyển đổi các mô tả định tính (văn bản) về hành vi vật nuôi sang dữ liệu định lượng (số liệu) phục vụ cho thuật toán gợi ý, chúng tôi áp dụng phương pháp **Semantic Scoring (Chấm điểm ngữ nghĩa)** thông qua mô hình ngôn ngữ lớn (**LLM - Gemini**). 

Quy trình thực hiện bao gồm 03 giai đoạn chính:

### Giai đoạn 1: Thu thập và Tiền xử lý dữ liệu (Data Acquisition)
* **Nguồn dữ liệu:** Tổng hợp mô tả đặc tính loài từ các tổ chức uy tín (AKC, Wikipedia, cẩm nang thú cưng quốc tế).
* **Cấu trúc hóa:** Dữ liệu thô được chuẩn hóa vào cột `Cách chăm sóc` (Care Instruction) để làm cơ sở dữ liệu đầu vào cho quá trình trích xuất.

### Giai đoạn 2: Trích xuất đặc tính và Phân tích ngữ cảnh (Contextual Feature Extraction)
Sử dụng kỹ thuật Xử lý ngôn ngữ tự nhiên (NLP) để phân tích sâu nội dung văn bản thay vì chỉ lọc từ khóa đơn thuần:
* **Phân tích trọng số dương:** Xác định các cụm từ thể hiện đặc tính tích cực (Ví dụ: "hiền lành", "yêu trẻ em", "dễ thích nghi").
* **Phân tích trọng số âm:** Xác định các yếu tố rủi ro hoặc hạn chế (Ví dụ: "nhạy cảm", "dễ giật mình", "xu hướng tự vệ cao").
* **Xử lý phủ định:** Hệ thống có khả năng phân biệt giữa các sắc thái ngữ nghĩa phức tạp để tránh sai lệch điểm số (Ví dụ: phân biệt "thân thiện" và "không hoàn toàn thân thiện").

### Giai đoạn 3: Định lượng và Chuẩn hóa (Quantization & Normalization)
Các đánh giá định tính được chuyển đổi sang thang đo **Likert 5 mức độ (1-5)**:
* **Mức 1:** Đặc tính rất thấp / Không phù hợp.
* **Mức 5:** Đặc tính rất cao / Cực kỳ phù hợp.

Việc chuẩn hóa này giúp đồng bộ hóa dữ liệu cho các thuật toán so khớp (Matching System) và bộ lọc (Filtering) trên giao diện người dùng.

---

## 2. Phân tích thực nghiệm: Trường hợp giống chó Chihuahua
Để minh chứng cho tính logic của phương pháp, chúng ta phân tích chỉ số **Kid-friendly (Thân thiện với trẻ em)** của giống Chihuahua (đạt mức 2/5):

> **Căn cứ khoa học và logic trích xuất:**
> * **Về sinh học:** Văn bản mô tả xác nhận Chihuahua có "thể trạng nhỏ bé", "xương khớp nhạy cảm". Theo logic an toàn, một loài có nguy cơ chấn thương cao khi tiếp xúc với trẻ em hiếu động sẽ không được chấm điểm tối đa.
> * **Về tâm lý học loài:** Dữ liệu ghi nhận xu hướng "phản ứng tự vệ (Defensive Aggression)" và "hay sủa báo động". Điều này phản ánh mức độ kiên nhẫn thấp đối với các tác động bất ngờ từ trẻ nhỏ.
> * **Kết luận:** Điểm 2 không mang ý nghĩa tiêu cực mà phản ánh chính xác trạng thái: *"Cần có sự giám sát chặt chẽ của người lớn khi tương tác"*, đảm bảo tính an toàn cho cả vật nuôi và trẻ em.

---

## 3. Đối chứng dữ liệu (Comparative Analysis)
Sự khác biệt về điểm số được minh chứng trực tiếp từ ngữ liệu (Textual Evidence):

| Giống loài | Từ khóa đặc trưng (Input) | Điểm số (Output) | Logic hệ thống |
| :--- | :--- | :---: | :--- |
| **Chihuahua** | "Nhạy cảm", "cần xã hội hóa để tránh cắn" | **2** | Ưu tiên tính phản ứng tự vệ. |
| **Shih Tzu** | "Hiền lành", "phù hợp với gia đình có trẻ nhỏ" | **5** | Ưu tiên tính ôn hòa, kiên nhẫn. |

---

## 4. Kiểm chứng và Đảm bảo chất lượng (Quality Assurance)
Để đảm bảo độ chính xác vượt trên 85% cho dự án, quy trình kiểm soát chất lượng (QA) được thiết lập chặt chẽ:
* **Human-in-the-loop (HITL):** Các chỉ số sau khi được trích xuất tự động đã trải qua bước thẩm định thủ công bởi kiểm sát viên dữ liệu.
* **Xử lý Outliers:** Sử dụng Script chuyên dụng (`fix_outliers.py`) để điều chỉnh các giá trị bất thường dựa trên đặc tính dòng giống (Ví dụ: nắn chỉnh điểm không gian cho dòng chó săn Hound hoặc điểm thân thiện cho dòng Terrier).
* **Validation:** Dữ liệu cuối cùng được chuyển đổi sang định dạng JSON (`pets_data.json`) để phục vụ trực tiếp cho logic hiển thị và tính toán điểm Quiz trên Frontend.

---
**Kết luận:** Phương pháp Semantic Scoring kết hợp LLM giúp hệ thống **PetAI** loại bỏ tính cảm tính, thay thế bằng một bộ dữ liệu có cấu trúc, khách quan và có khả năng giải trình logic cao.