import unittest
from types import SimpleNamespace

from src.core.chapter_settings import ChapterSettings


class ChapterListMarkerTests(unittest.TestCase):
    def test_uses_default_markers_when_file_has_no_override(self):
        config = SimpleNamespace(settings={})

        self.assertEqual(ChapterSettings.get_list_markers_by_level(config, 'Ch01_Test.md'), ['-', '+', '*'])
        self.assertEqual(ChapterSettings.get_list_marker(config, 'Ch01_Test.md', 2), '+')

    def test_reads_per_file_marker_override(self):
        config = SimpleNamespace(
            settings={
                'chapter_settings': {
                    'Ch01_Test.md': {
                        'list_markers_by_level': ['>', 'o', '~'],
                    }
                }
            }
        )

        self.assertEqual(ChapterSettings.get_list_marker(config, 'Ch01_Test.md', 1), '>')
        self.assertEqual(ChapterSettings.get_list_marker(config, 'Ch01_Test.md', 2), 'o')
        self.assertEqual(ChapterSettings.get_list_marker(config, 'Ch01_Test.md', 4), '~')

    def test_normalizes_blank_or_invalid_markers(self):
        config = SimpleNamespace(
            settings={
                'chapter_settings': {
                    'Ch01_Test.md': {
                        'list_markers_by_level': ['-', '', None, '  +  '],
                    }
                }
            }
        )

        self.assertEqual(ChapterSettings.get_list_markers_by_level(config, 'Ch01_Test.md'), ['-', '+', '*', '+'])


if __name__ == '__main__':
    unittest.main()
