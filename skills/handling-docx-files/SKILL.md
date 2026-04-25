---
name: handling-docx-files
description: Use when the user requests generating, editing, reading, or analyzing Microsoft Word (.docx) documents. Triggers include mentions of '.docx', 'Word doc', or requests for professional deliverables with complex formatting like TOCs, headers, and tracked changes.
---

# Handling DOCX Files

## Overview

Microsoft Word documents (.docx) are ZIP archives containing XML (OOXML). This skill provides patterns for programmatic creation and advanced editing through direct XML manipulation.

## When to Use

- Creating new professional reports, memos, or letters in Word format.
- Editing existing documents while preserving or adding tracked changes and comments.
- Converting Markdown or text content into polished, formatted DOCX files.
- **When NOT to use:** For basic text files, PDFs (unless converting from Word), or spreadsheets.

## Quick Reference

| Task                   | Approach                                   |
| ---------------------- | ------------------------------------------ |
| Read/analyze content   | `pandoc` or unpack for raw XML             |
| Create new document    | Use `docx-js` (JavaScript)                 |
| Edit existing document | Indirect editing: Unpack → Edit XML → Pack |
| Convert .doc to .docx  | `soffice.py --convert-to docx`             |

### Basic Conversions

```bash
# Convert .doc to .docx
python scripts/office/soffice.py --headless --convert-to docx document.doc

# Text extraction to Markdown
pandoc --track-changes=all document.docx -o output.md
```

## Implementation

**Programmatic Creation:** Detailed documentation on `docx-js` API patterns, styles, and page layouts can be found in [docx-js.md](docx-js.md).

**Advanced Editing:** XML schema reference, manual tracked changes, and comment insertion logic is available in [ooxml.md](ooxml.md).

## Common Mistakes

- **Dual Table Widths:** Tables render incorrectly if both `table.width` and `cell.width` are not set (recommend using DXA units).
- **Page Break Placement:** Inserting a `PageBreak` outside of a `Paragraph` results in invalid XML.
- **Manual Bullets:** Inserting unicode symbols (•) manually instead of using `LevelFormat.BULLET` in numbering configurations.
- **Table Shading:** Using `ShadingType.SOLID` instead of `ShadingType.CLEAR`, which can cause black backgrounds in some viewers.
- **Missing xml:space:** Failing to set `xml:space="preserve"` on `<w:t>` elements with leading/trailing whitespace.

## Dependencies

- `pandoc`: Text extraction.
- `docx`: `npm install -g docx`.
- `LibreOffice`: Headless conversion (`scripts/office/soffice.py`).
- `Poppler`: `pdftoppm` for image export.

## Real-World Impact

- **Professional Deliverables:** Enables creation of complex, board-ready reports with consistent branding.
- **Audit Trails:** Preserves authorship and history through precise tracked changes manipulation.
- **Automated Workflows:** Allows for large-scale document generation from data sources with pixel-perfect layout control.
