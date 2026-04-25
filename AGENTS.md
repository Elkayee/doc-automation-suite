# AGENTS.md — AI Agent Guidance for NMCNPM

This guide helps AI agents rapidly become productive in this document-processing codebase.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Architecture Overview

**NMCNPM** is a specialized toolkit for Vietnamese academic reports (NMCNPM group project). The workflow is:

- **Input:** Markdown chapters (`/chapters/Ch*.md`)
- **Processing:** Assemble → Render Mermaid diagrams → Convert MD → DOCX
- **Output:** Professional `.docx` report

**Critical:** The repo is split across **Python workflows** (file processing) and **`/skills`** (modular guidance). Most active work happens in `/chapters` (content) and three root-level scripts: `make.py`, `split_chapters.py`, and `convert_docx_to_md.py`.

## Essential Workflows

### 1. Build Complete Report: `python make.py`

**Two-stage pipeline:**

- **Stage 1:** Assembles `chapters/Ch0*.md` (excluding Ch08/09) → concatenates into `Bao_Cao_Tieu_Luan_NMCNPM.md`
- **Stage 2:** Converts MD → DOCX with formatting (headings, tables, Mermaid diagrams)

**Key mechanics:**

- Mermaid diagrams cached in `mermaid_cache/` (API calls to `mermaid.ink`)
- Heading colors: H1=`#1A3A5C`, H2=`#1F619E`, H3=`#2E86AB`, H4=`#449DD1`
- Tables use blue header (`#1F619E`) + light blue alternating rows (`#EBF4FB`)
- File save handles permission errors by appending `_new` suffix

### 2. Document Manipulation

- **Convert DOCX → Markdown:** `python convert_docx_to_md.py [input.docx] [output.md]`
- **Split Markdown into chapters:** `python split_chapters.py [input.md] [output_dir]`
- **Unpack DOCX to XML:** `python skills/xu-ly-van-phong/scripts/office/unpack.py file.docx output_dir`
- **Repack XML to DOCX:** `python skills/xu-ly-van-phong/scripts/office/pack.py input_dir output.docx`
- **Convert PDF → DOCX:** `python skills/xu-ly-van-phong/scripts/convert/convert_pdf_to_docx.py in.pdf out.docx`

**Principle:** For advanced edits (preserve formatting), use Unpack → Edit XML → Repack instead of recreating via python-docx.

## Code Patterns

### Markdown to DOCX Conversion (in `make.py`)

````python
# Parse markdown with inline formatting and special blocks
tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
# Handle: **bold**, *italic*, `code`

# Mermaid diagram handling
if line.strip().startswith('```mermaid'):
    render_mermaid(code, idx)  # Cache PNG, insert with aspect-ratio logic

# Tables: parse pipe-delimited rows, first row = header (blue background)
if line.startswith('|'):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
````

### DOCX Formatting Helpers (reused across scripts)

```python
# Cell/paragraph background shading
def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

# Page setup: A4 (21×29.7cm), margins 3/2/2.5/2.5cm, Times New Roman 13pt
def set_page_setup(doc):
    sec = doc.sections[0]
    sec.left_margin = Cm(3)
    # ... (matches Vietnamese standard formatting)
```

## Project-Specific Conventions

1. **File naming:** Reports use `Bao_Cao_Tieu_Luan_NMCNPM*.docx` (with optional `_Tung`, `_new` suffixes on errors)
2. **Chapter structure:** `chapters/Ch01.md`, `Ch02.md`, ... `Ch07.md` (Ch08/09 excluded from final build)
3. **Headings:** Markdown levels (H1–H6) → Heading 1–4 styles with Vietnamese colors
4. **Unicode handling:** Always use `encoding='utf-8'` and `sys.stdout.reconfigure(encoding='utf-8')`
5. **Vietnamese standards:** Refer to `skills/xu-ly-van-phong/standards/nd30.md` for administrative document rules

## Integration Points

### External Dependencies

- **`docx` (npm):** Core library (v9.6.1+) for DOCX creation/inspection
- **`mermaid.ink` API:** Diagram rendering (with 0.5s delays to avoid throttling)
- **`python-docx`, `openpyxl`, `pypdf`, `pdfplumber`:** Python ecosystem (install via pip)
- **`soffice` (LibreOffice):** Headless document conversion

### Cross-Component Communication

- Root scripts (`make.py`, `split_chapters.py`, `convert_docx_to_md.py`) own the primary report workflow
- `/skills/handling-docx-files/` provides XML-level DOCX manipulation for advanced use cases
- All office scripts write to consistent output directories (`chapters/`, `Bao_Cao_*.md`, `Bao_Cao_*.docx`)

