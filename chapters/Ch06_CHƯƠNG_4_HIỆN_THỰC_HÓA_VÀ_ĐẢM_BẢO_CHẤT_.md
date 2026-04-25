## CHƯƠNG 4: HIỆN THỰC HÓA VÀ ĐẢM BẢO CHẤT LƯỢNG (SQA)

> **Mục tiêu chương:** Chứng minh hệ thống vận hành được và không có lỗi nghiêm trọng. Tập trung vào giao diện và các ca kiểm thử của phân hệ Nhân sự/Chấm công. Chiếm khoảng 25%.

### 4.1. Ngăn xếp Công nghệ và Tiêu chuẩn Lập trình

| **Tầng**              | **Công nghệ**       | **Lý do lựa chọn**                                                |
| --------------------- | ------------------- | ----------------------------------------------------------------- |
| **Giao diện máy tính** | Java Swing / JavaFX | Chạy ổn định trên Windows; dễ tích hợp máy in nhiệt ESC/POS     |
| **API phía máy chủ**   | Java Spring Boot    | Hệ sinh thái trưởng thành; dễ xây dựng API REST; tích hợp tốt với ORM |
| **ORM**                | Hibernate / JPA     | Giảm mã SQL lặp lại; dễ chuyển đổi CSDL khi cần                  |
| **Cơ sở dữ liệu**     | MySQL 8.0           | Miễn phí; hiệu năng tốt với quy mô nhỏ-vừa; hỗ trợ ACID đầy đủ    |
| **Công cụ biên dịch**  | Maven               | Quản lý phụ thuộc chuẩn hóa; dễ tích hợp CI/CD                    |

Toàn bộ mã nguồn tuân thủ **hướng dẫn định dạng mã Java của Google**, được kiểm soát qua các công cụ tự động:

```mermaid
graph LR
    A["Viết mã nguồn"] --> B["Checkstyle\nKiểm tra quy tắc trình bày"]
    B --> C["SpotBugs\nPhát hiện lỗi tiềm ẩn"]
    C --> D["SonarLint\nPhát hiện mùi mã"]
    D --> E["Rà soát mã nguồn\nbởi đồng đội"]
    E --> F["Hợp nhất vào nhánh develop"]

    style A fill:#37474F,color:#fff
    style B fill:#1565C0,color:#fff
    style C fill:#C62828,color:#fff
    style D fill:#E65100,color:#fff
    style E fill:#4527A0,color:#fff
    style F fill:#2E7D32,color:#fff
```

**Các quy tắc viết mã sạch được áp dụng:**

- **Đặt tên có ý nghĩa:** Không dùng tên biến đơn lẻ (`x`, `temp`); tên phương thức phải là động từ mô tả hành động (`tinhTongTien()`, `layDanhSachBanTrong()`).
- **Hàm làm một việc (Single Responsibility):** Mỗi phương thức không dài hơn 20 dòng và chỉ giải quyết một vấn đề duy nhất.
- **Không có mã chết:** Xóa toàn bộ đoạn mã bị chú thích bỏ và hàm không được gọi trước khi hợp nhất.
- **Xử lý ngoại lệ rõ ràng:** Bắt `Exception` cụ thể, không dùng `catch(Exception e) {}` rỗng.

Mỗi tính năng được phát triển trên một nhánh `feature/` riêng biệt và phải trải qua ít nhất **1 lượt rà soát** từ thành viên khác trước khi hợp nhất vào nhánh `develop`. Danh sách kiểm tra gồm:

- [ ] Logic nghiệp vụ đúng với đặc tả ca sử dụng
- [ ] Không có lỗ hổng SQL Injection (dùng PreparedStatement)
- [ ] Có xử lý trường hợp null/empty đầu vào
- [ ] Có kiểm thử đơn vị cho logic phức tạp (tính tiền, tính lương)
- [ ] Tuân thủ quy ước lập trình

---

### 4.2. Thiết kế Giao diện — Màn hình Nhân sự và Chấm công

