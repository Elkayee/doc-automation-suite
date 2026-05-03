import unittest

from src.core.markdown_utils import MarkdownUtils


class MarkdownListContinuationTests(unittest.TestCase):
    def test_continues_top_level_list_with_configured_marker(self):
        result = MarkdownUtils.get_list_continuation_for_line('- item', ['-', '+', '*'])
        self.assertEqual(result, '\n- ')

    def test_continues_nested_list_with_marker_for_level(self):
        result = MarkdownUtils.get_list_continuation_for_line('  - item', ['-', '+', '*'])
        self.assertEqual(result, '\n  + ')

    def test_exits_list_when_item_is_empty(self):
        result = MarkdownUtils.get_list_continuation_for_line('  + ', ['-', '+', '*'])
        self.assertEqual(result, '\n')

    def test_returns_none_for_non_list_line(self):
        result = MarkdownUtils.get_list_continuation_for_line('regular paragraph', ['-', '+', '*'])
        self.assertIsNone(result)

    def test_indent_list_line_updates_marker_for_new_level(self):
        result = MarkdownUtils.shift_list_line('  + item', 1, ['-', '+', '*'])
        self.assertEqual(result, '    * item')

    def test_indent_prefers_marker_level_when_indent_and_marker_disagree(self):
        result = MarkdownUtils.shift_list_line('  - item', 1, ['-', '+', '*'])
        self.assertEqual(result, '  + item')

    def test_outdent_list_line_updates_marker_for_new_level(self):
        result = MarkdownUtils.shift_list_line('    * item', -1, ['-', '+', '*'])
        self.assertEqual(result, '  + item')

    def test_outdent_top_level_list_line_stays_top_level(self):
        result = MarkdownUtils.shift_list_line('- item', -1, ['-', '+', '*'])
        self.assertEqual(result, '- item')

    def test_shift_non_list_line_returns_original(self):
        result = MarkdownUtils.shift_list_line('paragraph', 1, ['-', '+', '*'])
        self.assertEqual(result, 'paragraph')

    def test_indent_resets_noncanonical_spacing_to_standard(self):
        result = MarkdownUtils.shift_list_line('     + item', 0, ['-', '+', '*'])
        self.assertEqual(result, '  + item')

    def test_reformat_document_normalizes_lists_and_paragraphs(self):
        source = (
            '### Tieu de\n\n'
            'Dong van thu nhat\n'
            'dong van thu hai\n\n'
            '     + muc sai indent\n'
            '  - muc sai marker\n'
        )
        expected = (
            '### Tieu de\n\n'
            'Dong van thu nhat dong van thu hai\n\n'
            '    * muc sai indent\n'
            '  + muc sai marker\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_preserves_plantuml_fence_verbatim(self):
        source = (
            '### So do\n\n'
            '```plantuml\n'
            '@startuml\n'
            'Alice -> Bob: hello\n'
            'note right\n'
            '  - must stay raw\n'
            '  + must stay raw\n'
            'end note\n'
            '@enduml\n'
            '```\n\n'
            'Doan 1\n'
            'Doan 2\n'
        )
        expected = (
            '### So do\n\n'
            '```plantuml\n'
            '@startuml\n'
            'Alice -> Bob: hello\n'
            'note right\n'
            '  - must stay raw\n'
            '  + must stay raw\n'
            'end note\n'
            '@enduml\n'
            '```\n\n'
            'Doan 1 Doan 2\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_detects_line_inside_fenced_block(self):
        text = (
            '### So do\n\n'
            '```plantuml\n'
            '@startuml\n'
            'Alice -> Bob: hello\n'
            '```\n'
        )

        self.assertTrue(MarkdownUtils.is_line_inside_fenced_block(text, 4))
        self.assertFalse(MarkdownUtils.is_line_inside_fenced_block(text, 1))

    def test_normalize_pasted_markdown_preserves_plantuml_block(self):
        source = (
            '```plantuml\n'
            '@startuml\n'
            'Alice -> Bob: hello\n'
            'note right\n'
            '  - keep this\n'
            'end note\n'
            '@enduml\n'
            '```\n'
        )

        result = MarkdownUtils.normalize_pasted_markdown(source)

        self.assertEqual(result, source)

    def test_normalize_pasted_markdown_converts_unicode_bullets_and_wrapped_lines(self):
        source = (
            'Phan mem quan ly gui xe duoc mo ta nhu sau:\n'
            '▪ Moi bai xe co ma bai, ten bai, suc chua toi da, loai xe ho tro (xe may, o\n'
            'to), mo ta.\n'
            '▪ Phi gui xe duoc tinh theo thoi gian:\n'
            '✓ Duoi 2 gio: gia co dinh\n'
            '✓ Tren 2 gio: tinh theo gio\n'
            '▪ Neu mat ve, khach phai tra phi phat co dinh.6\n'
            'Thuc hien module.\n'
        )
        expected = (
            'Phan mem quan ly gui xe duoc mo ta nhu sau:\n\n'
            '- Moi bai xe co ma bai, ten bai, suc chua toi da, loai xe ho tro (xe may, o to), mo ta.\n'
            '- Phi gui xe duoc tinh theo thoi gian:\n'
            '  - Duoi 2 gio: gia co dinh\n'
            '  - Tren 2 gio: tinh theo gio\n'
            '- Neu mat ve, khach phai tra phi phat co dinh.\n\n'
            '6. Thuc hien module.\n'
        )

        result = MarkdownUtils.normalize_pasted_markdown(source)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
