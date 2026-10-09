# Nghiên cứu nâng cấp Doc Automation Suite cho văn bản và báo cáo

Ngày khảo sát: 2026-10-09. Mã nguồn đối chiếu: commit `798dc745aa357e05003645097022d831b829eafa`.

Mục tiêu đã xác nhận: chuyên soạn văn bản, báo cáo bài tập lớn và báo cáo công sở; nâng cấp đồng
thời chất lượng Word/PDF, giao diện soạn và tự động hóa hàng loạt qua CLI/API.

Khuyến nghị: giữ lõi Python, Markdown và DOCX hiện có; sửa các lỗi ảnh hưởng nội dung trước, dùng
một luồng xuất chung, rồi hoàn thiện mẫu báo cáo và thao tác soạn. PDF phải được tạo từ DOCX đã dàn
trang và cập nhật mục lục. Khả năng xuất PDF và chất lượng dàn trang vẫn cần thử nghiệm trên mẫu
thật.

Đây là kết quả nghiên cứu, chưa phải bản nâng cấp đã triển khai. Trong phiên này chỉ tạo tài liệu
nghiên cứu trong repository; kiểm thử và tình huống tái hiện chạy ở bản sao tạm.

## 1. Nền tảng hiện tại

| Thành phần       | Đã có trong mã                                                                    | Khoảng trống liên quan mục tiêu                                                       |
| ---------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Dự án và mẫu     | Dashboard; tạo dự án từ YAML, boilerplate, assets và DOCX nếu có                  | Chỉ thấy hai mẫu tích hợp: bài kiểm tra và tiểu luận; mẫu tiểu luận thiếu DOCX mẫu    |
| Soạn nội dung    | Editor Markdown, cây chương/mục con, tìm kiếm, đổi tên, sắp xếp, undo và tự lưu   | Chương mới mặc định theo dàn ý nghiên cứu tiếng Anh; chưa phù hợp mọi báo cáo công sở |
| Định dạng        | Thiết lập đoạn văn, khổ giấy, lề, heading và dấu đầu dòng                         | Heading còn định dạng cứng; page setup hiện áp dụng section đầu tiên                  |
| Bảng và hình     | Bảng Markdown, hàng tiêu đề lặp, hình nội bộ, căn chỉnh/kích thước và caption chữ | Chưa thấy đánh số caption và tham chiếu chéo tự động trong pipeline chính             |
| Mục lục          | Nút Add TOC và helper tạo field Word khi gặp `[[TOC]]`                            | Field chứa lời nhắc Update Field; mẫu báo cáo mới chưa tự chèn marker này             |
| Xem trước        | HTML có chia trang và đồng bộ vị trí editor; fallback text                        | Chia trang theo ước lượng chiều cao khối, không dùng bộ dàn trang Word                |
| Xuất và tích hợp | GUI Build DOCX; CLI create/list-templates/compile; API create/compile; make.py    | Lặp phần điều phối; chưa thấy xuất PDF hoặc batch trong pipeline chính                |

Nguồn mã: [Dashboard](../../src/ui/dashboard.py),
[Visual Builder](../../src/ui/visual_builder/window.py), [Assembler](../../src/core/assembler.py),
[DOCX Builder](../../src/core/docx_builder.py), [DOCX Helpers](../../src/core/docx_helpers.py),
[CLI](../../src/cli.py), [API](../../src/api.py), [make.py](../../make.py).

Có công cụ [DOCX sang Markdown](../../convert_docx_to_md.py) và giao diện
[legacy](../../src/ui/legacy_workflow.py). Chuyển tài liệu Word có sẵn thành Markdown là một đường
nhập nội dung; chưa có bằng chứng bảo toàn đầy đủ bố cục, section, field hay bảng phức tạp khi
chuyển qua lại.

## 2. Những gì đã kiểm chứng

