## CHƯƠNG 6: NGHIÊN CỨU CHUYÊN SÂU — USE CASE QUẢN LÝ CA LÀM VIỆC VÀ CHẤM CÔNG (UC04)

Chương này đi sâu vào phân tích và thiết kế một ca sử dụng cụ thể: **UC04 — Quản lý Ca làm việc và Chấm công**. Đây là phân hệ hạt nhân trong quản trị nhân sự, có tính phức tạp cao do phải xử lý đồng thời nhiều ràng buộc thời gian, dữ liệu và quyền truy cập. Phân tích chuyên sâu UC04 minh họa cho toàn bộ vòng đời thiết kế Use Case từ đặc tả đến thiết kế dữ liệu và kiểm thử.

### 6.1. Biểu đồ Use Case chi tiết UC04

#### 6.1.1. Phân định các ca sử dụng con (Sub-Use Cases)

UC04 được phân rã thành các ca sử dụng con độc lập, có thể được phân công cho các thành viên nhóm khác nhau:

│ │

│ ┌─────────────────────────┐ ┌────────────────────────────┐ │

│ │ (Create Shift Template) │ │ (Assign Shift to Employee)│ │

│ └─────────────────────────┘ └────────────────────────────┘ │

│ ▲ ▲ │

│ │«include» │«include» │

│ │ │ │

│ ┌─────────────────────────┐ ┌────────────────────────────┐ │

│ │ UC04.3: Check-in Ca làm │ │ UC04.4: Check-out Ca làm │ │

│ │ (Employee Check-in) │ │ (Employee Check-out) │ │

│ └─────────────────────────┘ └────────────────────────────┘ │

│ │ │ │

│ └──────────────────┬────────────────┘ │

│ │«extends» │

│ ┌─────────────────────┐ │

│ │ (Calculate Salary) │ │

│ └─────────────────────┘ │

│ │«extends» │

│ ┌─────────────────────┐ │

│ │ UC04.6: Xem báo cáo │ │

│ └─────────────────────┘ │

│ │

└────────────────────────────────────────────────────────────────────────────────────┘

▲ ▲

│ │

[Manager] [Employee]

UC04.1, 04.2, 04.5, 04.6 UC04.3, UC04.4

### 6.2. Đặc tả Use Case (Use Case Specification)

#### 6.2.1. Đặc tả UC04.3 — Nhân viên Check-in Ca làm

| **Trường** | **Nội dung** |
| --- | --- |
| Mã Use Case | UC04.3 |
| Tên Use Case | Check-in Ca làm việc |
| Tác nhân chính | Nhân viên (Employee) |
| Tác nhân thứ cấp | Hệ thống chấm công |
| Điều kiện tiên quyết | Nhân viên đã đăng nhập; tồn tại bản phân công ca (ShiftAssignment) cho nhân viên này trong ngày hôm nay; trạng thái ca là "chưa bắt đầu" |
| Điều kiện kết thúc (thành công) | Bản ghi Attendance được tạo với check_in_time = thời gian hiện tại; trạng thái phân công chuyển sang "đang làm việc" |
| Điều kiện kết thúc (thất bại) | Hệ thống hiển thị thông báo lỗi; trạng thái Attendance không thay đổi |

**Luồng sự kiện chính (Main Flow):**

| **Bước** | **Tác nhân** | **Hành động** |
| --- | --- | --- |
| 1 | Nhân viên | Mở màn hình Chấm công, chọn "Check-in" |
| 2 | Hệ thống | Truy vấn ShiftAssignment theo id_nhan_vien và ngày hiện tại |
| 3 | Hệ thống | Xác nhận tồn tại ca được phân công và ca chưa bắt đầu |
| 4 | Hệ thống | Tạo bản ghi Attendance với check_in_time = NOW() |
| 5 | Hệ thống | Cập nhật ShiftAssignment.trang_thai = 'dang_lam' |
| 6 | Hệ thống | Hiển thị thông báo: _"Check-in thành công lúc HH:MM. Chúc bạn làm việc hiệu quả!"_ |

**Luồng ngoại lệ (Alternative / Exception Flows):**

