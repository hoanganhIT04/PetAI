# CƠ CHẾ HOẠT ĐỘNG CỦA THUẬT TOÁN GỢI Ý THÚ CƯNG (PET MATCHING ALGORITHM)

## 1. Tổng quan kiến trúc hệ thống (Overall Pipeline)
Hệ thống gợi ý của dự án PetAI hoạt động dựa trên mô hình **Vector Space Modeling** (Mô hình Không gian Vectơ). Thay vì sử dụng các cấu trúc điều kiện `if/else` tĩnh, hệ thống số hóa cả nhu cầu của người dùng và đặc tính của vật nuôi thành các tọa độ trong không gian đa chiều. 

Quá trình này trải qua 5 giai đoạn cốt lõi:
1. **Thu thập (Input):** Tiếp nhận dữ liệu cấu hình từ người dùng thông qua bài khảo sát (Quiz).
2. **Vectơ hóa (Vectorization):** Chuyển đổi các lựa chọn định tính thành một vectơ đặc trưng trong không gian $n$-chiều (với $n$ là số lượng tiêu chí đánh giá).
3. **Lọc thô (Hard-filtering):** Áp dụng các ràng buộc cứng để loại bỏ các trường hợp vi phạm điều kiện tiên quyết (như an toàn, phúc lợi động vật).
4. **Tính toán độ tương đồng (Weighted Euclidean Distance):** Đo lường khoảng cách giữa vectơ nhu cầu của người dùng và vectơ đặc tính của từng loài.
5. **Xếp hạng & Giải thích (Ranking & XAI):** Chuẩn hóa khoảng cách thành điểm phần trăm (%), sắp xếp và trích xuất lý do gợi ý (Explainable AI).

---

## 2. Kỹ thuật lọc thô (Hard-filters) - Đảm bảo tính khả thi
Trong kỹ thuật phần mềm, đây được gọi là **Ràng buộc cứng (Hard Constraints)**. Thuật toán tiến hành cắt tỉa (pruning) tập dữ liệu ngay từ đầu nhằm tiết kiệm tài nguyên tính toán (CPU) và bảo vệ trải nghiệm người dùng thực tế:

* **Ràng buộc Không gian (Space):** Ngăn chặn việc vi phạm phúc lợi động vật. 
  * *Logic:* Nếu người dùng ở không gian `Nhỏ (1)`, loại bỏ lập tức các loài yêu cầu không gian `Rộng (>= 4)` (VD: Golden Retriever, Husky).
* **Ràng buộc An toàn (Kid-friendly):** Đảm bảo an toàn tuyệt đối cho gia đình có trẻ nhỏ.
  * *Logic:* Nếu người dùng yêu cầu thú cưng `Rất hiền (1)`, loại bỏ các giống loài có bản tính hung dữ hoặc điểm thân thiện thấp `(<= 2)`.

---

## 3. Tiêu chí và Trọng số (Matching Weights)
Để giải quyết bài toán "Không phải tiêu chí nào cũng quan trọng như nhau", thuật toán sử dụng một ma trận trọng số. Sự can thiệp này giúp cá nhân hóa kết quả một cách tự nhiên hơn:

* `energy` (Năng lượng) - **Trọng số 2.0**: Yếu tố then chốt nhất quyết định sự hòa hợp lâu dài.
* `kid_friendly` (Thân thiện trẻ em) - **Trọng số 1.8**: Ưu tiên cao về mặt an toàn.
* `space` (Không gian sống) - **Trọng số 1.5**: Điều kiện vật chất để duy trì sự sống.
* `grooming` (Chăm sóc lông) - **Trọng số 1.0**: Yếu tố phụ, phụ thuộc vào ngưỡng chịu đựng cá nhân.

---

## 4. Thuật toán cốt lõi: Khoảng cách Euclid có trọng số
Thuật toán sử dụng hàm tính toán khoảng cách Euclid có trọng số để đo lường sự khác biệt giữa Vectơ Người dùng ($U$) và Vectơ Thú cưng ($P$).

**Công thức toán học:**
$$d(U, P) = \sqrt{\sum_{i=1}^{n} w_i (U_i - P_i)^2}$$

*Trong đó:*
* $w_i$: Trọng số của tiêu chí thứ $i$.
* $U_i, P_i$: Điểm của tiêu chí thứ $i$ tương ứng của người dùng và thú cưng.