| Kiểm tra                     | Kết quả                                                           | Giới hạn                                                          |
| ---------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| Bộ pytest hiện có            | **71 passed, 1 warning**, 4.62 giây                               | Không chứng minh chất lượng Word/PDF hoặc mọi thao tác GUI        |
| Ruff cho src/tests           | All checks passed                                                 | Cấu hình đang loại trừ API, CLI, config, logger và một file test  |
| Xuất qua CLI thực sự         | Exit code 0, tạo DOCX                                             | Dùng mẫu tiểu luận mặc định, không công thức hoặc sơ đồ           |
| Xuất qua FastAPI TestClient  | HTTP 200, success=true, tạo DOCX                                  | API nội bộ trên bản sao tạm; chưa kiểm tra dịch vụ mạng đang chạy |
| So sánh CLI/API cùng đầu vào | `word/document.xml` có cùng SHA-256                               | Chỉ một trường hợp; không so byte toàn bộ ZIP DOCX                |
| Runtime cục bộ               | Python 3.14.0; python-docx 1.2.0; TkinterWeb 4.25.2               | CI hiện cấu hình Ubuntu/Python 3.10                               |
| Công cụ PDF                  | Có WINWORD.EXE tại đường dẫn Office16 phổ biến                    | Chưa kiểm tra Word COM, license, cập nhật field hoặc xuất PDF     |
| LibreOffice/Pandoc           | Không tìm thấy trong PATH và các thư mục cài phổ biến đã kiểm tra | Không phải kiểm kê toàn bộ ổ đĩa                                  |

Warning quan sát được từ FastAPI/Starlette TestClient liên quan `httpx`; không làm hỏng các kiểm tra
đã chạy. Chưa đề xuất thay dependency chỉ dựa vào warning này.

Bản sao kiểm chứng nằm tại `C:\Users\Home33\AppData\Local\Temp\doc-suite-research-z30nnuwi`. Trong
đó có `research-tests.txt`, `research-diagnostics.json`, `research-entrypoints.json` và hai script
tái hiện. Các HTTP request render sơ đồ trong tình huống tái hiện được mock; không gửi nội dung báo
cáo đến dịch vụ render.

Lệnh pytest chạy trong bản sao tạm, không chạy trên các workspace tài liệu thật:

```powershell
rtk proxy D:\doc-automation-suite\.venv\Scripts\python.exe -X utf8 -m pytest -q -o addopts= -p no:cacheprovider
```

## 3. Vấn đề đã tái hiện được

| ID  | Tình huống và kết quả thực tế                                                                                                                   | Tác động                                                     | Hướng sửa tối thiểu                                                                           |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| R01 | Tạo dự án từ tieu_luan_nd30: không có template.docx; F01_toc.md không có marker TOC; DOCX không có field TOC và vẫn chứa lời nhắc nhập nội dung | Dự án mới chưa tạo báo cáo hoàn chỉnh, dù xuất thành công    | Hoàn thiện boilerplate/mẫu DOCX; chèn TOC thật; kiểm tra thông tin còn thiếu khi xuất bản nộp |
| R02 | Xóa Ch02_NOI_DUNG.md đã khai báo required_files: assembler vẫn trả kết quả thành công và bỏ qua chương này                                      | Báo cáo thiếu phần nội dung mà người dùng không nhận lỗi     | Kiểm tra các file bắt buộc trước khi ghép; trả danh sách thiếu                                |
| R03 | Markdown tham chiếu ảnh không tồn tại: builder vẫn lưu DOCX với dòng Khong tim thay anh                                                         | File nộp chứa thông báo lỗi thay ảnh                         | Phân biệt xuất nháp và bản nộp; bản nộp phải báo lỗi thiếu ảnh                                |
| R04 | Render hai sơ đồ khác nội dung, cùng vị trí số 1 và cache: chỉ gọi renderer một lần, lần hai trả ảnh đầu                                        | Nội dung báo cáo có thể sai vì sơ đồ cũ                      | Khóa cache bằng hash nội dung và tham số render, thay vì vị trí                               |
| R05 | Config đặt line_spacing=2.0 và first_line_indent=2.5: giá trị hiệu lực vẫn là 1.5 và 1.27                                                       | Các khóa cấu hình cũ không điều khiển định dạng như mong đợi | Ánh xạ khóa cũ sang khóa hiện tại khi load; lưu lại dạng chuẩn                                |

Nguồn và vị trí cần sửa:

