## CHƯƠNG 1: TỔNG QUAN, KHẢO SÁT VÀ ĐẶC TẢ YÊU CẦU

### 1.1. Khảo sát và Định hình bài toán hiện trạng

#### 1.1.1. Phương pháp và Phạm vi khảo sát

Để thu thập dữ liệu đầu vào cho giai đoạn đặc tả, nhóm nghiên cứu đã triển khai quy trình khảo sát theo chuẩn kỹ nghệ phần mềm (Software Engineering elicitation), kết hợp đồng thời ba kỹ thuật thu thập yêu cầu:

**Phỏng vấn có cấu trúc (Structured Interview):** Tiến hành phỏng vấn sâu với chủ quán và trưởng ca nhằm khai thác các quy trình nghiệp vụ cốt lõi và các điểm đau (pain points) đang tồn tại.

**Quan sát thực địa (Direct Observation):** Theo dõi quy trình xử lý đơn hàng trong ca bận (giờ cao điểm) để ghi nhận các thao tác thủ công dễ phát sinh lỗi.

**Phân tích tài liệu hiện tại (Document Analysis):** Nghiên cứu sổ ghi tay chấm công, phiếu thu và danh sách thực đơn để hiểu cách dữ liệu đang được lưu trữ phi số hóa.

#### 1.1.2. Mô tả hiện trạng và các vấn đề tồn tại

Kết quả khảo sát phác họa bức tranh một hệ thống vận hành hoàn toàn thủ công với nhiều khâu dễ phát sinh sai sót. Cụ thể, quy trình từ lúc khách gọi món đến khi hóa đơn được in ra phải qua ít nhất bốn lần truyền đạt thông tin bằng miệng hoặc phiếu viết tay, dẫn đến tỷ lệ sai lệch đơn hàng cao. Bên cạnh đó, việc quản lý ca làm và chấm công được thực hiện bằng sổ nhật ký thủ công khiến quá trình đối soát lương cuối tháng tốn nhiều thời gian và thiếu tính khách quan.

Dưới góc độ phân tích SWOT của hệ thống hiện tại:

|  | **Điểm mạnh (S)** | **Điểm yếu (W)** |
| --- | --- | --- |
| Nội tại | Chi phí vận hành ban đầu thấp; nhân viên quen với quy trình | Dễ sai sót; không có dữ liệu lịch sử để phân tích; khó mở rộng |
|  | Cơ hội (O) | Thách thức (T) |
| Ngoại cảnh | Nhu cầu số hóa F&B ngày càng tăng; chi phí phần cứng POS giảm | Sức cạnh tranh từ các chuỗi café đã có hệ thống số; kỳ vọng trải nghiệm từ khách hàng Gen Z |

#### 1.1.3. Tầm nhìn và Phạm vi dự án (Vision & Scope)

Từ những bất cập được nhận diện, tầm nhìn của dự án được phát biểu như sau: _"Xây dựng một nền tảng quản lý café tập trung, tự động hóa toàn bộ các quy trình vận hành cốt lõi — từ tiếp nhận đơn hàng, quản trị kho bãi đến chấm công nhân sự — nhằm loại bỏ sai sót thủ công, tối ưu hóa nguồn lực và nâng cao trải nghiệm thực khách."_

Phạm vi hệ thống được khoanh vùng rõ ràng: hệ thống phục vụ tối đa cho một chi nhánh café đơn lẻ với quy mô không quá 50 bàn và 20 nhân viên, chạy trên nền tảng Windows 7 trở lên và tích hợp với thiết bị POS chuẩn thị trường.

### 1.2. Xác định Tác nhân (Actors) và Biểu đồ Use Case tổng quát

#### 1.2.1. Phân định và Đặc tả chi tiết từng Tác nhân

Hệ thống được thiết kế với cơ chế phân quyền người dùng theo mô hình RBAC (Role-Based Access Control), phân cấp thành ba nhóm tác nhân chính:

**a. Cấp Quản lý — Manager**

*Đây là tác nhân nắm quyền cao nhất trong hệ thống, chịu trách nhiệm toàn diện về cấu hình và giám sát.*

Các chức năng chính của Manager bao gồm: thiết lập danh mục thực đơn và giá bán, quản trị tài khoản người dùng, lập kế hoạch ca làm việc (Shift Planning), phê duyệt điều chỉnh lương, giám sát tồn kho theo ngưỡng cảnh báo, và truy xuất báo cáo doanh thu theo ngày/tháng.