#### 4.2.1. Màn hình Đăng nhập

> **Màn hình Đăng nhập:** Giao diện tối giản gồm hai trường nhập liệu (_Tên đăng nhập_ và _Mật khẩu_) cùng nút _ĐĂNG NHẬP_. Hệ thống áp dụng cơ chế **khóa tài khoản tạm thời 5 phút** sau 3 lần sai liên tiếp và **bắt buộc đổi mật khẩu** ở lần đăng nhập đầu tiên.

_Sau 3 lần đăng nhập sai: tài khoản bị khoá tạm 5 phút. Lần đầu đăng nhập bắt buộc đổi mật khẩu._

#### 4.2.2. Màn hình Bảng điều khiển Nhân viên — Chấm công

> **Màn hình Bảng điều khiển Nhân viên:** Giao diện tập trung hiển thị thông tin ca làm việc hiện hành, trạng thái xác thực vị trí (GPS) và hai nút thao tác cốt lõi: **VÀO CA** và **KẾT THÚC CA**. Phần nửa dưới màn hình hiển thị bảng thống kê lịch làm việc chi tiết trong tuần (ngày, ca, trạng thái đi muộn/đúng giờ) và tổng hợp số giờ công cùng lương ước tính của tháng, hỗ trợ nhân viên chủ động theo dõi hiệu suất cá nhân.

#### 4.2.3. Màn hình Quản lý Nhân viên (dành cho Quản lý)

> **Màn hình Quản lý Nhân viên:** Giao diện quản trị trung tâm phân quyền riêng cho Quản lý. Màn hình cung cấp thanh công cụ để thêm mới nhân viên, tìm kiếm và xuất báo cáo. Dữ liệu được trình bày dưới dạng bảng lưới gồm mã định danh, họ tên, vai trò RBAC, trạng thái nhân sự (đang làm/nghỉ phép), cùng cột thao tác cho phép Quản lý nhanh chóng cập nhật thông tin hoặc khóa tài khoản hệ thống khi cần thiết.

### 4.3. Mô hình Tháp Kiểm thử và Chiến lược SQA

**Chiến lược tháp kiểm thử tự động** được dự án áp dụng thông qua việc phân lớp kiểm thử thành 4 cấp độ từ thấp lên cao. Mục tiêu cốt lõi là tối ưu hóa chi phí phát triển và tăng tốc độ phát hiện lỗi sớm trong chu kỳ:

1. **Kiểm thử đơn vị — Tỷ trọng khoảng 70%:** Tầng nền tảng chiếm tỷ lệ lớn nhất trong cấu trúc kiểm thử. Mục đích là cô lập và kiểm chứng tính đúng đắn của từng hàm, phương thức riêng lẻ.
2. **Kiểm thử tích hợp — Tỷ trọng khoảng 20%:** Tập trung đánh giá sự tương tác và tính toàn vẹn của luồng truyền tải dữ liệu giữa các mô-đun độc lập.
3. **Kiểm thử hệ thống — Tỷ trọng khoảng 8%:** Đánh giá toàn bộ luồng nghiệp vụ từ đầu đến cuối. Các kịch bản được chạy trên môi trường giả lập có cấu hình tương đương môi trường thực tế.
4. **Kiểm thử chấp nhận — Tỷ trọng khoảng 2%:** Cấp độ kiểm chứng cuối cùng do chính người dùng cuối hoặc đại diện khách hàng thực hiện để nghiệm thu sản phẩm.

### 4.4. Ca kiểm thử — UC04: Vào ca / Kết thúc ca

#### 4.4.1. Ca kiểm thử cho UC04.3 (Vào ca)