| **Mã** | **Điều kiện kích hoạt** | **Xử lý** |
| --- | --- | --- |
| E1 | Không tồn tại ShiftAssignment cho ngày hôm nay | Hiển thị: _"Bạn không có ca làm việc hôm nay. Liên hệ Quản lý."_ |
| E2 | Nhân viên đã Check-in trong ca này rồi | Hiển thị: _"Bạn đã Check-in lúc [giờ]. Không thể Check-in hai lần."_ |
| E3 | Check-in sớm hơn 30 phút so với giờ bắt đầu ca |  |
| E4 | Check-in muộn hơn 15 phút so với giờ bắt đầu ca | Ghi nhận Check-in bình thường nhưng đánh dấu is_late = TRUE trong bản ghi Attendance |
| E5 | Mất kết nối CSDL khi lưu | Thông báo lỗi kỹ thuật; ghi log; không tạo bản ghi Attendance |

#### 6.2.2. Đặc tả UC04.5 — Tính lương tự động

| **Trường** | **Nội dung** |
| --- | --- |
| Tác nhân | Manager (khởi tạo) / Hệ thống (thực thi) |
| Điều kiện tiên quyết | Tồn tại ít nhất một bản ghi Attendance có đủ cặp check-in/check-out trong kỳ tính lương |
| Kết quả | Hệ thống tổng hợp bảng lương cho từng nhân viên theo kỳ |

**Công thức tính lương:**

$$L_{nv} = \sum_{i=1}^{n} \left[ (t_{checkout_i} - t_{checkin_i}) \times r_{ca_i} \right] - P_{tre} + B_{bonus}$$

Trong đó:

$L_{nv}$: Tổng lương của nhân viên trong kỳ

$t_{checkout_i} - t_{checkin_i}$: Số giờ làm thực tế của ca $i$ (tính bằng giờ, làm tròn 2 chữ số thập phân)

$r_{ca_i}$: Đơn giá giờ của ca $i$ (có thể khác nhau giữa ca thường và ca cuối tuần/lễ)

$P_{tre}$: Khoản khấu trừ do đi muộn (nếu có, theo chính sách)

$B_{bonus}$: Thưởng thêm (nếu Quản lý nhập thủ công)

### 6.2.3. Xử lý Ngoại lệ Thông minh — Shift Swapping và Quên Check-out

Khác với các quy tắc cứng nhắc, hệ thống được thiết kế để xử lý **linh hoạt** các tình huống thực tế của nghiệp vụ ngành dịch vụ:

**a. Đổi ca đột xuất (Shift Swapping & Ad-hoc Check-in):**

Khi nhân viên đổi ca mà chưa có lịch trên hệ thống, hệ thống **không từ chối** chấm công. Thay vào đó:

Cho phép Check-in bình thường dựa trên xác thực GPS + khuôn mặt

Xếp bản ghi attendance vào trạng thái trang_thai = 'cho_phe_duyet' (Unscheduled Shift)

Gửi thông báo tới Quản lý để phê duyệt retroactively

shift_assignment tương ứng và liên kết lại

***Nguyên tắc thiết kế:** Hệ thống không được cản trở hoạt động vận hành; mọi ngoại lệ được thu thập để quản lý xử lý sau, không phải từ chối trước.*

**b. Xử lý "Quên Check-out":**

Trường hợp nhân viên quên bấm giờ ra, hệ thống **không được phép** gán giờ làm = 0 (vi phạm quyền lợi người lao động theo Bộ Luật Lao động):

![Image 17](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_017.png)

*Biểu đồ** 10*

### 6.2.4. Cơ chế Chấm công Sinh trắc học — Triệt tiêu Chấm công Hộ

Để ngăn chặn tình trạng **chấm công hộ (Buddy Punching)** — một vấn đề phổ biến trong ngành dịch vụ, ứng dụng di động tích hợp hai lớp bảo vệ:

| **Lớp** | **Công nghệ** | **Cơ chế hoạt động** |
| --- | --- | --- |
| Lớp 1: Vị trí | GPS Geofencing | Chỉ cho phép Check-in khi thiết bị nằm trong bán kính ≤ 100m từ tọa độ quán |
| Lớp 2: Danh tính | FaceID / Selfie AI | Chụp ảnh tại thời điểm Check-in, so sánh với ảnh đăng ký bằng thuật toán nhận diện khuôn mặt |

