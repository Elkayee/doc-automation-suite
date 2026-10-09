import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path

from src.core.runtime import resource_root


def find_renderer(name: str) -> Path | None:
    executable = 'soffice' if name == 'libreoffice' else 'pandoc'
    override = os.environ.get('DOC_SUITE_' + executable.upper())
    if override:
        path = Path(override).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f'{executable}: đường dẫn cấu hình không tồn tại: {path}')
        return path.resolve()
    relative = 'libreoffice/program/soffice.com' if name == 'libreoffice' else 'pandoc/Pandoc/pandoc.exe'
    bundled = resource_root() / 'tools' / relative
    if bundled.is_file():
        return bundled.resolve()
    found = shutil.which('soffice.com' if os.name == 'nt' and name == 'libreoffice' else executable)
    if found:
        return Path(found).resolve()
    manifest = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'DocAutomationSuite' / 'tools' / 'renderers.json'
    if manifest.is_file():
        path = Path(json.loads(manifest.read_text(encoding='utf-8')).get(name, ''))
        if path.is_file():
            return path.resolve()
    candidates = (
        ['C:/Program Files/LibreOffice/program/soffice.com', 'C:/Program Files (x86)/LibreOffice/program/soffice.com']
        if name == 'libreoffice'
        else ['C:/Program Files/Pandoc/pandoc.exe', str(Path(os.environ.get('LOCALAPPDATA', '')) / 'Pandoc/pandoc.exe')]
    )
    return next((Path(p) for p in candidates if Path(p).is_file()), None)


def require_renderer(name: str) -> Path:
    path = find_renderer(name)
    if path is None:
        raise RuntimeError(f'Chưa có {name}. Trên Windows, chạy python scripts/setup_renderers.py một lần.')
    return path


def run_process(command, *, cwd=None, timeout=120):
    result = subprocess.run(
        [str(arg) for arg in command],
        cwd=cwd,
        timeout=timeout,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
    )
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout or f'Renderer exit {result.returncode}')[-2000:])
    return result


def refresh_and_render_pdf(docx_path: Path, output_dir: Path) -> tuple[Path, Path]:
    # Keep per-job Writer profiles short, independent of the workspace path.
    with tempfile.TemporaryDirectory(prefix='doc-suite-lo-') as temporary:
        profile = Path(temporary).resolve()
        assert profile.parent == Path(tempfile.gettempdir()).resolve()
        return _render_with_profile(docx_path, output_dir, profile)


def _render_with_profile(docx_path: Path, output_dir: Path, profile: Path) -> tuple[Path, Path]:
    office = require_renderer('libreoffice')
    output_dir.mkdir(parents=True, exist_ok=True)
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        port = listener.getsockname()[1]
    command = [
        str(office),
        '--headless',
        '--nologo',
        '--nodefault',
        '--norestore',
        f'-env:UserInstallation={profile.resolve().as_uri()}',
        f'--accept=socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext',
    ]
    helper = Path(__file__).with_name('lo_refresh.py')
    interpreter = office.parent / 'python.exe' if os.name == 'nt' else Path('/usr/bin/python3')
    if not interpreter.is_file():
        raise RuntimeError('LibreOffice cần Python/UNO đi kèm để cập nhật mục lục trước khi xuất PDF.')
    log_path = output_dir / 'libreoffice.log'
    with log_path.open('wb') as log:
        process = subprocess.Popen(
            command, stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        try:
            deadline = time.monotonic() + 60
            while time.monotonic() < deadline:
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=0.5):
                        break
                except OSError:
                    if process.poll() is not None:
                        raise RuntimeError('LibreOffice kết thúc trước khi mở kết nối UNO')
                    time.sleep(0.2)
            else:
                raise RuntimeError('LibreOffice chưa sẵn sàng sau thời hạn khởi động')
            run_process(
                [interpreter, '-X', 'utf8', helper, str(port), docx_path.resolve(), output_dir.resolve()], timeout=180
            )
        except Exception as exc:
            log.flush()
            diagnostic = log_path.read_bytes().decode('utf-8', errors='replace')[-2000:]
            raise RuntimeError(f'{exc}\nLibreOffice process exit: {process.poll()}\n{diagnostic}') from exc
        finally:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                if os.name == 'nt':
                    subprocess.run(
                        ['taskkill.exe', '/PID', str(process.pid), '/T', '/F'],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                else:
                    process.terminate()
                process.wait(timeout=10)
    refreshed = output_dir / 'refreshed.docx'
    pdf = output_dir / 'rendered.pdf'
    if not refreshed.is_file() or not pdf.is_file():
        raise RuntimeError('Renderer không tạo đủ DOCX/PDF; bản xuất trước được giữ nguyên.')
    return refreshed, pdf


def renderer_status():
    return {name: str(path) if (path := find_renderer(name)) else None for name in ['libreoffice', 'pandoc']}
