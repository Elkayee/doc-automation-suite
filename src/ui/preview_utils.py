import html as html_lib
import math
import re
from html.parser import HTMLParser
from pathlib import Path

from src.core.chapter_settings import ChapterSettings
from src.core.docx_helpers import DocxHelpers
from src.core.markdown_image import MarkdownImage, parse_markdown_image_line
from src.core.markdown_utils import MarkdownUtils
from src.core.media_downloader import MediaDownloader


class PreviewTextExtractor(HTMLParser):
    BLOCK_TAGS = {
        'p',
        'div',
        'section',
        'article',
        'header',
        'footer',
        'aside',
        'ul',
        'ol',
        'li',
        'pre',
        'blockquote',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
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
    PX_PER_CM = 37.7952755906

    @staticmethod
    def _anchor_slug(filename):
        return re.sub(r'[^a-zA-Z0-9]+', '-', filename).strip('-').lower() or 'item'

    @classmethod
    def _anchor_id(cls, filename, line_number):
        return f'chapter-{cls._anchor_slug(filename)}-block-{line_number}'

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
        text = MarkdownUtils.normalize_report_inline_markup(text)
        segments, _, _ = MarkdownUtils.collect_inline_segments(text)
        for token, style in segments:
            escaped = html_lib.escape(token)
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
                        f'<span class="list-marker">{html_lib.escape(marker)}</span> '
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
        text = MarkdownUtils.normalize_report_inline_markup(text)
        segments, _, _ = MarkdownUtils.collect_inline_segments(text)
        for token, style in segments:
            style_names = set()
            if style['bold']:
                style_names.add('bold')
            if style['italic']:
                style_names.add('italic')
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
    def markdown_to_preview_blocks(cls, md_content, list_markers_by_level=None, filename=None):
        lines = md_content.splitlines()
        blocks = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()
            stripped = line.strip()
            start_line = i + 1

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
                        'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                        'line_number': start_line,
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
                        'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                        'line_number': start_line,
                    }
                )
                continue

            image = parse_markdown_image_line(stripped)
            if image:
                blocks.append(
                    {
                        'type': 'image',
                        'image': image,
                        'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                        'line_number': start_line,
                    }
                )
                i += 1
                continue

            if stripped.startswith('|'):
                rows = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    row = cls.parse_markdown_table_row(lines[i])
                    if row and not cls.is_markdown_table_separator(lines[i]):
                        rows.append(row)
                    i += 1
                if rows:
                    blocks.append(
                        {
                            'type': 'table',
                            'rows': rows,
                            'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                            'line_number': start_line,
                        }
                    )
                continue

            if re.match(r'^---+\s*$', stripped):
                blocks.append(
                    {
                        'type': 'rule',
                        'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                        'line_number': start_line,
                    }
                )
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
                        'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                        'line_number': start_line,
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
                    'anchor_id': cls._anchor_id(filename, start_line) if filename else None,
                    'line_number': start_line,
                }
            )

        return blocks

    @staticmethod
    def _page_metrics(config):
        page_settings = DocxHelpers.get_page_settings(config)
        paragraph_settings = DocxHelpers.get_paragraph_settings(config)
        page_width_px = int(float(page_settings.get('page_width_cm', 21.0)) * PreviewUtils.PX_PER_CM)
        page_height_px = int(float(page_settings.get('page_height_cm', 29.7)) * PreviewUtils.PX_PER_CM)
        margin_left_px = int(float(page_settings.get('margin_left_cm', 3.0)) * PreviewUtils.PX_PER_CM)
        margin_right_px = int(float(page_settings.get('margin_right_cm', 2.0)) * PreviewUtils.PX_PER_CM)
        margin_top_px = int(float(page_settings.get('margin_top_cm', 2.5)) * PreviewUtils.PX_PER_CM)
        margin_bottom_px = int(float(page_settings.get('margin_bottom_cm', 2.5)) * PreviewUtils.PX_PER_CM)
        content_width_px = max(320, page_width_px - margin_left_px - margin_right_px)
        content_height_px = max(320, page_height_px - margin_top_px - margin_bottom_px - 44)
        return {
            'page_width_px': page_width_px,
            'page_height_px': page_height_px,
            'margin_left_px': margin_left_px,
            'margin_right_px': margin_right_px,
            'margin_top_px': margin_top_px,
            'margin_bottom_px': margin_bottom_px,
            'content_width_px': content_width_px,
            'content_height_px': content_height_px,
            'font_size': float(paragraph_settings.get('font_size', 14)),
            'line_spacing_mode': str(paragraph_settings.get('line_spacing_mode', 'multiple')).lower(),
            'line_spacing_value': float(paragraph_settings.get('line_spacing_value', 1.5)),
        }

    @staticmethod
    def _block_plain_text(block):
        if block['type'] in {'paragraph', 'quote', 'heading', 'list_item'}:
            return ''.join(token for token, _styles in block.get('segments', []))
        if block['type'] == 'table':
            return ' '.join(' '.join(row) for row in block.get('rows', []))
        if block['type'] == 'image':
            image = block['image']
            return ' '.join(part for part in [image.alt, image.caption] if part)
        return ''

    @staticmethod
    def _line_height_px(metrics, multiplier=1.0):
        font_size = metrics['font_size']
        mode = metrics['line_spacing_mode']
        value = metrics['line_spacing_value']
        if mode == 'single':
            line_spacing = 1.0
        elif mode == 'double':
            line_spacing = 2.0
        elif mode == 'exactly':
            return max(18, value * 1.3333) * multiplier
        else:
            line_spacing = value
        return max(18, font_size * line_spacing * 1.15) * multiplier

    @classmethod
    def _estimate_image_dimensions_px(cls, image: MarkdownImage, workspace_dir: Path, md_path: Path, metrics):
        content_width_px = metrics['content_width_px']
        width_fraction = 1.0
        width_value = (image.width or '100%').strip()
        if width_value.endswith('%'):
            try:
                width_fraction = max(0.2, min(1.0, float(width_value[:-1]) / 100.0))
            except ValueError:
                width_fraction = 1.0

        target_width = max(180, int(content_width_px * width_fraction))
        resolved_path = None
        if re.match(r'^https?://', image.path, flags=re.IGNORECASE):
            return target_width, int(target_width * 0.62)
        resolved_path = DocxHelpers.resolve_media_path(workspace_dir, md_path, image.path)
        img_w, img_h = MediaDownloader.get_image_dimensions(resolved_path) if resolved_path.exists() else (None, None)
        if not img_w or not img_h:
            return target_width, int(target_width * 0.62)
        scale = target_width / float(img_w)
        return target_width, max(120, int(img_h * scale))

    @classmethod
    def _estimate_block_height(cls, block, metrics, workspace_dir: Path, md_path: Path):
        content_width_px = metrics['content_width_px']
        plain_text = cls._block_plain_text(block)
        chars_per_line = max(22, int(content_width_px / max(7, metrics['font_size'] * 0.56)))

        if block['type'] == 'heading':
            multiplier = max(1.15, 1.65 - (min(block.get('level', 2), 6) * 0.08))
            lines = max(1, math.ceil(len(plain_text) / max(14, int(chars_per_line * 0.78))))
            return int((cls._line_height_px(metrics, multiplier) * lines) + 18)
        if block['type'] == 'paragraph':
            lines = max(1, math.ceil(len(plain_text) / chars_per_line))
            return int((cls._line_height_px(metrics) * lines) + 14)
        if block['type'] == 'quote':
            lines = max(1, math.ceil(len(plain_text) / max(18, int(chars_per_line * 0.92))))
            return int((cls._line_height_px(metrics) * lines) + 18)
        if block['type'] == 'list_item':
            lines = max(1, math.ceil(len(plain_text) / max(18, chars_per_line - (block.get('indent_level', 0) * 6))))
            return int((cls._line_height_px(metrics) * lines) + 8)
        if block['type'] == 'table':
            total = 16
            for row in block.get('rows', []):
                longest = max((len(cell) for cell in row), default=0)
                row_lines = max(1, math.ceil(longest / max(10, int(chars_per_line / max(1, len(row))))))
                total += int((cls._line_height_px(metrics, 0.92) * row_lines) + 16)
            return total
        if block['type'] == 'image':
            _display_width, display_height = cls._estimate_image_dimensions_px(
                block['image'], workspace_dir, md_path, metrics
            )
            caption_height = int(cls._line_height_px(metrics, 0.9) + 8) if block['image'].caption else 0
            return display_height + caption_height + 24
        return 20

    @classmethod
    def _resolve_preview_image_src(cls, workspace_dir: Path, md_path: Path, image: MarkdownImage) -> str:
        if re.match(r'^https?://', image.path, flags=re.IGNORECASE):
            return image.path
        resolved = DocxHelpers.resolve_media_path(workspace_dir, md_path, image.path)
        if resolved.exists():
            return resolved.resolve().as_uri()
        return ''

    @classmethod
    def _render_block_html(cls, block, workspace_dir: Path, md_path: Path, metrics):
        anchor_attr = f' id="{block["anchor_id"]}"' if block.get('anchor_id') else ''
        if block['type'] == 'heading':
            level = min(block.get('level', 2), 6)
            return f'<div class="block heading-block"{anchor_attr}><h{level}>{cls._segments_html(block["segments"])}</h{level}></div>'
        if block['type'] == 'paragraph':
            return (
                f'<div class="block paragraph-block"{anchor_attr}><p>{cls._segments_html(block["segments"])}</p></div>'
            )
        if block['type'] == 'quote':
            return f'<div class="block quote-block"{anchor_attr}><blockquote>{cls._segments_html(block["segments"])}</blockquote></div>'
        if block['type'] == 'list_item':
            indent_level = block.get('indent_level', 0)
            marker = html_lib.escape(block.get('marker', '-'))
            return (
                f'<div class="block custom-list-block"{anchor_attr}>'
                f'<div class="custom-list-item level-{indent_level}">'
                f'<span class="list-marker">{marker}</span> '
                f'<span class="list-text">{cls._segments_html(block["segments"])}</span>'
                '</div></div>'
            )
        if block['type'] == 'table':
            rows_html = []
            for row_index, row in enumerate(block.get('rows', [])):
                tag = 'th' if row_index == 0 else 'td'
                cells = ''.join(f'<{tag}>{html_lib.escape(cell)}</{tag}>' for cell in row)
                rows_html.append(f'<tr>{cells}</tr>')
            return f'<div class="block table-block"{anchor_attr}><table>{"".join(rows_html)}</table></div>'
        if block['type'] == 'image':
            image = block['image']
            src = cls._resolve_preview_image_src(workspace_dir, md_path, image)
            if not src:
                return (
                    f'<div class="block image-missing"{anchor_attr}>'
                    f'<p>[Khong tim thay anh: {html_lib.escape(image.path)}]</p></div>'
                )
            width_style = f'width:{html_lib.escape(image.width or "100%")};'
            caption_html = f'<figcaption>{html_lib.escape(image.caption)}</figcaption>' if image.caption else ''
            return (
                f'<figure class="image-block align-{html_lib.escape(image.align or "center")} block"{anchor_attr}>'
                f'<img src="{html_lib.escape(src)}" alt="{html_lib.escape(image.alt)}" style="{width_style}">'
                f'{caption_html}</figure>'
            )
        return f'<div class="block rule-block"{anchor_attr}><hr></div>'

    @classmethod
    def _segments_html(cls, segments):
        parts = []
        for token, styles in segments:
            escaped = html_lib.escape(token)
            if 'bold' in styles:
                escaped = f'<strong>{escaped}</strong>'
            if 'italic' in styles:
                escaped = f'<em>{escaped}</em>'
            parts.append(escaped)
        return ''.join(parts)

    @classmethod
    def render_paginated_html_document(cls, entries, workspace_dir: Path, config, css_text=''):
        metrics = cls._page_metrics(config)
        anchors_by_file = {}
        page_sections = []
        current_blocks = []
        remaining_height = metrics['content_height_px']
        page_number = 1

        def flush_page():
            nonlocal current_blocks, remaining_height, page_number
            if not current_blocks:
                return
            page_sections.append(
                f'<section class="page" data-page-label="Page {page_number}">{"".join(current_blocks)}</section>'
            )
            page_number += 1
            current_blocks = []
            remaining_height = metrics['content_height_px']

        for entry in entries:
            markers = ChapterSettings.get_list_markers_by_level(config, entry.filename)
            blocks = cls.markdown_to_preview_blocks(
                entry.content, list_markers_by_level=markers, filename=entry.filename
            )
            anchors_by_file[entry.filename] = [
                {'anchor_id': block['anchor_id'], 'line_number': block['line_number']}
                for block in blocks
                if block.get('anchor_id')
            ]
            for block in blocks:
                block_height = cls._estimate_block_height(block, metrics, workspace_dir, entry.path)
                block_html = cls._render_block_html(block, workspace_dir, entry.path, metrics)
                if current_blocks and block_height > remaining_height:
                    flush_page()
                current_blocks.append(block_html)
                remaining_height -= block_height

        flush_page()

        if not page_sections:
            page_sections = ['<section class="empty-state">No chapter content available.</section>']

        dynamic_css = (
            ':root{'
            f'--page-width:{metrics["page_width_px"]}px;'
            f'--page-height:{metrics["page_height_px"]}px;'
            f'--page-padding-top:{metrics["margin_top_px"]}px;'
            f'--page-padding-right:{metrics["margin_right_px"]}px;'
            f'--page-padding-bottom:{metrics["margin_bottom_px"]}px;'
            f'--page-padding-left:{metrics["margin_left_px"]}px;'
            f'--body-font-size:{metrics["font_size"]}px;'
            '}'
        )
        html = (
            '<!DOCTYPE html><html><head><meta charset="utf-8">'
            f'<style>{dynamic_css}{css_text}</style></head><body><div class="document-shell">'
            + ''.join(page_sections)
            + '</div></body></html>'
        )
        return html, anchors_by_file

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
            elif block['type'] == 'image':
                image = block['image']
                preview_text.insert('end', f'[Image] {image.alt or image.path}', ('paragraph',))
                if image.caption:
                    preview_text.insert('end', f'\n{image.caption}', ('italic', 'paragraph'))
                preview_text.insert('end', '\n\n')
            elif block['type'] == 'rule':
                preview_text.insert('end', '-' * 42, ('rule',))
                preview_text.insert('end', '\n\n')
            else:
                cls.insert_preview_segments(preview_text, block['segments'], ['paragraph'])
                preview_text.insert('end', '\n\n')

        preview_text.config(state='disabled')
