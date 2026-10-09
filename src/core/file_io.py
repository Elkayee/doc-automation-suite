import hashlib
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path


def atomic_write(path: Path, content: str | bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode('utf-8') if isinstance(content, str) else content
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def file_hash(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


class ExternalEditError(RuntimeError):
    pass


def save_chapter(path: Path, content: str, expected_hash: str | None) -> str:
    current_hash = file_hash(path)
    recovery_dir = path.parent.parent / '.recovery'
    atomic_write(recovery_dir / 'drafts' / path.name, content)
    if current_hash != expected_hash:
        raise ExternalEditError(f'{path.name} đã thay đổi bên ngoài. Bản đang soạn được giữ trong .recovery/drafts.')
    if path.is_file():
        previous = path.read_bytes()
        atomic_write(recovery_dir / 'previous' / path.name, previous)
        history = recovery_dir / 'history' / path.name / f'{time.time_ns()}.md'
        atomic_write(history, previous)
    atomic_write(path, content)
    return file_hash(path)


@contextmanager
def export_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        if path.stat().st_size == 0:
            handle.write(b'\0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeError('Dự án đang được xuất bởi tác vụ khác. Hãy chờ tác vụ đó hoàn thành.') from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)
