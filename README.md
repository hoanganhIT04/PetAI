# 🧠 AI Pet Recognition System

---

## 📌 Giới thiệu (Introduction)

### 🔍 Bài toán đặt ra

Trong bối cảnh **trí tuệ nhân tạo (AI)** ngày càng được ứng dụng rộng rãi, việc **nhận diện vật nuôi** và cung cấp thông tin chính xác, trực quan cho người dùng vẫn còn nhiều hạn chế. Phần lớn người dùng **không có đủ kiến thức chuyên môn** để phân biệt các loại vật nuôi hoặc tìm kiếm thông tin đáng tin cậy về chúng một cách nhanh chóng và thuận tiện.

---

### 🤖 Ứng dụng được xây dựng để làm gì?

Ứng dụng này là một **hệ thống AI nhận diện vật nuôi**, cho phép người dùng:

* 📷 **Tải ảnh vật nuôi** lên hệ thống
* 🧠 **AI tự động phân tích & nhận diện** vật nuôi từ hình ảnh
* 📊 **Hiển thị thông tin chi tiết** liên quan đến vật nuôi đã nhận diện  
* 🖥️ Trải nghiệm giao diện **thân thiện – trực quan – dễ sử dụng**  
* ❓ Tích hợp **bộ câu hỏi trắc nghiệm (Quiz)** giúp người dùng trả lời các câu hỏi về nhu cầu, điều kiện sống và sở thích để **gợi ý vật nuôi phù hợp**  
* 📚 Xây dựng **thư viện vật nuôi** hiển thị danh sách các giống loài kèm thông tin mô tả, đặc điểm và khả năng chăm sóc


Hệ thống được phát triển theo hướng **kết hợp AI + Web Application**, phù hợp cho nghiên cứu khoa học, học tập và khả năng triển khai thực tế.

---

### 🌱 Giá trị thực tế

Ứng dụng mang lại nhiều giá trị thực tiễn:

* 👨‍🎓 **Hỗ trợ học tập & nghiên cứu** trong lĩnh vực AI, Computer Vision
* 🐾 **Giúp người dùng phổ thông** tiếp cận thông tin về vật nuôi dễ dàng hơn
* 🏥 Có tiềm năng mở rộng cho các lĩnh vực như:

  * Tư vấn chăm sóc vật nuôi
  * Hỗ trợ hệ thống quản lý, phân loại
  * Ứng dụng trong giáo dục hoặc thương mại

---

### 🚀 Khả năng mở rộng trong tương lai

Hệ thống được thiết kế theo hướng **mở và linh hoạt**, dễ dàng nâng cấp và mở rộng:

* ➕ Bổ sung **nhiều loại vật nuôi khác** mà không cần thay đổi kiến trúc tổng thể
* 🧠 Nâng cấp mô hình AI để **tăng độ chính xác**
* 🌐 Tích hợp thêm API, hệ thống gợi ý, hoặc chatbot AI
* 📱 Phát triển thêm phiên bản mobile / đa nền tảng

---

### 🛠️ Công nghệ & Thư viện sử dụng 

> *Phần này liệt kê tổng quan, chi tiết sẽ được mô tả kỹ hơn ở các mục tiếp theo*

* **AI / Machine Learning**
* **Computer Vision**
* **Backend Framework**
* **Frontend UI Framework (Bootstrap)**
* **Custom Fonts & Icons**
* **RESTful API**

---

✨ *Đây là sản phẩm phục vụ cho **Nghiên cứu khoa học (NCKH)**, đồng thời là nền tảng để phát triển các ứng dụng AI thực tế trong tương la

## 🎯 Objectives – Mục tiêu nghiên cứu

Nghiên cứu này được thực hiện nhằm xây dựng một hệ thống ứng dụng trí tuệ nhân tạo (AI) có khả năng hỗ trợ người dùng trong việc nhận diện và tìm hiểu thông tin về vật nuôi một cách trực quan, chính xác và dễ sử dụng.

Cụ thể, các mục tiêu chính của nghiên cứu bao gồm:

