"""
Doc Automation Suite - CLI Entrypoint
Dùng module này nếu chạy không qua giao diện UI (headless mode).
"""

import argparse
import os
import sys
from pathlib import Path

# Đảm bảo stdout in utf-8 trên windows
sys.stdout.reconfigure(encoding='utf-8')

from src.core.assembler import DocumentAssembler
from src.core.docx_builder import DocxBuilder

BASE = Path(__file__).resolve().parent

def run_build_pipeline(workspace_dir: Path, md_out: Path, docx_out: Path, img_cache: Path):
    os.makedirs(img_cache, exist_ok=True)

    print('=' * 55)
    print(f'BƯỚC 1: Ghép chapters -> MD tại {workspace_dir.name}')
    print('=' * 55)

    assembler = DocumentAssembler(workspace_dir)
    final_md, chapter_files = assembler.save_assembled(md_out)

    kb = len(final_md.encode('utf-8')) // 1024
    print(f'\n  => {md_out}')
    print(f'     {len(final_md.splitlines())} dong | {kb} KB | {len(chapter_files)} chapters\n')

    print('=' * 55)
    print('BƯỚC 2: Convert MD -> DOCX')
    print('=' * 55)

    builder = DocxBuilder(workspace_dir)
    builder.build_from_markdown(str(md_out), img_cache)
    builder.save(docx_out)

    size = os.path.getsize(docx_out) // 1024
    print(f'\n[DONE] {docx_out}  ({size} KB)')
    return docx_out

def parse_args():
    parser = argparse.ArgumentParser(description='Doc Automation Suite')
    parser.add_argument('--workspace', required=True, help='Thư mục dự án')
    parser.add_argument('--md-out', help='File output Markdown')
    parser.add_argument('--docx-out', help='File output DOCX')
    parser.add_argument('--img-cache', help='Thư mục cache ảnh')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    ws = Path(args.workspace).resolve()
    if not ws.exists() or not ws.is_dir():
        print(f"Lỗi: Workspace không tồn tại: {ws}")
        exit(1)

    md = Path(args.md_out) if args.md_out else ws / 'assembled.md'
    docx = Path(args.docx_out) if args.docx_out else ws / f'{ws.name}.docx'
    cache = Path(args.img_cache) if args.img_cache else ws / '.diagram_cache'

    run_build_pipeline(ws, md, docx, cache)
