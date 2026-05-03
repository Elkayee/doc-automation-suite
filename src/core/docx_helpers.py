from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Inches, Pt, RGBColor
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
        sec = doc.sections[0]
        sec.page_width = Cm(21)
        sec.page_height = Cm(29.7)
        sec.left_margin = Cm(3)
        sec.right_margin = Cm(2)
        sec.top_margin = Cm(2.5)
        sec.bottom_margin = Cm(2.5)

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
