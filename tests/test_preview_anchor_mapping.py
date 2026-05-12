import unittest
from pathlib import Path
from types import SimpleNamespace

from src.core.assembler import ChapterAssemblyEntry
from src.ui.preview_utils import PreviewUtils


class PreviewAnchorMappingTests(unittest.TestCase):
    def test_inject_block_anchors_tracks_heading_and_paragraph(self):
        markdown = '### Cau 1\n\nDoan mot\nvan tiep\n\n### Tra loi\n\nNoi dung\n'

        anchored_md, anchors = PreviewUtils.inject_block_anchors(markdown, 'Ch01_Test.md')

        self.assertIn('<div id="chapter-ch01-test-md-block-1"></div>', anchored_md)
        self.assertIn('<div id="chapter-ch01-test-md-block-3"></div>', anchored_md)
        self.assertEqual(anchors[0]['line_number'], 1)
        self.assertEqual(anchors[1]['line_number'], 3)
        self.assertEqual(anchors[2]['line_number'], 6)

    def test_find_anchor_for_line_returns_nearest_preceding_block(self):
        markdown = '### Cau 1\n\nDoan mot\nvan tiep\n\n### Tra loi\n\nNoi dung\n'
        _anchored_md, anchors = PreviewUtils.inject_block_anchors(markdown, 'Ch01_Test.md')

        anchor_id = PreviewUtils.find_anchor_for_line(anchors, 7)

        self.assertEqual(anchor_id, 'chapter-ch01-test-md-block-6')

    def test_preview_blocks_keep_nested_list_items_and_custom_markers(self):
        markdown = '- parent\n  - child\n    - grandchild\n'

        blocks = PreviewUtils.markdown_to_preview_blocks(markdown, list_markers_by_level=['-', '+', '*'])

        self.assertEqual(blocks[0]['type'], 'list_item')
        self.assertEqual(blocks[0]['marker'], '-')
        self.assertEqual(blocks[0]['indent_level'], 0)
        self.assertEqual(blocks[1]['marker'], '+')
        self.assertEqual(blocks[1]['indent_level'], 1)
        self.assertEqual(blocks[2]['marker'], '*')
        self.assertEqual(blocks[2]['indent_level'], 2)

    def test_parse_markdown_table_row_removes_html_break_tags(self):
        row = PreviewUtils.parse_markdown_table_row('| A<br>B | C<br/>D | E<br />F |')

        self.assertEqual(row, ['A B', 'C D', 'E F'])

    def test_markdown_to_html_body_with_markers_keeps_space_after_list_marker(self):
        html = PreviewUtils.markdown_to_html_body_with_markers('- **Muc**\n', list_markers_by_level=['-', '+', '*'])

        self.assertIn('<span class="list-marker">-</span> <span class="list-text">', html)

    def test_render_paginated_html_document_renders_images_and_splits_pages(self):
        import struct
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            workspace_dir = Path(td)
            md_file = workspace_dir / "tests" / "Ch01_Test.md"
            img_file = workspace_dir / "test_extracted.png"

            md_file.parent.mkdir(parents=True, exist_ok=True)
            md_file.write_text("dummy", encoding='utf-8')

            with open(img_file, "wb") as f:
                f.write(struct.pack('>8B', 137, 80, 78, 71, 13, 10, 26, 10))
                f.write(struct.pack('>I', 13))
                f.write(b'IHDR')
                f.write(struct.pack('>I', 100))
                f.write(struct.pack('>I', 100))
                f.write(struct.pack('>5B', 8, 2, 0, 0, 0))

            img_path_str = str(img_file).replace('\\', '/')

            entries = [
                ChapterAssemblyEntry(
                    filename='Ch01_Test.md',
                    path=md_file,
                    content=(
                        '### Tieu de\n\n'
                        'Doan van mo dau rat dai. ' * 40
                        + '\n\n'
                        f'![Dang nhap]({img_path_str}){{caption="Hình 1", width=80%, align=center}}\n\n'
                        + ('Them noi dung de tach trang.\n\n' * 30)
                    ),
                    start_line=1,
                    end_line=70,
                )
            ]
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

            html, anchors = PreviewUtils.render_paginated_html_document(
                entries,
                workspace_dir=workspace_dir,
                config=config,
            )

            self.assertGreater(html.count('<section class="page"'), 1)
            self.assertIn('class="image-block align-center', html)
            self.assertIn('Hình 1', html)
            self.assertIn('chapter-ch01-test-md-block-', html)
            self.assertIn('Ch01_Test.md', anchors)


if __name__ == '__main__':
    unittest.main()
