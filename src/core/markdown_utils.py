import re

from docx.shared import Cm


class MarkdownUtils:
    HEADING_RE = re.compile(r'^(#{1,6})\s+.+$')
    BULLET_RE = re.compile(r'^\s*[-*+]\s+')
    ORDERED_RE = re.compile(r'^\s*\d+\.\s+')
    RULE_RE = re.compile(r'^\s*(---+|\*\*\*+|___+)\s*$')
    LIST_LINE_RE = re.compile(r'^(?P<indent>\s*)(?P<marker>[-*+])(?P<spacing>\s+)(?P<text>.*)$')
    UNICODE_BULLET_RE = re.compile(r'^(?P<indent>\s*)(?P<marker>[▪•●◦✓✔])\s*(?P<text>.+)$')
    INLINE_CODE_RE = re.compile(r'`([^`\n]+)`')
    SIMPLE_PROSE_CODE_RE = re.compile(r'[A-Za-z][A-Za-z0-9_]*(?:\s+[A-Za-z0-9_]+)*')
    RELATION_SCHEMA_CODE_RE = re.compile(
        r'[A-Za-z][A-Za-z0-9_]*\(\s*[A-Za-z][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z][A-Za-z0-9_]*)*\s*\)'
    )
    UNICODE_WORD_RE = re.compile(r'\b[^\W\d_]+\b', re.UNICODE)
    PROTECTED_TITLECASE_WORDS = {
        'Châu', 'Á', 'Âu', 'Mỹ', 'Hà', 'Nội', 'Việt', 'Nam',
    }

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
    def normalize_html_breaks(text, replacement=' '):
        return re.sub(r'<br\s*/?>', replacement, text, flags=re.IGNORECASE)

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
        text = re.sub(r'([,;:])\s*\.(?=(?:\s|$|[*_`)\]}>"\']))', '.', text)
        text = re.sub(r'\s+([.,;:!?)])', r'\1', text)
        text = re.sub(r'([([{])\s+', r'\1', text)
        text = re.sub(r'\s+([)\]}])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s\d.,;:!?)\]}\'"\\`*_])', r'\1 \2', text)
        return text

    @classmethod
    def normalize_inline_special_terms(cls, text):
        def replace(match):
            content = match.group(1).strip()
            if not content:
                return match.group(0)
            if cls.SIMPLE_PROSE_CODE_RE.fullmatch(content):
                prose = re.sub(r'\s+', ' ', content.replace('_', ' ')).strip()
                return f'*{prose}*'
            if cls.RELATION_SCHEMA_CODE_RE.fullmatch(content):
                prose = re.sub(r'\s+', ' ', content).strip()
                return f'*{prose}*'
            return match.group(0)

        return cls.INLINE_CODE_RE.sub(replace, text)

    @classmethod
    def normalize_report_inline_markup(cls, text):
        normalized = cls.normalize_inline_special_terms(text)
        return cls.INLINE_CODE_RE.sub(lambda match: match.group(1), normalized)

    @classmethod
    def split_report_parenthetical_clauses(cls, text):
        text = re.sub(
            r'(\([A-Za-z][A-Za-z0-9\s_-]*\))\s+([A-ZÀ-Ỹ][^\n]*)',
            lambda match: f'{match.group(1)}\n\n{match.group(2)[0].upper()}{match.group(2)[1:]}',
            text,
        )
        return re.sub(
            r'(\*\*[^*\n]*\([A-Za-z][A-Za-z0-9\s_-]*\)\*\*)\s+([A-ZÀ-Ỹ][^\n]*)',
            lambda match: f'{match.group(1)}\n\n{match.group(2)}',
            text,
        )

    @classmethod
    def normalize_report_capitalization(cls, text):
        result = []
        last_index = 0

        for match in cls.UNICODE_WORD_RE.finditer(text):
            start, end = match.span()
            word = match.group(0)
            result.append(text[last_index:start])
            result.append(cls._normalize_report_word(word, text, start, end))
            last_index = end

        result.append(text[last_index:])
        return ''.join(result)

    @classmethod
    def _normalize_report_word(cls, word, text, start, end):
        sentence_start_kind = cls._sentence_start_kind(text, start)
        if sentence_start_kind:
            if sentence_start_kind in {'punct', 'colon'} and word[:1].islower():
                return word[:1].upper() + word[1:]
            return word
        if word in cls.PROTECTED_TITLECASE_WORDS:
            return word
        if word.isupper():
            return word
        if not word[:1].isupper():
            return word
        if all(ord(char) < 128 for char in word):
            return word
        return word.lower()

    @staticmethod
    def _sentence_start_kind(text, start):
        prefix = text[:start]
        if re.search(r'\n\s*\n\s*$', prefix):
            return 'punct'
        stripped = prefix.rstrip()
        if not stripped:
            return 'structural'
        if re.fullmatch(r'(?:[-*+]\s+|\d+\.\s+)?[*_`~>#\[\]()\s]*', stripped):
            return 'structural'
        if re.fullmatch(r'(?:[-*+]\s+|\d+\.\s+)?\*\*[^*]+\*\*\s*', stripped):
            return 'structural'
        if stripped.endswith(':'):
            prefix_before_colon = stripped[:-1].rstrip()
            if re.search(r'\b\d+\s+\w+$', prefix_before_colon, re.UNICODE):
                return None
            return 'colon'
        if re.search(r'[.!?]["”’)\]]*$', stripped):
            return 'punct'
        if re.search(r':\s*[“"\'‘]$', stripped):
            return 'colon'
        return None

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
        in_code_fence = False

        def flush_paragraph():
            nonlocal paragraph_parts
            if not paragraph_parts:
                return
            paragraph = ' '.join(part.strip() for part in paragraph_parts if part.strip())
            paragraph = re.sub(r'\s+', ' ', paragraph).strip()
            if paragraph:
                paragraph = cls.split_report_parenthetical_clauses(paragraph)
                paragraph = cls.normalize_report_capitalization(paragraph)
                normalized.append(paragraph)
            paragraph_parts = []

        i = 0
        while i < len(raw_lines):
            raw_line = raw_lines[i]
            stripped = raw_line.strip()

            split_match = re.match(r'^(?P<before>.+\.)\s*(?P<number>\d+)\s+(?P<after>.+)$', stripped)
            if split_match and not cls.ORDERED_RE.match(stripped):
                flush_paragraph()
                normalized.append(split_match.group('before').strip())
                normalized.append('')
                normalized.append(f'{split_match.group("number")}. {split_match.group("after").strip()}')
                i += 1
                continue

            if stripped.startswith('```'):
                flush_paragraph()
                normalized.append(raw_line)
                in_code_fence = not in_code_fence
                i += 1
                continue

            if in_code_fence:
                normalized.append(raw_line)
                i += 1
                continue

            if not stripped:
                flush_paragraph()
                if normalized and normalized[-1] != '':
                    normalized.append('')
                i += 1
                continue

            if stripped.startswith('*   '):
                stripped = '* ' + stripped[4:].strip()

            unicode_bullet_match = cls.UNICODE_BULLET_RE.match(raw_line)
            if unicode_bullet_match:
                flush_paragraph()
                text_value = unicode_bullet_match.group('text').strip()
                indent_level = 1 if unicode_bullet_match.group('marker') in {'✓', '✔'} else 0
                if (
                    indent_level == 0
                    and normalized
                    and normalized[-1] != ''
                    and not cls.BULLET_RE.match(normalized[-1])
                    and not cls.ORDERED_RE.match(normalized[-1])
                ):
                    normalized.append('')
                trailing_number_match = re.match(r'^(?P<body>.+\.)\s*(?P<number>\d+)$', text_value)
                if trailing_number_match and i + 1 < len(raw_lines):
                    next_stripped = raw_lines[i + 1].strip()
                    if next_stripped and not cls.is_markdown_block_line(next_stripped):
                        normalized.append(f'{"  " * indent_level}- {trailing_number_match.group("body").strip()}')
                        normalized.append('')
                        normalized.append(f'{trailing_number_match.group("number")}. {next_stripped}')
                        i += 2
                        continue
                i += 1
                while i < len(raw_lines):
                    continuation = raw_lines[i].strip()
                    if not continuation:
                        break
                    if (
                        continuation.startswith('```')
                        or cls.is_markdown_block_line(continuation)
                        or cls.UNICODE_BULLET_RE.match(raw_lines[i])
                    ):
                        break
                    text_value = f'{text_value} {continuation}'
                    i += 1
                text_value = re.sub(r'\s+', ' ', text_value).strip()
                text_value = cls.normalize_report_capitalization(text_value)
                normalized.append(f'{"  " * indent_level}- {text_value}')
                continue

            trailing_number_match = re.match(r'^(?P<body>.+\.)\s*(?P<number>\d+)$', stripped)
            if trailing_number_match and i + 1 < len(raw_lines):
                next_stripped = raw_lines[i + 1].strip()
                if next_stripped and not cls.is_markdown_block_line(next_stripped):
                    flush_paragraph()
                    normalized.append(trailing_number_match.group('body').strip())
                    normalized.append('')
                    normalized.append(f'{trailing_number_match.group("number")}. {next_stripped}')
                    i += 2
                    continue

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
                i += 1
                continue

            paragraph_parts.append(stripped)
            i += 1

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
    def get_list_continuation_for_line(cls, line, list_markers_by_level=None):
        match = cls.LIST_LINE_RE.match(line.rstrip('\n'))
        if not match:
            return None

        indent = match.group('indent')
        text = match.group('text')
        indent_level = len(indent.replace('\t', '    ')) // 2
        markers = list_markers_by_level or ['-', '+', '*']
        marker = markers[indent_level] if indent_level < len(markers) else markers[-1]

        if not text.strip():
            return '\n'

        return f'\n{indent}{marker} '

    @classmethod
    def shift_list_line(cls, line, delta, list_markers_by_level=None):
        match = cls.LIST_LINE_RE.match(line.rstrip('\n'))
        if not match:
            return line

        indent = match.group('indent')
        marker = match.group('marker')
        text = match.group('text')
        markers = list_markers_by_level or ['-', '+', '*']
        indent_level = len(indent.replace('\t', '    ')) // 2
        try:
            current_level = markers.index(marker)
        except ValueError:
            current_level = indent_level
        new_level = max(0, current_level + int(delta))
        new_indent = '  ' * new_level
        marker = markers[new_level] if new_level < len(markers) else markers[-1]
        return f'{new_indent}{marker} {text}'

    @classmethod
    def canonicalize_list_line_by_indent(cls, line, list_markers_by_level=None):
        match = cls.LIST_LINE_RE.match(line.rstrip('\n'))
        if not match:
            return line

        indent = match.group('indent')
        text = match.group('text')
        markers = list_markers_by_level or ['-', '+', '*']
        indent_level = len(indent.replace('\t', '    ')) // 2
        canonical_indent = '  ' * indent_level
        marker = markers[indent_level] if indent_level < len(markers) else markers[-1]
        return f'{canonical_indent}{marker} {text}'

    @classmethod
    def reformat_markdown_document(cls, text, list_markers_by_level=None):
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = text.split('\n')
        reformatted = []
        paragraph_parts = []
        list_prefix = None
        list_parts = []
        in_code_fence = False

        def flush_paragraph():
            nonlocal paragraph_parts
            if not paragraph_parts:
                return
            paragraph = ' '.join(part.strip() for part in paragraph_parts if part.strip())
            paragraph = re.sub(r'\s+', ' ', paragraph).strip()
            if paragraph:
                paragraph = cls.normalize_inline_special_terms(paragraph)
                paragraph = cls.split_report_parenthetical_clauses(paragraph)
                paragraph = cls.normalize_report_capitalization(paragraph)
                reformatted.append(cls.normalize_punctuation(paragraph))
            paragraph_parts = []

        def flush_list_item():
            nonlocal list_prefix, list_parts
            if list_prefix is None:
                return
            item_text = ' '.join(part.strip() for part in list_parts if part.strip())
            item_text = re.sub(r'\s+', ' ', item_text).strip()
            item_text = cls.normalize_inline_special_terms(item_text)
            item_text = cls.normalize_report_capitalization(item_text)
            reformatted.append(f'{list_prefix}{cls.normalize_punctuation(item_text)}' if item_text else list_prefix.rstrip())
            list_prefix = None
            list_parts = []

        for raw_line in lines:
            line = raw_line.rstrip()
            stripped = line.strip()

            if stripped.startswith('```'):
                flush_paragraph()
                flush_list_item()
                reformatted.append(line)
                in_code_fence = not in_code_fence
                continue

            if in_code_fence:
                reformatted.append(line)
                continue

            if not stripped:
                flush_paragraph()
                flush_list_item()
                if reformatted and reformatted[-1] != '':
                    reformatted.append('')
                continue

            list_match = cls.LIST_LINE_RE.match(line)
            ordered_match = cls.ORDERED_RE.match(line)
            if list_match or ordered_match:
                flush_paragraph()
                flush_list_item()
                if list_match:
                    markers = list_markers_by_level or ['-', '+', '*']
                    indent_level = len(list_match.group('indent').replace('\t', '    ')) // 2
                    canonical_indent = '  ' * indent_level
                    marker = markers[indent_level] if indent_level < len(markers) else markers[-1]
                    list_prefix = f'{canonical_indent}{marker} '
                    list_parts = [list_match.group('text').strip()]
                else:
                    ordered_prefix, ordered_text = line.split(None, 1)
                    list_prefix = f'{ordered_prefix} '
                    list_parts = [ordered_text.strip()]
                continue

            if (
                cls.HEADING_RE.match(stripped)
                or cls.RULE_RE.match(stripped)
                or stripped.startswith('>')
                or stripped.startswith('|')
            ):
                flush_paragraph()
                flush_list_item()
                reformatted.append(stripped if cls.HEADING_RE.match(stripped) or cls.RULE_RE.match(stripped) else line)
                continue

            if list_prefix is not None:
                list_parts.append(stripped)
                continue

            paragraph_parts.append(stripped)

        flush_paragraph()
        flush_list_item()

        compact = []
        blank_run = 0
        for line in reformatted:
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
    def is_line_inside_fenced_block(text, line_number):
        lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        safe_line_number = max(1, int(line_number))
        in_code_fence = False

        for index, line in enumerate(lines, start=1):
            if line.strip().startswith('```'):
                in_code_fence = not in_code_fence
                continue
            if index == safe_line_number:
                return in_code_fence

        return False

    @classmethod
    def add_formatted_run(cls, para, text):
        text = cls.normalize_report_inline_markup(cls.strip_md_links(text))
        segments, _, _ = cls.collect_inline_segments(text)
        for token, style in segments:
            if not token:
                continue

            run = para.add_run(token)

            if style['bold']:
                run.bold = True
            if style['italic']:
                run.italic = True
