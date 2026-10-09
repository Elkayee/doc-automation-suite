# Công việc triển khai

Cập nhật: 2026-10-09. Phạm vi trong [PLAN.md](PLAN.md). Đã triển khai nâng cấp và build ứng dụng
Windows cục bộ; chưa publish/merge. Giới hạn kiểm tra ghi riêng ở dưới.

## Windows EXE (yêu cầu tiếp theo)

Yêu cầu chữ đen đã hoàn thành: B01 DONE (hồi quy direct/theme/link/header/footer/footnote và bảo
toàn mẫu); B02 DONE (DOCX chỉ 000000, 1.422 glyph PDF đen trên 4 trang); B03 DONE (EXE/ZIP 0.2.1
riêng và hash toàn bộ file đạt).

| ID  | Công việc                            | Trạng thái    | Bằng chứng                                                                                                             |
| --- | ------------------------------------ | ------------- | ---------------------------------------------------------------------------------------------------------------------- |
| W01 | Phạm vi/định tuyến/đường dẫn runtime | DONE          | Control duyệt Hard; tests đường dẫn source/frozen/Unicode và ưu tiên renderer nội bộ                                   |
| W02 | Dashboard/editor/icon/DPI            | DONE          | Dashboard/form/editor, font/button/thanh xuất nhất quán; child conversion; native toolbar xuất với 374 heartbeat       |
| W03 | Build EXE kèm renderer và CLI/API    | DONE          | PyInstaller GUI/CLI EXE; cả hai renderer trong \_internal/tools; local API và Unicode CLI đã chạy thật                 |
| W04 | EXE smoke/Word/PDF/ZIP/manifest      | DONE          | 108 tests đạt; EXE mở/đóng từ cwd Unicode, PATH giới hạn; Word/PDF đóng gói 4 trang; ZIP/hash toàn bộ 20.849 file đạt  |
| W05 | Toàn bộ luồng bấm trên EXE cuối      | NOT_EVALUATED | Windows không cấp focus cho input automation; dừng sau hai lần; bằng chứng source GUI và frozen CLI/API được ghi riêng |

Windows review: [Standards/Spec và Control](docs/reviews/2026-10-09-windows-app.md). GUI SHA-256:
4f939f435727eac3e5a928f0e959ea6661b11d04bc56603110c80bcb68d26174. CLI SHA-256:
496c6effb4c030043dd3c7899c24514db6d22f8f650799dccbff748002689f85. Artifacts:
artifacts/windows-acceptance/frozen-startup.json, packaged-verification.json, native-authoring.json,
dashboard.png, native-authoring.png và packaged-academic.docx/pdf.

| ID  | Công việc                         | Trạng thái | Bằng chứng                                                                                                          |
| --- | --------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------- |
| T01 | Khảo sát/phạm vi/định tuyến       | DONE       | Nghiên cứu được duyệt; reassessment v2 bốn mức và Control review giữ Hard                                           |
| T02 | Chương bắt buộc/cache/cấu hình cũ | DONE       | Hồi quy từ 5 failed sang PASS; cache theo nội dung, TOC scaffold và template DOCX                                   |
| T03 | Lưu nguyên tử/phục hồi/xung đột   | DONE       | Lỗi ghi giữ bản cũ; draft/previous/history; external edit không bị ghi đè; GUI dùng safe save                       |
| T04 | Export chung và nháp/bản nộp      | DONE       | GUI/CLI/API/make cùng core; snapshot đầu vào; manifest/hash; nguồn và lock được bảo vệ                              |
| T05 | Mẫu và cấu trúc Word              | DONE       | BTL/công sở/biên bản; metadata, headings, sections, header/footer, TOC, caption/REF; giữ section ngang của template |
| T06 | PDF/citation/equation             | DONE       | LibreOffice/Pandoc thật; semantic text/image checks; TOC cập nhật; OMML; trích dẫn giữ năm thiếu                    |
| T07 | Batch/CSV/XLSX                    | DONE       | Mục lỗi không chặn mục hợp lệ; None/0 khác nhau; scope/output collision/cross-job source guards; MD riêng           |
| T08 | Giao diện                         | DONE       | Toolbar/form tiếng Việt; laptop layout; sửa nhảy chương; export nền; PDF stale theo nội dung/cấu trúc/settings      |
| T09 | Kiểm thử/rà soát                  | DONE       | 108 passed, 1 warning; Ruff/uv/formatter owned PASS; actual GUI/PDF/Word; recheck blockers closed                   |
| T10 | PLAN/TASK/AGENTS/README           | DONE       | Tài liệu gốc đồng bộ; AGENTS theo chính sách mới; hướng dẫn dùng và review artifact                                 |

## Kiểm chứng cuối

- Milestone report-authoring trước bản Windows: **103 passed, 1 warning**, 4.75 giây. Log:
  C:/Users/Home33/AppData/Local/Temp/doc-suite-upgrade-tests-r2grx55e/pytest-upgrade.txt.
