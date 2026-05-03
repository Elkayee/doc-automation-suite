"""
Doc Automation Suite - CLI entrypoint.
"""

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from src.core.assembler import DocumentAssembler
from src.core.docx_builder import DocxBuilder


BASE = Path(__file__).resolve().parent


def run_build_pipeline(workspace_dir: Path, md_out: Path, docx_out: Path, img_cache: Path):
    os.makedirs(img_cache, exist_ok=True)

    print('=' * 55)
    print(f'BUOC 1: Ghep chapters -> MD tai {workspace_dir.name}')
    print('=' * 55)

    assembler = DocumentAssembler(workspace_dir)
    final_md, chapter_files = assembler.save_assembled_for_export(md_out)

    kb = len(final_md.encode('utf-8')) // 1024
    print(f'\n  => {md_out}')
    print(f'     {len(final_md.splitlines())} dong | {kb} KB | {len(chapter_files)} chapters\n')

    print('=' * 55)
    print('BUOC 2: Convert MD -> DOCX')
    print('=' * 55)

    builder = DocxBuilder(workspace_dir)
    builder.build_from_markdown(str(md_out), img_cache)
    builder.save(docx_out)

    size = os.path.getsize(docx_out) // 1024
    print(f'\n[DONE] {docx_out}  ({size} KB)')
    return docx_out


def run_test_suite():
    if importlib.util.find_spec('pytest') is None:
        print('pytest is not installed. Install dev dependencies from pyproject.toml first.')
        return 1
    command = [sys.executable, '-m', 'pytest']
    completed = subprocess.run(command, cwd=BASE)
    return completed.returncode


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Doc Automation Suite')
    subparsers = parser.add_subparsers(dest='command', required=True)

    build_parser = subparsers.add_parser('build', help='Build a workspace into DOCX')
    build_parser.add_argument('--workspace', required=True, help='Thu muc du an')
    build_parser.add_argument('--md-out', help='File output Markdown')
    build_parser.add_argument('--docx-out', help='File output DOCX')
    build_parser.add_argument('--img-cache', help='Thu muc cache anh')

    subparsers.add_parser('test', help='Run automated test suite')

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.command == 'test':
        return run_test_suite()

    ws = Path(args.workspace).resolve()
    if not ws.exists() or not ws.is_dir():
        print(f'Loi: Workspace khong ton tai: {ws}')
        return 1

    md = Path(args.md_out) if args.md_out else ws / 'assembled.md'
    docx = Path(args.docx_out) if args.docx_out else ws / f'{ws.name}.docx'
    cache = Path(args.img_cache) if args.img_cache else ws / '.diagram_cache'

    run_build_pipeline(ws, md, docx, cache)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
