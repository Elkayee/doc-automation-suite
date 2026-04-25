## CHƯƠNG 1: TỔNG QUAN HỆ THỐNG VÀ PHÂN CÔNG NHÓM

> **Mục tiêu chương:** Trình bày bức tranh toàn cảnh gồm 6 phân hệ ca sử dụng, tác nhân, yêu cầu chức năng và yêu cầu phi chức năng. Phần này chiếm khoảng 10% báo cáo.

### 1.1. Bối cảnh và Tầm nhìn Dự án

Dự án xây dựng nền tảng quản lý café tích hợp, giải quyết đồng thời bài toán vận hành (POS, thu ngân, kho bãi) và quản trị nhân sự. Bộ sản phẩm gồm ba nền tảng:

| **Nền tảng**               | **Đối tượng**   | **Công nghệ**                     |
| -------------------------- | --------------- | --------------------------------- |
| Ứng dụng bảng điều khiển trên web | Quản lý cấp cao | React / Next.js, triển khai trên đám mây |
| Phần mềm POS máy tính bảng | Thu ngân        | Android tablet, giao thức ESC/POS |
| Ứng dụng di động nhân viên | Nhân viên       | Flutter, GPS + nhận diện khuôn mặt |

---

### 1.2. Biểu đồ Ca sử dụng Tổng quát

Biểu đồ thể hiện phạm vi hệ thống và tương tác giữa tác nhân với 6 ca sử dụng. **UC04 (tô màu tím)** là trọng tâm phân tích chuyên sâu của báo cáo này.

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Quản lý" as Manager
actor "Nhân viên" as Employee
actor "Khách hàng" as Customer

rectangle "HỆ THỐNG QUẢN LÝ CAFÉ" {
  usecase "UC01: Quản lý Thực đơn và Đồ uống" as UC01
  usecase "UC02: Quản lý Đơn hàng và Bàn" as UC02
  usecase "UC03: Quản lý Thanh toán và Hóa đơn" as UC03
  usecase "UC04: Quản lý Ca làm và Chấm công" as UC04
  usecase "UC05: Quản lý Kho và Nguyên liệu" as UC05
  usecase "UC06: Thống kê và Báo cáo" as UC06
}

