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

Giả sử người dùng đã chọn loại thú cưng là **Chó** ở câu hỏi đầu tiên. Hệ thống hiện đang xử lý dữ liệu với 4 tiêu chí cốt lõi: `[Năng lượng, Không gian, Chăm sóc, Thân thiện]`.

**1. Dữ liệu đầu vào (Input Vectors):**
* **Người dùng ($U$):** Ở căn hộ nhỏ (Không gian: 1), ít vận động (Năng lượng: 2), chăm sóc bình thường (Chăm sóc: 3), nhà có trẻ nhỏ nên cần chó rất hiền (Thân thiện: 5), và thích kích thước nhỏ (`small`).
  * Vectơ lý tưởng $U = [2, 1, 3, 5]$ | Size: `small`
* **Trích xuất 4 giống chó tiềm năng từ Database (đã chuẩn hóa):**
  * $P_1$ (Pug): $[2, 2, 3, 5]$ | Size: `small`
  * $P_2$ (Shih Tzu): $[2, 2, 5, 5]$ | Size: `small`
  * $P_3$ (Maltese): $[3, 2, 5, 4]$ | Size: `small`
  * $P_4$ (Basset Hound): $[2, 3, 4, 5]$ | Size: `medium`

**2. Bước 1: Áp dụng Hard-filters (Lọc thô)**
* Cả 4 giống chó trên đều có `space < 4` (không gian yêu cầu không quá lớn) và `kid_friendly > 2` (khá thân thiện). 
* **Kết quả:** Cả 4 loài đều thỏa mãn điều kiện an toàn và vượt qua vòng lọc cứng để vào vòng tính điểm chi tiết.

**3. Bước 2: Tính toán khoảng cách (Euclidean + Size Penalty)**
Áp dụng công thức Euclid có bộ trọng số $w = [2.0, 1.5, 1.0, 1.8]$ kết hợp hình phạt sai lệch kích thước (Penalty = $+1.5$ nếu khác size):

* **Tính điểm cho giống Pug ($P_1$):**
  * Độ lệch: $2.0(2-2)^2 + 1.5(1-2)^2 + 1.0(3-3)^2 + 1.8(5-5)^2 = 0 + 1.5 + 0 + 0 = 1.5$
  * Khoảng cách ban đầu = $\sqrt{1.5} \approx 1.22$
  * Trùng khớp size `small` $\rightarrow$ Penalty = 0. Tổng khoảng cách $d_1 = 1.22$
* **Tính điểm cho giống Basset Hound ($P_4$):**
  * Độ lệch: $2.0(2-2)^2 + 1.5(1-3)^2 + 1.0(3-4)^2 + 1.8(5-5)^2 = 0 + 6.0 + 1.0 + 0 = 7.0$
  * Khoảng cách ban đầu = $\sqrt{7.0} \approx 2.65$
  * Sai lệch size (`small` vs `medium`) $\rightarrow$ Penalty = $+1.5$. Tổng khoảng cách $d_4 = 4.15$
* *(Tương tự cho $P_2$ và $P_3$, ta có: $d_2 \approx 2.35$ và $d_3 \approx 3.05$)*

**4. Bước 3: Chuẩn hóa & Xếp hạng (Ranking & Slicing)**
Chuẩn hóa khoảng cách $d$ thành thang điểm $100\%$ qua công thức $Score = \frac{100}{1 + d \times 0.2}$:
1. **Pug ($d = 1.22$):** $Score = \frac{100}{1 + 1.22 \times 0.2} \approx \textbf{80.4\%}$
2. **Shih Tzu ($d = 2.35$):** $Score \approx \textbf{68.0\%}$
3. **Maltese ($d = 3.05$):** $Score \approx \textbf{62.1\%}$
4. **Basset Hound ($d = 4.15$):** $Score \approx \textbf{54.6\%}$

* **Thuật toán Slice(0, 3):** Hệ thống chỉ lấy Top 3. Giống Basset Hound đứng ở vị trí thứ 4 (do bị phạt điểm size và sai lệch không gian) sẽ bị **loại khỏi tập kết quả cuối cùng**.

**5. Bước 4: Explainable AI (Trích xuất lý do cho Pug)**
Hệ thống quét lại các tiêu chí của ứng viên Top 1 (Pug) có sai số $|U_i - P_i| \le 1$:
* Sai lệch Năng lượng ($|2 - 2| = 0$) $\rightarrow$ Gắn nhãn: *"Năng lượng phù hợp"*
* Sai lệch Không gian ($|1 - 2| = 1$) $\rightarrow$ Gắn nhãn: *"Phù hợp không gian"*
* Trùng Size $\rightarrow$ Gắn nhãn: *"Kích thước mong muốn"*

---

## 6. Kết luận
Kiến trúc thuật toán Pet Matching là sự giao thoa hiệu quả giữa **Toán học định lượng** (Weighted Euclidean Distance) và **Logic định tính** (Hard Filters). Cách tiếp cận này giúp dự án PetAI không chỉ đạt được hiệu suất tính toán tối ưu (Time Complexity tốt do đã cắt tỉa dữ liệu ngay từ đầu) mà còn đảm bảo các kết quả đầu ra luôn mang giá trị thực tiễn và nhân văn đối với người sử dụng.