import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from unittest.mock import MagicMock
sys.modules['docx'] = MagicMock()
sys.modules['docx.shared'] = MagicMock()
sys.modules['docx.enum'] = MagicMock()
sys.modules['docx.enum.text'] = MagicMock()
sys.modules['docx.enum.section'] = MagicMock()
sys.modules['docx.enum.table'] = MagicMock()
sys.modules['docx.oxml'] = MagicMock()
sys.modules['docx.oxml.ns'] = MagicMock()
sys.modules['requests'] = MagicMock()

from src.ui.preview_utils import PreviewUtils
from src.core.markdown_image import MarkdownImage
from types import SimpleNamespace

config = SimpleNamespace(
    settings={
        'page_height_cm': 10.0,
        'page_width_cm': 21.0,
        'margin_top_cm': 1.0,
        'margin_bottom_cm': 1.0,
        'margin_left_cm': 1.5,
        'margin_right_cm': 1.5,
        'font_size': 14,
        'line_spacing_mode': 'multiple',
        'line_spacing_value': 1.5,
    }
)
entries = [{'filename': 'Ch01_Test.md', 'path': Path('/D:/doc-automation-suite/tests/Ch01_Test.md'), 'content': '![Dang nhap](/D:/doc-automation-suite/test_extracted.png){caption="Hình 1", width=80%, align=center}\n', 'start_line': 1, 'end_line': 2}]
class DummyEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

print('is_absolute:', Path('/D:/doc-automation-suite/test_extracted.png').is_absolute())

html, anchors = PreviewUtils.render_paginated_html_document(
    [DummyEntry(**entries[0])],
    workspace_dir=Path('/D:/doc-automation-suite'),
    config=config
)
print("image-block align-center in html:", 'class="image-block align-center' in html)
print("image-missing in html:", 'class="block image-missing"' in html)
