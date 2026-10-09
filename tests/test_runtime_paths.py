import sys
from pathlib import Path

from src.core import renderers, runtime


def test_source_keeps_existing_data_directory(monkeypatch, tmp_path):
    monkeypatch.delenv('DOC_SUITE_DATA_DIR', raising=False)
    monkeypatch.delattr(sys, 'frozen', raising=False)
    assert runtime.data_root(tmp_path) == tmp_path


def test_frozen_resources_never_receive_user_projects(monkeypatch, tmp_path):
    resources, profile = tmp_path / 'installation', tmp_path / 'profile'
    monkeypatch.setattr(sys, 'frozen', True, raising=False)
    monkeypatch.setattr(sys, '_MEIPASS', str(resources), raising=False)
    monkeypatch.setenv('LOCALAPPDATA', str(profile))
    monkeypatch.delenv('DOC_SUITE_DATA_DIR', raising=False)
    assert runtime.resource_root() == resources
    assert runtime.data_root() == profile / 'DocAutomationSuite'
    assert not resources.exists()


def test_explicit_data_directory_works_with_unicode_and_spaces(monkeypatch, tmp_path):
    target = tmp_path / 'Báo cáo mẫu'
    monkeypatch.setenv('DOC_SUITE_DATA_DIR', str(target))
    assert runtime.data_root() == target.resolve()


def test_bundled_renderer_is_preferred_to_machine_installation(monkeypatch, tmp_path):
    bundled = tmp_path / 'tools/pandoc/Pandoc/pandoc.exe'
    bundled.parent.mkdir(parents=True)
    bundled.write_bytes(b'verified fixture')
    monkeypatch.delenv('DOC_SUITE_PANDOC', raising=False)
    monkeypatch.setattr(renderers, 'resource_root', lambda: tmp_path)
    monkeypatch.setattr(renderers.shutil, 'which', lambda _name: str(Path('unrelated-machine/pandoc.exe')))
    assert renderers.find_renderer('pandoc') == bundled.resolve()
