# CƠ CHẾ HOẠT ĐỘNG CỦA THUẬT TOÁN GỢI Ý THÚ CƯNG (PET MATCHING ALGORITHM)

## 1. Tổng quan kiến trúc hệ thống (Overall Pipeline)
Hệ thống gợi ý của dự án PetAI hoạt động dựa trên mô hình **Vector Space Modeling** kết hợp **Fuzzy Logic (Logic mờ)**. Thay vì sử dụng các cấu trúc điều kiện `if/else` tĩnh, hệ thống số hóa nhu cầu của người dùng thành các "Khoảng giá trị chấp nhận được" (Range bounds) và đối chiếu với tọa độ đặc tính của vật nuôi.

Quá trình này trải qua 5 giai đoạn cốt lõi:
1. **Thu thập (Input):** Tiếp nhận dữ liệu cấu hình từ người dùng thông qua bài khảo sát.
2. **Vectơ hóa (Vectorization):** Chuyển đổi lựa chọn thành các mảng giới hạn $[min, max]$ trong không gian $n$-chiều.
3. **Lọc thô (Hard-filtering):** Áp dụng các ràng buộc cứng để loại bỏ các trường hợp vi phạm điều kiện tiên quyết.
4. **Tính toán độ tương đồng (Fuzzy Euclidean Distance):** Đo lường khoảng cách từ đặc tính loài đến biên gần nhất của khoảng nhu cầu người dùng.
5. **Xếp hạng & Giải thích (Ranking & XAI):** Chuẩn hóa khoảng cách thành điểm phần trăm (%), sắp xếp và trích xuất lý do gợi ý (Explainable AI).

---

## 2. Kỹ thuật lọc thô (Hard-filters) - Đảm bảo tính khả thi
Trong kỹ thuật phần mềm, đây được gọi là **Ràng buộc cứng (Hard Constraints)**. Thuật toán tiến hành cắt tỉa (pruning) tập dữ liệu ngay từ đầu:

* **Ràng buộc Không gian (Space):** Ngăn chặn vi phạm phúc lợi động vật. 
  * *Logic:* Nếu người dùng ở không gian nhỏ (chọn mảng `[1, 2]`), loại bỏ lập tức các loài yêu cầu không gian rộng `(>= 4)`.
* **Ràng buộc An toàn (Kid-friendly):** Đảm bảo an toàn tuyệt đối cho gia đình có trẻ nhỏ.
  * *Logic:* Nếu người dùng yêu cầu thú cưng thân thiện (chọn mảng `[4, 5]`), loại bỏ các giống loài có điểm thân thiện thấp `(<= 2)`.

---

## 3. Tiêu chí và Trọng số (Matching Weights)
Hệ thống sử dụng ma trận trọng số để cá nhân hóa kết quả:
* `energy` (Năng lượng) - **Trọng số 2.0**: Yếu tố then chốt nhất quyết định sự hòa hợp lâu dài.
* `kid_friendly` (Thân thiện trẻ em) - **Trọng số 1.8**: Ưu tiên cao về mặt an toàn.
* `space` (Không gian sống) - **Trọng số 1.5**: Điều kiện vật chất để duy trì sự sống.
* `grooming` (Chăm sóc lông) - **Trọng số 1.0**: Yếu tố phụ thuộc vào ngưỡng chịu đựng cá nhân.

---

## 4. Thuật toán cốt lõi: Khoảng cách Euclid theo Logic mờ (Fuzzy Euclidean)
Thay vì phạt điểm ngay khi có sự sai lệch nhỏ, hệ thống coi nhu cầu của người dùng là một tập hợp mờ $[U_{min}, U_{max}]$. Khoảng cách $\Delta_i$ cho một tiêu chí $i$ của thú cưng ($P_i$) được tính bằng khoảng cách đến biên gần nhất:

* Nếu $P_i < U_{min} \rightarrow \Delta_i = U_{min} - P_i$
* Nếu $P_i > U_{max} \rightarrow \Delta_i = P_i - U_{max}$
* Nếu $U_{min} \le P_i \le U_{max} \rightarrow \Delta_i = 0$ (Khớp hoàn toàn)

**Công thức tổng quát:**
$$d(U, P) = \sqrt{\sum_{i=1}^{n} w_i (\Delta_i)^2}$$

**Chuẩn hóa điểm số (Score Normalization):**
Khoảng cách $d$ được ánh xạ về thang điểm phần trăm ($100\%$) thông qua hàm phân thức, với hệ số làm mượt là `0.2`:
$$Score = \frac{100}{1 + d \times 0.2}$$

