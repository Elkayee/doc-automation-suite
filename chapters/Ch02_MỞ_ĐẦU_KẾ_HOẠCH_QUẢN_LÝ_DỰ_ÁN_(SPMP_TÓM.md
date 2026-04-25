## MỞ ĐẦU: KẾ HOẠCH QUẢN LÝ DỰ ÁN (SPMP TÓM TẮT)

![1777105250246](image/Ch02*MỞ*ĐẦU*KẾ_HOẠCH_QUẢN_LÝ_DỰ*ÁN\_(SPMP_TÓM/1777105250246.png)

### Tóm tắt Bài toán và Nhu cầu Người dùng

Nhóm lựa chọn bài toán xây dựng **hệ thống quản lý quán café** để giải quyết các khó khăn phổ biến trong vận hành thực tế: dữ liệu bán hàng rời rạc, khó kiểm soát tồn kho, khó theo dõi lịch làm và chấm công của nhân viên, cũng như khó đối soát doanh thu và trách nhiệm vận hành giữa các ca làm việc.

Hệ thống được định hướng phục vụ bốn nhóm nhu cầu chính:

- Quản lý bán hàng, bàn phục vụ và thanh toán.
- Quản lý thực đơn, topping và công thức pha chế.
- Quản lý kho và nguyên liệu.
- Quản lý nhân sự, tài khoản, phân quyền, phân ca và chấm công.

### Tóm tắt Ràng buộc Nghiệp vụ

| **Mã**    | **Ràng buộc chính**                                                     |
| --------- | ----------------------------------------------------------------------- |
| BR-GEN-01 | Mỗi đơn hàng phải gắn với một bàn hoặc hình thức phục vụ hợp lệ.        |
| BR-GEN-02 | Chỉ người có quyền phù hợp mới được thay đổi dữ liệu quan trọng.        |
| BR-GEN-03 | Tồn kho phải được cập nhật theo công thức khi đơn hàng hoàn tất.        |
| BR-GEN-04 | Một nhân viên không được nhận hai ca chồng chéo trong cùng ngày.        |
| BR-GEN-05 | Dữ liệu chấm công phải ghi nhận đúng thời điểm và không được trùng lặp. |

### Phân Bổ Nhiệm Vụ Nhóm

Nhóm thực hiện phân chia trách nhiệm theo nguyên tắc **phân công theo phân hệ (module-based assignment)**. Mỗi thành viên phụ trách một nhóm Use Case đủ lớn, có nghiệp vụ và ràng buộc riêng:

| **Thành viên**       | **Phân hệ phụ trách**                                                   | **Các bảng CSDL liên quan**                                                           | **Use Case** |
| -------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | :----------: |
| **Thành**            | Bán hàng, Đơn hàng, Thanh toán & Hóa đơn, Quản lý bàn                   | `hoa_don`, `hoa_don_chi_tiet`, `ban`, `khu_vuc`, `order_item_topping`                 |  UC02, UC03  |
| **Bảo**              | Quản lý menu (sản phẩm) và công thức pha chế                            | `do_uong`, `nhom_do_uong`, `topping`, `cong_thuc`, `nguyen_lieu`                      |     UC01     |
| **Nguyễn Quang Đạo** | Quản lý nguyên liệu và tồn kho                                          | `nguyen_lieu`, `nhap_kho`, `cong_thuc`, `canh_bao_kho`                                |     UC05     |
| **Nguyễn Viết Tùng** | Usecase quản lý ca làm việc, chấm công, tài khoản và phân quyền nhân sự | `nhan_vien`, `tai_khoan`, `shift_template`, `shift`, `shift_assignment`, `attendance` | UC04 + UC07  |
| **Hồng Nhung**       | Báo cáo doanh thu / chi phí và quản lý danh sách cửa hàng               | `bao_cao_doanh_thu`, `chi_phi`, `danh_sach_cua_hang`, `hoa_don`                       |     UC06     |

---