## Debugging Checklist

Before implementing, check:

1. **Encoding issues?** Add `encoding='utf-8'` to file opens and `sys.stdout.reconfigure(encoding='utf-8')`
2. **Mermaid diagram blank?** Check API response status; if rendering fails, fallback text is inserted
3. **Table formatting broken?** Verify all rows have same column count; ensure cell background uses `.set(qn('w:fill'), hex)` not `ShadingType.SOLID`
4. **Permission error on save?** Script handles this—checks if file locked, saves as `_new` suffix
5. **Chapter not appearing?** Verify filename matches `Ch0*.md` pattern and isn't Ch08/09

## Key Files to Read First

1. **`make.py`** — The main build pipeline; assembles chapters and renders DOCX
2. **`split_chapters.py`** — Splits the assembled markdown back into chapter files
3. **`convert_docx_to_md.py`** — Converts the generated report back to markdown with extracted media
4. **`skills/xu-ly-van-phong/SKILL.md`** — 4-layer architecture for Vietnamese document standards

---

**Last Updated:** 2026-04-25
**Status:** Active development (NMCNPM group project deadline 23:00 same day)

YÊU CẦU BÀI TẬP NHÓM MÔN NMCNPM

1. Số lượng thành viên nhóm: 5-6 sinh viên
2. Công việc và yêu cầu của nhóm:

- Nhóm nhận chủ đề theo phân công. Danh sách kèm theo.
- Mỗi nhóm cử 1 sinh viên làm trưởng nhóm. Ghi chú trưởng nhóm trên link chia nhóm.
- Tạo nhóm Zalo để nhóm làm việc.
- Công việc làm chung của cả nhóm:
  o Mô tả bài toán (yêu cầu người sử dụng)
  o Đặc tả yêu cầu phần mềm: yêu cầu chức năng, phi chức năng.
  o Biểu đồ UC tổng quát.
  o Biểu đồ lớp thực thể.
- Mỗi thành viên trong nhóm chủ trì làm ít nhất 1 UseCase với các việc sau: o Biểu đồ UC chi tiết
  o Đặc tả UC
  o Biểu đồ hoạt động
  Chú ý: chọn UC phải đủ lớn, có nghiệp vụ, có ràng buộc. Nếu chọn những UC đơn giản (ví dụ đăng nhập, đăng xuất, đổi mật khẩu hoặc UC kiểu như thêm sửa xóa đơn giản) thì sẽ không đạt hoặc đánh giá kết quả thấp.

3. Thời hạn:
   o Đại diện nhóm nộp trên hệ thống LMS của nhà trường. o Thời gian: Trước 23h ngày 25/4/2026.
   o Báo cáo nộp ghép chung thành một file doc (hoặc pdf) gồm:
   ▪ Phần 1 là các nội dung chung của cả nhóm
   ▪ Phần 2 là nội dung của từng thành viên (tham khảo bố cục phía sau)
   1BỐ CỤC BÁO CÁO BÀI TẬP NHÓM
4. Trang bìa:
   ◦ Tên chủ đề của nhóm
   ◦ Danh sách thành viên nhóm và ghi rõ thành viên đó đảm nhiệm làm UseCase nào trong bài tập
5. Phần 1 – Công việc chung của nhóm
   a. Mô tả yêu cầu bài toán, yêu cầu người dùng:

- Mô tả bằng ngôn ngữ tự nhiên.
- Mô tả đủ các yêu cầu mà “người dùng” cần.
- Các ràng buộc nghiệp vụ.
  Chú ý: Phần này khoảng 2-3 trang và mô tả bằng ngôn ngữ tự nhiên, như
  mô tả của khách hàng (chứ chưa cần mô hình hóa, vẽ biểu đồ gì cả)
  b. Mô tả yêu cầu phần mềm
- Phân tích và xác định actor
- Xác định yêu cầu chức năng: các Usecase
- Xác định các yêu cầu phi chức năng
- Vẽ biểu đồ UC tổng quát.
  c. Xây dựng biểu đồ lớp thực thể
- Phân tích và xác định các thực thể
- Mô tả thực thể (thuộc tính, phương thức,..)
- Vẽ biểu đồ lớp thực thể.

23. Phần 2 – Kết quả từng thành viên
    Từng thành viên trên cơ sở UC mà mình chọn làm thì cần thực hiện các nội dung sau:
    a. Vẽ biểu đồ UC
    b. Viết đặc tả UC
    c. Vẽ biểu đồ hoạt động UC