**b. Nhân viên nghiệp vụ — Employee**

*Tác nhân trực tiếp tạo ra giá trị dịch vụ, tương tác với hệ thống thường xuyên nhất.*

Nhóm nhân viên được phân vai chuyên biệt:

**Thu ngân (Cashier):** Tạo, sửa, tính tiền và đóng hóa đơn; tiếp nhận thanh toán đa hình thức (tiền mặt, thẻ, QR).

**Phục vụ (Waiter):** Cập nhật trạng thái bàn, thêm món vào đơn đang mở, phản hồi yêu cầu của thực khách.

**Pha chế (Barista):** Nhận thông báo đơn hàng qua màn hình pha chế (KDS), cập nhật trạng thái sẵn sàng của từng đồ uống.

**c. Khách hàng — Customer**

*Tác nhân thụ hưởng kết quả của hệ thống, tương tác gián tiếp.*

Khách hàng không đăng nhập vào hệ thống nhưng là đối tượng trung tâm của toàn bộ nghiệp vụ. Trong các mô hình café hiện đại, khách hàng có thể tương tác trực tiếp thông qua giao diện tự order (Self-Service Kiosk) hoặc mã QR đặt bàn — đây là hướng mở rộng tiềm năng của hệ thống.

**d. Tác nhân AI — AI Service Agent** _(tác nhân phi người dùng)_

*Tác nhân tự động chạy ngầm (background agent), không tương tác người dùng trực tiếp.*

Đây là thành phần trí tuệ nhân tạo của hệ thống, bao gồm ba module:

**Demand Forecasting Engine:** Phân tích lịch sử bán hàng kết hợp dữ liệu thời tiết để dự báo nhu cầu nguyên liệu, tự động đề xuất phiếu nhập kho — giảm thiểu lãng phí thực phẩm.

**Staff Scheduling Optimizer:** Đề xuất lịch làm việc tối ưu dựa trên dự báo lưu lượng khách hàng theo ngày/khung giờ.

**Customer Behavior Analyzer:** Phân cụm hành vi mua hàng (K-Means) để cá nhân hóa chương trình khuyến mãi và gợi ý Up-selling cho từng nhóm khách hàng thân thiết.

#### 1.2.2. Biểu đồ Use Case tổng quát (mô tả văn bản)

Biểu đồ Use Case tổng quát thể hiện phạm vi hệ thống (System Boundary) và các tương tác giữa tác nhân với các ca sử dụng:

![Image 6](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_006.png)

*Biểu đồ** 3*

### 1.3. Đặc tả Yêu cầu Chức năng (Functional Requirements)

Yêu cầu chức năng được thu thập, phân loại và đánh mã theo chuẩn IEEE 830, đảm bảo tính truy vết (traceability) từ yêu cầu đến thiết kế:

| **Mã YC** | **Phân hệ** | **Mô tả yêu cầu** | **Mức độ ưu tiên** |
| --- | --- | --- | --- |
| FR-01 | Đơn hàng | Nhân viên có thể tạo mới, sửa đổi và hủy đơn hàng trên bàn đang hoạt động | Cao |
| FR-02 | Đơn hàng | Hệ thống tự động gửi thông báo cho khu vực pha chế khi có đơn mới | Cao |
| FR-03 | Bàn | Trạng thái bàn cập nhật theo thời gian thực, không cần làm mới trang | Cao |
| FR-04 | Thanh toán | Hỗ trợ tối thiểu 3 hình thức thanh toán: tiền mặt, thẻ và QR Pay | Trung bình |
| FR-05 | Thanh toán | Hóa đơn có thể xuất ra máy in nhiệt theo định dạng chuẩn | Cao |
| FR-06 | Kho | Tự động cập nhật tồn kho khi đơn hàng được xác nhận, theo công thức Recipe | Cao |
| FR-07 | Kho | Cảnh báo khi tồn kho nguyên liệu xuống dưới ngưỡng tối thiểu định trước | Trung bình |
| FR-08 | Nhân sự | Quản lý tạo và phân công ca làm cho từng nhân viên theo ngày/tuần | Cao |
| FR-09 | Nhân sự | Nhân viên thực hiện Check-in/Check-out, hệ thống ghi nhận giờ làm thực tế | Cao |
| FR-10 | Nhân sự | Hệ thống tính lương đa biến theo Nghị định 38/2022/NĐ-CP: giờ hành chính, tăng ca (hệ số 1.5/2.0/3.0), ca đêm (hệ số +30%), phụ cấp và khấu trừ | Cao |
| FR-11 | Báo cáo | Tổng hợp và trực quan hóa doanh thu theo ngày, tuần, tháng | Trung bình |
| FR-12 | Báo cáo | Thống kê top 10 mặt hàng bán chạy nhất trong kỳ được chọn | Thấp |
| FR-13 | AI — Kho | Module AI dự báo nhu cầu nguyên liệu dựa trên lịch sử bán hàng và yếu tố thời tiết, tự động tạo đề xuất phiếu nhập | Trung bình |
| FR-14 | AI — Nhân sự | Module AI tự động đề xuất lịch phân ca dựa trên dự báo lưu lượng khách hàng theo ngày/giờ | Trung bình |
| FR-15 | Chấm công | Ứng dụng di động hỗ trợ chấm công bằng Geofencing (GPS) kết hợp xác thực khuôn mặt/selfie, ngăn chặn chấm công hộ | Cao |
| FR-16 | Khách hàng | Hệ thống quản lý khách hàng thân thiết; AI phân cụm hành vi để cá nhân hóa khuyến mãi và gợi ý up-selling | Thấp |