- R01: [mẫu tiểu luận](../../templates/tieu_luan_nd30/config.yaml),
  [TemplateManager](../../src/core/template_manager.py) dòng 41–64,
  [DocxBuilder](../../src/core/docx_builder.py) dòng 30–41.
- R02: [DocumentAssembler](../../src/core/assembler.py) dòng 35–63.
- R03: [add_markdown_image](../../src/core/docx_helpers.py) dòng 568 trở đi.
- R04: [MediaDownloader](../../src/core/media_downloader.py) dòng 82–120. Nhánh công thức cũng đặt
  tên cache theo vị trí; lỗi sơ đồ đã được tái hiện, công thức mới được xác định cùng cơ chế qua mã.
- R05: [get_paragraph_settings](../../src/core/docx_helpers.py) dòng 132–148 và
  [DocxBuilder](../../src/core/docx_builder.py) dòng 69–78.

Những trường hợp này chưa được bộ 71 test hiện tại bao phủ đầy đủ. Khi triển khai nên thêm kiểm tra
hồi quy đúng các tình huống trên.

## 4. Rủi ro xác định qua đọc mã

Các mục dưới đây là phân tích mã, chưa phải kết quả đo tải hoặc thử phá lỗi.

| Điểm                              | Bằng chứng                                                                                                                                         | Việc nên làm                                                                       |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Tự lưu ghi trực tiếp              | save_current_file dùng write_text; khi có thay đổi ngoài editor chỉ báo trạng thái, chưa có bước giải quyết xung đột trước lần lưu tiếp theo       | Ghi file tạm rồi thay thế; giữ bản phục hồi; kiểm tra thay đổi ngoài trước khi ghi |
| Xuất có thể giữ UI chờ            | build_docx ghép và render ngay trong callback; render mạng có timeout 30/15 giây                                                                   | Chạy tác vụ xuất ngoài callback UI; cập nhật tiến trình qua main thread            |
| Xem trước khác bản xuất           | \_estimate_block_height dùng độ dài chữ và chiều cao ước lượng                                                                                     | Dùng preview nhanh để soạn; kiểm tra bản PDF thực trước khi nộp/in                 |
| Mẫu không khớp loại báo cáo       | \_build_scholarly_chapter_content luôn tạo Research Question/Theoretical Basis/Analysis…                                                           | Dàn ý chương theo mẫu học thuật hoặc công sở                                       |
| Dependency runtime khai báo thiếu | config import yaml; requirements.txt có PyYAML nhưng pyproject.toml không khai báo trực tiếp; uv tree hiện thấy PyYAML qua pre-commit của nhóm dev | Khai báo dependency runtime trực tiếp; kiểm tra cài không có dev dependency        |
| Cách khởi chạy thay dependency    | launch.bat nâng pip và cài requirements mỗi lần mở                                                                                                 | Tách bước cài/cập nhật khỏi mở ứng dụng; dùng lockfile hiện có                     |
| CI chưa bao phủ đầy đủ thay đổi   | PR workflow lọc src/\*\*; test/template/dependency-only changes không nằm trong bộ lọc                                                             | Mở trigger phù hợp; thêm kiểm tra Windows cho thao tác desktop/export              |

Nguồn: [Visual Builder](../../src/ui/visual_builder/window.py) dòng 912, 1225, 1778, 1825;
[PreviewUtils](../../src/ui/preview_utils.py) dòng 479, 578;
[dependency metadata](../../pyproject.toml), [requirements](../../requirements.txt),
[launcher](../../launch.bat), [CI](../../.github/workflows/ci-cd.yml).