- 🧠 **Xây dựng hệ thống AI nhận diện vật nuôi từ hình ảnh đầu vào**, cho phép người dùng tải ảnh và nhận kết quả dự đoán tự động  
- 🔍 **Áp dụng mô hình học sâu (Deep Learning)** để phân loại vật nuôi dựa trên đặc trưng hình ảnh  
- 📊 **Cung cấp thông tin chi tiết** liên quan đến vật nuôi sau khi được nhận diện, giúp người dùng hiểu rõ hơn về đặc điểm và khả năng chăm sóc  
- 🧩 **Tích hợp các chức năng hỗ trợ người dùng**, bao gồm bộ câu hỏi gợi ý vật nuôi phù hợp và thư viện vật nuôi  
- 🚀 **Thiết kế hệ thống theo hướng mở rộng**, cho phép bổ sung thêm nhiều loài vật nuôi và dữ liệu trong tương lai mà không cần thay đổi kiến trúc tổng thể

Thông qua các mục tiêu trên, nghiên cứu hướng đến việc kết hợp giữa **AI – trải nghiệm người dùng – giá trị thực tiễn**, tạo nền tảng cho việc phát triển các ứng dụng thông minh trong lĩnh vực chăm sóc và tư vấn vật nuôi.

## 🧩 System Overview / Architecture – Tổng quan hệ thống

Hệ thống được thiết kế theo kiến trúc **Client – Server – AI Model**, trong đó mỗi thành phần đảm nhiệm một vai trò riêng biệt nhằm đảm bảo khả năng mở rộng, dễ bảo trì và hiệu quả trong quá trình xử lý dữ liệu.

### 🔄 Luồng hoạt động tổng thể

![Overall Model Pipeline](images/Overall%20Model%20Pipeline.png)

Quy trình xử lý của hệ thống được mô tả như sau:

1. **Người dùng (Frontend)** tải lên hình ảnh vật nuôi thông qua giao diện web  
2. **Backend (FastAPI)** tiếp nhận ảnh, xử lý tiền xử lý (resize, normalize) và gửi đến mô hình AI  
3. **Hệ thống AI** thực hiện nhận diện theo mô hình hai tầng:
   - **Model 1 – Animal Filter**:  
     Phân loại ảnh đầu vào thành *animal* hoặc *non-animal* nhằm loại bỏ các ảnh không liên quan trước khi đi vào bước nhận diện chi tiết
   - **Model 2 – Breed Classifier (+ unknown)**:  
     Nhận diện vật nuôi và xử lý các trường hợp mơ hồ thông qua lớp *unknown*, đồng thời áp dụng ngưỡng tin cậy (confidence threshold) để giảm sai lệch
4. **Backend** trả kết quả dự đoán về cho Frontend dưới dạng JSON
5. **Frontend** hiển thị kết quả, thông tin chi tiết và các gợi ý liên quan cho người dùng

---

### 🖥️ Frontend

- Xây dựng bằng **HTML, CSS, JavaScript**
- Sử dụng **Bootstrap** để thiết kế giao diện responsive, thân thiện với người dùng
- Áp dụng **Font tùy chỉnh** và icon để tăng tính trực quan
- Chức năng chính:
  - Tải ảnh vật nuôi
  - Hiển thị kết quả nhận diện và độ tin cậy
  - Truy cập thư viện vật nuôi
  - Tham gia bộ câu hỏi (quiz) gợi ý vật nuôi phù hợp

---

### ⚙️ Backend (API Server)

- Xây dựng bằng **FastAPI (Python)**
- Đóng vai trò trung gian giữa Frontend và hệ thống AI
- Chức năng chính:
  - Nhận ảnh từ người dùng
  - Tiền xử lý dữ liệu hình ảnh
  - Gọi mô hình AI để dự đoán
  - Trả kết quả nhận diện dưới dạng API JSON
- Hỗ trợ **CORS** để kết nối với Frontend
- Quản lý static files (ảnh, tài nguyên) phục vụ giao diện

---

### 🧠 AI Model