### 1.4. Đặc tả Yêu cầu Phi chức năng (Non-functional Requirements)

Yêu cầu phi chức năng là các ràng buộc chất lượng hệ thống, không trực tiếp mô tả hành vi mà quy định **cách** hệ thống thực hiện. Chúng được phân tích theo mô hình chất lượng ISO/IEC 25010:

| **Thuộc tính** | **Yêu cầu cụ thể** | **Cách đo lường** |
| --- | --- | --- |
| Hiệu năng (Performance) | Thời gian phản hồi mọi thao tác nghiệp vụ < 3 giây trong điều kiện mạng LAN bình thường | Đo bằng công cụ profiling khi tải 20 người dùng đồng thời |
| Tính sẵn sàng (Availability) | Hệ thống hoạt động 24/7; RTO (Recovery Time Objective) < 30 phút khi có sự cố | Theo dõi uptime log; kịch bản drill phục hồi dữ liệu |
| Bảo mật (Security) | Phân quyền RBAC nghiêm ngặt; mật khẩu được băm (hashed) bằng BCrypt; nhật ký thao tác (Audit Log) lưu tối thiểu 90 ngày | Kiểm tra thâm nhập (Penetration Test) mức cơ bản |
| Tính khả dụng (Usability) | Nhân viên mới (không có kỹ năng CNTT) có thể thành thạo các chức năng cơ bản sau ≤ 2 giờ đào tạo | Kiểm thử người dùng (User Testing) với mẫu 5 nhân viên mới |
| Tính tương thích (Compatibility) | Chạy ổn định trên Windows 7 SP1 trở lên; tương thích với máy in nhiệt chuẩn ESC/POS | Kiểm thử trên 3 cấu hình phần cứng POS phổ biến tại thị trường Việt Nam |
| Khả năng bảo trì (Maintainability) | Mã nguồn đạt độ bao phủ kiểm thử (Code Coverage) ≥ 70%; tài liệu hóa đầy đủ tại mọi module | Đo bằng JaCoCo hoặc công cụ tương đương |

### 1.5. Phân tích rủi ro dự án (Preliminary Risk Analysis)

Nhằm chủ động kiểm soát các nguy cơ có thể ảnh hưởng đến tiến độ và chất lượng, nhóm thực hiện một phân tích rủi ro sơ bộ theo ma trận Xác suất × Tác động:

| **Rủi ro** | **Xác suất** | **Tác động** | **Biện pháp giảm thiểu** |
| --- | --- | --- | --- |
| Yêu cầu thay đổi giữa chừng (Scope Creep) | Cao | Cao | Sử dụng Use Case Specification làm tài liệu ký kết; áp dụng Change Management Process |
| Thiếu dữ liệu thực tế để kiểm thử | Trung bình | Trung bình | Sinh dữ liệu mẫu (Seed Data) mô phỏng hoạt động thực tế |
| Thành viên nhóm vắng giữa sprint | Thấp | Cao | Phân công chéo nghiệp vụ; tài liệu hóa handover |
| Lỗi tích hợp phần cứng POS | Trung bình | Cao | Kiểm thử thiết bị từ sớm; chuẩn bị driver dự phòng |
