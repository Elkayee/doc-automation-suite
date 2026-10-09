# Review nâng cấp báo cáo

Baseline: 798dc745aa357e05003645097022d831b829eafa. Candidate là worktree
feat/report-authoring-upgrade; không có push/merge. Hai reviewer Codex đọc mã độc lập; Codex Control
quyết định và sửa các phát hiện.

## Standards

- Phạm vi batch: đã chặn workspace/output/cache ra ngoài base, các output trùng, ghi vào đầu vào của
  mục khác; thêm kiểm tra hồi quy.
- Legacy: workspace có config dùng export core; Markdown rời giữ nháp tương thích. Ngoại lệ đã ghi
  rõ trong AGENTS/README.
- Khóa xuất: output/cache không được trỏ vào build/.export.lock; đã có hồi quy.
- Fixture ảnh: kiểm tra lại chứng minh test dùng file test_extracted.png ở gốc repository, được Git
  theo dõi; phản ánh thiếu tests/test_extracted.png là nhầm đường dẫn, không phải lỗi candidate.
- Smell monolith/nhánh math: là nhận xét thiết kế; giữ phạm vi sửa chức năng, không mở refactor toàn
  bộ giao diện đang có.

## Spec

- PDF: so sánh text với DOCX đã compose, kiểm tra ảnh bắt buộc và TOC đã cập nhật; PDF chỉ có tiêu
  đề hoặc mất ảnh bị từ chối trong kiểm tra hồi quy.
- Batch: cache_dir là control column; DOCX/PDF/MD/manifest được kiểm tra xung đột; các dòng khác
  metadata có MD độc lập.
- PDF cũ: đổi cây chương, cấu hình và file ngoài editor cập nhật revision/stale.
- Legacy: ngoại lệ nháp không có config đã được ghi rõ; main GUI/CLI/API/make và legacy có config
  cùng dùng core.
- README: code fence text giữ các marker/bảng trên từng dòng, tránh formatter ghép thành cú pháp
  không chạy được.

Recheck Spec không còn blocker cụ thể. Các lỗi Standards về phạm vi/khóa/cú pháp và đồng bộ trạng
thái đã được xử lý; Codex Control kiểm tra phần còn lại và bộ nghiệm thu. Giới hạn tự động: text/ảnh
có mặt không chứng minh mọi vị trí, thứ tự hình hoặc toàn bộ bố cục pixel; mẫu thật còn được xem
bằng mắt.

## Bằng chứng

- Candidate cuối: 103 passed, 1 warning; log và giới hạn ghi trong TASK.md.
- Ruff, uv lock check, formatter các file sở hữu, Node DOCX smoke và npm audit.
- Mẫu học thuật DOCX/PDF 4 trang; mẫu công sở 5 trang có section ngang/dọc, header, TOC và tham
  chiếu Bảng 1.
- Giao diện thật: metadata/bảng/lưu, export nền, 377 heartbeat callbacks, chọn chương không bị
  preview đổi ngược và pane điều hướng ở kích thước laptop.
- Word 16.0 mở hai mẫu ở chế độ chỉ đọc. Hai process automation của phép thử được nhận diện từ
  event/script creation và dọn đúng PID sau khi đóng tài liệu.

Full npm run lint vẫn báo định dạng các tài liệu có trước và dữ liệu thử cũ; baseline package.json
đã được kiểm tra có cùng lỗi. Không coi đây là CI PASS.
