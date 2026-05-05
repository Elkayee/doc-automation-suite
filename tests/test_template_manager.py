import shutil
import unittest
from pathlib import Path

from src.core.template_manager import TemplateManager


class TemplateManagerTests(unittest.TestCase):
    def test_exam_template_creates_editable_cover_boilerplate(self):
        dest = Path('D:/doc-automation-suite/tests/_tmp_exam_template_create')
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        try:
            manager = TemplateManager(Path('D:/doc-automation-suite/templates'))
            manager.create_project('bai_kiem_tra', dest)

            header_text = (dest / 'chapters' / 'F00_header.md').read_text(encoding='utf-8')

            self.assertIn('**Môn:** ...', header_text)
            self.assertIn('**Giảng viên:** ...', header_text)
            self.assertIn('**Thời gian:** Hà Nội, Tháng .../....', header_text)
            self.assertTrue((dest / 'assets' / 'ptit-logo.png').exists())
        finally:
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
