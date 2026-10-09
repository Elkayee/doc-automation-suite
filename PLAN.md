# Kế hoạch nâng cấp phần mềm văn bản và báo cáo

Cập nhật: 2026-10-09. Người dùng đã yêu cầu triển khai toàn bộ hướng nghiên cứu và cập nhật PLAN.md,
TASK.md, AGENTS.md theo tiến độ.

## Bìa tiểu luận PTIT

Hoàn thành cục bộ: hai lựa chọn tiểu luận PTIT bài tập nhóm/cá nhân dùng bố cục Cover_Ptit.docx đã
cung cấp. Giữ logo, lề và thụt dòng gốc; điền metadata trong Word; không in hướng dẫn nội bộ hoặc
tạo bìa trùng. Bìa nguồn và dự án cũ giữ nguyên. Control duyệt Hard theo chính sách bốn mức; triển
khai/rà soát trực tiếp, không Dely Run.

114 tests đạt trong bản sao riêng; Ruff, lockfile và formatter đạt. Đã xem source GUI và Word/PDF 3
trang, chữ đen, TOC cập nhật. EXE 0.2.2 mở từ cwd khác; frozen CLI tạo/xuất cả hai mẫu và API xuất
cá nhân đạt. ZIP có 20.854 mục (20.853 file kê trong manifest và manifest), tất cả khớp hash. Frozen
GUI input đầy đủ vẫn NOT_EVALUATED.

Phạm vi: [PTIT covers](docs/superpowers/specs/2026-10-09-ptit-covers.md). Review:
[PTIT covers](docs/reviews/2026-10-09-ptit-covers.md).

## Màu chữ khi xuất

Yêu cầu: báo cáo xuất Word/PDF chỉ dùng chữ đen. Áp dụng ở bước lưu DOCX chung, bao gồm màu trực
tiếp/theme trong mẫu, style, bảng, hyperlink, header/footer và field. Kiểm tra hồi quy mẫu nhiều màu
và bảo toàn nguồn đạt; 1.422 glyph PDF trên 4 trang đều đen, DOCX chỉ 000000. Bản 0.2.1 đã build
riêng vì 0.2.0 đang mở; ZIP/hash toàn bộ file đạt. Trạng thái: hoàn thành. Review:
docs/reviews/2026-10-09-black-text-export.md.

## Bản ứng dụng Windows

Yêu cầu mới: EXE hoàn chỉnh và giao diện chỉn chu. Phạm vi ở
[Windows app](docs/superpowers/specs/2026-10-09-windows-app.md), Control đánh giá Hard.

1. Tách tài nguyên đóng gói khỏi dữ liệu có thể ghi; kiểm tra đường dẫn frozen và source.
2. Làm dashboard/editor nhất quán, rõ thao tác soạn và xuất; kiểm tra cửa sổ thật.
3. Đóng gói EXE GUI/CLI, mẫu và renderer; kiểm tra từ thư mục làm việc khác.
4. Nghiệm thu Word/PDF từ bản đóng gói, tạo ZIP/manifest và cập nhật tài liệu.

Trạng thái: đã build EXE GUI/CLI và nghiệm thu cục bộ các phần có thể chạy: 108 tests, mở/đóng EXE,
CLI/API đóng gói và báo cáo học thuật Word/PDF 4 trang. Giao diện source đã kiểm tra form/lưu/xuất
bằng renderer trong gói. ZIP/hash đã kiểm tra: 20.849 file khớp manifest và EXE khớp bản nghiệm thu.
Toàn bộ luồng bấm tạo/soạn/xuất trên EXE cuối vẫn NOT_EVALUATED do giới hạn focus của Windows; không
gộp bằng chứng source GUI thành kiểm tra EXE.

Review và giới hạn: [Windows review](docs/reviews/2026-10-09-windows-app.md).

