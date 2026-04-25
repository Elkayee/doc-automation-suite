## CHƯƠNG 4: HIỆN THỰC HÓA VÀ ĐẢM BẢO CHẤT LƯỢNG (SQA)

> **Mục tiêu chương:** Chứng minh hệ thống chạy được và không có bug. Tập trung vào giao diện và test case của phân hệ Nhân sự/Chấm công. Chiếm ~25%.

### 4.1. Ngăn xếp Công nghệ và Tiêu chuẩn Lập trình (Tech Stack)

| **Tầng**              | **Công nghệ**       | **Lý do lựa chọn**                                                |
| --------------------- | ------------------- | ----------------------------------------------------------------- |
| **Giao diện Desktop** | Java Swing / JavaFX | Cross-platform trên Windows; dễ tích hợp máy in nhiệt ESC/POS     |
| **Backend API**       | Java Spring Boot    | Hệ sinh thái trưởng thành; dễ viết REST API; tích hợp tốt với ORM |
| **ORM**               | Hibernate / JPA     | Giảm boilerplate SQL; dễ chuyển đổi CSDL khi cần                  |
| **Cơ sở dữ liệu**     | MySQL 8.0           | Miễn phí; hiệu năng tốt với quy mô nhỏ-vừa; hỗ trợ ACID đầy đủ    |
| **Build Tool**        | Maven               | Quản lý phụ thuộc chuẩn hóa; dễ tích hợp CI/CD                    |

Toàn bộ mã nguồn tuân thủ **Google Java Style Guide**, được kiểm soát qua các công cụ tự động:

```mermaid
graph LR
    A["✍️ Viết code"] --> B["🔍 Checkstyle\nStyle check"]
    B --> C["🐛 SpotBugs\nBug detect"]
    C --> D["📊 SonarLint\nCode smell"]
    D --> E["👥 Code Review\nPeer review"]
    E --> F["✅ Merge\nvào develop"]

    style A fill:#37474F,color:#fff
    style B fill:#1565C0,color:#fff
    style C fill:#C62828,color:#fff
    style D fill:#E65100,color:#fff
    style E fill:#4527A0,color:#fff
    style F fill:#2E7D32,color:#fff
```

**Các quy tắc Clean Code được áp dụng:**

- **Đặt tên có ý nghĩa:** Không dùng tên biến đơn lẻ (`x`, `temp`); tên phương thức phải là động từ mô tả hành động (`tinhTongTien()`, `layDanhSachBanTrong()`).
- **Hàm làm một việc (Single Responsibility):** Mỗi phương thức không dài hơn 20 dòng và chỉ giải quyết một vấn đề duy nhất.
- **Không có mã chết (No Dead Code):** Xóa toàn bộ code comment-out và hàm không được gọi trước khi merge.
- **Xử lý ngoại lệ rõ ràng:** Bắt `Exception` cụ thể, không dùng `catch(Exception e) {}` rỗng.

Mỗi tính năng được phát triển trên một nhánh `feature/` riêng biệt và phải trải qua ít nhất **1 lượt review** từ thành viên khác trước khi merge vào nhánh `develop`. Checklist review bao gồm:

- [ ] Logic nghiệp vụ đúng với đặc tả Use Case
- [ ] Không có lỗ hổng SQL Injection (dùng PreparedStatement)
- [ ] Có xử lý trường hợp null/empty đầu vào
- [ ] Có unit test cho logic phức tạp (tính tiền, tính lương)
- [ ] Tuân thủ coding convention

---

### 4.2. Thiết kế Giao diện — Màn hình Nhân sự và Chấm công

#### 4.2.1. Màn hình Đăng nhập

> **Màn hình Đăng nhập (Login Screen):** Giao diện tối giản gồm hai trường nhập liệu (_Tên đăng nhập_ và _Mật khẩu_) cùng nút _ĐĂNG NHẬP_. Hệ thống áp dụng cơ chế **khóa tài khoản tạm thời 5 phút** sau 3 lần sai liên tiếp và **bắt buộc đổi mật khẩu** ở lần đăng nhập đầu tiên.

