# Doc Automation Suite

Ứng dụng soạn văn bản, báo cáo bài tập lớn và báo cáo công sở bằng Python/Tkinter. Nội dung lưu
trong Markdown; cấu hình/mẫu trong YAML và DOCX. Phiên bản nâng cấp: 0.2.1.

## Mở ứng dụng

**Bản Windows portable:** giải nén toàn bộ `dist/DocAutomationSuite-0.2.1-win64.zip`, mở thư mục
DocAutomationSuite-0.2.1 rồi chạy **DocAutomationSuite.exe**. Giữ EXE cùng thư mục \_internal. Gói
có sẵn Python, mẫu và renderer Word/PDF. Dự án lưu ở `%LOCALAPPDATA%\DocAutomationSuite\workspaces`,
tách khỏi thư mục ứng dụng. [Hướng dẫn Windows/CLI/API](docs/WINDOWS.md).

**Chạy từ mã nguồn:** trên Windows, chạy `launch.bat`. Lần đầu script tạo môi trường và cài
dependency; những lần sau mở ứng dụng trực tiếp. Để cài đúng lockfile với uv:

```powershell
uv sync --locked
.venv\Scripts\python.exe main.py
```

Để có PDF, mục lục đã cập nhật và công thức Word/trích dẫn:

```powershell
.venv\Scripts\python.exe scripts/setup_renderers.py
.venv\Scripts\python.exe -m src.cli doctor
```

Để build lại bản Windows từ source đã cài renderer:

```powershell
uv sync --locked
.venv\Scripts\python.exe scripts/build_windows.py
```

Builder tạo EXE GUI, EXE CLI, ZIP, checksum và release-manifest.json. Nó giữ thư viện/giấy phép
renderer và kiểm tra SHA-256 gói vendor trước khi đóng gói.

Script Windows kiểm tra SHA-256 và trích xuất LibreOffice/Pandoc từ gói vendor vào
`%LOCALAPPDATA%\DocAutomationSuite\tools`. Không thay thế Office đang có. Trên Linux, cài
LibreOffice Writer, Python UNO và Pandoc bằng trình quản lý gói của hệ điều hành. Có thể chỉ định
executable bằng `DOC_SUITE_SOFFICE` và `DOC_SUITE_PANDOC`.

## Soạn báo cáo

1. Chọn **Tạo báo cáo mới** và mẫu: bài tập lớn, công sở, biên bản, tiểu luận hoặc bài kiểm tra. Mẫu
   mới là khung chung, chỉnh theo yêu cầu trường/đơn vị.
2. Trong **Văn bản → Thông tin báo cáo**, nhập thông tin bìa. Dấu `*` chỉ trường cần có khi xuất bản
   nộp; thông tin chưa biết có thể để trống trong bản nháp.
3. Soạn theo cây chương. Menu **Chèn** có tiêu đề, bảng, hình, tham chiếu, nguồn trích dẫn và công
   thức. Ctrl+S lưu; Ctrl+B/Ctrl+I định dạng đoạn chọn.
4. Chọn **Kiểm tra**, rồi **Xuất Word** hoặc **Xuất PDF**. Bật **Bản nộp** để chặn nội dung/ảnh bắt
   buộc còn thiếu và cập nhật fields trước khi công bố file.
5. Dùng **Xem PDF** để xem bản đã xuất. Xem trước HTML giúp soạn và điều hướng; chia trang trong
   vùng đó là ước lượng.

Xuất chạy nền để tiếp tục soạn. Khi nội dung đổi trong lúc xuất, giao diện báo bản PDF đang cũ. Lưu
dùng file tạm/thay thế nguyên tử; sửa từ bên ngoài sẽ chặn ghi đè và giữ nội dung editor ở
`.recovery/drafts`. Bản trước và lịch sử nằm trong `.recovery/previous` và `.recovery/history`.

## CLI

```powershell
.venv\Scripts\python.exe -m src.cli list-templates
.venv\Scripts\python.exe -m src.cli create bao_cao --template bao_cao_cong_so
.venv\Scripts\python.exe -m src.cli compile workspaces/bao_cao --json
.venv\Scripts\python.exe -m src.cli compile workspaces/bao_cao --final --format docx --format pdf
.venv\Scripts\python.exe -m src.cli batch batch.json --result-out batch-results.json
```

