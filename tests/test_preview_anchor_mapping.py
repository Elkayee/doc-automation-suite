import unittest

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


if __name__ == '__main__':
    unittest.main()
