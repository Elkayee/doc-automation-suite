import shutil
import unittest
from pathlib import Path
from types import SimpleNamespace

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

    def test_frontmatter_insert_index_places_cover_and_toc_before_chapters(self):
        window = VisualBuilderWindow.__new__(VisualBuilderWindow)

        order = ['Ch01_Intro.md', 'Ch02_Body.md']
        self.assertEqual(window._frontmatter_insert_index(order, 0), 0)
        self.assertEqual(window._frontmatter_insert_index(order, 1), 0)

        order_with_cover = ['F00_header.md', 'Ch01_Intro.md']
        self.assertEqual(window._frontmatter_insert_index(order_with_cover, 1), 1)

    def test_build_cover_frontmatter_content_uses_exam_placeholders(self):
        window = VisualBuilderWindow.__new__(VisualBuilderWindow)
        window._get_workspace_config = lambda: SimpleNamespace(type='exam')

        content = window._build_cover_frontmatter_content()

        self.assertIn('**Môn:** ...', content)
        self.assertIn('**Giảng viên:** ...', content)
        self.assertIn('**Thời gian:** Hà Nội, Tháng .../....', content)

    def test_ensure_frontmatter_file_creates_toc_once(self):
        workspace = Path('D:/doc-automation-suite/tests/_tmp_visual_frontmatter')
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)
        (workspace / 'chapters').mkdir(parents=True, exist_ok=True)

        try:
            saved_orders = []

            class FakeAssembler:
                def __init__(self):
                    self.order = ['Ch01_Intro.md']

                def get_chapter_filenames(self):
                    return list(self.order)

                def save_chapter_order(self, order):
                    self.order = list(order)
                    saved_orders.append(list(order))

            window = VisualBuilderWindow.__new__(VisualBuilderWindow)
            window.project_path = workspace
            window.assembler = FakeAssembler()
            window._known_mtimes = {}

            filename = window._ensure_frontmatter_file(1, 'toc', 'TOC', '[[TOC]]\n')
            filename_again = window._ensure_frontmatter_file(1, 'toc', 'TOC', '[[TOC]]\n')

            self.assertEqual(filename, 'F01_toc.md')
            self.assertEqual(filename_again, 'F01_toc.md')
            self.assertEqual(window.assembler.order, ['F01_toc.md', 'Ch01_Intro.md'])
            self.assertEqual((workspace / 'chapters' / 'F01_toc.md').read_text(encoding='utf-8'), '[[TOC]]\n')
            self.assertEqual(len(saved_orders), 1)
        finally:
            if workspace.exists():
                shutil.rmtree(workspace, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
