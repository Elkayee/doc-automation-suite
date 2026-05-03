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
    def _anchor_slug(filename):
        return re.sub(r'[^a-zA-Z0-9]+', '-', filename).strip('-').lower() or 'item'

    @classmethod
    def inject_block_anchors(cls, md_content, filename):
        lines = md_content.splitlines()
        anchored_lines = []
        anchors = []
        in_code_fence = False
        previous_blank = True
        slug = cls._anchor_slug(filename)

        for index, raw_line in enumerate(lines, start=1):
            stripped = raw_line.strip()
            if stripped.startswith('```'):
                if not in_code_fence:
                    anchor_id = f'chapter-{slug}-block-{index}'
                    anchored_lines.append(f'<div id="{anchor_id}"></div>')
                    anchors.append({'anchor_id': anchor_id, 'line_number': index})
                in_code_fence = not in_code_fence
                anchored_lines.append(raw_line)
                previous_blank = False
                continue

            if in_code_fence:
                anchored_lines.append(raw_line)
                previous_blank = False
                continue

            is_block_start = False
            if stripped:
                if re.match(r'^(#{1,6})\s+', stripped):
                    is_block_start = True
                elif re.match(r'^[-*+]\s+', stripped):
                    is_block_start = previous_blank
                elif re.match(r'^\d+[.)]\s+', stripped):
                    is_block_start = previous_blank
                elif stripped.startswith(('>', '|')):
                    is_block_start = previous_blank
                elif re.match(r'^---+\s*$', stripped):
                    is_block_start = True
                elif previous_blank:
                    is_block_start = True

            if is_block_start:
                anchor_id = f'chapter-{slug}-block-{index}'
                anchored_lines.append(f'<div id="{anchor_id}"></div>')
                anchors.append({'anchor_id': anchor_id, 'line_number': index})

            anchored_lines.append(raw_line)
            previous_blank = not stripped

        anchored_md = '\n'.join(anchored_lines)
        if md_content.endswith('\n'):
            anchored_md += '\n'
        return anchored_md, anchors

    @staticmethod
    def find_anchor_for_line(anchors, line_number):
        if not anchors:
            return None

        target_line = max(1, int(line_number))
        selected_anchor = anchors[0]['anchor_id']
        for anchor in anchors:
            if anchor['line_number'] > target_line:
                break
            selected_anchor = anchor['anchor_id']
        return selected_anchor

    @staticmethod
    def markdown_to_html_body(md_content):
        return PreviewUtils.markdown_to_html_body_with_markers(md_content)

    @staticmethod
    def inline_segments_to_html(text):
        html_parts = []
        segments, _, _ = MarkdownUtils.collect_inline_segments(text)
        for token, style in segments:
            escaped = html_lib.escape(token)
            if style['code']:
                html_parts.append(f'<code>{escaped}</code>')
                continue
            if style['bold']:
                escaped = f'<strong>{escaped}</strong>'
            if style['italic']:
                escaped = f'<em>{escaped}</em>'
            html_parts.append(escaped)
        return ''.join(html_parts)

    @staticmethod
    def markdown_to_html_body_with_markers(md_content, list_markers_by_level=None):
        from urllib.parse import quote

        lines = md_content.splitlines()
        out = []
        placeholders = {}
        idx = 0
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith('```plantuml'):
                buffer = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    buffer.append(lines[i])
                    i += 1
                key = f'PLANTUMLBLOCK{idx}PLACEHOLDER'
                image_url = MediaDownloader.plantuml_png_url('\n'.join(buffer))
                placeholders[key] = (
                    f'<p class="diagram"><img src="{quote(image_url, safe=":/?=~")}" alt="PlantUML diagram"></p>'
                )
                out.append(key)
                idx += 1
            elif re.match(r'^\s*[-*+]\s+', line):
                list_items = []
                while i < len(lines) and re.match(r'^\s*[-*+]\s+', lines[i]):
                    list_match = re.match(r'^(?P<indent>\s*)[-*+]\s+(?P<text>.*)', lines[i])
                    indent_level = len(list_match.group('indent').replace('\t', '    ')) // 2
                    marker = PreviewUtils._list_marker_for_level(list_markers_by_level, indent_level)
                    text_html = PreviewUtils.inline_segments_to_html(list_match.group('text').strip())
                    list_items.append(
                        f'<div class="custom-list-item level-{indent_level}">'
                        f'<span class="list-marker">{html_lib.escape(marker)}</span>'
                        f'<span class="list-text">{text_html}</span>'
                        '</div>'
                    )
                    i += 1
                key = f'LISTBLOCK{idx}PLACEHOLDER'
                placeholders[key] = '<div class="custom-list-block">' + ''.join(list_items) + '</div>'
                out.append(key)
                idx += 1
                continue
            else:
                out.append(line)
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
    def markdown_to_preview_text(md_content, list_markers_by_level=None):
        body = PreviewUtils.markdown_to_html_body_with_markers(md_content, list_markers_by_level=list_markers_by_level)
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
        cells = [
            MarkdownUtils.strip_md_markup(MarkdownUtils.normalize_html_breaks(cell.strip(), ' '))
            for cell in line.strip().strip('|').split('|')
        ]
        return cells

    @staticmethod
    def is_markdown_table_separator(line):
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        return bool(cells) and all(cell and set(cell) <= {'-', ':'} for cell in cells)

    @staticmethod
    def _list_marker_for_level(list_markers_by_level, indent_level):
        markers = list_markers_by_level or ['-', '+', '*']
        safe_index = max(0, indent_level)
        if safe_index < len(markers):
            return markers[safe_index]
        return markers[-1]

    @classmethod
    def markdown_to_preview_blocks(cls, md_content, list_markers_by_level=None):
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

            list_match = re.match(r'^(?P<indent>\s*)[-*+]\s+(?P<text>.*)', line)
            if list_match:
                indent_level = len(list_match.group('indent').replace('\t', '    ')) // 2
                blocks.append(
                    {
                        'type': 'list_item',
                        'indent_level': indent_level,
                        'marker': cls._list_marker_for_level(list_markers_by_level, indent_level),
                        'segments': cls.inline_segments_to_preview_spans(list_match.group('text').strip()),
                    }
                )
                i += 1
                continue

            paragraph_lines = [stripped]
            i += 1
            while i < len(lines):
                candidate_line = lines[i]
                candidate = candidate_line.strip()
                if not candidate:
                    break
                if candidate.startswith(('>', '|', '```')) or re.match(r'^(#{1,6})\s+', candidate):
                    break
                if re.match(r'^---+\s*$', candidate):
                    break
                if re.match(r'^\s*[-*+]\s+', candidate_line):
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
        preview_text.tag_configure('list_item', spacing1=1, spacing3=4, lmargin1=24, lmargin2=24)
        preview_text.tag_configure('quote_block', lmargin1=18, lmargin2=18, spacing1=4, spacing3=10, foreground='#000')
        preview_text.tag_configure('table_row', lmargin1=10, lmargin2=10, spacing1=1, spacing3=1)
        preview_text.tag_configure('rule', foreground='#000', spacing1=4, spacing3=8)
        preview_text.tag_configure('bold', font=('Georgia', 10, 'bold'))
        preview_text.tag_configure('italic', font=('Georgia', 10, 'italic'))
        preview_text.tag_configure('code', font=('Consolas', 10), background='#f0f0f0', foreground='#000')
        preview_text.tag_configure('h1', font=('Georgia', 16, 'bold'), foreground='#000', spacing1=8, spacing3=8)
        preview_text.tag_configure('h2', font=('Georgia', 14, 'bold'), foreground='#000', spacing1=8, spacing3=7)
        preview_text.tag_configure('h3', font=('Georgia', 13, 'bold'), foreground='#000', spacing1=7, spacing3=6)
        preview_text.tag_configure('h4', font=('Georgia', 12, 'bold'), foreground='#000', spacing1=6, spacing3=5)
        preview_text.tag_configure('h5', font=('Georgia', 11, 'bold'), foreground='#000', spacing1=5, spacing3=4)
        preview_text.tag_configure('h6', font=('Georgia', 10, 'bold'), foreground='#000', spacing1=4, spacing3=4)

    @staticmethod
    def insert_preview_segments(preview_text, segments, block_tags):
        for token, style_names in segments:
            tags = list(block_tags) + sorted(style_names)
            preview_text.insert('end', token, tuple(tags))

    @classmethod
    def render_markdown_to_preview_widget(cls, preview_text, md_content, list_markers_by_level=None, append=False):
        preview_text.config(state='normal')
        if not append:
            preview_text.delete('1.0', 'end')

        for block in cls.markdown_to_preview_blocks(md_content, list_markers_by_level=list_markers_by_level):
            if block['type'] == 'heading':
                heading_tag = f'h{min(block["level"], 6)}'
                cls.insert_preview_segments(preview_text, block['segments'], [heading_tag])
                preview_text.insert('end', '\n\n')
            elif block['type'] == 'list_item':
                indent = '    ' * block['indent_level']
                preview_text.insert('end', f'{indent}{block["marker"]} ', ('list_item',))
                cls.insert_preview_segments(preview_text, block['segments'], ['list_item'])
                preview_text.insert('end', '\n')
            elif block['type'] == 'quote':
                preview_text.insert('end', '| ', ('quote_block',))
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
                preview_text.insert('end', '-' * 42, ('rule',))
                preview_text.insert('end', '\n\n')
            else:
                cls.insert_preview_segments(preview_text, block['segments'], ['paragraph'])
                preview_text.insert('end', '\n\n')

        preview_text.config(state='disabled')