_Sau 3 lần đăng nhập sai: tài khoản bị khoá tạm 5 phút. Lần đầu đăng nhập bắt buộc đổi mật khẩu._

#### 4.2.2. Màn hình Dashboard Nhân viên — Chấm công

> **Màn hình Dashboard Nhân viên:** Giao diện tập trung hiển thị thông tin ca làm việc hiện hành, trạng thái xác thực vị trí (GPS) và hai nút thao tác cốt lõi: **CHECK-IN** và **CHECK-OUT**. Phần nửa dưới màn hình hiển thị bảng thống kê lịch làm việc chi tiết trong tuần (ngày, ca, trạng thái đi muộn/đúng giờ) và tổng hợp số giờ công cùng lương ước tính của tháng, hỗ trợ nhân viên chủ động theo dõi hiệu suất cá nhân.

#### 4.2.3. Màn hình Quản lý Nhân viên (dành cho Manager)

> **Màn hình Quản lý Nhân viên:** Giao diện quản trị trung tâm phân quyền riêng cho Manager. Màn hình cung cấp thanh công cụ để thêm mới nhân viên, tìm kiếm và xuất báo cáo. Dữ liệu được trình bày dưới dạng bảng lưới (Data Grid) bao gồm mã ID, họ tên, vai trò RBAC, trạng thái nhân sự (đang làm/nghỉ phép), cùng cột thao tác (Action) cho phép Quản lý nhanh chóng cập nhật thông tin hoặc khóa tài khoản hệ thống khi cần thiết.

### 4.3. Mô hình Tháp Kiểm thử và Chiến lược SQA

**Chiến lược Tháp Kiểm thử (Test Automation Pyramid)** được dự án áp dụng thông qua việc phân lớp kiểm thử thành 4 cấp độ từ thấp lên cao. Mục tiêu cốt lõi là tối ưu hóa chi phí phát triển và tăng tốc độ phát hiện lỗi sớm trong chu kỳ (Shift-Left Testing):

1. **Kiểm thử Đơn vị (Unit Testing) — Tỷ trọng ~70%:** Tầng nền tảng chiếm tỷ lệ lớn nhất trong cấu trúc kiểm thử. Mục đích là cô lập và kiểm chứng tính đúng đắn của từng hàm, phương thức riêng lẻ. Ở cấp độ này, số lượng kịch bản (test cases) là nhiều nhất, tốc độ thực thi tự động nhanh nhất và chi phí sửa lỗi thấp nhất.
2. **Kiểm thử Tích hợp (Integration Testing) — Tỷ trọng ~20%:** Tập trung đánh giá sự tương tác và tính toàn vẹn của luồng truyền tải dữ liệu giữa các module độc lập (ví dụ: giữa Business Logic Layer và Data Access Layer, hoặc tích hợp API ngoại vi).
3. **Kiểm thử Hệ thống (System Testing) — Tỷ trọng ~8%:** Đánh giá toàn bộ luồng nghiệp vụ từ đầu đến cuối (End-to-End Testing). Các kịch bản được chạy trên môi trường giả lập (Staging) có cấu hình tương đương môi trường thực tế (Production) nhằm đảm bảo phần mềm đáp ứng đúng và đủ mọi đặc tả yêu cầu (SRS).
4. **Kiểm thử Chấp nhận (Acceptance Testing/UAT) — Tỷ trọng ~2%:** Cấp độ kiểm chứng cuối cùng do chính người dùng cuối (hoặc đại diện khách hàng) thực hiện để nghiệm thu sản phẩm. Do đòi hỏi nhiều nỗ lực thao tác thủ công, tốc độ phản hồi chậm và rủi ro chi phí cao, số lượng kịch bản ở tầng này được giới hạn chặt chẽ ở mức tối thiểu.

