import re

with open('tests/test_preview_anchor_mapping.py', 'r') as f:
    content = f.read()

import_search = "from src.ui.preview_utils import PreviewUtils"
import_replace = "from unittest.mock import patch\nfrom src.ui.preview_utils import PreviewUtils"
content = content.replace(import_search, import_replace)

mock_search = """    def test_render_paginated_html_document_renders_images_and_splits_pages(self):"""
mock_replace = """    @patch('src.ui.preview_utils.PreviewUtils._resolve_preview_image_src', return_value='file:///mock.png')
    def test_render_paginated_html_document_renders_images_and_splits_pages(self, mock_resolve):"""

content = content.replace(mock_search, mock_replace)

with open('tests/test_preview_anchor_mapping.py', 'w') as f:
    f.write(content)