---

## 5. Ví dụ minh họa thực tế (Case Study)

Hệ thống xử lý dữ liệu với 4 tiêu chí: `[Năng lượng, Không gian, Chăm sóc, Thân thiện]`.

**1. Dữ liệu đầu vào (Input):**
* **Người dùng ($U$):** Nhà nhỏ (`[1, 2]`), thích chó lười (`[1, 2]`), ít thời gian chải lông (`[1, 2]`), cần chó hiền (`[4, 5]`), kích thước nhỏ (`small`).
* **Dữ liệu 4 loài chó từ CSV:**
  * $P_1$ (Pug): $[2, 2, 3, 5]$ | Size: `small`
  * $P_2$ (Shih Tzu): $[2, 2, 5, 5]$ | Size: `small`
  * $P_3$ (Maltese): $[3, 2, 5, 4]$ | Size: `small`
  * $P_4$ (Basset): $[2, 3, 4, 5]$ | Size: `medium`

**2. Bước 1: Áp dụng Hard-filters**
* $P_4$ (Basset) có điểm không gian `3`. Yêu cầu lọc: Không gian `>= 4` mới bị loại.
* **Kết quả:** Cả 4 loài đều thỏa mãn và đi tiếp.

**3. Bước 2: Tính toán khoảng cách (Fuzzy Euclidean + Size Penalty)**
Sử dụng trọng số $w = [2.0, 1.5, 1.0, 1.8]$.

* **Tính cho Pug ($P_1$):**
  * Năng lượng (2) nằm trong `[1, 2]` $\rightarrow \Delta = 0$
  * Không gian (2) nằm trong `[1, 2]` $\rightarrow \Delta = 0$
  * Chăm sóc (3) nằm ngoài `[1, 2]` $\rightarrow \Delta = 3 - 2 = 1$
  * Thân thiện (5) nằm trong `[4, 5]` $\rightarrow \Delta = 0$
  * $d^2 = 2.0(0)^2 + 1.5(0)^2 + 1.0(1)^2 + 1.8(0)^2 = 1.0$. Khoảng cách $d = \sqrt{1.0} = 1.0$. (Không phạt size).
* **Tính cho Basset Hound ($P_4$):**
  * $\Delta_{energy} = 0$, $\Delta_{space} = 3 - 2 = 1$, $\Delta_{groom} = 4 - 2 = 2$, $\Delta_{kid} = 0$.
  * $d^2 = 2.0(0) + 1.5(1)^2 + 1.0(2)^2 + 1.8(0) = 0 + 1.5 + 4.0 + 0 = 5.5$. 
  * Cơ bản $\sqrt{5.5} \approx 2.34$. Phạt kích thước (+1.5) $\rightarrow d_{tổng} = 3.84$.

*(Tính tương tự cho $P_2$ ra $d=3.0$ và $P_3$ ra $d \approx 3.31$)*

**4. Bước 3: Chuẩn hóa & Xếp hạng**
1. **Pug:** $Score = \frac{100}{1 + 1.0 \times 0.2} = \frac{100}{1.2} \approx \textbf{83.3\%}$
2. **Shih Tzu:** $Score = \frac{100}{1 + 3.0 \times 0.2} = \frac{100}{1.6} \approx \textbf{62.5\%}$
3. **Maltese:** $Score = \frac{100}{1 + 3.31 \times 0.2} = \frac{100}{1.662} \approx \textbf{60.1\%}$
4. **Basset:** $Score = \frac{100}{1 + 3.84 \times 0.2} \approx \textbf{56.5\%}$

**5. Kết quả (Top 3):**
1. Hạng 1: Pug (83%) - Khớp hoàn toàn nhu cầu cốt lõi.
2. Hạng 2: Shih Tzu (62%)
3. Hạng 3: Maltese (60%)
*Basset Hound bị loại khỏi Top 3 do sai lệch nhiều tiêu chí phụ và kích thước.*

---

## 6. Kết luận
Kiến trúc thuật toán Pet Matching là sự giao thoa hiệu quả giữa **Toán học định lượng** và **Logic mờ (Fuzzy Range Matching)**. Cách tiếp cận này loại bỏ triệt để hiện tượng "cạnh vực" (Edge effect) trong các mô hình tính điểm cũ, giúp hệ thống bao dung hơn với các sai số tự nhiên, từ đó mang lại kết quả có tỷ lệ thu hồi (Recall) cao và sát với tâm lý người dùng.