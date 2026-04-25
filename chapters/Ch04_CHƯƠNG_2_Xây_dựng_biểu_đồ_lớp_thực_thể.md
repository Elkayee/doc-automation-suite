## CHƯƠNG 2: Xây dựng Biểu đồ lớp thực thể

Biểu đồ Lớp là công cụ mô hình hóa cấu trúc tĩnh (static structure) của hệ thống, thể hiện các lớp đối tượng, thuộc tính, phương thức và mối quan hệ giữa chúng. Các lớp cốt lõi của hệ thống được thiết kế theo nguyên tắc **Separation of Concerns** (Phân tách mối quan tâm):

### 2.1. Phân tích

### 2.2. Đặc tả

| **Tên thực thể** |  | **Mô tả** |
| --- | --- | --- |
| Store |  |  |
| Order |  |  |
| OrderItem |  |  |
| CafeTable |  |  |
| TableSession |  |  |
| Revenue |  |  |
| CostOfGoodSold |  |  |
| Product |  |  |
| Category |  |  |
| ProductVariant |  |  |
| Topping |  |  |
| Ingredient |  |  |
| Recipe |  |  |
| Inventory |  |  |
| InventoryTransaction |  |  |
| Employee |  |  |
| Shift |  |  |
| ShiftTemplate |  |  |
| Attendance |  |  |

**Các mối quan hệ đáng chú ý:**

HoaDon — Ban: Quan hệ **Liên kết (Association)** 1–1 tại một thời điểm (một bàn có tối đa một hóa đơn đang mở).

HoaDon — HoaDonChiTiet — DoUong: Quan hệ **Tổng hợp (Aggregation)** và **Liên kết N-N** được giải quyết qua bảng trung gian.

DoUong — CongThuc — NguyenLieu: Quan hệ **Phụ thuộc (Dependency)** thể hiện công thức pha chế.

TaiKhoan — NhanVien: Quan hệ **Kết hợp (Composition)** — một tài khoản gắn với đúng một nhân viên.

### 2.3. Vẽ Biểu đồ

![Image 7](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_007.png)
