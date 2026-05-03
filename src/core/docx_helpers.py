from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Inches, Pt, RGBColor
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from pathlib import Path
from src.core.media_downloader import MediaDownloader

# ── MÀUSẮC ───────────────────────────────────────────────────────────────────
COLOR_H1 = RGBColor(0x1A, 0x3A, 0x5C)
COLOR_H2 = RGBColor(0x1F, 0x61, 0x9E)
COLOR_H3 = RGBColor(0x2E, 0x86, 0xAB)
COLOR_H4 = RGBColor(0x44, 0x9D, 0xD1)

class DocxHelpers:
    @staticmethod
    def get_page_settings(config):
        settings = (config.settings if config and config.settings else {}).copy()
        defaults = {
            'page_width_cm': 21.0,
            'page_height_cm': 29.7,
            'margin_top_cm': 2.5,
            'margin_bottom_cm': 2.5,
            'margin_left_cm': 3.0,
            'margin_right_cm': 2.0,
            'gutter_cm': 0.0,
            'orientation': 'portrait',
        }
        defaults.update(settings)
        return defaults

    @staticmethod
    def get_paragraph_settings(config):
        settings = (config.settings if config and config.settings else {}).copy()
        defaults = {
            'font_name': 'Times New Roman',
            'font_size': 13,
            'alignment': 'justify',
            'left_indent_cm': 0.0,
            'right_indent_cm': 0.0,
            'special_indent': 'first_line',
            'special_indent_by_cm': 1.27,
            'space_before_pt': 0.0,
            'space_after_pt': 6.0,
            'line_spacing_mode': 'multiple',
            'line_spacing_value': 1.5,
        }
        defaults.update(settings)
        return defaults

    @staticmethod
    def parse_alignment(value):
        mapping = {
            'left': WD_ALIGN_PARAGRAPH.LEFT,
            'center': WD_ALIGN_PARAGRAPH.CENTER,
            'right': WD_ALIGN_PARAGRAPH.RIGHT,
            'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
        }
        return mapping.get(str(value).lower(), WD_ALIGN_PARAGRAPH.JUSTIFY)

    @staticmethod
    def apply_paragraph_format(paragraph, settings, use_spacing_after=True):
        paragraph.alignment = DocxHelpers.parse_alignment(settings.get('alignment', 'justify'))
        paragraph.paragraph_format.left_indent = Cm(float(settings.get('left_indent_cm', 0.0)))
        paragraph.paragraph_format.right_indent = Cm(float(settings.get('right_indent_cm', 0.0)))

        special_indent = str(settings.get('special_indent', 'first_line')).lower()
        special_indent_by_cm = float(settings.get('special_indent_by_cm', 1.27))
        paragraph.paragraph_format.first_line_indent = None
        if special_indent == 'first_line':
            paragraph.paragraph_format.first_line_indent = Cm(special_indent_by_cm)
        elif special_indent == 'hanging':
            paragraph.paragraph_format.first_line_indent = Cm(-special_indent_by_cm)

        paragraph.paragraph_format.space_before = Pt(float(settings.get('space_before_pt', 0.0)))
        paragraph.paragraph_format.space_after = Pt(float(settings.get('space_after_pt', 6.0 if use_spacing_after else 0.0)))

        line_spacing_mode = str(settings.get('line_spacing_mode', 'multiple')).lower()
        line_spacing_value = float(settings.get('line_spacing_value', 1.5))
        if line_spacing_mode == 'single':
            paragraph.paragraph_format.line_spacing = 1.0
        elif line_spacing_mode == 'double':
            paragraph.paragraph_format.line_spacing = 2.0
        elif line_spacing_mode == 'exactly':
            paragraph.paragraph_format.line_spacing = Pt(line_spacing_value)
        else:
            paragraph.paragraph_format.line_spacing = line_spacing_value

    @staticmethod
    def set_cell_bg(cell, hex_color):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), hex_color)
        tcPr.append(shd)

    @staticmethod
    def set_para_shading(para, hex_color):
        pPr = para._p.get_or_add_pPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), hex_color)
        pPr.append(shd)

    @staticmethod
    def set_page_setup(doc):
        DocxHelpers.apply_page_settings(doc, DocxHelpers.get_page_settings(None))

    @staticmethod
    def apply_page_settings(doc, settings):
        sec = doc.sections[0]
        width_cm = float(settings.get('page_width_cm', 21.0))
        height_cm = float(settings.get('page_height_cm', 29.7))
        orientation = str(settings.get('orientation', 'portrait')).lower()
        if orientation == 'landscape':
            sec.orientation = WD_ORIENTATION.LANDSCAPE
            sec.page_width = Cm(max(width_cm, height_cm))
            sec.page_height = Cm(min(width_cm, height_cm))
        else:
            sec.orientation = WD_ORIENTATION.PORTRAIT
            sec.page_width = Cm(min(width_cm, height_cm))
            sec.page_height = Cm(max(width_cm, height_cm))

        sec.left_margin = Cm(float(settings.get('margin_left_cm', 3.0)))
        sec.right_margin = Cm(float(settings.get('margin_right_cm', 2.0)))
        sec.top_margin = Cm(float(settings.get('margin_top_cm', 2.5)))
        sec.bottom_margin = Cm(float(settings.get('margin_bottom_cm', 2.5)))
        sec.gutter = Cm(float(settings.get('gutter_cm', 0.0)))

    @staticmethod
    def get_content_frame_size(doc, height_reserve=Cm(1.5)):
        sec = doc.sections[0]
        max_width = Emu(sec.page_width - sec.left_margin - sec.right_margin)
        max_height = Emu(sec.page_height - sec.top_margin - sec.bottom_margin - height_reserve)
        return max_width, max_height

    @staticmethod
    def add_picture_fit(run, image_path, doc, max_width=None, max_height=None):
        if max_width is None or max_height is None:
            max_width, max_height = DocxHelpers.get_content_frame_size(doc)

        img_w, img_h = MediaDownloader.get_image_dimensions(image_path)
        if not img_w or not img_h:
            run.add_picture(str(image_path), width=max_width)
            return

        width_inches = img_w / 96.0
        height_inches = img_h / 96.0

        width_scale = max_width.inches / width_inches if width_inches else 1.0
        height_scale = max_height.inches / height_inches if height_inches else 1.0
        scale = min(width_scale, height_scale)

        target_width = Inches(width_inches * scale)
        target_height = Inches(height_inches * scale)
        run.add_picture(str(image_path), width=target_width, height=target_height)

    @staticmethod
    def resolve_media_path(base_dir, md_path, asset_path):
        asset = Path(asset_path)
        if asset.is_absolute():
            return asset
        primary = (Path(md_path).resolve().parent / asset).resolve()
        if primary.exists():
            return primary
        fallback_text = asset_path.replace('../', '').replace('..\\', '').replace('./', '').replace('.\\', '')
        return (Path(base_dir) / Path(fallback_text)).resolve()

    @staticmethod
    def add_markdown_image(doc, base_dir, md_path, image_ref):
        image_path = DocxHelpers.resolve_media_path(base_dir, md_path, image_ref)
        if not image_path.exists():
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(f'[Khong tim thay anh: {image_ref}]')
            r.italic = True
            r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
            return

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run()
        max_width, max_height = DocxHelpers.get_content_frame_size(doc, height_reserve=Cm(2))
        DocxHelpers.add_picture_fit(run, image_path, doc, max_width=max_width, max_height=max_height)

    @staticmethod
    def add_page_break(doc):
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    @staticmethod
    def add_table_of_contents(doc):
        p = doc.add_paragraph()
        begin_run = OxmlElement('w:r')
        fld_begin = OxmlElement('w:fldChar')
        fld_begin.set(qn('w:fldCharType'), 'begin')
        begin_run.append(fld_begin)

        instr_run = OxmlElement('w:r')
        instr = OxmlElement('w:instrText')
        instr.set(qn('xml:space'), 'preserve')
        instr.text = 'TOC \\o "1-4" \\h \\z \\u'
        instr_run.append(instr)

        separate_run = OxmlElement('w:r')
        fld_separate = OxmlElement('w:fldChar')
        fld_separate.set(qn('w:fldCharType'), 'separate')
        separate_run.append(fld_separate)

        hint_run = OxmlElement('w:r')
        hint_text = OxmlElement('w:t')
        hint_text.text = 'Cap nhat Muc luc trong Word bang Update Field.'
        hint_run.append(hint_text)

        end_run = OxmlElement('w:r')
        fld_end = OxmlElement('w:fldChar')
        fld_end.set(qn('w:fldCharType'), 'end')
        end_run.append(fld_end)

        p._p.append(begin_run)
        p._p.append(instr_run)
        p._p.append(separate_run)
        p._p.append(hint_run)
        p._p.append(end_run)
