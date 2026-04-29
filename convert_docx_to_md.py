"""
Convert a DOCX report back to reusable Markdown.

Default usage:
    python convert_docx_to_md.py
    python convert_docx_to_md.py input.docx output.md

Behavior:
    - preserves document order for paragraphs and tables
    - maps Heading 1-4 styles to markdown headings
    - keeps simple bold/italic inline formatting
    - extracts embedded images to a deterministic media directory
    - writes a new markdown file by default
"""

from __future__ import annotations

import argparse
import os
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

from docx import Document as load_document
from docx.document import Document as DocxDocument
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / 'Bao_Cao_Tieu_Luan_NMCNPM.docx'
DEFAULT_OUTPUT = BASE_DIR / 'Bao_Cao_Tieu_Luan_NMCNPM_from_docx.md'
DEFAULT_MEDIA_DIR = BASE_DIR / 'extracted_media' / 'Bao_Cao_Tieu_Luan_NMCNPM'
REL_EMBED = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed'


@dataclass
class ConversionState:
    media_dir: Path
    output_dir: Path
    image_counter: int = 0
    image_map: dict[str, tuple[int, Path]] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert DOCX to Markdown.')
    parser.add_argument('input', nargs='?', default=str(DEFAULT_INPUT))
    parser.add_argument('output', nargs='?', default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        '--media-dir',
        default=str(DEFAULT_MEDIA_DIR),
        help='Directory where embedded images will be extracted.',
    )
    return parser.parse_args()


def iter_block_items(parent: DocxDocument | _Cell) -> Iterator[Paragraph | Table]:
    if isinstance(parent, DocxDocument):
        parent_element = parent.element.body
    else:
        parent_element = parent._tc

    for child in parent_element.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def escape_markdown(text: str) -> str:
    text = text.replace('\\', '\\\\')
    text = text.replace('|', '\\|')
    return text


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.replace('\xa0', ' ')).strip()


def wrap_run_text(text: str, *, bold: bool, italic: bool) -> str:
    if not text:
        return ''
    if bold and italic:
        return f'***{text}***'
    if bold:
        return f'**{text}**'
    if italic:
        return f'*{text}*'
    return text


def paragraph_text_to_markdown(paragraph: Paragraph) -> str:
    parts: list[str] = []
    for run in paragraph.runs:
        text = run.text.replace('\xa0', ' ')
        if not text:
            continue
        wrapped = wrap_run_text(text, bold=bool(run.bold), italic=bool(run.italic))
        parts.append(wrapped)

    combined = ''.join(parts).strip()
    combined = re.sub(r'[ \t]+', ' ', combined)
    return combined


def export_image(part, state: ConversionState) -> tuple[int, Path]:
    part_key = str(part.partname)
    existing = state.image_map.get(part_key)
    if existing:
        return existing

    state.image_counter += 1
    suffix = Path(part.partname).suffix or '.bin'
    image_path = state.media_dir / f'image_{state.image_counter:03d}{suffix}'
    image_path.write_bytes(part.blob)
    state.image_map[part_key] = (state.image_counter, image_path)
    return state.image_counter, image_path


def extract_paragraph_images(paragraph: Paragraph, state: ConversionState) -> list[str]:
    image_lines: list[str] = []
    blips = paragraph._p.xpath(".//*[local-name()='blip']")

    for blip in blips:
        rel_id = blip.get(REL_EMBED)
        if not rel_id:
            continue
        image_part = paragraph.part.related_parts[rel_id]
        image_index, image_path = export_image(image_part, state)
        relative_path = os.path.relpath(image_path, output_file_dir(state.output_dir))
        image_lines.append(f'![Image {image_index}]({Path(relative_path).as_posix()})')

    return image_lines


def paragraph_to_markdown(paragraph: Paragraph, state: ConversionState) -> list[str]:
    style_name = paragraph.style.name if paragraph.style is not None else ''
    text = paragraph_text_to_markdown(paragraph)
    images = extract_paragraph_images(paragraph, state)
    lines: list[str] = []

    if style_name.startswith('Heading '):
        try:
            level = int(style_name.split()[-1])
        except ValueError:
            level = 1
        level = max(1, min(level, 4))
        if text:
            lines.append(f'{"#" * level} {text}')
    elif style_name.startswith('List Bullet'):
        if text:
            lines.append(f'- {text}')
    elif style_name.startswith('List Number'):
        if text:
            lines.append(f'1. {text}')
    elif text and re.fullmatch(r'-{3,}', text):
        lines.append('---')
    elif text.startswith('>'):
        lines.append(text)
    elif 'quote' in style_name.lower() and text:
        lines.append(f'> {text}')
    elif text:
        lines.append(text)

    lines.extend(images)
    return lines


def cell_to_text(cell: _Cell) -> str:
    pieces: list[str] = []
    for paragraph in cell.paragraphs:
        text = paragraph_text_to_markdown(paragraph)
        if text:
            pieces.append(text)
    return escape_markdown(' <br> '.join(pieces))


def table_to_markdown(table: Table) -> list[str]:
    rows: list[list[str]] = []
    for row in table.rows:
        row_values = [cell_to_text(cell) for cell in row.cells]
        rows.append(row_values)

    if not rows:
        return []

    width = max(len(row) for row in rows)
    normalized_rows = [row + [''] * (width - len(row)) for row in rows]
    header = normalized_rows[0]
    separator = ['---'] * width
    lines = [
        '| ' + ' | '.join(header) + ' |',
        '| ' + ' | '.join(separator) + ' |',
    ]
    for row in normalized_rows[1:]:
        lines.append('| ' + ' | '.join(row) + ' |')
    return lines


def normalize_lines(lines: list[str]) -> str:
    normalized: list[str] = []
    blank_pending = False

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line:
            if normalized and not blank_pending:
                normalized.append('')
                blank_pending = True
            continue

        normalized.append(line)
        blank_pending = False

    while normalized and normalized[-1] == '':
        normalized.pop()

    return '\n'.join(normalized) + '\n'


def output_file_dir(output_path: Path) -> Path:
    return output_path.parent


def convert_docx_to_markdown(
    input_path: str | Path,
    output_path: str | Path | None = None,
    media_dir: str | Path | None = None,
) -> Path:
    input_file = Path(input_path).resolve()
    output_file = Path(output_path).resolve() if output_path else DEFAULT_OUTPUT.resolve()
    media_root = Path(media_dir).resolve() if media_dir else DEFAULT_MEDIA_DIR.resolve()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    media_root.mkdir(parents=True, exist_ok=True)

    document = load_document(str(input_file))
    state = ConversionState(media_dir=media_root, output_dir=output_file)

    lines: list[str] = []
    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            block_lines = paragraph_to_markdown(block, state)
        else:
            block_lines = table_to_markdown(block)

        if block_lines:
            lines.extend(block_lines)
            lines.append('')

    output_file.write_text(normalize_lines(lines), encoding='utf-8')
    return output_file


def main() -> int:
    args = parse_args()
    result = convert_docx_to_markdown(args.input, args.output, args.media_dir)
    print(f'[OK] Markdown written to: {result}')
    print(f'[OK] Media extracted to: {Path(args.media_dir).resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
