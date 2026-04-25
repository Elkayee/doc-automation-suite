## CHƯƠNG 7: NGHIÊN CỨU CHUYÊN SÂU — USE CASE QUẢN LÝ NHÂN SỰ (UC07)

Chương này phân tích chuyên sâu **UC07 — Quản lý Tài khoản và Phân quyền Nhân sự**, bao gồm toàn bộ vòng đời quản lý hồ sơ nhân viên: từ tuyển dụng/onboarding, phân quyền hệ thống, đến chấm dứt hợp đồng. Đây là phân hệ nền tảng vì mọi UC khác đều phụ thuộc vào danh tính và quyền hạn được định nghĩa tại đây.

### 7.1. Biểu đồ Use Case chi tiết UC07

#### 7.1.1. Phân định các ca sử dụng con (Sub-Use Cases)

UC07 được phân rã thành các ca sử dụng con gắn với vòng đời nhân viên:

│ │

│ ┌──────────────────────┐ ┌────────────────────────┐ ┌──────────────────────────┐ │

│ │ nhân viên │ │ đăng nhập │ │ (Role-Based Access) │ │

│ └──────────────────────┘ └────────────────────────┘ └──────────────────────────┘ │

│ ▲ ▲ ▲ │

│ │«include» │«include» │«include» │

│ └──────────────────────────┴─────────────────────────────┘ │

│ │ │

│ ┌──────────────────────┐ │

│ └──────────────────────┘ │

│ │«extends» │

│ ┌──────────────────────┐ │

│ └──────────────────────┘ │

│ │«extends» │

│ ┌──────────────────────┐ │

│ │ UC07.6: Xem danh sách │ │

│ └──────────────────────┘ │

│ │

└────────────────────────────────────────────────────────────────────────────────────────┘

▲ ▲

│ │

[Manager] [Employee]

### 7.2. Đặc tả Use Case (Use Case Specification)

#### 7.2.1. Đặc tả UC07.1 — Thêm hồ sơ nhân viên mới

| **Trường** | **Nội dung** |
| --- | --- |
| Mã Use Case | UC07.1 |
| Tên Use Case | Thêm hồ sơ nhân viên mới (Onboarding) |
| Tác nhân chính | Manager |
| Tác nhân thứ cấp | Hệ thống (System), Nhân viên mới (người nhận tài khoản) |
| Điều kiện tiên quyết | Manager đã đăng nhập; có quyền MANAGE_EMPLOYEE |
| Điều kiện kết thúc (thành công) | Bản ghi nhan_vien và tai_khoan được tạo; tài khoản ở trạng thái kich_hoat; email thông báo được gửi đi |
| Điều kiện kết thúc (thất bại) | Không có bản ghi nào được tạo; hệ thống hiển thị lỗi cụ thể |
| Mức độ ưu tiên | Cao |

**Luồng sự kiện chính (Main Flow):**

| **Bước** | **Tác nhân** | **Hành động** |
| --- | --- | --- |
| 1 | Manager |  |
| 2 | Hệ thống | Hiển thị form nhập: Họ tên, CCCD, SĐT, Email, Ngày sinh, Vị trí công việc, Lương theo giờ |
| 3 | Manager | Điền đầy đủ thông tin và nhấn Lưu |
| 4 | Hệ thống | Validate dữ liệu đầu vào (kiểm tra CCCD trùng, SĐT định dạng, email hợp lệ) |
| 5 | Hệ thống | INSERT bản ghi vào bảng nhan_vien |
| 6 | Hệ thống | Tự động tạo tai_khoan với mat_khau ngẫu nhiên (8 ký tự); gán vai_tro mặc định = NHAN_VIEN |
| 7 | Hệ thống | Gửi email/SMS thông báo thông tin đăng nhập đến nhân viên mới |
| 8 | Hệ thống | Hiển thị thông báo: _"Thêm nhân viên thành công. Thông tin đăng nhập đã được gửi."_ |

**Luồng ngoại lệ (Exception Flows):**

| **Mã** | **Điều kiện kích hoạt** | **Xử lý** |
| --- | --- | --- |
| E1 | CCCD đã tồn tại trong hệ thống | Hiển thị: _"Nhân viên với CCCD này đã được đăng ký."_ Không INSERT. |
| E2 | Email không đúng định dạng | Highlight trường lỗi, thông báo: _"Email không hợp lệ."_ |
| E3 | Lương theo giờ < mức lương tối thiểu vùng | Cảnh báo: _"Mức lương thấp hơn quy định (22.500đ/giờ). Xác nhận tiếp tục?"_ |
| E4 | Gửi email thất bại | Vẫn tạo tài khoản thành công; ghi log lỗi gửi mail; Manager tự thông báo thủ công |

#### 7.2.2. Đặc tả UC07.2 — Cấp và Quản lý tài khoản đăng nhập