Tài liệu Tkinter chính thức khuyến nghị tránh công việc dài trong event handler, dùng timer hoặc
luồng riêng. Đề xuất tác vụ nền cho export xuất phát từ callback hiện tại và hướng dẫn này.
[Python Tkinter threading model](https://docs.python.org/3/library/tkinter.html#threading-model).

## 5. Nâng cấp chất lượng Word/PDF

### 5.1 Mẫu tài liệu và cấu trúc báo cáo

Đề xuất bộ mẫu ban đầu theo mục tiêu đã xác nhận:

| Nhóm                       | Nội dung mẫu                                                                                    | Thông tin nhập qua form                                      |
| -------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Bài tập lớn/đồ án          | Bìa, mục lục, mở đầu, cơ sở, phân tích/thiết kế, kết quả, kết luận, tài liệu tham khảo, phụ lục | Trường, khoa, môn, đề tài, giảng viên, nhóm/thành viên, ngày |
| Tiểu luận/báo cáo thực tập | Bìa, mục lục, phần nội dung, kết luận, tham khảo/phụ lục                                        | Đơn vị, người thực hiện, người hướng dẫn, kỳ báo cáo         |
| Báo cáo công sở            | Tiêu đề, tóm tắt, mục tiêu, kết quả, số liệu, vấn đề, đề xuất, phụ lục                          | Đơn vị, người lập, người nhận, kỳ báo cáo                    |
| Biên bản/tờ trình          | Các phần theo mẫu cụ thể của đơn vị                                                             | Thời gian, địa điểm, thành phần, nội dung và xác nhận        |

Đây là dàn ý đề xuất, không phải quy định mặc định của mọi trường hoặc cơ quan. Mẫu học thuật và mẫu
công sở cần tùy chỉnh độc lập. Tên mẫu hiện có chứa “Nghị định 30” chưa được thẩm định về tuân thủ
trong nghiên cứu này.

Lưu mẫu dưới `templates/` như hiện tại: YAML cấu hình, boilerplate nội dung, DOCX chứa styles và
assets. Metadata nhập một lần, dùng cho bìa và phần đầu/chân trang. Nội dung còn thiếu phải hiển thị
cho người dùng; không tự điền thông tin tác giả, số liệu hoặc nguồn tham khảo.

### 5.2 Tính năng báo cáo cần hoàn thiện

- Heading và đánh số chương/mục nhất quán; dùng styles thực trong Word.
- Section riêng cho bìa, phần đầu và thân bài; thiết lập số trang, header/footer, trang ngang cho
  bảng rộng.
- Mục lục tự động có dữ liệu và số trang sau cập nhật.
- Caption có số tự động cho hình/bảng; danh mục hình/bảng và tham chiếu chéo.
- Bảng giữ hàng tiêu đề, độ rộng hợp lý, không mất nội dung; hình và caption không bị tách ngoài ý
  muốn.
- Mẫu có styles cho thân bài, tiêu đề, bảng, caption và code; hạn chế định dạng cứng trong builder.
- Với báo cáo học thuật cần trích dẫn/công thức: thử hỗ trợ bibliography/CSL và công thức chỉnh sửa
  được, sau khi kiểm chứng đường xuất tương ứng.

`python-docx` có API styles, sections và header/footer phù hợp để phát triển từ lõi hiện có. Section
là đơn vị cho lề, hướng trang và header/footer.
[Styles](https://python-docx.readthedocs.io/en/stable/user/styles-using.html),
[Sections](https://python-docx.readthedocs.io/en/latest/user/sections.html),
[Headers and footers](https://python-docx.readthedocs.io/en/latest/user/hdrftr.html).

Caption và tham chiếu chéo Word cần giữ đối tượng/field có thể cập nhật khi nội dung đổi. Đề xuất
helper OOXML nhỏ cho field và bookmark, cùng kiểm tra sau khi chèn/xóa/di chuyển hình.
[Word captions](https://support.microsoft.com/en-gb/word/add-format-or-delete-captions-in-word),
[Cross-reference](https://support.microsoft.com/en-us/word/create-a-cross-reference),
[OOXML field representation](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.fieldchar?view=openxml-3.0.1).

### 5.3 Chọn đường xuất PDF

| Công cụ              | Vai trò phù hợp                                                | Điều kiện trước khi tích hợp                                            |
| -------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------- |
| python-docx hiện tại | Tạo DOCX và cấu trúc tài liệu                                  | Kiểm tra template/style/field; dùng ứng dụng dàn trang cho bước PDF     |
| Word trên desktop    | Cập nhật field và xuất PDF trong phiên làm việc của người dùng | Kiểm chứng tự động hóa trên máy này; xử lý tài liệu đang mở và lỗi xuất |
| LibreOffice headless | Ứng viên cho CLI/API/batch không giao diện                     | Thử cài đặt, font, field/TOC và khả năng tương thích mẫu Word           |
| Pandoc               | Ứng viên cho trích dẫn, CSL và công thức của báo cáo học thuật | Thử trên mẫu thật; không thay toàn bộ core trước khi chứng minh lợi ích |
| TkinterWeb           | Xem trước nhanh khi soạn                                       | Không dùng số trang HTML làm kết quả kiểm chứng PDF                     |

Word cung cấp API cập nhật fields và xuất fixed-format/PDF. Tuy nhiên Microsoft không hỗ trợ Office
automation trong ứng dụng server hoặc môi trường không tương tác; vì vậy Word desktop không nên trở
thành backend mặc định cho API/batch không giám sát.
[Fields.Update](https://learn.microsoft.com/en-us/office/vba/api/word.fields.update),
[ExportAsFixedFormat](https://learn.microsoft.com/en-us/office/vba/api/word.document.exportasfixedformat),
[Office server-side automation](https://support.microsoft.com/en-us/visio/considerations-for-server-side-automation-of-office).

LibreOffice hỗ trợ headless, convert-to và profile riêng. Writer có chức năng cập nhật
field/index/mục lục và dàn trang; adapter phải kiểm tra bước cập nhật trước khi xuất. Exit code 0
của chuyển đổi chưa đủ chứng minh mục lục đúng. Word và LibreOffice có thể cho bố cục khác nhau; cần
chọn renderer của bản PDF phát hành và đối chiếu mẫu trong Word.
[Command-line parameters](https://help.libreoffice.org/latest/en-GB/text/shared/guide/start_parameters.html?DbPAR=WRITER&System=WIN),
[PDF export](https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html?DbPAR=SHARED),
[Writer Update](https://help.libreoffice.org/latest/en-US/text/swriter/01/06990000.html).

Pandoc hỗ trợ DOCX reference-doc, citeproc/CSL và xuất toán sang OMML; manual cũng nêu giới hạn
chuyển đổi đối với bố cục và bảng phức tạp. Đề xuất thử riêng đường báo cáo học thuật có trích
dẫn/công thức; kiểm tra định dạng tùy chỉnh hiện tại, không đưa vào mọi job ngay từ đầu.
[Pandoc User’s Guide](https://pandoc.org/MANUAL.html).

## 6. Nâng cấp giao diện và thao tác soạn

Giữ Tkinter trong gói nâng cấp đầu. Từ việc đọc giao diện hiện tại, chưa có bằng chứng rằng chuyển
sang web hoặc một toolkit mới giải quyết các lỗi nội dung và export.

Luồng người dùng đề xuất:

1. Chọn loại văn bản và mẫu.
2. Nhập thông tin báo cáo qua form.
3. Soạn theo cây chương/mục; chèn bảng, hình, caption và tham chiếu.
4. Chạy kiểm tra tài liệu; chuyển tới vị trí lỗi hoặc thông tin còn thiếu.
5. Xuất Word/PDF và xem bản PDF trước khi nộp/in.

Các thay đổi ưu tiên:

- Tiếng Việt nhất quán cho nhãn, trợ giúp và thông báo.
- Gom các nút hiện tại thành nhóm Văn bản, Chèn, Bố cục, Xuất; kiểm tra thao tác trên màn hình
  laptop.
- Thêm thao tác chọn heading, in đậm/nghiêng, tạo bảng và sửa caption bằng form; vẫn lưu nội dung
  theo cấu trúc dự án hiện tại.
- Dàn ý chương lấy từ mẫu thay cho một khung nghiên cứu chung.
- Trạng thái lưu rõ ràng; phục hồi bản chưa lưu khi mở lại; xử lý xung đột file ngoài editor.
- Xuất có tiến trình; thao tác soạn không bị chặn bởi render mạng hoặc chuyển PDF.
- Xem trước nội dung nhanh và nút Xem PDF đã xuất. Khi nội dung đã đổi sau lần xuất, hiển thị bản
  PDF đang cũ.

TkinterWeb là widget HTML/CSS, không phải bộ dàn trang DOCX. Nghiên cứu này chưa có thử nghiệm sử
dụng trực tiếp hoặc ảnh chụp giao diện; đề xuất UX cần được kiểm tra bằng các tác vụ thật ở mục 9.
[TkinterWeb documentation](https://tkinterweb.readthedocs.io/en/latest/).

## 7. Nâng cấp CLI/API và tự động hóa hàng loạt

### 7.1 Dùng chung đường xuất

GUI, CLI, API và make.py đã dùng cùng Assembler/DocxBuilder, nhưng lặp phần chọn đường dẫn, tạo
cache, ghép và lưu. Chỉ cần tách phần điều phối vào một hàm core chung, chẳng hạn
`compile_document(...)` trong `src/core/export.py`.

Luồng đề xuất:

```text
Dự án hiện có: config.yaml + chapters/*.md + assets + template.docx
    -> kiểm tra đầu vào và chụp phiên bản nội dung
    -> ghép Markdown
    -> tạo DOCX tạm
    -> cập nhật field/dàn trang và tạo PDF nếu được yêu cầu
    -> kiểm tra kết quả
    -> công bố file và trả kết quả cho GUI/CLI/API
```

Gói đầu giữ định dạng dự án hiện tại. Chưa cần tạo AST tài liệu mới, plugin engine hoặc hệ thống
dịch vụ riêng.

Kết quả xuất tối thiểu: trạng thái, đường dẫn artifact, lỗi/cảnh báo và trạng thái cập nhật field.
Có thể bổ sung hash đầu vào/đầu ra vào JSON kết quả để batch biết bản nào được tạo từ nội dung nào.
Không công bố file xuất lỗi thay cho bản thành công trước đó.

Phân biệt rõ xuất nháp có cảnh báo và bản nộp đã đạt các kiểm tra tự động. Trạng thái đạt kiểm tra
kỹ thuật vẫn không thay thế việc duyệt nội dung báo cáo.

### 7.2 Batch và dữ liệu đầu vào

- CLI đọc manifest JSON/YAML gồm danh sách workspace, định dạng xuất và thư mục đích.
- Chạy tuần tự trước; ghi kết quả từng mục để chạy lại mục lỗi.
- Một mục lỗi không làm mất kết quả các mục còn lại; exit code tổng thể phản ánh có lỗi.
- Mỗi job dùng bộ đầu vào nhất quán, tránh vừa xuất vừa lấy các phiên bản chương khác nhau.
- Không cho hai job cùng ghi một output; cache/profile PDF cần có quy tắc sử dụng rõ ràng.
- API dùng cùng hàm core. Với export kéo dài, bổ sung job id/trạng thái khi đã đo nhu cầu thực; gói
  ban đầu có thể giữ endpoint hiện tại.
- Tạo báo cáo hàng loạt theo dữ liệu CSV/Excel là phần mở rộng tiếp theo: ánh xạ trường dữ liệu vào
  metadata/mẫu, giữ nguyên dữ liệu thiếu và báo lỗi theo dòng.

Giữ API ở phạm vi triển khai đã xác định. Nếu sau này phục vụ người dùng qua mạng, đánh giá xác
thực, phân quyền workspace và giới hạn tác vụ trước khi mở dịch vụ; nghiên cứu này không xác nhận
API hiện tại phù hợp triển khai công khai.

## 8. Các gói triển khai và tiêu chí hoàn thành

| Thứ tự | Gói                                 | Phạm vi chính                                                                                          | Bằng chứng hoàn thành                                                                                       |
| ------ | ----------------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| 1      | Ổn định nội dung và lưu/xuất        | R01–R05; lưu an toàn; phụ thuộc runtime; hàm export chung; CI phù hợp                                  | Các lỗi tái hiện có test hồi quy; thiếu chương/ảnh không được báo bản nộp thành công; đổi sơ đồ tạo ảnh mới |
| 2      | Báo cáo hoàn chỉnh và thao tác soạn | Mẫu BTL/công sở; metadata; styles; section/số trang; TOC; caption; toolbar/form; export nền            | Người dùng tạo và chỉnh sửa hai loại báo cáo qua GUI; Word mở được, cấu trúc và field đúng sau cập nhật     |
| 3      | PDF và hàng loạt                    | PoC renderer trước; tích hợp backend đạt mẫu kiểm tra; preview PDF; batch manifest; API/CLI thống nhất | PDF có nội dung/số trang/ảnh đúng; batch có mục lỗi vẫn giữ mục thành công; kết quả từng mục rõ ràng        |
| 4      | Học thuật và dữ liệu nâng cao       | Trích dẫn/CSL, công thức OMML, tham chiếu chéo đầy đủ, dữ liệu CSV/Excel                               | Mẫu có trích dẫn/công thức xuất và chỉnh sửa đúng; dữ liệu thiếu không bị tự điền                           |

Ba nhóm người dùng yêu cầu đều nằm trong lộ trình. Gói 1 tạo nền chung cho GUI/CLI/API; gói 2 hoàn
thiện việc soạn; gói 3 hoàn thiện PDF/batch. Không gắn số ngày, chi phí hoặc tỷ lệ chất lượng khi
chưa có mẫu chuẩn và phạm vi triển khai chi tiết.

## 9. Bộ nghiệm thu nên sử dụng

| Mẫu/tình huống                    | Điều cần kiểm tra                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------------- |
| BTL tiếng Việt                    | Bìa, heading nhiều cấp, mục lục, số trang, code, bảng/hình, tham khảo và phụ lục      |
| Báo cáo công sở                   | Metadata, tóm tắt, bảng số liệu, header/footer, logo và phần đề xuất                  |
| Bảng rộng và tài liệu dài         | Section ngang, lặp hàng tiêu đề, nội dung không tràn lề; bảng/caption ngắt trang đúng |
| Sửa nội dung sau lần xuất đầu     | TOC và số trang được cập nhật; đổi sơ đồ/công thức không tái dùng ảnh cũ              |
| Thiếu chương/ảnh/thông tin        | Lỗi chỉ đúng vị trí; nháp và bản nộp có trạng thái khác nhau                          |
| File đích đang mở hoặc lỗi ghi    | Bản xuất trước còn nguyên; báo lỗi có cách xử lý                                      |
| Đóng bất thường và sửa file ngoài | Phục hồi nội dung; không âm thầm ghi đè phiên bản bên ngoài                           |
| GUI/CLI/API cùng đầu vào          | Cấu trúc DOCX và danh sách lỗi/cảnh báo nhất quán                                     |
| Batch có cả mục hợp lệ và lỗi     | Kết quả từng mục độc lập, không ghi nhầm output, chạy lại được mục lỗi                |
| Báo cáo có citation/công thức     | Citation và bibliography khớp nguồn; công thức chỉnh sửa được; PDF đọc đúng           |

Kiểm tra đầu ra cần kết hợp: mở DOCX không có repair warning; kiểm tra styles/section/fields và ảnh
trong OOXML; tìm/chọn được chữ tiếng Việt trong PDF; xem trang có bảng, hình, công thức; kiểm tra
mục lục/số trang sau khi nội dung đổi. Không dùng việc file tồn tại làm tiêu chí duy nhất.

Đóng ứng dụng hoặc gây lỗi ghi chỉ thử trong bản sao dự án nghiệm thu, không thử trên báo cáo đang
làm thật.

## 10. Những việc chưa được xác nhận

- Mẫu chuẩn thực tế của trường và đơn vị công sở; cần mẫu nguồn trước khi cam kết chuẩn định dạng.
- Bộ font mục tiêu, yêu cầu đánh số trang, citation style và cách duyệt văn bản.
- Chất lượng render Word/LibreOffice/Pandoc trên tài liệu thật; chưa tạo PDF trong phiên nghiên cứu.
- Khả năng xử lý tải, hủy job, xuất đồng thời và trải nghiệm giao diện ở các kích thước màn hình.
- Phạm vi API: dùng cá nhân trên máy hay phục vụ nhiều người; chưa coi đây là hệ thống nhiều người
  dùng.

Bước triển khai có cơ sở nhất là gói 1: sửa các tình huống đã tái hiện và thống nhất đường xuất. Các
quyết định renderer và mẫu chuẩn cần chốt bằng thử nghiệm tài liệu trước khi đưa vào bản phát hành.