**Luồng xác thực:**

***Lưu trữ:** Ảnh selfie được mã hóa và lưu kèm bản ghi `attendance`, giữ tối thiểu 90 ngày để phục vụ kiểm toán nội bộ.*

### 6.2.5. Payroll Engine Đa biến — Tuân thủ NĐ 38/2022/NĐ-CP

Hệ thống loại bỏ công thức tính lương đơn giản và triển khai **động cơ tính lương đa biến** tuân thủ đầy đủ pháp luật lao động Việt Nam:

$$S_{total} = \sum_{i=1}^{n} \left( H_{basic,i} \times R \right) + \sum_{j=1}^{m} \left( H_{OT,j} \times R \times M_j \right) + \sum_{k=1}^{p} \left( H_{night,k} \times R \times N_k \right) + A_{total} - D_{total}$$

**Giải thích các biến số:**

| **Biến** | **Ý nghĩa** | **Giá trị theo luật** |
| --- | --- | --- |
| $H_{basic,i}$ | Giờ hành chính tiêu chuẩn |  |
| $R$ | Lương cơ bản theo giờ | ≥ 22.500 đ/giờ (Vùng I, 2024) |
| $H_{OT,j}$ | Giờ làm thêm (tăng ca) | ≤ 40h/tháng, ≤ 200h/năm |
| $M_j$ | Hệ số tăng ca | 1.5 (ngày thường) / 2.0 (ngày nghỉ) / 3.0 (Lễ, Tết) |
| $H_{night,k}$ | Giờ làm ca đêm (22:00–06:00) | Theo lịch thực tế |
| $N_k$ | Hệ số phụ cấp đêm | +30% (≥ 1.3); nếu vừa tăng ca vừa đêm → cộng thêm +20% |
| $A_{total}$ | Tổng phụ cấp (ăn ca, xăng xe...) | Theo chính sách quán |
| $D_{total}$ | Tổng khấu trừ (BHXH, đi muộn...) | Theo chính sách + pháp luật |

**Kiến trúc tách biệt hệ số khỏi mã nguồn:**

*Mọi hệ số $M_j$ và $N_k$ được lưu trong **Bảng ma trận cấu hình (Compliance Matrix)** riêng biệt trong CSDL, không hardcode vào logic code. Khi Chính phủ ban hành quy định mới, Nhân sự chỉ cần cập nhật bảng cấu hình mà **không cần phát hành phiên bản phần mềm mới**.*

| **Bảng** | **compliance_matrix** |
| --- | --- |
| loai_ca | ENUM: 'ngay_thuong', 'ngay_nghi', 'le_tet', 'ca_dem' |
| he_so | DECIMAL(4,2) — hệ số áp dụng |
| hieu_luc_tu | DATE — ngày bắt đầu hiệu lực |
| van_ban_phap_ly | VARCHAR — số nghị định tham chiếu |

#### 6.3.1. Lược đồ 4 bảng — Tách biệt Kế hoạch và Thực tế

Nguyên tắc thiết kế cốt lõi của UC04 là **tách biệt hoàn toàn** dữ liệu kế hoạch (Planning) khỏi dữ liệu thực tế (Actual), tương tự mô hình Planning vs. Actuals phổ biến trong kế toán quản trị:

![Image 18](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_018.png)

*Biểu đồ** 11*

***Ghi chú thiết kế:** 2 nhóm bảng trên tách biệt hoàn toàn **Kế hoạch** (shift_template, shift, shift_assignment) khỏi **Thực tế** (attendance), giúp dễ đối soát và kiểm toán.*

#### 6.3.2. Các Quy tắc Nghiệp vụ (Business Rules) cho UC04