| **Trường** | **Nội dung** |
| --- | --- |
| Mã Use Case | UC07.2 |
| Tác nhân | Manager |
| Điều kiện tiên quyết | Nhân viên đã có hồ sơ trong hệ thống (UC07.1 đã thực hiện) |
| Kết quả | Tài khoản được cấp phát, cập nhật hoặc thu hồi đúng với trạng thái thực tế của nhân viên |

**Luồng sự kiện — Đặt lại mật khẩu:**

| **Bước** | **Hành động** |
| --- | --- |
| 1 | Manager chọn nhân viên → Đặt lại mật khẩu |
| 2 | Hệ thống tạo mật khẩu ngẫu nhiên mới và hash bằng BCrypt (salt 12 rounds) |
| 3 | Gửi mật khẩu tạm thời qua SMS/Email |
| 4 | Lần đăng nhập đầu, hệ thống bắt buộc nhân viên đổi mật khẩu mới |

#### 7.2.3. Đặc tả UC07.3 — Phân quyền RBAC

Hệ thống phân quyền theo mô hình **Role-Based Access Control (RBAC)**, quản lý 3 cấp độ vai trò:

| **Vai trò (Role)** | **Mã vai trò** | **Quyền hạn chính** |
| --- | --- | --- |
| Quản lý | MANAGER | Toàn quyền: CRUD nhân viên, phê duyệt lương, xem báo cáo, cấu hình hệ thống |
| Thu ngân | CASHIER | Tạo/đóng đơn hàng, xử lý thanh toán, in hóa đơn; xem lịch ca của bản thân |
| Nhân viên phục vụ | WAITER | Cập nhật trạng thái bàn, thêm món vào đơn; chấm công cá nhân |

**Ma trận phân quyền chi tiết:**

| **Chức năng** | **MANAGER** | **CASHIER** | **WAITER** |
| --- | --- | --- | --- |
| Xem danh sách nhân viên |  |  |  |
| Thêm/Sửa nhân viên |  |  |  |
| Phân công ca làm |  |  |  |
| Check-in/Check-out |  |  |  |
| Xem lịch sử chấm công |  |  |  |
| Duyệt điều chỉnh chấm công |  |  |  |
| Tạo đơn hàng |  |  |  |
| Xử lý thanh toán |  |  |  |
| Xem báo cáo doanh thu |  |  |  |
| Cấu hình thực đơn |  |  |  |

### 7.3. Biểu đồ Tuần tự (Sequence Diagram) — Luồng Check-in Nhân viên

Biểu đồ này mô tả chi tiết giao tiếp giữa các lớp trong kiến trúc phân lớp khi nhân viên thực hiện Check-in, tập trung vào việc **xác thực danh tính** và **kiểm tra phân công ca** trước khi ghi nhận:

![Image 19](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_019.png)

*Biểu đồ** 13*

**Giải thích các biến số:**

id_nv — Mã nhân viên (ID Nhân viên), lấy từ session đăng nhập.

tg_ht — Thời gian hiện tại, dùng để đối chiếu với bảng shift_assignment.

tg_vao — Thời gian Check-in thực tế, tương đương check_in_time trong bảng attendance.

### 7.4. Biểu đồ Hoạt động (Activity Diagram) — Quy trình Onboarding nhân viên mới

![Image 20](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_020.png)

*Biểu đồ** 14*

### 7.5. Mô hình Dữ liệu (ERD) — Phân hệ Nhân sự

Lược đồ CSDL của phân hệ nhân sự được thiết kế tách bạch rõ ràng giữa **hồ sơ nhân sự** (thông tin cứng, ít thay đổi) và **tài khoản hệ thống** (thông tin xác thực, phân quyền):

![Image 21](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_021.png)

*Biểu đồ** 15*

***Quyết định thiết kế:** Tách bảng `nhan_vien` và `tai_khoan` thay vì gộp chung nhằm tuân thủ **Nguyên tắc Phân tách mối quan tâm (Separation of Concerns)**. Khi nhân viên nghỉ việc, tài khoản bị `kich_hoat = 0` (không xóa) để bảo toàn toàn bộ lịch sử `audit_log` và dữ liệu chấm công phục vụ kiểm toán.*

### 7.6. Ràng buộc Nghiệp vụ (Business Rules)