Manager --> UC01
Manager --> UC04
Manager --> UC05
Manager --> UC06
Employee --> UC01
Employee --> UC02
Employee --> UC03
Employee --> UC04
Customer ..> UC02 : gián tiếp
@enduml
```

---

### 1.3. Bảng Tóm tắt Chức năng Toàn Hệ thống

|  **UC**  | **Phân hệ**             | **Chức năng cốt lõi**                                                                             | **Người phụ trách**  |       **Mức chi tiết**       |
| :------: | ----------------------- | ------------------------------------------------------------------------------------------------- | -------------------- | :--------------------------: |
|   UC01   | Thực đơn & Đồ uống      | CRUD sản phẩm, nhóm, topping, công thức pha chế                                                   | Bảo                  |           Tóm tắt            |
|   UC02   | Đơn hàng & Bàn          | Tạo/sửa đơn, quản lý trạng thái bàn theo thời gian thực                                            | Thành                |           Tóm tắt            |
|   UC03   | Thanh toán & Hóa đơn    | Xử lý thanh toán đa kênh (tiền mặt/thẻ/QR), in hóa đơn                                            | Thành                |           Tóm tắt            |
|   UC05   | Kho & Nguyên liệu       | Nhập kho, trừ tồn theo công thức pha chế, cảnh báo ngưỡng                                          | Nguyễn Quang Đạo     |           Tóm tắt            |
|   UC06   | Báo cáo & Cửa hàng      | Thống kê doanh thu, top sản phẩm, quản lý chi nhánh                                               | Hồng Nhung           |           Tóm tắt            |
| **UC04** | **Nhân sự & Chấm công** | **Hồ sơ nhân viên, phân ca sáng/tối, chấm công bằng GPS, tính lương theo ca với hệ số cuối tuần/lễ, RBAC** | **Nguyễn Viết Tùng** | **Chuyên sâu (Chương 3)** |

---

### 1.4. Yêu cầu Chức năng

Yêu cầu chức năng được phân loại theo chuẩn **IEEE 830**, đảm bảo tính truy vết từ yêu cầu đến thiết kế:

| **Mã**    | **Phân hệ**   | **Mô tả yêu cầu**                                                                                              | **Ưu tiên** |
| --------- | ------------- | -------------------------------------------------------------------------------------------------------------- | :---------: |
| FR-01     | Đơn hàng      | Nhân viên tạo mới, sửa đổi và hủy đơn hàng trên bàn đang hoạt động                                             |     Cao     |
| FR-02     | Đơn hàng      | Hệ thống tự động thông báo khu vực pha chế khi có đơn mới                                                      |     Cao     |
| FR-03     | Bàn           | Trạng thái bàn cập nhật theo thời gian thực, không cần làm mới trang                                           |     Cao     |
| FR-04     | Thanh toán    | Hỗ trợ tối thiểu 3 hình thức: tiền mặt, thẻ và QR Pay                                                          | Trung bình  |
| FR-05     | Thanh toán    | Hóa đơn xuất ra máy in nhiệt theo định dạng chuẩn ESC/POS                                                      |     Cao     |
| FR-06     | Kho           | Tự động cập nhật tồn kho khi đơn xác nhận, theo công thức Recipe                                               |     Cao     |
| FR-07     | Kho           | Cảnh báo khi tồn kho xuống dưới ngưỡng tối thiểu                                                               | Trung bình  |
| **FR-08** | **Nhân sự**   | **Quản lý tạo và phân công ca làm cho từng nhân viên theo ngày/tuần**                                          |   **Cao**   |
| **FR-09** | **Nhân sự**   | **Nhân viên chấm công vào ca và kết thúc ca, hệ thống ghi nhận giờ làm thực tế**                               |   **Cao**   |
| **FR-10** | **Nhân sự**   | **Tính lương theo 2 loại ca cố định: ca sáng và ca tối; có hệ số riêng cho ngày thường, cuối tuần và ngày lễ** |   **Cao**   |
| **FR-15** | **Chấm công** | **Chấm công bằng định vị GPS theo vùng kết hợp xác thực khuôn mặt, ngăn chấm công hộ**                         |   **Cao**   |
| FR-11     | Báo cáo       | Tổng hợp và trực quan hóa doanh thu theo ngày/tuần/tháng                                                       | Trung bình  |
| FR-12     | Báo cáo       | Thống kê top 10 mặt hàng bán chạy nhất trong kỳ                                                                |    Thấp     |
| FR-13     | AI — Kho      | Module AI dự báo nhu cầu nguyên liệu, tự động tạo đề xuất phiếu nhập                                           |  Kiến nghị  |
| FR-14     | AI — Nhân sự  | Module AI tự động đề xuất lịch phân ca theo dự báo lưu lượng khách                                             |  Kiến nghị  |
| FR-16     | Khách hàng    | Quản lý khách hàng thân thiết; AI cá nhân hóa khuyến mãi                                                       |  Kiến nghị  |

> **Lưu ý:** FR-08, FR-09, FR-10, FR-15 (in đậm) là trọng tâm phân tích của báo cáo, được đặc tả đầy đủ tại Chương 3.

---

### 1.5. Yêu cầu Phi chức năng

Phân tích theo mô hình chất lượng **ISO/IEC 25010**:

| **Thuộc tính**    | **Yêu cầu cụ thể**                                             | **Cách đo lường**       |
| ----------------- | -------------------------------------------------------------- | ----------------------- |
| **Hiệu năng**     | Phản hồi dưới 3 giây trong điều kiện LAN, 20 người dùng đồng thời | Công cụ phân tích hiệu năng |
| **Tính sẵn sàng** | Hoạt động liên tục; thời gian phục hồi dưới 30 phút khi có sự cố | Nhật ký thời gian hoạt động |
| **Bảo mật**       | RBAC nghiêm ngặt; mật khẩu băm bằng BCrypt; nhật ký thao tác lưu ít nhất 90 ngày | Kiểm tra thâm nhập cơ bản |
| **Tính khả dụng** | Nhân viên mới thành thạo chức năng cơ bản sau không quá 2 giờ đào tạo | Kiểm thử người dùng với 5 người |
| **Tương thích**   | Windows 7 SP1+; máy in nhiệt chuẩn ESC/POS                     | Kiểm thử 3 cấu hình POS |
| **Bảo trì**       | Độ bao phủ kiểm thử từ 70% trở lên; tài liệu hóa đầy đủ        | JaCoCo                  |

---

### 1.6. Phân tích Rủi ro Dự án

| **Rủi ro**                                | **Xác suất** | **Tác động** | **Biện pháp giảm thiểu**                                      |
| ----------------------------------------- | :----------: | :----------: | ------------------------------------------------------------- |
| Yêu cầu thay đổi giữa chừng (phình phạm vi) |     Cao      |     Cao      | Đặc tả ca sử dụng làm tài liệu ký kết; quản lý thay đổi |
| Thiếu dữ liệu thực tế để kiểm thử         |  Trung bình  |  Trung bình  | Sinh dữ liệu mẫu mô phỏng thực tế |
| Thành viên nhóm vắng giữa sprint          |     Thấp     |     Cao      | Phân công chéo; tài liệu handover                             |
| Lỗi tích hợp phần cứng POS                |  Trung bình  |     Cao      | Kiểm thử thiết bị sớm; driver dự phòng                        |

---
