## MỞ ĐẦU: KẾ HOẠCH QUẢN LÝ DỰ ÁN PHẦN MỀM (SPMP)

### 0.1. Mô tả Bài toán và Nhu cầu Người dùng

Nhóm lựa chọn bài toán xây dựng **hệ thống quản lý chuỗi quán café** nhằm hỗ trợ vận hành đồng bộ giữa quầy thu ngân, khu vực pha chế, kho nguyên liệu, bộ phận quản lý và nhân viên theo ca. Trong thực tế, nhiều cửa hàng quy mô vừa và nhỏ vẫn quản lý bằng sổ tay, file Excel rời rạc hoặc trao đổi qua tin nhắn. Cách làm này dẫn đến dữ liệu phân tán, dễ sai lệch, khó đối soát doanh thu, khó kiểm tra tồn kho và đặc biệt khó quản lý lịch làm việc cũng như chấm công của nhân viên.

Từ góc nhìn của người quản lý, vấn đề lớn nhất không chỉ là bán được hàng mà là **kiểm soát toàn bộ quy trình vận hành**. Khi quán đông khách, quản lý cần biết bàn nào đang phục vụ, đơn nào đang chờ pha chế, ca làm nào đang thiếu người, nguyên liệu nào sắp hết và doanh thu trong ngày biến động ra sao. Nếu không có hệ thống tập trung, việc ra quyết định thường chậm, phụ thuộc vào kinh nghiệm cá nhân và dễ phát sinh tranh cãi khi đối chiếu số liệu cuối ngày.

Từ góc nhìn của nhân viên, nhu cầu cốt lõi là thao tác nhanh, dễ hiểu và phù hợp với công việc thực tế tại quầy. Thu ngân cần tạo đơn hàng, chuyển bàn, áp dụng topping, in hóa đơn và xử lý thanh toán mà không bị rối giao diện. Nhân viên pha chế hoặc phục vụ cần nhận biết đơn mới ngay khi phát sinh, tránh bỏ sót hoặc làm nhầm món. Nhân viên theo ca cần có công cụ để xem lịch làm, vào ca, kết thúc ca và biết giờ công của mình được ghi nhận minh bạch.

Từ góc nhìn của chủ cửa hàng hoặc quản lý chi nhánh, hệ thống còn phải giải quyết bài toán **minh bạch dữ liệu và trách nhiệm vận hành**. Mỗi thông tin quan trọng như doanh thu, chi phí, tồn kho, tài khoản nhân viên, bảng chấm công và phân quyền truy cập đều phải được lưu tập trung, có khả năng kiểm tra lại khi cần. Điều này đặc biệt quan trọng trong môi trường có nhiều nhân viên làm theo ca, đổi ca thường xuyên và có sự phân tách trách nhiệm giữa quản lý, thu ngân và nhân viên phục vụ.

Do đó, bài toán người dùng đặt ra cho hệ thống gồm bốn nhóm nhu cầu chính:

- Quản lý bán hàng tại quán: tạo đơn, cập nhật trạng thái bàn, thanh toán và in hóa đơn.
- Quản lý thực đơn và công thức pha chế: cập nhật món, topping, định lượng nguyên liệu.
- Quản lý kho và nguyên liệu: nhập kho, theo dõi tiêu hao, cảnh báo thiếu hụt.
- Quản lý nhân sự theo ca: hồ sơ nhân viên, tài khoản đăng nhập, phân quyền, phân ca, chấm công và tổng hợp lương theo ca.

Mục tiêu của hệ thống không phải thay đổi mô hình kinh doanh của quán café, mà là **số hóa quy trình vận hành hiện có** để giảm thao tác thủ công, tăng độ chính xác dữ liệu và hỗ trợ quản lý ra quyết định nhanh hơn.

### 0.2. Phạm vi Nghiệp vụ và Ràng buộc Chung

Phần mô tả yêu cầu của khách hàng cho thấy hệ thống phải đáp ứng đồng thời nhu cầu tác nghiệp hằng ngày và nhu cầu kiểm soát quản trị. Các ràng buộc nghiệp vụ chính được tổng hợp như sau:

