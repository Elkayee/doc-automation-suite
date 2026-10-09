import time
import tkinter as tk

import pytest
from docx import Document

from src.core.config import TemplateConfig
from src.ui.visual_builder.window import VisualBuilderWindow


def test_conversion_tools_open_as_child_without_blocking_dashboard(monkeypatch, tmp_path):
    from src.core.runtime import resource_root
    from src.ui.dashboard import DashboardApp

    monkeypatch.setenv('DOC_SUITE_DATA_DIR', str(tmp_path))
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip('No native display in this test environment')
    root.withdraw()
    try:
        app = DashboardApp(root, resource_root())
        app.open_legacy_workflow()
        children = [child for child in root.winfo_children() if isinstance(child, tk.Toplevel)]
        assert len(children) == 1
        assert 'Công cụ chuyển đổi' in children[0].title()
        assert children[0].master is root
        children[0].destroy()
    finally:
        root.destroy()


def test_chapter_selection_survives_preview_layout_and_navigator_is_readable(tmp_path):
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip('No native display in this test environment')
    root.withdraw()
    window = None
    (tmp_path / 'chapters').mkdir()
    TemplateConfig(required_files=['F00_header.md', 'Ch01_Body.md']).save(tmp_path / 'config.yaml')
    Document().save(tmp_path / 'template.docx')
    (tmp_path / 'chapters/F00_header.md').write_text('[[COVER]]\n', encoding='utf-8')
    (tmp_path / 'chapters/Ch01_Body.md').write_text('# Nội dung\n\nDòng kiểm thử.\n', encoding='utf-8')
    try:
        window = VisualBuilderWindow(root, tmp_path)
        window.geometry('1000x680')
        root.update()
        window._load_chapter_list(select_filename='Ch01_Body.md')
        deadline = time.monotonic() + 0.6
        while time.monotonic() < deadline:
            root.update()
            time.sleep(0.02)
        assert window.current_file.name == 'Ch01_Body.md'
        assert window.chapter_listbox.winfo_width() > 180
        assert window.paned.sashpos(0) >= 220
        window._pdf_is_stale = False
        before = window._edit_revision
        window._save_workspace_settings({'font_size': 13})
        assert window._pdf_is_stale and window._edit_revision > before
        window._pdf_is_stale = False
        window._load_chapter_list(select_filename='Ch01_Body.md')
        assert window._pdf_is_stale
    finally:
        if window is not None and window.winfo_exists():
            window._on_close()
        root.destroy()
