"""
Split the assembled report markdown into chapter files.

Default usage:
    python split_chapters.py
    python split_chapters.py input.md output_dir
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BAD_CHARS = '\\/:*?"<>|'


def sanitize_title(title: str) -> str:
    cleaned = title
    for char in BAD_CHARS:
        cleaned = cleaned.replace(char, '')
    return cleaned.replace(' ', '_')


def split_markdown_sections(markdown_text: str) -> list[tuple[str, str]]:
    lines = markdown_text.splitlines()
    sections: list[tuple[str, int, int]] = []
    current_title = 'header'
    current_start = 0

    for index, line in enumerate(lines):
        if line.startswith('## ') and index > 0:
            sections.append((current_title, current_start, index - 1))
            current_title = line.lstrip('#').strip()[:40]
            current_start = index

    sections.append((current_title, current_start, len(lines) - 1))

    return [
        (title, '\n'.join(lines[start:end + 1]))
        for title, start, end in sections
    ]


def write_chapter_files(source_path: str | Path, output_dir: str | Path) -> list[Path]:
    source_file = Path(source_path)
    destination = Path(output_dir)
    sections = split_markdown_sections(source_file.read_text(encoding='utf-8'))
    destination.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []
    for index, (title, content) in enumerate(sections):
        filename = destination / f'Ch{index:02d}_{sanitize_title(title)[:40]}.md'
        filename.write_text(content, encoding='utf-8')
        written_files.append(filename)
        print(f'  [{index:02d}] {filename.name}  ({len(content.splitlines())} dong)')

    print(f'\n[OK] Da tao {len(written_files)} file chapter trong thu muc {destination}/')
    return written_files


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    source_path = Path(args[0]) if len(args) >= 1 else Path.cwd() / 'Bao_Cao_Tieu_Luan_NMCNPM_from_docx.md'
    output_dir = Path(args[1]) if len(args) >= 2 else Path.cwd() / 'chapters'
    write_chapter_files(source_path, output_dir)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