Mục tiêu: báo cáo bài tập lớn và công sở; nâng cấp chất lượng Word/PDF, thao tác soạn và tự động hóa
CLI/API/batch. Giữ Python/Tkinter và dự án Markdown/YAML hiện có; mẫu mới là mẫu chung có thể chỉnh
sửa.

Thiết kế: [nghiên cứu](docs/research/2026-10-09-document-authoring-upgrade.md) và
[phạm vi đã phê duyệt](docs/superpowers/specs/2026-10-09-report-authoring-upgrade.md). Trạng
thái/bằng chứng chi tiết nằm trong [TASK.md](TASK.md).

## Trình tự và nghiệm thu

1. **Bảo toàn nội dung:** chương bắt buộc, ảnh, cache, cấu hình cũ, lưu nguyên tử và bản phục hồi.
   Kiểm tra: hồi quy đúng lỗi; lỗi ghi/xung đột giữ bản trước.
2. **Đường xuất chung:** GUI, CLI, API và make.py dùng cùng core; phân biệt nháp và bản nộp. Kiểm
   tra: cùng đầu vào có cấu trúc và lỗi/cảnh báo nhất quán.
3. **Báo cáo hoàn chỉnh:** mẫu, metadata, heading, section, mục lục, số trang, caption và tham
   chiếu. Kiểm tra: OOXML và tài liệu được renderer cập nhật.
4. **PDF/học thuật:** LibreOffice cập nhật field/dàn trang; Pandoc cho citation và công thức Word.
   Kiểm tra: PDF thật có chữ/ảnh/mục lục; DOCX có OMML.
5. **Hàng loạt:** manifest, CSV/XLSX metadata và kết quả từng tài liệu. Kiểm tra: mục lỗi không làm
   mất mục hợp lệ; dữ liệu thiếu giữ nguyên.
6. **Giao diện:** nhóm thao tác tiếng Việt, form metadata/bảng/tham chiếu, xuất nền và phục hồi.
   Kiểm tra: ứng dụng thật ở kích thước màn hình laptop.
7. **Nghiệm thu tích hợp:** bộ test, lint, CLI/API, tài liệu mẫu và rà soát độc lập; ghi rõ các giới
   hạn còn lại trước khi báo hoàn thành.

## Quyết định hiện tại

Triển khai và nghiệm thu cục bộ các bước 1–7 đã hoàn thành; suite sau bản Windows có 108 test đạt,
Ruff và lockfile check đạt; formatter các file của nâng cấp đạt. Mẫu học thuật DOCX/PDF 4 trang và
mẫu công sở 5 trang đã kiểm tra cấu trúc, nội dung, ảnh và bố cục. Giao diện thật có form, lưu/phục
hồi, chọn chương ổn định và xuất nền.

Lỗi kết nối UNO của lần xuất sau đã xử lý bằng chờ renderer sẵn sàng trước helper; GUI đã xuất lại
đạt. Hai reviewer Codex đã rà Standards/Spec và Control xử lý các phát hiện, ghi tại
docs/reviews/2026-10-09-report-authoring-upgrade.md. Full npm run lint vẫn có lỗi định dạng baseline
ở tài liệu cũ; xem TASK.md.

- Task-routing đã được Control duyệt Hard: Codex trực tiếp; không mở Dely Run.
- Quy tắc AGENTS thay thế đã nhận; đánh giá được chạy lại bằng chính sách bốn mức
  jev-task-routing-v2 của script đang cài.
- Nhánh làm việc: feat/report-authoring-upgrade; chưa yêu cầu push/merge.
- Tài liệu nghiên cứu là đầu vào được bảo toàn; báo cáo trong workspaces không được dùng cho các
  phép thử mất dữ liệu.
- Renderer được chuẩn bị ở thư mục tools của tài khoản hiện tại, kiểm tra hash gói vendor trước khi
  trích xuất; không thay thế cài đặt Office của người dùng.
- Chưa cam kết mẫu đáp ứng quy định riêng của trường/cơ quan khi chưa có mẫu nguồn.
