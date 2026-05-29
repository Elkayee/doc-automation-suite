from unittest.mock import patch
from src.ui.preview_utils import PreviewUtils

with patch('src.ui.preview_utils.PreviewUtils._resolve_preview_image_src', return_value='file:///mock.png'):
    print("Mock applied!")