### 4.4. Test Case — UC04: Check-in / Check-out

#### 4.4.1. Test Case cho UC04.3 (Check-in)

| **Mã TC**  | **Kịch bản**                   | **Điều kiện đầu vào**                               | **Kết quả mong đợi**                                        | **Trạng thái** |
| ---------- | ------------------------------ | --------------------------------------------------- | ----------------------------------------------------------- | -------------- |
| TC-UC04-01 | Check-in thành công (đúng giờ) | Có ShiftAssignment hôm nay; chưa check-in; đúng giờ | Tạo Attendance; thông báo thành công                        | Chờ test       |
| TC-UC04-02 | Check-in thành công (đến sớm)  | Sớm hơn 30 phút                                     | Hỏi xác nhận → Tạo Attendance sau khi xác nhận              | Chờ test       |
| TC-UC04-03 | Check-in muộn                  | Muộn hơn 15 phút                                    | Tạo Attendance; `is_late = TRUE`; thông báo có ghi chú muộn | Chờ test       |
| TC-UC04-04 | Check-in khi không có ca       | Không có ShiftAssignment hôm nay                    | Thông báo lỗi E1; không tạo Attendance                      | Chờ test       |
| TC-UC04-05 | Check-in lần 2 trong cùng ca   | Đã có Attendance với check_in_time                  | Thông báo lỗi E2; không ghi đè                              | Chờ test       |

#### 4.4.2. Test Case cho UC04.5 (Tính lương)

| **Mã TC**  | **Kịch bản**            | **Dữ liệu đầu vào**                       | **Kết quả mong đợi**                                            |
| ---------- | ----------------------- | ----------------------------------------- | --------------------------------------------------------------- |
| TC-UC04-06 | Tính lương ca thường    | 8 giờ làm, đơn giá 25.000đ/giờ            | Lương = 8 × 25.000 = 200.000đ                                   |
| TC-UC04-07 | Tính lương ca cuối tuần | 8 giờ làm, đơn giá 25.000đ/giờ, hệ số 1.5 | Lương = 8 × 25.000 × 1.5 = 300.000đ                             |
| TC-UC04-08 | Ca chưa check-out       | check_out_time = NULL                     | so_gio_lam = 0; không tính vào lương                            |
| TC-UC04-09 | Tổng hợp cả tháng       | 22 ca thường (8h) + 4 ca cuối tuần (8h)   | L = 22×8×25k + 4×8×25k×1.5 = 4.400.000 + 1.200.000 = 5.600.000đ |

### 4.5. Test Case — Phân quyền RBAC

| **Mã TC**  | **Kịch bản**                        | **Điều kiện đầu vào**                 | **Kết quả mong đợi**                              | **Trạng thái** |
| ---------- | ----------------------------------- | ------------------------------------- | ------------------------------------------------- | -------------- |
| TC-RBAC-01 | Thêm NV — email sai định dạng       | `email = "khong_hop_le"`              | Highlight lỗi E2; không submit                    | Chờ test       |
| TC-RBAC-02 | Lương thấp hơn tối thiểu vùng       | `luong_gio = 15000` (< 22.500đ)       | Cảnh báo E3; Manager xác nhận mới lưu             | Chờ test       |
| TC-RBAC-03 | Gửi email thất bại sau khi tạo      | SMTP server down                      | NV vẫn được tạo; ghi log; không rollback          | Chờ test       |
| TC-RBAC-04 | CASHIER truy cập quản lý nhân viên  | `CASHIER` gọi API `/employees`        | HTTP 403 Forbidden; ghi `audit_log`               | Chờ test       |
| TC-RBAC-05 | MANAGER nâng quyền WAITER → CASHIER | `vai_tro = 'CASHIER'` cho `id_nv = 5` | Cập nhật `tai_khoan.vai_tro`; quyền thay đổi ngay | Chờ test       |
| TC-RBAC-06 | Đăng nhập khi tài khoản bị khoá     | `kich_hoat = 0`                       | HTTP 401; thông báo _"Tài khoản bị tạm khoá."_    | Chờ test       |
| TC-RBAC-07 | WAITER xem chấm công người khác     | WAITER gọi API `attendance?id_nv=10`  | HTTP 403 Forbidden; chỉ xem bản ghi của mình      | Chờ test       |

