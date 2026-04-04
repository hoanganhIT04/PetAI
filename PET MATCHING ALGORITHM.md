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

Giả sử người dùng chọn đối tượng là **Chó**. Hệ thống xử lý dữ liệu với 4 tiêu chí: `[Năng lượng, Không gian, Chăm sóc, Thân thiện]`.

**1. Dữ liệu đầu vào (Input Vectors):**
* **Người dùng ($U$):** Nhà nhỏ (Không gian: 1), thích chó lười (Năng lượng: 1), ít thời gian chải lông (Chăm sóc: 1), cần chó hiền (Thân thiện: 5), kích thước nhỏ (`small`).
  * Vectơ người dùng $U = [1, 1, 1, 5]$ | Size: `small`
* **Dữ liệu 4 loài chó tiềm năng (Trích xuất từ CSV):**
  * $P_1$ (Pug): $[2, 2, 3, 5]$ | Size: `small`
  * $P_2$ (Shih Tzu): $[2, 2, 5, 5]$ | Size: `small`
  * $P_3$ (Maltese Dog): $[3, 2, 5, 4]$ | Size: `small`
  * $P_4$ (Basset Hound): $[2, 3, 4, 5]$ | Size: `medium`

**2. Bước 1: Áp dụng Hard-filters**
* Kiểm tra $P_4$ (Basset Hound): Người dùng ở không gian `1`. Basset Hound có điểm không gian `3`. 
* **Kết quả:** Vì $3 < 4$, Basset Hound vẫn **vượt qua** vòng lọc thô nhưng sẽ bị trừ điểm nặng ở bước tính khoảng cách do chênh lệch không gian và kích thước (`medium` vs `small`).

**3. Bước 2: Tính toán khoảng cách (Euclidean + Size Penalty)**
Sử dụng trọng số $w = [energy: 2.0, space: 1.5, grooming: 1.0, kid: 1.8]$ và hình phạt kích thước $+1.5$.

* **Tính cho Pug ($P_1$):**
  * $d^2 = 2.0(1-2)^2 + 1.5(1-2)^2 + 1.0(1-3)^2 + 1.8(5-5)^2 = 2.0 + 1.5 + 4.0 + 0 = 7.5$
  * Khoảng cách $d = \sqrt{7.5} \approx 2.73$. (Không phạt size vì cùng là `small`).
* **Tính cho Basset Hound ($P_4$):**
  * $d^2 = 2.0(1-2)^2 + 1.5(1-3)^2 + 1.0(1-4)^2 + 1.8(5-5)^2 = 2.0 + 6.0 + 9.0 + 0 = 17.0$
  * Khoảng cách cơ bản $\sqrt{17.0} \approx 4.12$. 
  * Cộng phạt kích thước: $d = 4.12 + 1.5 = 5.62$.

**4. Bước 3: Chuẩn hóa & Xếp hạng (Ranking)**
Sử dụng công thức $Score = \frac{100}{1 + d \times 0.2}$:
1. **Pug:** $Score = \frac{100}{1 + 2.73 \times 0.2} \approx \textbf{64.6\%}$
2. **Shih Tzu:** $Score \approx \textbf{59.4\%}$
3. **Maltese:** $Score \approx \textbf{53.8\%}$
4. **Basset Hound:** $Score \approx \textbf{47.0\%}$

**5. Kết quả cuối cùng (Top 3):**
Hệ thống sử dụng hàm `.slice(0, 3)` để lấy 3 kết quả cao nhất:
1. **Hạng 1:** Pug (65%) - Phù hợp nhất về Năng lượng và Không gian.
2. **Hạng 2:** Shih Tzu (59%)
3. **Hạng 3:** Maltese Dog (54%)
*Giống Basset Hound bị loại khỏi danh sách hiển thị do xếp hạng 4.*

---

## 6. Kết luận
Kiến trúc thuật toán Pet Matching là sự giao thoa hiệu quả giữa **Toán học định lượng** (Weighted Euclidean Distance) và **Logic định tính** (Hard Filters). Cách tiếp cận này giúp dự án PetAI không chỉ đạt được hiệu suất tính toán tối ưu (Time Complexity tốt do đã cắt tỉa dữ liệu ngay từ đầu) mà còn đảm bảo các kết quả đầu ra luôn mang giá trị thực tiễn và nhân văn đối với người sử dụng.