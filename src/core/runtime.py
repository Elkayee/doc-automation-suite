"""Read-only application resources and writable user data."""

import os
import sys
from pathlib import Path

VERSION = '0.2.2'


def resource_root() -> Path:
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[2]))


def data_root(source_root: Path | None = None) -> Path:
    override = os.environ.get('DOC_SUITE_DATA_DIR')
    if override:
        return Path(override).expanduser().resolve()
    if getattr(sys, 'frozen', False):
        return Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'DocAutomationSuite'
    return source_root if source_root is not None else resource_root()