---

### 4.6. Kế hoạch SQA và Bảo trì (Maintenance Plan)

SQA không chỉ là kiểm thử — đây là một **quy trình xuyên suốt** toàn bộ SDLC nhằm phòng ngừa lỗi từ sớm. Các hoạt động SQA chính:

| **Hoạt động SQA**                   | **Thời điểm**                 | **Công cụ/Phương pháp**    |
| ----------------------------------- | ----------------------------- | -------------------------- |
| Review Use Case Specification       | Cuối giai đoạn Đặc tả         | Walkthrough với giảng viên |
| Review Thiết kế ERD & Class Diagram | Cuối giai đoạn Thiết kế       | Peer review nội bộ         |
| Static Code Analysis                | Liên tục trong quá trình code | SonarLint, Checkstyle      |
| Unit Testing                        | Song song với Implementation  | JUnit 5, Mockito           |
| Integration Testing                 | Sau khi ghép module           | Postman (API), JUnit       |
| System Testing                      | Trước khi bàn giao            | Kiểm thử tay theo kịch bản |
| User Acceptance Testing (UAT)       | Giai đoạn bàn giao            | Người dùng cuối thực hiện  |

Sau khi hệ thống được triển khai, giai đoạn bảo trì chiếm đến **~60-70% tổng chi phí vòng đời** của phần mềm (theo nghiên cứu của Pigoski, 1996). Do đó, kế hoạch bảo trì được lập chi tiết theo bốn loại hình:

| **Loại bảo trì**            | **Mục tiêu**                                          | **Ví dụ cụ thể trong dự án**                               | **Tần suất**               |
| --------------------------- | ----------------------------------------------------- | ---------------------------------------------------------- | -------------------------- |
| **Corrective** (Sửa lỗi)    | Khắc phục các lỗi (bug) được phát hiện sau triển khai | Sửa lỗi tính sai tiền thừa khi thanh toán bằng tiền mặt    | Ngay khi phát hiện         |
| **Perfective** (Hoàn thiện) | Nâng cấp, thêm tính năng mới theo nhu cầu             | Thêm phương thức thanh toán Momo/ZaloPay                   | Theo sprint (2-4 tuần/lần) |
| **Adaptive** (Thích nghi)   | Cập nhật để tương thích với môi trường mới            | Nâng cấp lên Windows 11; cập nhật MySQL từ 8.0 lên 8.4     | Khi môi trường thay đổi    |
| **Preventive** (Phòng ngừa) | Tái cấu trúc (refactor) để giảm nợ kỹ thuật           | Tách lớp `HoaDonService` quá lớn thành các service nhỏ hơn | Mỗi quý                    |

**Quy trình xử lý lỗi sau triển khai (Bug Tracking Workflow):**

Quy trình xử lý lỗi được thực hiện tuần tự qua **6 bước**:

1. **Phát hiện lỗi** — Người dùng hoặc tester ghi nhận lỗi
2. **Ghi nhận** — Tạo Issue trên GitHub Issues kèm mô tả, ảnh chụp màn hình
3. **Phân loại** — Đánh giá mức độ: _Critical_ (ảnh hưởng dữ liệu) / _Major_ / _Minor_
4. **Phân công xử lý** — Assign cho thành viên phụ trách, fix trên nhánh `hotfix/`
5. **Review & Test lại** — Peer review + chạy unit test trước khi merge
6. **Merge & Đóng Issue** — Deploy và đóng Issue trên GitHub

---
