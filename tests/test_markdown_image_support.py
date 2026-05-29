import unittest

from src.core.markdown_image import MarkdownImage, build_markdown_image, parse_markdown_image_line


class MarkdownImageSupportTests(unittest.TestCase):
    def test_parse_extended_markdown_image_line(self):
        image = parse_markdown_image_line(
            '![Dang nhap](assets/images/login.png){caption="Hình 4.1. Giao diện", width=85%, align=center}'
        )

        self.assertEqual(
            image,
            MarkdownImage(
                alt='Dang nhap',
                path='assets/images/login.png',
                caption='Hình 4.1. Giao diện',
                width='85%',
                align='center',
            ),
        )

    def test_build_markdown_image_round_trips_with_defaults(self):
        markdown = build_markdown_image('assets/images/login.png', alt='Dang nhap', caption='', width='100%', align='center')
        image = parse_markdown_image_line(markdown)

        self.assertEqual(image.alt, 'Dang nhap')
        self.assertEqual(image.path, 'assets/images/login.png')
        self.assertEqual(image.caption, '')
        self.assertEqual(image.width, '100%')
        self.assertEqual(image.align, 'center')


if __name__ == '__main__':
    unittest.main()
