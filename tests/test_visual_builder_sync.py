import unittest
from pathlib import Path

from src.core.assembler import ChapterAssemblyEntry
from src.ui.visual_builder.window import VisualBuilderWindow


class VisualBuilderSyncTests(unittest.TestCase):
    def test_global_line_uses_current_file_offset(self):
        entries = [
            ChapterAssemblyEntry(
                filename='Ch01_Intro.md',
                path=Path('Ch01_Intro.md'),
                content='a\nb\nc',
                start_line=1,
                end_line=3,
            ),
            ChapterAssemblyEntry(
                filename='Ch02_Body.md',
                path=Path('Ch02_Body.md'),
                content='d\ne\nf\ng',
                start_line=5,
                end_line=8,
            ),
        ]

        global_line = VisualBuilderWindow._compute_global_line_for_file(entries, 'Ch02_Body.md', 3)

        self.assertEqual(global_line, 7)

    def test_scroll_fraction_tracks_global_line_in_document(self):
        entries = [
            ChapterAssemblyEntry(
                filename='Ch01_Intro.md',
                path=Path('Ch01_Intro.md'),
                content='a\nb\nc',
                start_line=1,
                end_line=3,
            ),
            ChapterAssemblyEntry(
                filename='Ch02_Body.md',
                path=Path('Ch02_Body.md'),
                content='d\ne\nf\ng',
                start_line=5,
                end_line=8,
            ),
        ]

        fraction = VisualBuilderWindow._compute_preview_scroll_fraction(entries, 7)

        self.assertAlmostEqual(fraction, 6 / 8)

    def test_scroll_fraction_is_zero_without_entries(self):
        fraction = VisualBuilderWindow._compute_preview_scroll_fraction([], 1)
        self.assertEqual(fraction, 0.0)

    def test_global_line_can_be_derived_back_from_fraction(self):
        entries = [
            ChapterAssemblyEntry(
                filename='Ch01_Intro.md',
                path=Path('Ch01_Intro.md'),
                content='a\nb\nc',
                start_line=1,
                end_line=3,
            ),
            ChapterAssemblyEntry(
                filename='Ch02_Body.md',
                path=Path('Ch02_Body.md'),
                content='d\ne\nf\ng',
                start_line=5,
                end_line=8,
            ),
        ]

        global_line = VisualBuilderWindow._compute_global_line_from_preview_fraction(entries, 0.75)

        self.assertEqual(global_line, 7)

    def test_global_line_resolves_to_file_and_local_line(self):
        entries = [
            ChapterAssemblyEntry(
                filename='Ch01_Intro.md',
                path=Path('Ch01_Intro.md'),
                content='a\nb\nc',
                start_line=1,
                end_line=3,
            ),
            ChapterAssemblyEntry(
                filename='Ch02_Body.md',
                path=Path('Ch02_Body.md'),
                content='d\ne\nf\ng',
                start_line=5,
                end_line=8,
            ),
        ]

        filename, local_line = VisualBuilderWindow._resolve_file_line_from_global_line(entries, 7)

        self.assertEqual(filename, 'Ch02_Body.md')
        self.assertEqual(local_line, 3)


if __name__ == '__main__':
    unittest.main()
