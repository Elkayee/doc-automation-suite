# Doc Automation Suite cho Windows

Giải nén toàn bộ ZIP, mở thư mục DocAutomationSuite và chạy **DocAutomationSuite.exe**. Giữ EXE cùng
thư mục \_internal; không cần cài Python, LibreOffice hoặc Pandoc.

Chọn **Bài tập lớn**, **Báo cáo công sở** hoặc **Biên bản**, nhập tên dự án rồi tạo. Trong trình
soạn, mở **Thông tin báo cáo** để nhập thông tin bìa. Chọn chương bên trái, soạn nội dung ở giữa và
xem trước bên phải. Menu **Chèn** có bảng, hình, tham chiếu, trích dẫn và công thức. Ctrl+S lưu nội
dung; Ctrl+B/I định dạng.

**Kiểm tra** hiển thị nội dung còn thiếu. **Bản nộp** yêu cầu hoàn thiện thông tin và chương bắt
buộc. **Xuất Word + PDF** tạo hai file trong thư mục dự án; **Xem PDF đã xuất** mở bản dàn trang
thật. Xem trước trong trình soạn là bố cục ước lượng.

Dự án mới ở `%LOCALAPPDATA%\DocAutomationSuite\workspaces`. **Thư mục tài liệu** mở nơi lưu. **Mở dự
án** nhận dự án có config.yaml và chapters. Có thể sao lưu cả thư mục dự án hoặc chuyển nó sang máy
khác. Thay bản ứng dụng không xóa dự án. Nhật ký lỗi ở
`%LOCALAPPDATA%\DocAutomationSuite\logs\application.log`.

## Tự động hóa

Mở PowerShell trong thư mục ứng dụng:

```powershell
.\DocAutomationCLI.exe --help
.\DocAutomationCLI.exe doctor
.\DocAutomationCLI.exe list-templates
.\DocAutomationCLI.exe compile "C:\BaoCao\du-an" --format docx --format pdf --json
.\DocAutomationCLI.exe batch "C:\BaoCao\jobs.yaml" --result-out "C:\BaoCao\results.json"
.\DocAutomationCLI.exe serve --port 8000
```

API chạy cục bộ tại http://127.0.0.1:8000/docs. Đóng cửa sổ console hoặc Ctrl+C để dừng.
`DOC_SUITE_DATA_DIR` cho phép chỉ định thư mục dữ liệu khác. Gói bao gồm bộ renderer riêng, không
thay cài đặt Microsoft Office hiện có.

Mẫu là khung chung có thể chỉnh sửa. Cần đối chiếu mẫu riêng của trường/cơ quan trước khi nộp. Bản
portable hiện tại chưa ký số và chưa có trình tự cập nhật. Giấy phép thành phần Python ở
THIRD_PARTY; giấy phép LibreOffice/Pandoc ở thư mục \_internal/tools. release-manifest.json ghi
phiên bản và hash các file.
