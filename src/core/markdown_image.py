import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownImage:
    alt: str
    path: str
    caption: str = ''
    width: str = '100%'
    align: str = 'center'


IMAGE_LINE_RE = re.compile(
    r'^\s*!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)\s*(?:\{(?P<meta>[^}]*)\})?\s*$'
)
META_TOKEN_RE = re.compile(r'(\w+)\s*=\s*("(?:[^"\\]|\\.)*"|[^,\s]+)')


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    return value


def parse_markdown_image_line(line: str) -> MarkdownImage | None:
    match = IMAGE_LINE_RE.match(line)
    if not match:
        return None

    alt = match.group('alt').strip()
    path = match.group('path').strip()
    meta = {'caption': '', 'width': '100%', 'align': 'center'}
    meta_text = match.group('meta') or ''
    for key, raw_value in META_TOKEN_RE.findall(meta_text):
        key_lower = key.strip().lower()
        if key_lower in meta:
            meta[key_lower] = _unquote(raw_value.strip())

    return MarkdownImage(
        alt=alt,
        path=path,
        caption=meta['caption'],
        width=meta['width'] or '100%',
        align=(meta['align'] or 'center').lower(),
    )


def build_markdown_image(path: str, *, alt: str = '', caption: str = '', width: str = '100%', align: str = 'center') -> str:
    safe_caption = caption.replace('"', '\\"')
    return f'![{alt}]({path}){{caption="{safe_caption}", width={width}, align={align}}}'
