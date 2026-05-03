import html as html_lib
import re
from html.parser import HTMLParser
from src.core.media_downloader import MediaDownloader
from src.core.markdown_utils import MarkdownUtils

class PreviewTextExtractor(HTMLParser):
    BLOCK_TAGS = {
        'p', 'div', 'section', 'article', 'header', 'footer', 'aside',
        'ul', 'ol', 'li', 'pre', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    }

    def __init__(self):
        super().__init__()
        self.parts = []
        self._cells_in_row = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'br':
            self.parts.append('\n')
        elif tag == 'tr':
            if self.parts and not self.parts[-1].endswith('\n'):
                self.parts.append('\n')
            self._cells_in_row = 0
        elif tag in {'td', 'th'}:
            if self._cells_in_row > 0:
                self.parts.append(' | ')
            self._cells_in_row += 1

    def handle_endtag(self, tag):
        if tag == 'tr':
            self._cells_in_row = 0
            self.parts.append('\n')
        elif tag in self.BLOCK_TAGS:
            self.parts.append('\n\n')

    def handle_data(self, data):
        if not data or not data.strip():
            return
        self.parts.append(re.sub(r'\s+', ' ', data))

    def get_text(self):
        text = ''.join(self.parts)
        text = text.replace('\n| ', ' | ')
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n[ \t]+', '\n', text)
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        return '\n'.join(lines)


