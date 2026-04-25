# AGENTS.md — AI Agent Guidance for NMCNPM

This guide helps AI agents rapidly become productive in this document-processing codebase.

## Architecture Overview

**NMCNPM** is a specialized toolkit for Vietnamese academic reports (NMCNPM group project). The workflow is:
- **Input:** Markdown chapters (`/chapters/Ch*.md`)
- **Processing:** Assemble → Render Mermaid diagrams → Convert MD → DOCX
- **Output:** Professional `.docx` report

**Critical:** The repo is split across **Python workflows** (file processing) and **`/skills`** (modular guidance). Most active work happens in `/chapters` (content) and root-level scripts (`make.py`, `merge_reports.py`, `split_chapters.py`).

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
- **Unpack DOCX to XML:** `python skills/xu-ly-van-phong/scripts/office/unpack.py file.docx output_dir`
- **Repack XML to DOCX:** `python skills/xu-ly-van-phong/scripts/office/pack.py input_dir output.docx`
- **Convert PDF → DOCX:** `python skills/xu-ly-van-phong/scripts/convert/convert_pdf_to_docx.py in.pdf out.docx`

**Principle:** For advanced edits (preserve formatting), use Unpack → Edit XML → Repack instead of recreating via python-docx.

## Code Patterns

### Markdown to DOCX Conversion (in `make.py`)

```python
# Parse markdown with inline formatting and special blocks
tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
# Handle: **bold**, *italic*, `code`

# Mermaid diagram handling
if line.strip().startswith('```mermaid'):
    render_mermaid(code, idx)  # Cache PNG, insert with aspect-ratio logic
    
# Tables: parse pipe-delimited rows, first row = header (blue background)
if line.startswith('|'):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
```

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
- Root scripts (`make.py`, `merge_reports.py`) call into `/skills/xu-ly-van-phong/scripts/` for low-level operations
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

1. **`CLAUDE.md`** — Behavioral guidelines (caution-over-speed, simplicity, surgical changes)
2. **`make.py`** — The main build pipeline; demonstrates the full workflow
3. **`skills/xu-ly-van-phong/SKILL.md`** — 4-layer architecture for Vietnamese document standards
4. **`skills/handling-docx-files/SKILL.md`** — XML manipulation and DOCX internals
5. **`package.json`** — Minimal (only `docx` as npm dependency; most work is Python)

---

**Last Updated:** 2026-04-25  
**Status:** Active development (NMCNPM group project deadline 23:00 same day)
