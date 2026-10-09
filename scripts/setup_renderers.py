"""Extract verified vendor renderers into the current user's tool directory.

Uses MSI administrative extraction, without replacing the user's Office setup.
"""

import hashlib
import json
import os
import subprocess
from pathlib import Path

import requests

PACKAGES = {
    'libreoffice': (
        'https://download.documentfoundation.org/libreoffice/stable/26.8.1/win/x86_64/LibreOffice_26.8.1_Win_x86-64.msi',
        'c6298b10cfa1748bcbedad94c62ce771e240e5021bfd6d7a967cd571b04b5312',
        'soffice.com',
    ),
    'pandoc': (
        'https://github.com/jgm/pandoc/releases/download/3.11/pandoc-3.11-windows-x86_64.msi',
        '4c70230cfdca774af92084e9c4b88aad4031ca3f99a11b885d6bc755a5332cca',
        'pandoc.exe',
    ),
}


def main():
    if os.name != 'nt':
        raise SystemExit('Install LibreOffice and Pandoc using your operating system package manager.')
    root = (Path(os.environ['LOCALAPPDATA']) / 'DocAutomationSuite' / 'tools').resolve()
    root.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, (url, expected, binary) in PACKAGES.items():
        destination = (root / name).resolve()
        assert destination.is_relative_to(root)
        matches = list(destination.rglob(binary)) if destination.exists() else []
        if not matches:
            installer = root / f'{name}.msi'
            valid = installer.exists() and hashlib.sha256(installer.read_bytes()).hexdigest() == expected
            if not valid:
                print(f'Downloading {name} from vendor...', flush=True)
                digest = hashlib.sha256()
                with requests.get(url, stream=True, timeout=(30, 90)) as response:
                    response.raise_for_status()
                    with installer.open('wb') as handle:
                        downloaded = 0
                        for chunk in response.iter_content(1024 * 1024):
                            handle.write(chunk)
                            digest.update(chunk)
                            downloaded += len(chunk)
                            if downloaded % (20 * 1024 * 1024) == 0:
                                print(f'{name}: {downloaded // 1024 // 1024} MiB', flush=True)
                if digest.hexdigest() != expected:
                    raise RuntimeError(f'Checksum mismatch for {name}; package will not execute.')
            print(f'Extracting {name} into {destination}', flush=True)
            command = ['msiexec.exe', '/a', str(installer), '/qn', f'TARGETDIR={destination}', '/L*v', str(root / f'{name}-extract.log')]
            result = subprocess.run(command, timeout=600, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode not in (0, 3010):
                raise RuntimeError(f'{name} extraction failed ({result.returncode}); see {root / (name + "-extract.log")}')
            matches = list(destination.rglob(binary))
        if not matches:
            raise RuntimeError(f'{binary} not found after extraction')
        paths[name] = str(matches[0].resolve())
        print(f'{name}: {paths[name]}', flush=True)
    (root / 'renderers.json').write_text(json.dumps(paths, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