class PreviewUtils:
    @staticmethod
    def markdown_to_html_body(md_content):
        """Chuyển Markdown sang HTML body, dùng placeholder để giữ PlantUML block."""
        from urllib.parse import quote

        lines = md_content.splitlines()
        out = []
        placeholders = {}
        idx = 0
        i = 0
        while i < len(lines):
            ln = lines[i]
            if ln.strip().startswith('```plantuml'):
                buf = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    buf.append(lines[i])
                    i += 1
                key = f'PLANTUMLBLOCK{idx}PLACEHOLDER'
                img_url = MediaDownloader.plantuml_png_url('\n'.join(buf))
                placeholders[key] = (
                    f'<p class="diagram"><img src="{quote(img_url, safe=":/?=~")}" alt="PlantUML diagram"></p>'
                )
                out.append(key)
                idx += 1
            else:
                out.append(ln)
            i += 1

        raw_md = '\n'.join(out)
        try:
            import markdown
            body = markdown.markdown(raw_md, extensions=['tables', 'fenced_code'], output_format='html')
        except ImportError:
            body = '<pre>' + html_lib.escape(raw_md) + '</pre>'

        for key, html_block in placeholders.items():
            body = body.replace('<p>' + key + '</p>', html_block)
            body = body.replace(key, html_block)
        return body

    @staticmethod
    def markdown_to_preview_text(md_content):
        body = PreviewUtils.markdown_to_html_body(md_content)
        extractor = PreviewTextExtractor()
        extractor.feed(body)
        return extractor.get_text()

    @staticmethod
    def inline_segments_to_preview_spans(text):
        spans = []
        segments, _, _ = MarkdownUtils.collect_inline_segments(text)
        for token, style in segments:
            style_names = set()
            if style['bold']:
                style_names.add('bold')
            if style['italic']:
                style_names.add('italic')
            if style['code']:
                style_names.add('code')
            spans.append((token, style_names))
        return spans

    @staticmethod
    def parse_markdown_table_row(line):
        if not line.strip().startswith('|'):
            return None
        cells = [MarkdownUtils.strip_md_markup(cell.strip()) for cell in line.strip().strip('|').split('|')]
        return cells

    @staticmethod
    def is_markdown_table_separator(line):
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        return bool(cells) and all(c and set(c) <= {'-', ':'} for c in cells)

    @classmethod
    def markdown_to_preview_blocks(cls, md_content):
        lines = md_content.splitlines()
        blocks = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            heading = re.match(r'^(#{1,6})\s+(.*)', stripped)
            if heading:
                blocks.append(
                    {
                        'type': 'heading',
                        'level': len(heading.group(1)),
                        'segments': cls.inline_segments_to_preview_spans(heading.group(2).strip()),
                    }
                )
                i += 1
                continue

            if stripped.startswith('>'):
                quote_lines = []
                while i < len(lines) and lines[i].strip().startswith('>'):
                    quote_lines.append(lines[i].strip().lstrip('> ').strip())
                    i += 1
                blocks.append(
                    {
                        'type': 'quote',
                        'segments': cls.inline_segments_to_preview_spans(' '.join(quote_lines)),
                    }
                )
                continue

            if stripped.startswith('|'):
                rows = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    row = cls.parse_markdown_table_row(lines[i])
                    if row and not cls.is_markdown_table_separator(lines[i]):
                        rows.append(row)
                    i += 1
                if rows:
                    blocks.append({'type': 'table', 'rows': rows})
                continue

            if re.match(r'^---+\s*$', stripped):
                blocks.append({'type': 'rule'})
                i += 1
                continue

            paragraph_lines = [stripped]
            i += 1
            while i < len(lines):
                candidate = lines[i].strip()
                if not candidate:
                    break
                if candidate.startswith(('>', '|', '```')) or re.match(r'^(#{1,6})\s+', candidate):
                    break
                if re.match(r'^---+\s*$', candidate):
                    break
                paragraph_lines.append(candidate)
                i += 1
            blocks.append(
                {
                    'type': 'paragraph',
                    'segments': cls.inline_segments_to_preview_spans(' '.join(paragraph_lines)),
                }
            )

        return blocks

    @staticmethod
    def configure_preview_text_tags(preview_text):
        preview_text.tag_configure('paragraph', spacing1=2, spacing3=10, lmargin1=0, lmargin2=0)
        preview_text.tag_configure('quote_block', lmargin1=18, lmargin2=18, spacing1=4, spacing3=10, foreground='#555')
        preview_text.tag_configure('table_row', lmargin1=10, lmargin2=10, spacing1=1, spacing3=1)
        preview_text.tag_configure('rule', foreground='#999', spacing1=4, spacing3=8)
        preview_text.tag_configure('bold', font=('Georgia', 10, 'bold'))
        preview_text.tag_configure('italic', font=('Georgia', 10, 'italic'))
        preview_text.tag_configure('code', font=('Consolas', 10), background='#f0f0f0', foreground='#9c2f52')
        preview_text.tag_configure('h1', font=('Georgia', 16, 'bold'), foreground='#1A3A5C', spacing1=8, spacing3=8)
        preview_text.tag_configure('h2', font=('Georgia', 14, 'bold'), foreground='#1F619E', spacing1=8, spacing3=7)
        preview_text.tag_configure('h3', font=('Georgia', 13, 'bold'), foreground='#2E86AB', spacing1=7, spacing3=6)
        preview_text.tag_configure('h4', font=('Georgia', 12, 'bold'), foreground='#449DD1', spacing1=6, spacing3=5)
        preview_text.tag_configure('h5', font=('Georgia', 11, 'bold'), foreground='#449DD1', spacing1=5, spacing3=4)
        preview_text.tag_configure('h6', font=('Georgia', 10, 'bold'), foreground='#449DD1', spacing1=4, spacing3=4)

    @staticmethod
    def insert_preview_segments(preview_text, segments, block_tags):
        for token, style_names in segments:
            tags = list(block_tags) + sorted(style_names)
            preview_text.insert('end', token, tuple(tags))

    @classmethod
    def render_markdown_to_preview_widget(cls, preview_text, md_content):
        preview_text.config(state='normal')
        preview_text.delete('1.0', 'end')

        for block in cls.markdown_to_preview_blocks(md_content):
            if block['type'] == 'heading':
                heading_tag = f'h{min(block["level"], 6)}'
                cls.insert_preview_segments(preview_text, block['segments'], [heading_tag])
                preview_text.insert('end', '\n\n')
            elif block['type'] == 'quote':
                preview_text.insert('end', '▌ ', ('quote_block',))
                cls.insert_preview_segments(preview_text, block['segments'], ['quote_block'])
                preview_text.insert('end', '\n\n')
            elif block['type'] == 'table':
                for row_index, row in enumerate(block['rows']):
                    row_text = ' | '.join(row)
                    tags = ('table_row', 'bold') if row_index == 0 else ('table_row',)
                    preview_text.insert('end', row_text, tags)
                    preview_text.insert('end', '\n')
                preview_text.insert('end', '\n')
            elif block['type'] == 'rule':
                preview_text.insert('end', '─' * 42, ('rule',))
                preview_text.insert('end', '\n\n')
            else:
                cls.insert_preview_segments(preview_text, block['segments'], ['paragraph'])
                preview_text.insert('end', '\n\n')

        preview_text.config(state='disabled')
