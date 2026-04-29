## CHƯƠNG 5: NGHIÊN CỨU CHUYÊN SÂU — USE CASE QUẢN LÝ NGUYÊN LIỆU VÀ TỒN KHO (UC03)

Chương này đi sâu vào mô tả và phân tích thiết kế một use case sử dụng cụ thể: **UC03 — Quản lý
Nguyên liệu và Tồn kho**. Use case này cho phép nhân viên theo dõi, nhập, xuất, điều chỉnh và xem
lịch sử tồn kho nguyên liệu.

### 5.1. Biểu đồ Use Case

![Image 10](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_010.png)

_Biểu đồ 5.1. Biểu đồ use case của phân hệ quản lý nguyên liệu và tồn kho (UC03)_

### 5.2. Đặc tả Use Case

#### 5.2.1. Xem tồn kho

| **Trường**           | **Nội dung**                                                                                                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Mã Use Case          | UC03.1                                                                                                                                                                         |
| Tên Use Case         | Xem tồn kho                                                                                                                                                                    |
| Tác nhân chính       | Nhân viên                                                                                                                                                                      |
| Tác nhân thứ cấp     | Hệ thống                                                                                                                                                                       |
| Điều kiện tiên quyết | - Nhân viên đã đăng nhập thành công <br> - Cửa hàng đã tồn tại trong hệ thống <br> - Nhân viên có quyền xem tồn kho                                                            |
| Điều kiện kết thúc   | Danh sách tồn kho được hiển thị                                                                                                                                                |
| Luồng chính          | - Nhân viên truy cập màn hình tồn kho <br> - Hệ thống nhận mã cửa hàng (store_id) <br> - Hệ thống truy vấn danh sách nguyên liệu và số lượng tồn kho <br> - Hiển thị danh sách |
| Luồng thay thế       |                                                                                                                                                                                |
| Luồng ngoại lệ       | -                                                                                                                                                                              |

#### 5.2.2. Nhập kho

#### 5.2.3. Xuất kho thủ công

#### 5.2.4. Xuất kho tự động

#### 5.2.5. Điều chỉnh tồn kho

#### 5.2.6. Xem lịch sử hoạt động

### 5.3. Biểu đồ hoạt động Use Case

![Image 11](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_011.png)

_Biểu đồ 5.2. Biểu đồ hoạt động xem tồn kho_

![Image 12](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_012.png)

_Biểu đồ 5.3. Biểu đồ hoạt động nhập kho_

![Image 13](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_013.png)

_Biểu đồ 5.4. Biểu đồ hoạt động xuất kho thủ công_

![Image 14](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_014.png)

_Biểu đồ 5.5. Biểu đồ hoạt động xuất kho tự động_

![Image 15](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_015.png)

_Biểu đồ 5.6. Biểu đồ hoạt động điều chỉnh tồn kho_

![Image 16](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_016.png)

_Biểu đồ 5.7. Biểu đồ hoạt động xem lịch sử hoạt động kho_
