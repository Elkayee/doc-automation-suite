import re

INLINE_MATH_RE = re.compile(r'(?<!\\)\$(?![\s$])([^$\n]*\S)\$(?!\d)')
CITATION_RE = re.compile(r'(?<!\\)\[(?:[^\]\n]*\s)?-?@[A-Za-z0-9_][^\]\n]*\]')
CODE_SPAN_RE = re.compile(r'(`+)(.*?)\1')


def content_lines(markdown):
    fence = None
    for line in markdown.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            yield line


def text_parts(text):
    position = 0
    for match in CODE_SPAN_RE.finditer(text):
        yield False, text[position:match.start()]
        yield True, match.group(0)
        position = match.end()
    yield False, text[position:]


def has_academic_markup(markdown):
    return any(CITATION_RE.search(part) or INLINE_MATH_RE.search(part) or line.strip().startswith('$$')
               for line in content_lines(markdown) for code, part in text_parts(line) if not code)