| **Mã TC**  | **Kịch bản**                   | **Điều kiện đầu vào**                               | **Kết quả mong đợi**                                        | **Trạng thái** |
| ---------- | ------------------------------ | --------------------------------------------------- | ----------------------------------------------------------- | -------------- |
| TC-UC04-01 | Vào ca thành công (đúng giờ) | Có ShiftAssignment hôm nay; chưa chấm công vào ca; đúng giờ | Tạo Attendance; thông báo thành công                        | Chờ kiểm thử   |
| TC-UC04-02 | Vào ca thành công (đến sớm)  | Sớm hơn 30 phút                                     | Hỏi xác nhận, sau đó tạo Attendance khi nhân viên đồng ý    | Chờ kiểm thử   |
| TC-UC04-03 | Vào ca muộn                  | Muộn hơn 15 phút                                    | Tạo Attendance; `is_late = TRUE`; thông báo có ghi chú muộn | Chờ kiểm thử   |
| TC-UC04-04 | Vào ca khi không có ca       | Không có ShiftAssignment hôm nay                    | Thông báo lỗi E1; không tạo Attendance                      | Chờ kiểm thử   |
| TC-UC04-05 | Vào ca lần 2 trong cùng ca   | Đã có Attendance với check_in_time                  | Thông báo lỗi E2; không ghi đè                              | Chờ kiểm thử   |

#### 4.4.2. Ca kiểm thử cho UC04.5 (Tính lương)

| **Mã TC**  | **Kịch bản**            | **Dữ liệu đầu vào**                       | **Kết quả mong đợi**                                            |
| ---------- | ----------------------- | ----------------------------------------- | --------------------------------------------------------------- |
| TC-UC04-06 | Tính lương 1 ca sáng ngày thường | Hoàn thành 1 ca sáng, `R_sang = 120.000đ` | Lương = 120.000đ |
| TC-UC04-07 | Tính lương 1 ca tối cuối tuần | Hoàn thành 1 ca tối cuối tuần, `R_toi = 140.000đ` | Lương = 140.000 × 1.5 = 210.000đ |
| TC-UC04-08 | Ca chưa check-out       | check_out_time = NULL                     | Chưa đưa vào bảng lương, chờ quản lý xác nhận                  |
| TC-UC04-09 | Tổng hợp cả tháng       | 18 ca sáng ngày thường + 8 ca tối ngày thường + 2 ca tối cuối tuần + 1 ca sáng ngày lễ | L = 18×120.000 + 8×140.000 + 2×140.000×1.5 + 1×120.000×2.0 = 3.940.000đ |

### 4.5. Ca kiểm thử — Phân quyền RBAC

| **Mã TC**  | **Kịch bản**                        | **Điều kiện đầu vào**                 | **Kết quả mong đợi**                              | **Trạng thái** |
| ---------- | ----------------------------------- | ------------------------------------- | ------------------------------------------------- | -------------- |
| TC-RBAC-01 | Thêm nhân viên, thư điện tử sai định dạng | `email = "khong_hop_le"`              | Tô nổi bật lỗi E2; không cho gửi biểu mẫu         | Chờ kiểm thử   |
| TC-RBAC-02 | Mức lương ca nhập không hợp lệ      | Mức lương ca sáng hoặc ca tối nhỏ hơn cấu hình tối thiểu của quán | Cảnh báo E3; Quản lý xác nhận mới lưu | Chờ kiểm thử |
| TC-RBAC-03 | Gửi thư điện tử thất bại sau khi tạo | Máy chủ SMTP ngừng hoạt động         | Nhân viên vẫn được tạo; ghi nhật ký lỗi; không hoàn tác | Chờ kiểm thử |
| TC-RBAC-04 | Thu ngân truy cập quản lý nhân viên  | `CASHIER` gọi API `/employees`        | HTTP 403; ghi `audit_log`               | Chờ kiểm thử   |
| TC-RBAC-05 | Quản lý nâng quyền nhân viên phục vụ thành thu ngân | `vai_tro = 'CASHIER'` cho `id_nv = 5` | Cập nhật `tai_khoan.vai_tro`; quyền thay đổi ngay | Chờ kiểm thử |
| TC-RBAC-06 | Đăng nhập khi tài khoản bị khóa     | `kich_hoat = 0`                       | HTTP 401; thông báo _"Tài khoản bị tạm khóa."_    | Chờ kiểm thử   |
| TC-RBAC-07 | Nhân viên phục vụ xem chấm công người khác | WAITER gọi API `attendance?id_nv=10`  | HTTP 403; chỉ xem bản ghi của mình      | Chờ kiểm thử   |