Mặc định là bản nháp DOCX. `--engine auto` chọn học thuật khi có math/citation; `--engine academic`
dùng Pandoc cho OMML và citeproc, `--engine builtin` giữ đường Markdown/DOCX cơ bản. Bản nộp không
chấp nhận citation chưa được xử lý. `--metadata metadata.json` bổ sung dữ liệu cho lần xuất mà không
ghi đè config nguồn. Output mặc định của CLI ở `build/`; GUI giữ file theo tên dự án tại gốc
workspace. Mỗi lần xuất có file `.export.json` ghi trạng thái, warnings và hashes.

Manifest `batch.json`: đường dẫn tính từ vị trí manifest và phải nằm trong thư mục đó. Với file
CSV/XLSX, quy tắc phạm vi giống nhau:

```json
{
  "jobs": [
    {
      "workspace": "workspaces/bao_cao",
      "formats": ["docx", "pdf"],
      "mode": "final",
      "metadata": { "period": "Kỳ báo cáo đã xác nhận" }
    }
  ]
}
```

CSV/XLSX dùng cột `workspace`, `docx_out`, `formats`, `mode`, `engine` và các cột metadata như
`title`, `author`, `organization`, `period`. Các cột metadata được ánh xạ theo đúng tên khóa, không
đoán nghĩa số liệu. Ô trống là thiếu dữ liệu, số 0 giữ nguyên. Với nhiều dòng cùng workspace, đặt
`docx_out` khác nhau. XLSX đọc sheet đang active và giá trị formula đã lưu; formula chưa có cache
được xem là thiếu dữ liệu. Batch ghi kết quả từng mục và tiếp tục sau mục lỗi; exit code khác 0 nếu
có mục thất bại.

## Trích dẫn và các thành phần Word

Menu nguồn trích dẫn tạo CSL JSON và chèn `[@id]`. Có thể dùng BibTeX/CSL YAML bằng khóa
`bibliography` trong config; `csl` trỏ tới file kiểu trích dẫn trong dự án. `[[REFERENCES]]` tạo
danh mục nguồn đã trích dẫn. Năm chưa biết để trống; citeproc xử lý theo kiểu trích dẫn, không tự
điền năm.

```text
[[COVER]]
[[TOC]]
[[BODY]]

# Chương 1 {#intro}

![Minh chứng](assets/images/example.png){caption="Kết quả", width=60%, align=center, id=figure1}

[[TABLE: table1 | Bảng kết quả]]
| Nội dung | Kết quả |
| --- | --- |
| Mục đã xác nhận | Giá trị đã xác nhận |

Xem [[REF: figure1]] và [[REF: table1]].

[[LANDSCAPE]]
[[PORTRAIT]]
[[FIGURES]]
[[TABLES]]
```

Công thức `$...$`/`$$...$$` trên đường học thuật là OMML chỉnh sửa được trong Word. Sơ đồ PlantUML
của đường cơ bản vẫn dùng dịch vụ render qua mạng như trước; công thức học thuật và PDF dùng công cụ
cục bộ. Các trường TOC/PAGE/SEQ/REF được cập nhật bằng LibreOffice với profile riêng trước PDF hoặc
bản nộp.

## API

```powershell
.venv\Scripts\python.exe -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Xem `/docs`; các endpoint: `/templates`, `/capabilities`, `/workspaces/create`,
`/workspaces/compile`, `/workspaces/batch`. Compile nhận `workspace_name`, `formats`, `mode`,
`engine`, metadata và các đường output tương đối trong dự án. Batch nhận `jobs` là danh sách request
compile, chạy tuần tự và trả kết quả từng mục. Cùng core được dùng cho GUI, CLI, API và make.py;
legacy có config cũng dùng core, còn chuyển Markdown rời không có config giữ đường nháp cũ.

API dành cho phạm vi cục bộ. Triển khai nhiều người dùng qua mạng cần đánh giá xác thực và quyền
workspace riêng; nâng cấp này chưa cung cấp cấu hình đó.

## Kiểm tra và tiến độ

Xem [PLAN.md](PLAN.md), [TASK.md](TASK.md) và [AGENTS.md](AGENTS.md) cho phạm vi, bằng chứng đã chạy
và quy tắc bảo toàn tài liệu. Bộ pytest cũ có thư mục tạm cố định; chạy full suite trong bản sao cô
lập khi đang có dữ liệu thử cần giữ. Ruff: `python -m ruff check .`; định dạng Markdown/JSON:
`npm run lint`.

Nguồn nền tảng: [python-docx](https://python-docx.readthedocs.io/en/latest/),
[Pandoc](https://pandoc.org/MANUAL.html),
[LibreOffice command line](https://help.libreoffice.org/latest/en-GB/text/shared/guide/start_parameters.html).