| **Mã BR** | **Quy tắc** | **Cơ chế kiểm soát** |
| --- | --- | --- |
| BR-01 | Một nhân viên không thể có 2 ca chồng chéo thời gian trong cùng ngày | Trigger kiểm tra overlap khi INSERT vào shift_assignment |
| BR-02 | Chỉ có thể Check-out sau khi đã Check-in | check_out_time chỉ được UPDATE khi check_in_time IS NOT NULL |
| BR-03 | so_gio_lam không được tính nếu check_out_time IS NULL | Dùng CASE WHEN trong câu truy vấn tính lương |
| BR-04 | Giờ làm tối đa 16 giờ/ca; nếu vượt → đánh dấu cần xem xét thủ công | Constraint: CHECK(so_gio_lam <= 16) hoặc cờ needs_review = 1 |
| BR-05 | Ca cuối tuần (Thứ 7, Chủ nhật) được nhân hệ số 1.5 | Hàm tính lương kiểm tra DAYOFWEEK(ngay_lam_viec) trước khi áp đơn giá |

### 6.4. Biểu đồ Hoạt động (Activity Diagram) — Quy trình Chấm công toàn luồng

![Image 18](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_018.png)

*Biểu đồ** 12*

### 6.5. Kiểm thử Use Case UC04

#### 6.5.1. Test Case cho UC04.3 (Check-in)

| **Mã TC** | **Kịch bản** | **Điều kiện đầu vào** | **Kết quả mong đợi** | **Trạng thái** |
| --- | --- | --- | --- | --- |
| TC-UC04-01 | Check-in thành công (đúng giờ) | Có ShiftAssignment hôm nay; chưa check-in; đúng giờ | Tạo Attendance; thông báo thành công | Chờ test |
| TC-UC04-02 | Check-in thành công (đến sớm) | Sớm hơn 30 phút |  | Chờ test |
| TC-UC04-03 | Check-in muộn | Muộn hơn 15 phút | Tạo Attendance; is_late = TRUE; thông báo có ghi chú muộn | Chờ test |
| TC-UC04-04 | Check-in khi không có ca | Không có ShiftAssignment hôm nay | Thông báo lỗi E1; không tạo Attendance | Chờ test |
| TC-UC04-05 | Check-in lần 2 trong cùng ca | Đã có Attendance với check_in_time | Thông báo lỗi E2; không ghi đè | Chờ test |

#### 6.5.2. Test Case cho UC04.5 (Tính lương)

| **Mã TC** | **Kịch bản** | **Dữ liệu đầu vào** | **Kết quả mong đợi** |
| --- | --- | --- | --- |
| TC-UC04-06 | Tính lương ca thường | 8 giờ làm, đơn giá 25.000đ/giờ | Lương = 8 × 25.000 = 200.000đ |
| TC-UC04-07 | Tính lương ca cuối tuần | 8 giờ làm, đơn giá 25.000đ/giờ, hệ số 1.5 | Lương = 8 × 25.000 × 1.5 = 300.000đ |
| TC-UC04-08 | Ca chưa check-out | check_out_time = NULL | so_gio_lam = 0; không tính vào lương |
| TC-UC04-09 | Tổng hợp cả tháng | 22 ca thường (8h) + 4 ca cuối tuần (8h) | L = 22×8×25k + 4×8×25k×1.5 = 4.400.000 + 1.200.000 = 5.600.000đ |

### 6.6. Đánh giá và Định hướng mở rộng UC04

**Những điểm mạnh của thiết kế hiện tại:**

Kiến trúc **4 bảng phân tách kế hoạch/thực tế** đảm bảo tính toàn vẹn dữ liệu và dễ đối soát.

Luồng ngoại lệ được xử lý tường minh, không để hệ thống ở trạng thái không xác định.

Business Rules được mã hóa thành Trigger và Constraint ở tầng CSDL, tránh phụ thuộc hoàn toàn vào tầng ứng dụng.

**Hướng mở rộng trong phiên bản tương lai:**

| **Tính năng** | **Mô tả** | **Độ phức tạp** |
| --- | --- | --- |
| Chấm công bằng QR Code | Nhân viên quét QR được tạo theo ca làm, giới hạn địa điểm | Trung bình |
| Tích hợp xử lý lương tự động | Xuất file Excel bảng lương và gửi email thông báo | Thấp |
| Phân tích chuyên cần | Dashboard thống kê tỷ lệ đi muộn, vắng mặt theo tháng | Cao |
| Phê duyệt tăng ca |  | Trung bình |