| **Mã ràng buộc** | **Nội dung** |
| --- | --- |
| BR-GEN-01 | Mỗi đơn hàng phải gắn với một bàn hoặc một hình thức phục vụ hợp lệ tại thời điểm tạo đơn. |
| BR-GEN-02 | Chỉ người có quyền phù hợp mới được thay đổi thực đơn, giá bán, tài khoản hoặc dữ liệu nhân sự. |
| BR-GEN-03 | Tồn kho phải được cập nhật theo công thức pha chế khi đơn hàng được xác nhận hoàn thành. |
| BR-GEN-04 | Một nhân viên không được nhận hai ca chồng chéo thời gian trong cùng ngày. |
| BR-GEN-05 | Dữ liệu chấm công phải phản ánh đúng thời điểm vào ca và kết thúc ca; không được ghi nhận trùng. |
| BR-GEN-06 | Doanh thu, chi phí và dữ liệu công lao động phải lưu vết để có thể đối soát khi cần. |
| BR-GEN-07 | Hệ thống phải hoạt động ổn định trong môi trường quán đông khách, ưu tiên thao tác nhanh và ít bước. |

Ngoài các ràng buộc nghiệp vụ, dự án còn chịu ràng buộc thực tế của môn học: nhóm cần lựa chọn các Use Case đủ lớn, có nghiệp vụ và có thể đặc tả rõ luồng chính, luồng ngoại lệ, biểu đồ hoạt động và mô hình dữ liệu liên quan. Vì vậy, nhóm không chọn các ca sử dụng quá nhỏ như đăng nhập đơn lẻ hoặc các chức năng CRUD đơn giản làm trọng tâm nghiên cứu.

### 0.3. Phạm vi Giải pháp Phần mềm

Để đáp ứng các nhu cầu trên, nhóm định hướng hệ thống thành ba bề mặt sử dụng chính:

| **Nền tảng** | **Đối tượng** | **Mục đích sử dụng** |
| --- | --- | --- |
| Ứng dụng bảng điều khiển trên web | Quản lý | Theo dõi vận hành, cấu hình dữ liệu, xem báo cáo, quản lý nhân sự |
| Phần mềm POS máy tính bảng | Thu ngân | Tạo đơn, cập nhật bàn, thanh toán, in hóa đơn |
| Ứng dụng di động nhân viên | Nhân viên | Xem lịch làm, chấm công, nhận thông báo liên quan đến ca làm |

Phần công nghệ triển khai được lựa chọn nhằm phục vụ bài toán nghiệp vụ, không phải mục tiêu chính của báo cáo. Vì vậy, trong phần chung này nhóm chỉ giữ mức mô tả vừa đủ để giải thích cách hệ thống được sử dụng, còn chi tiết hiện thực và kiểm thử sẽ được trình bày ở các chương sau.

### 0.4. Phân Bổ Nhiệm Vụ Nhóm

Nhằm đảm bảo tiến độ và chất lượng, nhóm thực hiện phân chia trách nhiệm theo nguyên tắc **phân công theo phân hệ**; mỗi thành viên chịu trách nhiệm toàn diện từ đặc tả đến thiết kế, cài đặt và kiểm thử cho một phân hệ ca sử dụng tương ứng:

| **Thành viên** | **Phân hệ phụ trách** | **Các bảng CSDL liên quan** | **Ca sử dụng** |
| --- | --- | --- | --- |
| Thành | Bán hàng, Quản lý khách hàng, Quản lý bàn phục vụ | hoa_don, hoa_don_chi_tiet, ban, khu_vuc, order_item_topping | UC1 |
| Tạ Bảo Anh Ngọc | Quản lý menu (sản phẩm) và công thức pha chế | do_uong, nhom_do_uong, topping, cong_thuc, nguyen_lieu | UC2 |
| Nguyễn Quang Đạo | Quản lý nguyên liệu và tồn kho | Cửa hàng, tồn kho, đơn hàng, sản phẩm, công thức, nguyên liệu, chi tiết công thức, giao dịch kho, chi tiết giao dịch kho | UC3 |
| Nguyễn Viết Tùng | Usecase quản lý ca làm việc, chấm công, tài khoản và phân quyền nhân sự | nhan_vien, tai_khoan, shift_template, shift, shift_assignment, attendance | UC04 + UC07 |
| Ngô Thị Hồng Nhung | Báo cáo doanh thu / chi phí và quản lý danh sách cửa hàng | bao_cao_doanh_thu, chi_phi, danh_sach_cua_hang, hoa_don | UC5 + UC6 |

***Lưu ý****: Mỗi phân hệ UC liên quan đến một nhóm thực thể nghiệp vụ đủ lớn, có nhiều ràng buộc và luồng ngoại lệ. Việc phân công theo phân hệ giúp nhóm tránh chồng chéo nội dung, đồng thời bảo đảm mỗi thành viên đều có đủ phạm vi để xây dựng biểu đồ UC chi tiết, đặc tả UC và biểu đồ hoạt động.*

**Sơ đồ tổng quan phân công:**

![Image 5](extracted_media/Bao_Cao_Tieu_Luan_NMCNPM/image_005.png)

*Biểu đồ 2. Sơ đồ tổng quan phân công nhóm*