| **Mã BR** | **Quy tắc** | **Cơ chế kiểm soát** |
| --- | --- | --- |
| BR-NS-01 | Mỗi nhân viên chỉ có đúng một tài khoản đăng nhập (quan hệ 1-1) | Unique Constraint trên tai_khoan.id_nhan_vien |
| BR-NS-02 | Mật khẩu phải được băm bằng BCrypt trước khi lưu; không lưu plain text | Xử lý tại tầng Service; không bao giờ lưu chuỗi gốc |
| BR-NS-03 | Lần đăng nhập đầu tiên bắt buộc đổi mật khẩu | Cờ buoc_doi_mat_khau = 1; middleware chặn mọi request trừ endpoint đổi mật khẩu |
| BR-NS-04 | Không được xóa vật lý (hard delete) bản ghi nhân viên | Chỉ đặt trang_thai = 'da_nghi_viec' và kich_hoat = 0 (Soft Delete) |
| BR-NS-05 | Mọi thao tác thêm/sửa/xoá nhân viên phải được ghi vào audit_log | Database Trigger AFTER INSERT/UPDATE/DELETE trên bảng nhan_vien và tai_khoan |
| BR-NS-06 | Không thể phân công ca cho nhân viên có tài khoản bị khóa | Trigger kiểm tra tai_khoan.kich_hoat = 1 trước khi INSERT vào shift_assignment |

### 7.7. Kiểm thử Use Case UC07

#### 7.7.1. Test Case cho UC07.1 (Thêm nhân viên)

| **Mã TC** | **Kịch bản** | **Điều kiện đầu vào** | **Kết quả mong đợi** | **Trạng thái** |
| --- | --- | --- | --- | --- |
| TC-UC07-01 | Thêm nhân viên thành công | Dữ liệu hợp lệ, CCCD chưa tồn tại | Tạo bản ghi nhan_vien + tai_khoan; email được gửi | Chờ test |
| TC-UC07-02 | CCCD đã tồn tại trong hệ thống | CCCD trùng với nhân viên khác | Hiển thị lỗi E1; không INSERT bất kỳ bản ghi nào | Chờ test |
| TC-UC07-03 | Email sai định dạng | email = "khong_hop_le" | Highlight lỗi, thông báo E2; không cho phép submit | Chờ test |
| TC-UC07-04 | Lương thấp hơn tối thiểu vùng | luong_gio = 15000 (< 22.500đ) | Hiển thị cảnh báo E3; Manager xác nhận mới lưu | Chờ test |
| TC-UC07-05 | Gửi email thất bại sau khi tạo xong | SMTP server down | Nhân viên vẫn được tạo; ghi log lỗi; không rollback | Chờ test |

#### 7.7.2. Test Case cho UC07.3 (Phân quyền RBAC)

| **Mã TC** | **Kịch bản** | **Điều kiện đầu vào** | **Kết quả mong đợi** | **Trạng thái** |
| --- | --- | --- | --- | --- |
| TC-UC07-06 | CASHIER truy cập chức năng quản lý nhân viên | Vai trò CASHIER gọi API /employees | HTTP 403 Forbidden; ghi audit_log | Chờ test |
| TC-UC07-07 |  | vai_tro = 'CASHIER' cho id_nv = 5 | Cập nhật tai_khoan.vai_tro; quyền hạn thay đổi ngay | Chờ test |
| TC-UC07-08 | Đăng nhập sau khi tài khoản bị khoá | kich_hoat = 0 | HTTP 401; thông báo: _"Tài khoản bị tạm khoá."_ | Chờ test |
| TC-UC07-09 | Xem lịch sử chấm công của người khác (WAITER) | WAITER gọi API chấm công id_nv = 10 | HTTP 403 Forbidden; chỉ được xem bản ghi của chính mình | Chờ test |

### 7.8. Đánh giá và Định hướng mở rộng UC07

**Những điểm mạnh của thiết kế hiện tại:**

Mô hình **Soft Delete** đảm bảo toàn vẹn dữ liệu lịch sử, đặc biệt quan trọng khi kiểm toán tài chính.

Kiến trúc **RBAC** với bảng vai_tro_quyen trung gian cho phép thêm/sửa quyền hạn mà không cần thay đổi mã nguồn.

**BCrypt (12 rounds)** cung cấp bảo vệ mật khẩu đủ mạnh, chịu được brute-force attack với phần cứng hiện đại.

**Audit Log** ở tầng CSDL (trigger) đảm bảo ghi nhận ngay cả khi ứng dụng gặp sự cố.

**Hướng mở rộng trong phiên bản tương lai:**

| **Tính năng** | **Mô tả** | **Độ phức tạp** |
| --- | --- | --- |
| Đăng nhập 2 yếu tố (2FA) | OTP qua SMS/Authenticator app tại mỗi lần đăng nhập | Trung bình |
| Single Sign-On (SSO) | Tích hợp đăng nhập qua Google Workspace cho chuỗi nhiều chi nhánh | Cao |
| Hợp đồng lao động điện tử | Lưu trữ và ký số hợp đồng ngay trong hệ thống | Cao |
| Dashboard phân tích nhân sự | Thống kê tỷ lệ turnover, thâm niên, Biểu đồ cơ cấu nhân sự | Trung bình |
