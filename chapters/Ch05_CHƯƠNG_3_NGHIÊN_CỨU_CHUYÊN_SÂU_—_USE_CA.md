## CHƯƠNG 3: NGHIÊN CỨU CHUYÊN SÂU — USE CASE BÁN HÀNG (UC01)

### 3.1. Biểu đồ UC chi tiết

![Image 8](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_008.png)

### 3.2. Đặc tả UC

#### 3.2.1. Thông tin chung

#### 3.2.2. Tiền điều kiện

Hệ thống hoạt động bình thường

Nhân viên đã đăng nhập

Menu chức năng tạo đơn hàng đã được cấu hình

Tồn kho đã được cập nhật

#### 3.2.3. Hậu điều kiện

**Thành công:**

Đơn hàng được hoàn tất

Thanh toán thành công

Tồn kho bị khấu trừ

Doanh thu và chi phí được ghi nhận

**Thất bại:**

Đơn hàng bị hủy

Không thay đổi tồn kho

Không ghi nhận doanh thu và chi phí

#### 3.2.4. Luồng chính

Thu ngân (Cashier) hoặc bồi bàn (Waitor) tạo đơn hàng

Người lên đơn chọn loại đơn: đặt tại chỗ (dine-in) hoặc mang về (takeaway) hoặc delivery (giao hàng)

Nếu đặt giao hàng => lên đơn vận chuyển giao cho khách hàng, nếu đặt tại chỗ => chọn bàn

Người lên đơn thêm sản phẩm theo yêu cầu khách hàng

Người lên đơn chọn size / variant theo yêu cầu khách hàng

Người lên đơn thêm topping (nếu có) theo yêu cầu khách hàng

Lặp lại bước 4–6 cho đến khi hoàn tất

Người lên đơn chọn thanh toán (checkout)

Hệ thống tính toán nguyên liệu cần dùng

Hệ thống kiểm tra tồn kho

Nếu đủ tồn kho => tiếp tục

Hệ thống trừ tồn kho (deduct inventory)

Khách hàng thực hiện thanh toán, người lên đơn thực hiện kiểm tra

Nếu thanh toán thành công => tiếp tục

Hệ thống ghi nhận doanh thu và chi phí

Nhân viên thực hiện pha chế => chuyển trạng thái đơn hàng thành Đang xử lý

Nhân viên giao đồ uống cho khách (tại bàn/ giao hàng) => chuyển trạng thái đơn hàng thành Hoàn tất

#### 3.2.5. Luồng thay thế

**A1 - Hết hàng**

Tại bước 10

Nếu tồn kho không đủ:

Hệ thống thông báo "Không đủ nguyên liệu"

Kết thúc use case

**A2 - Thanh toán thất bại**

Tại bước 14

Nếu thanh toán thất bại:

Hệ thống hủy đơn hàng

Không trừ kho (hoặc rollback)

Kết thúc use case

**A3 - Khách không ngồi bàn**

Tại bước 2

Bỏ qua bước chọn bàn

**A4 - Khách chọn giao hàng**

Tại bước 2

Lên đơn vận chuyển giao cho khách

**A5 - Khách chọn giao hàng**

Tại bước 2

Khách yêu cầu đăng ký thành viên để tích điểm, đổi điểm => tạo thông tin khách hàng và gán vào đơn hàng

#### 3.2.6. Quy tắc nghiệp vụ

BR1: Không cho phép bán khi tồn kho không đủ

BR2: Kiểm tra tồn kho phải thực hiện trong 1 giao dịch

BR3: Doanh thu và chi phí chỉ ghi nhận khi thanh toán thành công

BR4: Đặt đồ uống tại chỗ phải gắn với bàn

BR5: Giá sản phẩm được snapshot tại thời điểm order

#### 3.2.7. Yêu cầu phi chức năng

Thời gian phản hồi của các thao tác < 2s

Hỗ trợ xử lý nhiều đơn hàng cùng lúc

### 3.3. Biểu đồ luồng hoạt động

![Image 9](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_009.png)