Hệ thống AI được thiết kế theo mô hình hai tầng nhằm tăng độ chính xác và giảm nhiễu:

- **Model 1 – Animal Filter**
  - Phân loại nhị phân: *animal* / *non-animal*
  - Giúp loại bỏ ảnh không hợp lệ trước khi nhận diện chi tiết

- **Model 2 – Classification Model**
  - Nhận diện vật nuôi
  - Tích hợp lớp *unknown* để xử lý các trường hợp mơ hồ
  - Áp dụng **confidence threshold (T = 0.35)** để quyết định chấp nhận hay yêu cầu quét lại ảnh

Thiết kế này giúp hệ thống tránh việc dự đoán sai với độ tự tin cao và nâng cao độ tin cậy của kết quả.

---

### 📁 Dataset

Dataset được xây dựng có chủ đích nhằm phục vụ cho **hệ thống nhận diện vật nuôi hai tầng**, bao gồm dữ liệu vật nuôi, dữ liệu không phải vật nuôi (*non-animal*) và dữ liệu mơ hồ (*unknown*). Tổng thể dataset được chuẩn hóa về kích thước, định dạng và phân bố để phù hợp với các mô hình học sâu.

---

#### 🐾 Dataset vật nuôi (Animal)

Hệ thống hiện tại sử dụng **140 giống loài vật nuôi**, trong đó bao gồm:

- **120 giống chó**
  - Thu thập từ **Stanford Dogs Dataset** (nguồn dữ liệu học thuật, phổ biến trong nghiên cứu)
- **12 giống mèo**
  - Thu thập từ **Oxford-IIIT Pets Dataset**
- **8 giống mèo bổ sung**
  - Thu thập từ các nguồn chính thống và hình ảnh được chọn lọc thủ công từ **Pinterest** nhằm đa dạng hóa dữ liệu

📊 **Tổng quan dữ liệu cho Model 2 – Breed Classifier (+ unknown):**
- Khoảng **25,000 ảnh vật nuôi**
- **140 lớp giống loài**
- Trung bình **~200 ảnh mỗi lớp**
- **Unknown class**: ~3,000 ảnh vật nuôi mơ hồ (góc chụp khó, che khuất, giống loài không rõ ràng)

---

#### 🚫 Dataset không phải vật nuôi (Non-Animal)

Dataset *non-animal* được thiết kế để huấn luyện **Model 1 – Animal Filter**, giúp hệ thống loại bỏ ảnh không liên quan trước khi nhận diện chi tiết.

📁 Các nhóm dữ liệu *non-animal* bao gồm:

- **building**  
  Nhà ở, chung cư, cao ốc, văn phòng, trường học, bệnh viện, cầu đường và các công trình xây dựng

- **electronic**  
  Laptop, PC, điện thoại, TV, máy ảnh, tai nghe, loa và các thiết bị điện tử (chụp sản phẩm hoặc đặt trên bàn)

- **food**  
  Món ăn, đồ uống, bánh, trái cây, đồ ăn nhanh, ảnh cận cảnh thực phẩm (không xuất hiện vật nuôi)

- **nature**  
  Núi, rừng, sông, biển, cây cối, bầu trời, mây, hoa và các cảnh quan thiên nhiên (không có động vật)

- **object**  
  Bàn ghế, quần áo, giày dép, ba lô, đồng hồ, sách vở, đồ gia dụng và các vật dụng thường ngày

- **text_logo**  
  Logo thương hiệu, biển hiệu, bảng quảng cáo, poster, banner và các hình ảnh chứa nhiều chữ hoặc ký hiệu

- **vehicle**  
  Xe máy, ô tô, xe đạp, xe buýt, xe tải, tàu hỏa và các phương tiện giao thông

📊 **Tổng quan dữ liệu cho Model 1 – Animal Filter:**
- **Animal**: ~2,000 ảnh vật nuôi (phân bố cân bằng)
- **Non-animal**: ~2,000 ảnh không phải vật nuôi  
- Các lớp *non-animal* được phân bố **cân bằng** nhằm giảm bias trong quá trình huấn luyện

---

