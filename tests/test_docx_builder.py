import unittest
from pathlib import Path
import shutil

import yaml

from src.core.docx_builder import DocxBuilder


class DocxBuilderListMarkerTests(unittest.TestCase):
    def test_build_preserves_literal_bullet_marker_from_markdown(self):
        workspace = Path('D:/doc-automation-suite/tests/_tmp_docx_builder')
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)
        workspace.mkdir(parents=True, exist_ok=True)
        try:
            config_path = workspace / 'config.yaml'
            markdown_path = workspace / 'assembled.md'
            image_cache = workspace / '.diagram_cache'

            config_path.write_text(
                yaml.safe_dump(
                    {
                        'name': 'Test',
                        'description': '',
                        'type': 'report',
                        'docx_template': 'template.docx',
                        'required_files': ['Ch01_Test.md'],
                        'settings': {
                            'chapter_settings': {
                                'Ch01_Test.md': {
                                    'list_markers_by_level': ['-', '+', '*'],
                                }
                            }
                        },
                    },
                    allow_unicode=True,
                    sort_keys=False,
                ),
                encoding='utf-8',
            )
            markdown_path.write_text(
                '<!-- FILE: Ch01_Test.md -->\n\n'
                '+ Muc cap 1\n'
                '  * Muc cap 2\n',
                encoding='utf-8',
            )

            builder = DocxBuilder(workspace)
            builder.build_from_markdown(str(markdown_path), image_cache)

            paragraph_texts = [paragraph.text for paragraph in builder.doc.paragraphs if paragraph.text.strip()]
            self.assertIn('+ Muc cap 1', paragraph_texts)
            self.assertIn('* Muc cap 2', paragraph_texts)
        finally:
            if workspace.exists():
                shutil.rmtree(workspace, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
