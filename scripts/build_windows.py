"""Build a complete portable distribution, retaining vendor libraries/licenses."""

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

import PyInstaller.__main__

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.create_app_icon import main as create_icon
from scripts.setup_renderers import PACKAGES
from src.core.renderers import run_process
from src.core.runtime import VERSION


def sha256(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-build', action='store_true', help='Archive an already verified distribution.')
    parser.add_argument('--no-zip', action='store_true', help='Build a candidate before native verification.')
    args = parser.parse_args()
    if os.name != 'nt':
        raise SystemExit('Windows builds must run on Windows.')
    root = Path(__file__).resolve().parents[1]
    bundle = root / 'dist/DocAutomationSuite'
    if (root / 'dist').resolve() != root / 'dist' or bundle.resolve() != bundle:
        raise SystemExit('Build destination must not redirect outside the project dist directory.')
    tools = Path(os.environ['LOCALAPPDATA']) / 'DocAutomationSuite/tools'
    if not args.skip_build:
        # Verify vendor inputs before copying extracted programs into the package.
        for name, (_, expected, _) in PACKAGES.items():
            if sha256(tools / f'{name}.msi') != expected:
                raise SystemExit(f'Vendor checksum mismatch: {name}')
        create_icon()
        PyInstaller.__main__.run(
            [
                str(root / 'packaging/windows.spec'),
                '--noconfirm',
                '--distpath',
                str(root / 'dist'),
                '--workpath',
                str(root / 'build/windows'),
            ]
        )
        for name in PACKAGES:
            shutil.copytree(
                tools / name,
                bundle / '_internal/tools' / name,
                ignore=shutil.ignore_patterns('*.msi'),
                dirs_exist_ok=True,
            )
        shutil.copy2(root / 'docs/WINDOWS.md', bundle / 'HUONG_DAN.md')
        notices = bundle / 'THIRD_PARTY'
        for distribution in importlib.metadata.distributions():
            for file in distribution.files or []:
                if any(part.lower().startswith(('license', 'copying', 'notice')) for part in file.parts):
                    source = Path(distribution.locate_file(file))
                    if source.is_file():
                        dest = notices / distribution.metadata['Name'] / Path(str(file))
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, dest)
    for required in [
        'DocAutomationSuite.exe',
        'DocAutomationCLI.exe',
        '_internal/tools/libreoffice/program/soffice.com',
        '_internal/tools/pandoc/Pandoc/pandoc.exe',
        '_internal/src/core/lo_refresh.py',
    ]:
        if not (bundle / required).is_file():
            raise SystemExit(f'Incomplete distribution: {required}')
    manifest = {
        'version': VERSION,
        'platform': 'Windows x64',
        'python': sys.version.split()[0],
        'packages': {
            name: importlib.metadata.version(name)
            for name in ['pyinstaller', 'python-docx', 'tkinterweb', 'pydantic', 'lxml', 'pypdf']
        },
        'vendor_inputs': {name: {'url': url, 'sha256': digest} for name, (url, digest, _) in PACKAGES.items()},
        'tools': {
            name: run_process([bundle / '_internal/tools' / relative, '--version']).stdout.splitlines()[0]
            for name, relative in {
                'libreoffice': 'libreoffice/program/soffice.com',
                'pandoc': 'pandoc/Pandoc/pandoc.exe',
            }.items()
        },
        'build_environment': {dist.metadata['Name']: dist.version for dist in importlib.metadata.distributions()},
        'files': {
            str(file.relative_to(bundle)).replace('\\', '/'): sha256(file)
            for file in sorted(bundle.rglob('*'))
            if file.is_file() and file.name != 'release-manifest.json'
        },
    }
    (bundle / 'release-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    if not args.no_zip:
        archive = root / f'dist/DocAutomationSuite-{VERSION}-win64.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
            for file in sorted(bundle.rglob('*')):
                if file.is_file():
                    target.write(file, file.relative_to(bundle.parent))
        archive.with_suffix('.zip.sha256').write_text(f'{sha256(archive)}  {archive.name}\n', encoding='ascii')
        print(f'Archive: {archive}', flush=True)
    print(f'GUI: {bundle / "DocAutomationSuite.exe"}', flush=True)
    print(f'SHA256: {sha256(bundle / "DocAutomationSuite.exe")}', flush=True)


if __name__ == '__main__':
    main()