#### 🔧 Tiền xử lý & khả năng mở rộng

- Tất cả hình ảnh được:
  - Chuẩn hóa kích thước
  - Chuyển đổi định dạng phù hợp
  - Làm sạch dữ liệu trước khi huấn luyện
- Cấu trúc dataset được thiết kế linh hoạt, cho phép:
  - **Bổ sung thêm giống loài vật nuôi mới**
  - **Mở rộng sang các loài động vật khác trong tương lai**
  - Không làm ảnh hưởng đến kiến trúc và mô hình hiện tại
---

## 🧩 Cấu trúc thư mục dữ liệu

```text
data/
├── data_model_1/
│   ├── animal/
│   └── non_animal/
│
├── data_model_2/
│   ├── abyssinian/
│   ├── affenpinscher/
│   ├── afghan_hound/
│   ├── african_hunting_dog/
│   ├── airedale/
│   ├── american_staffordshire_terrier/
│   ├── appenzeller/
│   ├── australian_terrier/
│   ├── ...
│   └── unknown/


---

Thiết kế kiến trúc này đảm bảo hệ thống hoạt động ổn định, dễ mở rộng và phù hợp cho các nghiên cứu cũng như ứng dụng thực tế liên quan đến trí tuệ nhân tạo trong lĩnh vực nhận diện vật nuôi.

---

### 🧠 Metadata & Knowledge Base

Bên cạnh dữ liệu hình ảnh, hệ thống còn xây dựng **metadata cho từng giống loài vật nuôi** nhằm cung cấp thông tin chi tiết và hỗ trợ các chức năng tư vấn thông minh.

---

#### 📌 Nguồn thu thập metadata

Metadata được tổng hợp và chuẩn hóa từ các nguồn **chính thống và uy tín**, bao gồm:

- **AKC (American Kennel Club)** – Thông tin tiêu chuẩn giống loài chó  
- **CFA (Cat Fanciers’ Association)** – Dữ liệu đặc điểm và phân loại mèo  
- **TICA (The International Cat Association)** – Thông tin chuyên sâu về giống mèo  
- **PetFinder** – Dữ liệu thực tế liên quan đến chăm sóc, hành vi và nhu cầu nuôi dưỡng

Các nguồn dữ liệu này giúp đảm bảo **độ chính xác, tính học thuật và khả năng ứng dụng thực tế** của hệ thống.

---

#### 📊 Nội dung metadata thu thập

Mỗi giống loài vật nuôi được xây dựng metadata bao gồm:

- Giá cả tham khảo
- Tuổi thọ trung bình
- Cân nặng trung bình
- Chiều cao / kích thước cơ thể
- Đặc điểm ngoại hình
- Cách chăm sóc và nuôi dưỡng
- Mức độ phù hợp với môi trường sống (nhà ở, căn hộ, không gian rộng…)

---

#### 🔑 Trích xuất keyword & hệ thống đánh giá

Từ bộ metadata thu thập được, hệ thống tiến hành:

- Trích xuất **keyword mô tả đặc tính giống loài**
- Chuẩn hóa các thuộc tính thành **thang điểm đánh giá**

Các tiêu chí đánh giá bao gồm:

- ⚡ **Mức độ hoạt động**
- 🏠 **Nhu cầu không gian sống**
- 🧹 **Độ rụng lông**
- 📏 **Kích thước cơ thể**
- 🤝 **Mức độ thân thiện với con người**

Mỗi tiêu chí được lượng hóa theo thang điểm, giúp hệ thống:
- So sánh giữa các giống loài
- Hỗ trợ **gợi ý vật nuôi phù hợp** thông qua quiz và hành vi người dùng
- Làm nền tảng cho các tính năng tư vấn thông minh trong tương lai

---

#### 🚀 Khả năng mở rộng

Cấu trúc metadata được thiết kế linh hoạt, cho phép:
- Bổ sung thêm tiêu chí đánh giá mới
- Mở rộng sang nhiều loài vật nuôi khác
- Kết hợp với AI và hệ thống gợi ý để nâng cao trải nghiệm người dùng
