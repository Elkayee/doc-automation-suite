import hashlib
import json
from copy import deepcopy
from pathlib import Path

from docx import Document

from src.core.file_io import atomic_write
from src.core.markdown_semantics import CITATION_RE, INLINE_MATH_RE, content_lines, text_parts
from src.core.renderers import require_renderer, run_process


def inline_text(nodes):
    parts = []
    for node in nodes:
        kind, value = node['t'], node.get('c')
        if kind == 'Str':
            parts.append(value)
        elif kind in {'Space', 'SoftBreak', 'LineBreak'}:
            parts.append(' ')
        elif kind in {'Emph', 'Strong'}:
            marker = '*' if kind == 'Emph' else '**'
            parts.append(marker + inline_text(value) + marker)
        elif kind in {'SmallCaps', 'Superscript', 'Subscript'}:
            parts.append(inline_text(value))
        elif kind in {'Span', 'Quoted', 'Cite'}:
            parts.append(inline_text(value[1]))
        elif kind == 'Link':
            parts.append(inline_text(value[1]))
        elif kind == 'Code':
            parts.append(value[1])
    return ''.join(parts)


def walk_nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_nodes(child)


class AcademicRenderer:
    def __init__(self, workspace, config, cache):
        self.workspace = Path(workspace)
        self.config = config
        self.cache = Path(cache)
        self.pandoc = require_renderer('pandoc')
        self.version = run_process([self.pandoc, '--version']).stdout.splitlines()[0]
        self.references = []

    def render_citations(self, markdown):
        if not self.config.bibliography:
            if any(CITATION_RE.search(part) for line in content_lines(markdown) for code, part in text_parts(line) if not code):
                raise ValueError('Trích dẫn cần file bibliography. Thêm nguồn trong mục Tài liệu tham khảo.')
            return markdown, []
        bibliography = self.workspace / self.config.bibliography
        if not bibliography.is_file():
            raise FileNotFoundError(f'Thiếu tài liệu tham khảo: {self.config.bibliography}')
        source = self.workspace / 'citeproc-input.md'
        atomic_write(source, markdown)
        command = [self.pandoc, source, '--from=markdown+citations+tex_math_dollars', '--to=json',
                   '--citeproc', '--bibliography', bibliography]
        if self.config.csl:
            style = self.workspace / self.config.csl
            if not style.is_file():
                raise FileNotFoundError(f'Thiếu CSL: {self.config.csl}')
            command.extend(['--csl', style])
        result = run_process(command, cwd=self.workspace)
        tree = json.loads(result.stdout)
        citations = [inline_text(node['c'][1]) for node in walk_nodes(tree) if node.get('t') == 'Cite']
        for node in walk_nodes(tree):
            if node.get('t') == 'Div' and node['c'][0][0].startswith('ref-'):
                paragraphs = [inline_text(n['c']) for n in walk_nodes(node['c'][1]) if n.get('t') in {'Para', 'Plain'}]
                self.references.append(' '.join(paragraphs))
        citation_index = 0
        in_code = False
        output = []

        def replace(match):
            nonlocal citation_index
            if citation_index >= len(citations):
                raise ValueError('Không ánh xạ được đầy đủ trích dẫn. Kiểm tra cú pháp [@id].')
            value = citations[citation_index]
            citation_index += 1
            return value

        for line in markdown.splitlines():
            if line.lstrip().startswith(('```', '~~~')):
                in_code = not in_code
            if not in_code:
                line = ''.join(part if code else CITATION_RE.sub(replace, part) for code, part in text_parts(line))
            output.append(line)
        if citation_index != len(citations):
            raise ValueError('Cú pháp trích dẫn chưa hỗ trợ đầy đủ; bản xuất chưa được công bố.')
        warnings = [line for line in result.stderr.splitlines() if line.strip()]
        return '\n'.join(output) + '\n', warnings

    def render_math(self, equation, *, block=True):
        digest = hashlib.sha256((self.version + str(block) + equation).encode()).hexdigest()
        fragment = self.cache / f'omml-{digest}.docx'
        if not fragment.is_file():
            source = self.workspace / f'math-{digest}.md'
            atomic_write(source, f'$$\n{equation}\n$$\n' if block else f'${equation}$\n')
            run_process([self.pandoc, source, '--from=markdown+tex_math_dollars', '--to=docx', '--output', fragment],
                        cwd=self.workspace)
        document = Document(fragment)
        nodes = document.element.xpath('.//m:oMathPara' if block else './/m:oMath')
        if not nodes:
            raise ValueError('Pandoc không tạo công thức Word chỉnh sửa được.')
        return deepcopy(nodes[0])

    def add_text(self, paragraph, text, write_text):
        if not INLINE_MATH_RE.search(text):
            write_text(paragraph, text)
            return
        for code, part in text_parts(text):
            if code:
                write_text(paragraph, part)
            else:
                self._add_math_text(paragraph, part, write_text)

    def _add_math_text(self, paragraph, text, write_text):
        position = 0
        for match in INLINE_MATH_RE.finditer(text):
            write_text(paragraph, text[position:match.start()])
            paragraph._p.append(self.render_math(match.group(1), block=False))
            position = match.end()
        write_text(paragraph, text[position:])
