"""
Doc Automation Suite - CLI entrypoint.
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from src.core.export import compile_document

BASE = Path(__file__).resolve().parent


def run_build_pipeline(workspace_dir: Path, md_out: Path, docx_out: Path, img_cache: Path,
                       formats=('docx',), mode='draft', engine='auto'):
    result = compile_document(workspace_dir, md_out=md_out, docx_out=docx_out,
                              cache_dir=img_cache, formats=formats, mode=mode, engine=engine)
    print(f'[DONE] {result.compiled_docx}')
    if result.compiled_pdf:
        print(f'[PDF] {result.compiled_pdf}')
    for warning in result.warnings:
        print(f'[WARN] {warning}')
    return Path(result.compiled_docx)


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
    build_parser.add_argument('--format', dest='formats', action='append', choices=['docx', 'pdf'])
    build_parser.add_argument('--final', action='store_true')
    build_parser.add_argument('--engine', choices=['auto', 'builtin', 'academic'], default='auto')

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

    run_build_pipeline(ws, md, docx, cache, formats=args.formats or ('docx',),
                       mode='final' if args.final else 'draft', engine=args.engine)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