---

### 4.6. Kế hoạch SQA và Bảo trì (Maintenance Plan)

SQA không chỉ là kiểm thử — đây là một **quy trình xuyên suốt** toàn bộ SDLC nhằm phòng ngừa lỗi từ sớm. Các hoạt động SQA chính:

| **Hoạt động SQA**                   | **Thời điểm**                 | **Công cụ/Phương pháp**    |
| ----------------------------------- | ----------------------------- | -------------------------- |
| Rà soát đặc tả ca sử dụng           | Cuối giai đoạn Đặc tả         | Duyệt nội dung với giảng viên |
| Rà soát thiết kế ERD và biểu đồ lớp | Cuối giai đoạn Thiết kế       | Rà soát chéo nội bộ         |
| Phân tích tĩnh mã nguồn             | Liên tục trong quá trình viết mã | SonarLint, Checkstyle      |
| Kiểm thử đơn vị                     | Song song với giai đoạn hiện thực  | JUnit 5, Mockito           |
| Kiểm thử tích hợp                   | Sau khi ghép mô-đun           | Postman (API), JUnit       |
| Kiểm thử hệ thống                   | Trước khi bàn giao            | Kiểm thử tay theo kịch bản |
| Kiểm thử chấp nhận của người dùng   | Giai đoạn bàn giao            | Người dùng cuối thực hiện  |

Sau khi hệ thống được triển khai, giai đoạn bảo trì chiếm đến **~60-70% tổng chi phí vòng đời** của phần mềm (theo nghiên cứu của Pigoski, 1996). Do đó, kế hoạch bảo trì được lập chi tiết theo bốn loại hình:

| **Loại bảo trì**            | **Mục tiêu**                                          | **Ví dụ cụ thể trong dự án**                               | **Tần suất**               |
| --------------------------- | ----------------------------------------------------- | ---------------------------------------------------------- | -------------------------- |
| **Sửa lỗi**    | Khắc phục các lỗi được phát hiện sau triển khai | Sửa lỗi tính sai tiền thừa khi thanh toán bằng tiền mặt    | Ngay khi phát hiện         |
| **Hoàn thiện** | Nâng cấp, thêm tính năng mới theo nhu cầu      | Thêm phương thức thanh toán Momo/ZaloPay                   | Theo sprint (2-4 tuần/lần) |
| **Thích nghi** | Cập nhật để tương thích với môi trường mới     | Nâng cấp lên Windows 11; cập nhật MySQL từ 8.0 lên 8.4     | Khi môi trường thay đổi    |
| **Phòng ngừa** | Tái cấu trúc để giảm nợ kỹ thuật                | Tách lớp `HoaDonService` quá lớn thành các dịch vụ nhỏ hơn | Mỗi quý                    |

**Quy trình theo dõi và xử lý lỗi sau triển khai:**

Quy trình xử lý lỗi được thực hiện tuần tự qua **6 bước**:

1. **Phát hiện lỗi** — Người dùng hoặc tester ghi nhận lỗi
2. **Ghi nhận** — Tạo vấn đề trên GitHub Issues kèm mô tả, ảnh chụp màn hình
3. **Phân loại** — Đánh giá mức độ: _Nghiêm trọng_ / _Lớn_ / _Nhỏ_
4. **Phân công xử lý** — Giao cho thành viên phụ trách, sửa trên nhánh `hotfix/`
5. **Rà soát và kiểm thử lại** — Rà soát chéo và chạy kiểm thử đơn vị trước khi hợp nhất
6. **Hợp nhất và đóng vấn đề** — Triển khai và đóng vấn đề trên GitHub

---
