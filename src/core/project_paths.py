from pathlib import Path


def workspace_path(base: Path, name: str) -> Path:
    target = (base / name).resolve()
    if not name.strip() or target == base.resolve() or not target.is_relative_to(base.resolve()):
        raise ValueError('Tên/đường dẫn dự án phải nằm trong workspaces')
    return target