**Tại sao áp dụng bình phương hiệu số $(U_i - P_i)^2$?**
Việc bình phương sẽ khuếch đại sai số. Nhờ đó, thuật toán sẽ "phạt rất nặng" những loài thú cưng có một đặc điểm hoàn toàn trái ngược với mong muốn của người dùng, trong khi những loài chỉ sai lệch nhỏ sẽ ít bị ảnh hưởng hơn.

**Chuẩn hóa điểm số (Score Normalization):**
Khoảng cách $d$ được ánh xạ về thang điểm phần trăm ($100\%$) thông qua hàm phân thức:
$$Score = \frac{100}{1 + d \times 0.2}$$
* Hệ số `0.2` đóng vai trò là hệ số làm mượt (smoothing factor), giúp biểu đồ điểm số giảm độ dốc, tránh việc điểm số tụt quá nhanh khi có sự sai lệch nhẹ.

---

## 5. Ví dụ minh họa thực tế (Case Study)

Giả sử hệ thống đang xử lý dữ liệu với 4 tiêu chí: `[Năng lượng, Không gian, Chăm sóc, Thân thiện]`.

**1. Dữ liệu đầu vào:**
* **Người dùng ($U$):** Ở căn hộ nhỏ (Không gian: 1), các tiêu chí khác ở mức trung bình khá.
  * Vectơ $U = [3, 1, 3, 4]$
* **Thú cưng A (Chó Husky):** Rất hiếu động và cần không gian cực lớn.
  * Vectơ $P_A = [5, 5, 4, 3]$
* **Thú cưng B (Mèo Anh lông ngắn):** Trầm tính, không gian nhỏ, dễ chăm sóc.
  * Vectơ $P_B = [2, 2, 3, 4]$

**2. Bước 1: Áp dụng Hard-filters**
* Kiểm tra thú cưng A (Husky): Không gian của người dùng = 1. Mức yêu cầu của Husky = 5 ($\ge 4$). 
* **Kết quả:** Thú cưng A bị **loại bỏ** ngay lập tức, bỏ qua bước tính toán phức tạp.

**3. Bước 2: Tính toán cho Thú cưng B (Mèo Anh lông ngắn)**
Áp dụng công thức Euclid có trọng số tương ứng:
* Sai lệch Năng lượng: $2.0 \times (3 - 2)^2 = 2.0$
* Sai lệch Không gian: $1.5 \times (1 - 2)^2 = 1.5$
* Sai lệch Chăm sóc: $1.0 \times (3 - 3)^2 = 0$
* Sai lệch Thân thiện: $1.8 \times (4 - 4)^2 = 0$

=> Tổng bình phương độ lệch = $2.0 + 1.5 + 0 + 0 = 3.5$
=> Khoảng cách $d = \sqrt{3.5} \approx 1.87$

**4. Bước 3: Chuẩn hóa & Xếp hạng**
* Tính điểm tương đồng: 
  $$Score = \frac{100}{1 + 1.87 \times 0.2} = \frac{100}{1.374} \approx 72.7\%$$
* Thú cưng B đạt độ tương thích **73%** và được đưa vào tập kết quả. 

**5. Bước 4: Explainable AI (Trích xuất lý do)**
Hệ thống quét lại các tiêu chí có sai lệch $\le 1$.
* Sai lệch Chăm sóc ($|3 - 3| = 0$) $\le 1$ $\rightarrow$ Gắn nhãn: *"Chăm sóc phù hợp"*.
* Sai lệch Thân thiện ($|4 - 4| = 0$) $\le 1$ $\rightarrow$ Gắn nhãn: *"Thân thiện gia đình"*.

---

## 6. Kết luận
Kiến trúc thuật toán Pet Matching là sự giao thoa hiệu quả giữa **Toán học định lượng** (Weighted Euclidean Distance) và **Logic định tính** (Hard Filters). Cách tiếp cận này giúp dự án PetAI không chỉ đạt được hiệu suất tính toán tối ưu (Time Complexity tốt do đã cắt tỉa dữ liệu ngay từ đầu) mà còn đảm bảo các kết quả đầu ra luôn mang giá trị thực tiễn và nhân văn đối với người sử dụng.