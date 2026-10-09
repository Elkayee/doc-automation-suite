import re
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

from src.core.docx_helpers import DocxHelpers
from src.core.file_io import atomic_write
from src.core.markdown_image import parse_markdown_image_line
from src.core.markdown_semantics import content_lines
from src.core.markdown_utils import MarkdownUtils
from src.core.media_downloader import MediaDownloader
from src.core.report_fields import (
    add_caption,
    add_field,
    add_reference_runs,
    add_report_cover,
    configure_styles,
    end_bookmark,
    set_page_numbering,
    start_body_section,
    start_bookmark,
)


class DocxBuilder:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.config = self._get_config()
        self.doc = self._init_document()
        self.diagram_idx = 0
        self.math_idx = 0
        self.warnings = []
        self.academic = None
        configure_styles(self.doc, self.config)
        if self.config and self.config.settings.get('report_fields'):
            set_page_numbering(self.doc.sections[0])

    def _get_config(self):
        from src.core.config import TemplateConfig

        config_path = self.workspace_dir / 'config.yaml'
        if config_path.exists():
            return TemplateConfig.load(config_path)
        return None

    def _init_document(self):
        """Loads template.docx if it exists, otherwise creates a blank Document."""
        page_settings = DocxHelpers.get_page_settings(self.config)
        if self.config and self.config.docx_template:
            template_path = self.workspace_dir / self.config.docx_template
            if template_path.exists():
                doc = Document(str(template_path))
                DocxHelpers.apply_page_settings(doc, page_settings)
                return doc
        doc = Document()
        DocxHelpers.apply_page_settings(doc, page_settings)
        return doc

    def build_from_markdown(self, md_path: str, img_cache_dir: Path):
        """
        Applies markdown parsing and writes to self.doc.
        Integrated from make.py's parse_and_write.
        """
        with open(md_path, encoding='utf-8') as f:
            lines = f.readlines()

        numbered_captions = bool(self.config and self.config.settings.get('numbered_captions'))
        references = {}
        image_index = table_index = 0
        table_caption_re = re.compile(r'^\[\[TABLE:\s*([A-Za-z][A-Za-z0-9_]{0,39})\s*\|\s*(.+?)\]\]$')
        for source_line in content_lines(''.join(lines)):
            image = parse_markdown_image_line(source_line.rstrip('\n'))
            caption = table_caption_re.match(source_line.strip())
            heading_id = re.match(r'^#{1,6}\s+(.*?)\s+\{#([A-Za-z][A-Za-z0-9_]{0,39})\}\s*$', source_line)
            identifier = ''
            if image and image.caption:
                image_index += 1
                identifier, value = image.identifier, f'Hình {image_index}'
            elif caption:
                table_index += 1
                identifier, value = caption.group(1), f'Bảng {table_index}'
            elif heading_id:
                identifier, value = heading_id.group(2), heading_id.group(1)
            if identifier:
                if identifier in references:
                    raise ValueError(f'Mã tham chiếu trùng: {identifier}')
                references[identifier] = value
        image_index = table_index = 0
        pending_table_caption = None

        paragraph_settings = DocxHelpers.get_paragraph_settings(self.config)
        markdown_table_settings = DocxHelpers.get_markdown_table_settings(self.config)
        style = self.doc.styles['Normal']
        style.font.name = paragraph_settings.get('font_name', 'Times New Roman')
        style.font.size = Pt(float(paragraph_settings.get('font_size', 14)))
        style.paragraph_format.alignment = DocxHelpers.parse_alignment(paragraph_settings.get('alignment', 'justify'))
        style.paragraph_format.left_indent = Cm(float(paragraph_settings.get('left_indent_cm', 0.0)))
        style.paragraph_format.right_indent = Cm(float(paragraph_settings.get('right_indent_cm', 0.0)))
        style.paragraph_format.space_before = Pt(float(paragraph_settings.get('space_before_pt', 0.0)))
        style.paragraph_format.space_after = Pt(float(paragraph_settings.get('space_after_pt', 6.0)))
        special_indent = str(paragraph_settings.get('special_indent', 'first_line')).lower()
        special_indent_by_cm = float(paragraph_settings.get('special_indent_by_cm', 1.27))
        style.paragraph_format.first_line_indent = None
        if special_indent == 'first_line':
            style.paragraph_format.first_line_indent = Cm(special_indent_by_cm)
        elif special_indent == 'hanging':
            style.paragraph_format.first_line_indent = Cm(-special_indent_by_cm)

        line_spacing_mode = str(paragraph_settings.get('line_spacing_mode', 'multiple')).lower()
        line_spacing_value = float(paragraph_settings.get('line_spacing_value', 1.5))
        if line_spacing_mode == 'single':
            style.paragraph_format.line_spacing = 1.0
        elif line_spacing_mode == 'double':
            style.paragraph_format.line_spacing = 2.0
        elif line_spacing_mode == 'exactly':
            style.paragraph_format.line_spacing = Pt(line_spacing_value)
        else:
            style.paragraph_format.line_spacing = line_spacing_value

        # Tiền xử lý: rút gọn ≥2 dòng trống liên tiếp thành tối đa 1
        compressed, blank_run = [], 0
        for _ln in lines:
            if not _ln.strip():
                blank_run += 1
                if blank_run == 1:
                    compressed.append(_ln)
            else:
                blank_run = 0
                compressed.append(_ln)
        lines = compressed

        i, in_code, mermaid_block, mermaid_buf = 0, False, False, []
        current_source_filename = None
        skip_current_source = None
        exam_cover_rendered = False

        while i < len(lines):
            line = lines[i].rstrip('\n')

            source_match = re.match(r'^\s*<!--\s*FILE:\s+(.+?)\s*-->\s*$', line)
            if source_match:
                current_source_filename = source_match.group(1).strip()
                if (
                    self.config
                    and self.config.type == 'exam'
                    and current_source_filename == 'F00_header.md'
                    and not exam_cover_rendered
                ):
                    skip_current_source = current_source_filename
                else:
                    skip_current_source = None
                i += 1
                continue

            if (
                skip_current_source
                and current_source_filename == skip_current_source
                and self.config
                and self.config.type == 'exam'
                and current_source_filename == 'F00_header.md'
            ):
                cover_lines = []
                while i < len(lines):
                    candidate = lines[i].rstrip('\n')
                    if re.match(r'^\s*<!--\s*FILE:\s+(.+?)\s*-->\s*$', candidate):
                        break
                    cover_lines.append(candidate)
                    i += 1
                cover_defaults = DocxHelpers.get_exam_cover_settings(self.config)
                cover_settings = DocxHelpers.parse_exam_cover_content('\n'.join(cover_lines), cover_defaults)
                self.config.settings = dict(self.config.settings or {})
                self.config.settings['cover_page'] = cover_settings
                DocxHelpers.add_exam_cover(self.doc, self.workspace_dir, self.config)
                exam_cover_rendered = True
                continue

            if skip_current_source and current_source_filename == skip_current_source:
                i += 1
                continue

            # Code/Mermaid block
            if line.strip().startswith(('```', '~~~')):
                if not in_code:
                    in_code = True
                    lang = line.strip()[3:].strip().lower()
                    mermaid_block = lang in {'plantuml', 'puml'}
                    mermaid_buf = []
                else:
                    if mermaid_block and mermaid_buf:
                        self.diagram_idx += 1
                        img_path = MediaDownloader.render_plantuml(
                            '\n'.join(mermaid_buf), self.diagram_idx, str(img_cache_dir)
                        )
                        if img_path:
                            p = self.doc.add_paragraph()
                            DocxHelpers.configure_media_paragraph(p, space_before=18, space_after=18)
                            run = p.add_run()
                            max_width, max_height = DocxHelpers.get_content_frame_size(self.doc, height_reserve=Cm(3))
                            DocxHelpers.add_picture_fit(
                                run, img_path, self.doc, max_width=max_width, max_height=max_height
                            )
                        else:
                            self.warnings.append(f'Không render được sơ đồ {self.diagram_idx}')
                            p = self.doc.add_paragraph()
                            r = p.add_run(f'[Bieu do PlantUML {self.diagram_idx} - khong the render]')
                            r.italic = True
                            r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
                    in_code = mermaid_block = False
                    mermaid_buf = []
                i += 1
                continue

            if in_code:
                if mermaid_block:
                    mermaid_buf.append(line)
                else:
                    p = self.doc.add_paragraph()
                    run = p.add_run(line if line else ' ')
                    run.font.name = 'Courier New'
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                    DocxHelpers.set_para_shading(p, 'F4F4F4')
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                i += 1
                continue

            # Bảng
            caption_match = table_caption_re.match(line.strip())
            if caption_match:
                pending_table_caption = (caption_match.group(1), caption_match.group(2))
                i += 1
                continue

            if line.startswith('|'):
                if pending_table_caption:
                    table_index += 1
                    identifier, caption_text = pending_table_caption
                    add_caption(self.doc, 'Bảng', caption_text, table_index, identifier)
                    pending_table_caption = None
                table_rows = []
                while i < len(lines) and lines[i].startswith('|'):
                    cells = MarkdownUtils.split_table_row(lines[i])
                    table_rows.append(cells)
                    i += 1
                data_rows = [r for r in table_rows if not all(re.match(r'^[-: ]+$', c) for c in r)]
                if not data_rows:
                    continue
                max_cols = max(len(r) for r in data_rows)
                data_rows = [r + [''] * (max_cols - len(r)) for r in data_rows]
                tbl = self.doc.add_table(rows=len(data_rows), cols=max_cols)
                tbl.style = 'Table Grid'
                for ri, row in enumerate(data_rows):
                    if ri == 0:
                        DocxHelpers.set_table_row_repeat_header(tbl.rows[ri])
                    for ci, cell_text in enumerate(row):
                        cell = tbl.cell(ri, ci)
                        DocxHelpers.format_markdown_table_cell(
                            cell,
                            MarkdownUtils.strip_md_markup(MarkdownUtils.normalize_html_breaks(cell_text, '\n')),
                            is_header=ri == 0,
                            settings=markdown_table_settings,
                        )
                _sp = self.doc.add_paragraph()
                _sp.paragraph_format.space_before = Pt(0)
                _sp.paragraph_format.space_after = Pt(6)
                _sp.add_run('').font.size = Pt(4)
                continue

            # Horizontal rule
            if re.match(r'^---+\s*$', line):
                p = self.doc.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(4)
                i += 1
                continue

            # Centered text
            m_center = re.match(r'^\s*<center>(.*?)</center>\s*$', line)
            if m_center:
                text = m_center.group(1).strip()
                p = self.doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                MarkdownUtils.add_formatted_run(p, text)
                i += 1
                continue

            # Markdown image
            parsed_image = parse_markdown_image_line(line)
            if parsed_image:
                image_path = DocxHelpers.resolve_media_path(self.workspace_dir, md_path, parsed_image.path)
                if not image_path.is_file():
                    self.warnings.append(f'Thiếu ảnh: {parsed_image.path}')
                caption_index = None
                if parsed_image.caption and (numbered_captions or parsed_image.identifier):
                    image_index += 1
                    caption_index = image_index
                DocxHelpers.add_markdown_image(self.doc, self.workspace_dir, md_path, parsed_image, caption_index)
                i += 1
                continue

            if line.strip() == '[[COVER]]':
                if not self.config:
                    raise ValueError('Trang bìa cần config.yaml')
                for paragraph in self.doc.sections[-1].footer.paragraphs:
                    paragraph.clear()
                add_report_cover(self.doc, self.config)
                i += 1
                continue

            if line.strip() == '[[BODY]]':
                start_body_section(self.doc, self.config)
                i += 1
                continue

            if line.strip() in {'[[LANDSCAPE]]', '[[PORTRAIT]]'}:
                section = self.doc.add_section(WD_SECTION_START.NEW_PAGE)
                page_settings = DocxHelpers.get_page_settings(self.config)
                page_settings['orientation'] = 'landscape' if 'LANDSCAPE' in line else 'portrait'
                DocxHelpers.apply_section_settings(section, page_settings)
                page_number = section._sectPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType')
                if page_number is not None:
                    page_number.attrib.pop('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}start', None)
                i += 1
                continue

            if line.strip() in {'[[FIGURES]]', '[[TABLES]]'}:
                label = 'Hình' if 'FIGURES' in line else 'Bảng'
                add_field(self.doc.add_paragraph(), f'TOC \\h \\z \\c "{label}"', 'Cập nhật danh mục trong Word.')
                i += 1
                continue

            if line.strip() == '[[PAGEBREAK]]':
                DocxHelpers.add_page_break(self.doc)
                i += 1
                continue

            if line.strip() == '[[TOC]]':
                DocxHelpers.add_table_of_contents(self.doc)
                i += 1
                continue

            # Heading
            m = re.match(r'^(#{1,6})\s+(.*)', line)
            if m:
                level = len(m.group(1))
                text = MarkdownUtils.strip_md_markup(m.group(2))
                heading_id = re.search(r'\s+\{#([A-Za-z][A-Za-z0-9_]{0,39})\}$', text)
                identifier = heading_id.group(1) if heading_id else ''
                if heading_id:
                    text = text[:heading_id.start()]
                heading_style = 'Title' if current_source_filename and current_source_filename.startswith('F01_') else f'Heading {level}'
                p = self.doc.add_paragraph(style=heading_style)
                heading_indent = MarkdownUtils.get_heading_indent(text)
                if heading_indent is not None:
                    p.paragraph_format.left_indent = heading_indent
                _space_before = [Pt(12), Pt(10), Pt(8), Pt(6), Pt(6), Pt(4)]
                p.paragraph_format.space_before = _space_before[level - 1]
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                if identifier:
                    start_bookmark(p, identifier, 30000 + i)
                run = p.add_run(text)
                run.font.name = 'Times New Roman'
                run.font.size = Pt([16, 14, 13, 12, 12, 11][level - 1])
                run.bold = level <= 3
                if self.config and self.config.settings.get('report_fields'):
                    run.font.name = self.config.settings.get('font_name', 'Times New Roman')
                    run.font.size = p.style.font.size
                    p.paragraph_format.line_spacing = paragraph_settings.get('line_spacing_value', 1.5)
                    p.paragraph_format.first_line_indent = Cm(0)
                if identifier:
                    end_bookmark(p, 30000 + i)
                i += 1
                continue

            # Blockquote
            if line.startswith('>'):
                quote_lines = []
                while i < len(lines) and lines[i].startswith('>'):
                    quote_lines.append(lines[i].lstrip('> ').strip())
                    i += 1

                p = self.doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(1)
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(6)
                MarkdownUtils.add_formatted_run(p, ' '.join(quote_lines))

                for run in p.runs:
                    if run.font.name != 'Courier New':
                        run.italic = True
                    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
                continue

            # Checkbox
            if re.match(r'^-\s+\[[ xX]\]', line):
                text = re.sub(r'^-\s+\[[ xX]\]\s*', '', line)
                p = self.doc.add_paragraph()
                base_indent_cm = float(paragraph_settings.get('left_indent_cm', 0.0))
                special_indent_mode = str(paragraph_settings.get('special_indent', 'first_line')).lower()
                special_indent_cm = float(paragraph_settings.get('special_indent_by_cm', 1.27))
                p.paragraph_format.left_indent = Cm(base_indent_cm)
                p.paragraph_format.first_line_indent = (
                    Cm(special_indent_cm) if special_indent_mode == 'first_line' else Cm(0.0)
                )
                MarkdownUtils.add_formatted_run(p, '[  ] ' + text)
                i += 1
                continue

            # Bullet list
            m_bullet = re.match(r'^( *)[-\*\+]\s+(.*)', line)
            if m_bullet:
                indent_lvl = len(m_bullet.group(1)) // 2
                marker = m_bullet.group(0).strip().split(maxsplit=1)[0]
                p = self.doc.add_paragraph()
                base_indent_cm = float(paragraph_settings.get('left_indent_cm', 0.0))
                special_indent_mode = str(paragraph_settings.get('special_indent', 'first_line')).lower()
                special_indent_cm = float(paragraph_settings.get('special_indent_by_cm', 1.27))
                p.paragraph_format.left_indent = Cm(base_indent_cm + (indent_lvl * 1.0))
                p.paragraph_format.first_line_indent = (
                    Cm(special_indent_cm) if special_indent_mode == 'first_line' else Cm(0.0)
                )
                MarkdownUtils.add_formatted_run(p, f'{marker} {m_bullet.group(2)}')
                i += 1
                continue

            # Numbered list
            if re.match(r'^\d+\.\s+', line):
                text = re.sub(r'^\d+\.\s+', '', line)
                p = self.doc.add_paragraph(style='List Number')
                MarkdownUtils.add_formatted_run(p, text)
                i += 1
                continue

            # Công thức toán (khối $$ ... $$)
            if line.strip() == '$$':
                math_buf = []
                i += 1
                while i < len(lines) and lines[i].rstrip('\n').strip() != '$$':
                    math_buf.append(lines[i].rstrip('\n'))
                    i += 1
                i += 1
                latex_code = ' '.join(b.strip() for b in math_buf if b.strip())
                if latex_code:
                    if self.academic:
                        p = self.doc.add_paragraph()
                        DocxHelpers.configure_media_paragraph(p, space_before=6, space_after=6)
                        p._p.append(self.academic.render_math(latex_code))
                        continue
                    self.math_idx += 1
                    img_path = MediaDownloader.render_latex(latex_code, self.math_idx, str(img_cache_dir))
                    if img_path:
                        p = self.doc.add_paragraph()
                        DocxHelpers.configure_media_paragraph(p, space_before=6, space_after=6)
                        max_width, max_height = DocxHelpers.get_content_frame_size(self.doc, height_reserve=Cm(4))
                        DocxHelpers.add_picture_fit(
                            p.add_run(), img_path, self.doc, max_width=max_width, max_height=max_height
                        )
                    else:
                        self.warnings.append(f'Không render được công thức {self.math_idx}')
                        p = self.doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = p.add_run(latex_code)
                        run.font.name = 'Cambria Math'
                        run.font.size = Pt(11)
                continue

            # Công thức toán inline: $$ ... $$ trên một dòng
            if line.strip().startswith('$$') and line.strip().endswith('$$') and len(line.strip()) > 4:
                latex_code = line.strip()[2:-2].strip()
                if latex_code:
                    if self.academic:
                        p = self.doc.add_paragraph()
                        DocxHelpers.configure_media_paragraph(p, space_before=6, space_after=6)
                        p._p.append(self.academic.render_math(latex_code))
                        i += 1
                        continue
                    self.math_idx += 1
                    img_path = MediaDownloader.render_latex(latex_code, self.math_idx, str(img_cache_dir))
                    if img_path:
                        p = self.doc.add_paragraph()
                        DocxHelpers.configure_media_paragraph(p, space_before=6, space_after=6)
                        max_width, max_height = DocxHelpers.get_content_frame_size(self.doc, height_reserve=Cm(4))
                        DocxHelpers.add_picture_fit(
                            p.add_run(), img_path, self.doc, max_width=max_width, max_height=max_height
                        )
                    else:
                        self.warnings.append(f'Không render được công thức {self.math_idx}')
                        p = self.doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p.add_run(latex_code).font.name = 'Cambria Math'
                i += 1
                continue

            if line.strip() == '[[REFERENCES]]':
                if self.academic and self.academic.references:
                    for reference in self.academic.references:
                        MarkdownUtils.add_formatted_run(self.doc.add_paragraph(), reference)
                else:
                    self.warnings.append('Chưa có tài liệu tham khảo được trích dẫn')
                i += 1
                continue

            # Dòng trống → bỏ qua hoàn toàn, không tạo paragraph
            if not line.strip():
                i += 1
                continue

            # Đoạn văn thường — chuẩn NĐ30: justify, lùi đầu dòng, dãn 1.5
            p = self.doc.add_paragraph()
            DocxHelpers.apply_paragraph_format(p, paragraph_settings)
            def write_text(paragraph, text):
                if self.academic:
                    self.academic.add_text(paragraph, text, MarkdownUtils.add_formatted_run)
                else:
                    MarkdownUtils.add_formatted_run(paragraph, text)

            add_reference_runs(p, MarkdownUtils.normalize_punctuation(line.strip()), references, write_text)
            i += 1

    def save(self, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            buffer = BytesIO()
            self.doc.save(buffer)
            atomic_write(output_path, buffer.getvalue())
        except PermissionError as exc:
            raise RuntimeError(
                f'Khong the ghi file {output_path.name}. Hay dong file Word cu truoc khi build lai.'
            ) from exc