- Ruff toàn repo: PASS. `uv lock --check --offline`: PASS.
- Prettier các file của nâng cấp: PASS. Full `npm run lint` còn báo các tài liệu có trước,
  package.json baseline và snapshot `_tmp` cũ; stdin từ commit baseline chứng minh package.json đã
  lỗi trước thay đổi. Không ghi CI PASS.
- npm audit sau patch nanoid: 0 vulnerabilities; Node DOCX smoke tạo buffer hợp lệ.
- LibreOffice 26.8.1.1/Pandoc 3.11 có hash vendor khớp; dùng thư mục tools của tài khoản hiện tại,
  không thay thế Office.
- Học thuật: workspaces/upgrade-demo-wk0em8ip/academic/build/academic.docx và academic.pdf, 4 trang;
  TOC/SEQ/REF, ảnh, citation và OMML đã kiểm tra.
- Công sở: workspaces/upgrade-demo-wk0em8ip/office/build/office.docx và office.pdf, 5 trang; header,
  bảng, Bảng 1, section ngang/dọc và số trang đã kiểm tra bằng mắt.
- Native GUI: metadata/table/save/export thật; 377 heartbeat callbacks trong lúc xuất. Ảnh chụp trực
  tiếp cửa sổ: workspaces/upgrade-demo-h9d1wa9a/gui-demo-9p0_yndg/native-ui-direct.png.
- Word 16.0 mở hai DOCX mẫu bằng OpenNoRepairDialog ở chế độ chỉ đọc, cùng 4 trang. Checker dừng sau
  hai lỗi helper cleanup; process của phép thử được đối chiếu event launch/creation và đóng đúng
  PID, không dùng kill toàn bộ Word.
- Review: [Standards/Spec và Control](docs/reviews/2026-10-09-report-authoring-upgrade.md).

## Giới hạn nghiệm thu

- Mẫu trường/đơn vị và citation style cụ thể chưa được cung cấp; mẫu là khung chung có thể chỉnh
  sửa, chưa chứng nhận tuân thủ quy định riêng.
- Kiểm tra PDF tự động chứng minh text/ảnh có mặt; vị trí, thứ tự ảnh, dàn trang và template mới vẫn
  cần xem trang thật. Không hứa pixel-identical Word/LibreOffice.
- FastAPI/Starlette TestClient có warning httpx không làm fail suite; API dành cho phạm vi cục bộ,
  chưa có cấu hình xác thực nhiều người dùng.
- Nhánh feat/report-authoring-upgrade có thay đổi cục bộ; đã build bản portable Windows, chưa
  push/remote CI, merge hoặc publish. Output nghiệm thu dùng dữ liệu mẫu.

## Kết quả bản Windows cuối

EXE: dist/DocAutomationSuite/DocAutomationSuite.exe. ZIP: dist/DocAutomationSuite-0.2.0-win64.zip
(632.781.780 byte).

ZIP SHA-256: 89284c41461643377456476ad3e93862b85f077c29215d6036c1941fd8b8082b. Toàn bộ 20.849 file
trong ZIP khớp danh sách/hash manifest, hai EXE khớp bản nghiệm thu, tool version không chứa đường
dẫn người dùng. Bằng chứng: artifacts/windows-acceptance/release-verification.json.

Suite mới nhất: 108 passed, 1 warning, 5,63 giây; log ở
C:/Users/Home33/AppData/Local/Temp/doc-suite-upgrade-tests-d_strq65/pytest-upgrade.txt. Ruff, uv
lock check và formatter file sở hữu đạt.

W05 vẫn NOT_EVALUATED; giới hạn này được giữ rõ trong Windows review. Bản portable là kết quả build
cục bộ, chưa publish/merge.

## Bản 0.2.1 — chữ đen khi xuất

EXE: dist/DocAutomationSuite-0.2.1/DocAutomationSuite.exe. ZIP:
dist/DocAutomationSuite-0.2.1-win64.zip.

GUI SHA-256: 2652b31c5a5ace3cb7458bfb2ec346f32bd0b47bde1c42564617169993064d39. CLI SHA-256:
b2902ae9a5b5467d560d73b2da574906d2a0b9b1701ff8829f860d197248a75e.

ZIP SHA-256: fdf8377eb93a0c99572109ba26daa68c6164fa948efe2edfb21f4637b2cd9b09; 20849 file khớp
manifest, 633035027 byte.

Bằng chứng: artifacts/windows-acceptance/black-text-verification.json, black-text-release.json và
black-text-report.docx/pdf. Review: docs/reviews/2026-10-09-black-text-export.md.

Hồi quy mới baseline-red rồi PASS. Suite trước bump version: 109 passed, 1 warning; sau bump: 108
passed, 1 native-display skipped, 1 warning (doc-suite-upgrade-tests-dgasv93z/pytest-upgrade.txt).
Ruff, lockfile và formatter file sở hữu đạt. Giới hạn frozen GUI input W05 giữ NOT_EVALUATED; màu
chữ đã kiểm chứng bằng CLI đóng gói thật.
