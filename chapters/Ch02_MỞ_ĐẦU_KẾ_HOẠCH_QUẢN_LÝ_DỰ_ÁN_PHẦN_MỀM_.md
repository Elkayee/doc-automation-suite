## MỞ ĐẦU: KẾ HOẠCH QUẢN LÝ DỰ ÁN PHẦN MỀM (SPMP)

### 0.1. Mục đích, Phạm vi và Tầm nhìn Chiến lược

Dự án hướng tới xây dựng một nền tảng quản lý chuỗi café ứng dụng công nghệ **điện toán đám mây (Cloud-native)** và **Trí tuệ nhân tạo (AI)**. Hệ thống không chỉ giải quyết bài toán vận hành cơ bản (POS, thu ngân, kho bãi) mà còn tối ưu hóa nguồn lực nhân sự thông qua phân hệ quản trị ca làm việc thông minh. Bộ sản phẩm bao gồm ba nền tảng tích hợp:

| **Nền tảng** | **Đối tượng** | **Công nghệ** |
| --- | --- | --- |
| Ứng dụng Web Dashboard | Quản lý cấp cao | React / Next.js, Cloud-hosted |
| Phần mềm POS máy tính bảng | Thu ngân | Android tablet, giao thức ESC/POS |
| Ứng dụng di động nhân viên | Nhân viên | Flutter, GPS + FaceID |

### 0.2. Kế hoạch Phát triển — Agile CI/CD

Dự án được tổ chức theo mô hình **Agile (Scrum)** kết hợp quy trình **Tích hợp và Triển khai liên tục (CI/CD)**:

**Tích hợp liên tục (CI):** Mã nguồn được hợp nhất tự động sau mỗi Pull Request, kích hoạt bộ Unit Test và kiểm tra chất lượng mã lệnh (SonarQube). Hệ thống từ chối merge nếu code coverage module tính lương dưới 80%.

**Triển khai liên tục (CD):** Hệ thống được đóng gói dưới dạng **Container (Docker)** và triển khai lên môi trường Đám mây với khả năng **Auto-scaling** trong giờ cao điểm — đảm bảo hiệu năng không suy giảm khi lưu lượng tăng đột biến.

![Image 4](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_004.png)

*Biểu đồ** 1*

### 0.3. Phân Bổ Nhiệm Vụ Nhóm

Nhằm đảm bảo tiến độ và chất lượng, nhóm thực hiện phân chia trách nhiệm theo nguyên tắc **phân công theo phân hệ (module-based assignment)** — mỗi thành viên chịu trách nhiệm toàn diện (từ đặc tả đến thiết kế, cài đặt và kiểm thử) một phân hệ Use Case tương ứng:

| **Thành viên** | **Phân hệ phụ trách** | **Các bảng CSDL liên quan** | **Use Case** |
| --- | --- | --- | --- |
| Thành | Bán hàng, Quản lý khách hàng, Quản lý bàn phục vụ | hoa_don, hoa_don_chi_tiet, ban, khu_vuc, order_item_topping | UC1 |
| Tạ Bảo Anh Ngọc | Quản lý menu (sản phẩm) và công thức pha chế | do_uong, nhom_do_uong, topping, cong_thuc, nguyen_lieu | UC2 |
| Nguyễn Quang Đạo | Quản lý nguyên liệu và tồn kho | Store, Inventory, Order, Product, Recipe, Ingredient, RecipeItem , InventoryTransaction, InventoryTransactionItem | UC3 |
| Nguyễn Viết Tùng | Quản lý nhân viên, ca làm việc và chấm công | nhan_vien, tai_khoan, shift_template, shift, shift_assignment, attendance | UC4 |
| Ngô Thị Hồng Nhung | Báo cáo doanh thu / chi phí và quản lý danh sách cửa hàng | bao_cao_doanh_thu, chi_phi, danh_sach_cua_hang, hoa_don | UC5 + UC6 |

***Lưu ý****: Mỗi phân hệ UC liên quan đến 3–4 bảng dữ liệu, do đó mức độ phức tạp kỹ thuật của từng phần là tương đương nhau. Việc phân công theo phân hệ giúp tránh xung đột mã nguồn (code conflict) khi làm việc song song trên hệ thống quản lý phiên bản (Git).*

**Sơ đồ tổng quan phân công:**

![Image 5](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_005.png)

*Biểu đồ** 2*
