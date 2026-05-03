import re

from docx.shared import Cm, Pt, RGBColor


class MarkdownUtils:
    HEADING_RE = re.compile(r'^(#{1,6})\s+.+$')
    BULLET_RE = re.compile(r'^\s*[-*+]\s+')
    ORDERED_RE = re.compile(r'^\s*\d+\.\s+')
    RULE_RE = re.compile(r'^\s*(---+|\*\*\*+|___+)\s*$')

    @staticmethod
    def strip_md_links(text):
        return re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)

    @staticmethod
    def strip_md_markup(text):
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        return text

    @staticmethod
    def is_inline_word_char(char):
        return bool(char) and (char.isalnum() or char == '_')

    @classmethod
    def can_open_inline_marker(cls, text, idx, marker):
        marker_len = len(marker)
        prev_char = text[idx - 1] if idx > 0 else ''
        next_char = text[idx + marker_len] if idx + marker_len < len(text) else ''

        if not next_char or next_char.isspace():
            return False

        if marker.startswith('_') and cls.is_inline_word_char(prev_char):
            return False

        return True

    @classmethod
    def can_close_inline_marker(cls, text, idx, marker):
        marker_len = len(marker)
        prev_char = text[idx - 1] if idx > 0 else ''
        next_char = text[idx + marker_len] if idx + marker_len < len(text) else ''

        if not prev_char or prev_char.isspace():
            return False

        if marker.startswith('_') and cls.is_inline_word_char(next_char):
            return False

        return True

    @staticmethod
    def append_inline_segment(segments, text, style):
        if not text:
            return

        if segments and segments[-1][1] == style:
            segments[-1] = (segments[-1][0] + text, style)
            return

        segments.append((text, style.copy()))

    @classmethod
    def collect_inline_segments(cls, text, start=0, end_marker=None, style=None):
        if style is None:
            style = {'bold': False, 'italic': False, 'code': False}

        segments = []
        buffer = []
        i = start

        while i < len(text):
            if end_marker and text.startswith(end_marker, i) and cls.can_close_inline_marker(text, i, end_marker):
                cls.append_inline_segment(segments, ''.join(buffer), style)
                return segments, i + len(end_marker), True

            if text[i] == '`':
                close_idx = text.find('`', i + 1)
                if close_idx != -1:
                    cls.append_inline_segment(segments, ''.join(buffer), style)
                    buffer = []
                    cls.append_inline_segment(
                        segments,
                        text[i + 1 : close_idx],
                        {'bold': False, 'italic': False, 'code': True},
                    )
                    i = close_idx + 1
                    continue

            matched_marker = False
            for marker, style_key in (('**', 'bold'), ('__', 'bold'), ('*', 'italic'), ('_', 'italic')):
                if not text.startswith(marker, i):
                    continue
                if not cls.can_open_inline_marker(text, i, marker):
                    continue

                nested_style = style.copy()
                nested_style[style_key] = True
                nested_segments, new_idx, closed = cls.collect_inline_segments(
                    text,
                    start=i + len(marker),
                    end_marker=marker,
                    style=nested_style,
                )
                if not closed:
                    continue

                cls.append_inline_segment(segments, ''.join(buffer), style)
                buffer = []
                segments.extend(nested_segments)
                i = new_idx
                matched_marker = True
                break

            if matched_marker:
                continue

            buffer.append(text[i])
            i += 1

        cls.append_inline_segment(segments, ''.join(buffer), style)
        return segments, i, False

    @staticmethod
    def normalize_punctuation(text):
        text = re.sub(r'\s+([.,;:!?)])', r'\1', text)
        text = re.sub(r'([([{])\s+', r'\1', text)
        text = re.sub(r'\s+([)\]}])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s\d.,;:!?)\]}\'"\\`*_])', r'\1 \2', text)
        return text

    @classmethod
    def is_markdown_block_line(cls, text):
        stripped = text.strip()
        if not stripped:
            return True
        return bool(
            cls.HEADING_RE.match(stripped)
            or cls.BULLET_RE.match(stripped)
            or cls.ORDERED_RE.match(stripped)
            or cls.RULE_RE.match(stripped)
            or stripped.startswith('>')
            or stripped.startswith('```')
            or stripped.startswith('|')
            or re.match(r'^\*\*.+\*\*$', stripped)
        )

    @classmethod
    def normalize_pasted_markdown(cls, text):
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        raw_lines = [line.rstrip() for line in text.split('\n')]
        normalized = []
        paragraph_parts = []

        def flush_paragraph():
            nonlocal paragraph_parts
            if not paragraph_parts:
                return
            paragraph = ' '.join(part.strip() for part in paragraph_parts if part.strip())
            paragraph = re.sub(r'\s+', ' ', paragraph).strip()
            if paragraph:
                normalized.append(paragraph)
            paragraph_parts = []

        for raw_line in raw_lines:
            stripped = raw_line.strip()

            if not stripped:
                flush_paragraph()
                if normalized and normalized[-1] != '':
                    normalized.append('')
                continue

            if stripped.startswith('*   '):
                stripped = '- ' + stripped[4:].strip()
            elif re.match(r'^\*\s+', stripped):
                stripped = '- ' + stripped[2:].strip()
            elif re.match(r'^\+\s+', stripped):
                stripped = '- ' + stripped[2:].strip()

            if cls.is_markdown_block_line(stripped):
                flush_paragraph()
                if normalized and normalized[-1] != '':
                    previous = normalized[-1]
                    if (
                        cls.HEADING_RE.match(stripped)
                        or re.match(r'^\*\*.+\*\*$', stripped)
                        or cls.RULE_RE.match(stripped)
                    ) and previous != '':
                        normalized.append('')
                normalized.append(stripped)
                continue

            paragraph_parts.append(stripped)

        flush_paragraph()

        compact = []
        blank_run = 0
        for line in normalized:
            if line == '':
                blank_run += 1
                if blank_run == 1:
                    compact.append(line)
            else:
                blank_run = 0
                compact.append(line)

        result = '\n'.join(compact).strip()
        if result:
            result += '\n'
        return result

    @staticmethod
    def get_heading_indent(text):
        match = re.match(r'^\s*(\d+(?:\.\d+)+)\b', text)
        if not match:
            return None
        depth = match.group(1).count('.')
        return Cm(0.5 * depth)

    @classmethod
    def add_formatted_run(cls, para, text):
        text = cls.strip_md_links(text)
        segments, _, _ = cls.collect_inline_segments(text)
        for token, style in segments:
            if not token:
                continue

            run = para.add_run(token)
            if style['code']:
                run.font.name = 'Courier New'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0xC7, 0x25, 0x4E)
                continue

            if style['bold']:
                run.bold = True
            if style['italic']:
                run.italic = True
