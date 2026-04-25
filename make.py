"""
make.py — Tool duy nhat: Ghep chapters -> MD -> convert DOCX
Usage: uv run python make.py
"""
import re, base64, io, os, sys, glob, struct, time
import requests
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.stdout.reconfigure(encoding='utf-8')

# ── CONFIG ───────────────────────────────────────────────────────────────────
BASE      = r'c:\Users\Home33\IdeaProjects\NMCNPM'
CH_DIR    = os.path.join(BASE, 'chapters')
MD_OUT    = os.path.join(BASE, 'Bao_Cao_Tieu_Luan_NMCNPM.md')
DOCX_OUT  = os.path.join(BASE, 'Bao_Cao_Tieu_Luan_NMCNPM.docx')
IMG_CACHE = os.path.join(BASE, 'mermaid_cache')
os.makedirs(IMG_CACHE, exist_ok=True)

# ── MÀUSẮC ───────────────────────────────────────────────────────────────────
COLOR_H1 = RGBColor(0x1A, 0x3A, 0x5C)
COLOR_H2 = RGBColor(0x1F, 0x61, 0x9E)
COLOR_H3 = RGBColor(0x2E, 0x86, 0xAB)
COLOR_H4 = RGBColor(0x44, 0x9D, 0xD1)

# ════════════════════════════════════════════════════════════════════════════
# BƯỚC 1: GỘP CHAPTERS → MD
# ════════════════════════════════════════════════════════════════════════════
def step_assemble():
    print('=' * 55)
    print('BƯỚC 1: Ghép chapters → MD')
    print('=' * 55)

    all_files = sorted(glob.glob(os.path.join(CH_DIR, 'Ch0*.md')))
    keep = [f for f in all_files
            if not os.path.basename(f).startswith('Ch08')
            and not os.path.basename(f).startswith('Ch09')]

    parts = []
    for fp in keep:
        content = open(fp, encoding='utf-8').read().strip()
        parts.append(content)
        print(f'  [OK] {os.path.basename(fp)}  ({len(content.splitlines())} dong)')

    final = '\n\n'.join(parts)
    with open(MD_OUT, 'w', encoding='utf-8') as f:
        f.write(final)

    kb = len(final.encode('utf-8')) // 1024
    print(f'\n  => {MD_OUT}')
    print(f'     {len(final.splitlines())} dong | {kb} KB | {len(keep)} chapters\n')

# ════════════════════════════════════════════════════════════════════════════
# BƯỚC 2: CONVERT MD → DOCX
# ════════════════════════════════════════════════════════════════════════════

# ── Mermaid render ───────────────────────────────────────────────────────────
def get_png_dimensions(path):
    with open(path, 'rb') as f:
        f.read(16)
        w = struct.unpack('>I', f.read(4))[0]
        h = struct.unpack('>I', f.read(4))[0]
    return w, h

def render_mermaid(code, idx):
    cache_file = os.path.join(IMG_CACHE, f'diagram_{idx:03d}.png')
    if os.path.exists(cache_file):
        print(f'  [cache] diagram_{idx:03d}.png')
        return cache_file
    encoded = base64.urlsafe_b64encode(code.encode('utf-8')).decode('ascii')
    url = f'https://mermaid.ink/img/{encoded}?type=png&bgColor=white'
    try:
        print(f'  [render] Dang render diagram {idx}...')
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200 and resp.headers.get('content-type','').startswith('image'):
            with open(cache_file, 'wb') as f:
                f.write(resp.content)
            print(f'  [OK] Luu vao {cache_file}')
            time.sleep(0.5)
            return cache_file
        print(f'  [WARN] API tra ve {resp.status_code}')
        return None
    except Exception as e:
        print(f'  [ERROR] {e}')
        return None

# ── DOCX helpers ─────────────────────────────────────────────────────────────
def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_para_shading(para, hex_color):
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    pPr.append(shd)

def set_page_setup(doc):
    sec = doc.sections[0]
    sec.page_width    = Cm(21)
    sec.page_height   = Cm(29.7)
    sec.left_margin   = Cm(3)
    sec.right_margin  = Cm(2)
    sec.top_margin    = Cm(2.5)
    sec.bottom_margin = Cm(2.5)

def strip_md_links(text):
    return re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)

def strip_md_markup(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*',     r'\1', text)
    text = re.sub(r'`([^`]+)`',       r'\1', text)
    return text

def add_formatted_run(para, text):
    text = strip_md_links(text)
    tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
    for token in tokens:
        if not token:
            continue
        run = para.add_run()
        if token.startswith('**') and token.endswith('**'):
            run.text = token[2:-2]
            run.bold = True
        elif token.startswith('*') and token.endswith('*'):
            run.text = token[1:-1]
            run.italic = True
        elif token.startswith('`') and token.endswith('`'):
            run.text = token[1:-1]
            run.font.name  = 'Courier New'
            run.font.size  = Pt(9)
            run.font.color.rgb = RGBColor(0xC7, 0x25, 0x4E)
        else:
            run.text = token

# ── Parser MD → DOCX ─────────────────────────────────────────────────────────
def parse_and_write(doc, md_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(13)

    i, in_code, mermaid_block, mermaid_buf, diagram_idx = 0, False, False, [], 0

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Code/Mermaid block
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                lang = line.strip()[3:].strip().lower()
                mermaid_block = (lang == 'mermaid')
                mermaid_buf = []
            else:
                if mermaid_block and mermaid_buf:
                    diagram_idx += 1
                    img_path = render_mermaid('\n'.join(mermaid_buf), diagram_idx)
                    if img_path:
                        p = doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = p.add_run()
                        img_w, img_h = get_png_dimensions(img_path)
                        PAGE_W, PAGE_H = Inches(6.2), Inches(8.0)
                        aspect = img_h / img_w if img_w > 0 else 1.0
                        if aspect > 1.2:
                            calc_w = Inches(min(6.2, PAGE_H.inches / aspect))
                            run.add_picture(img_path, width=calc_w, height=PAGE_H)
                        else:
                            run.add_picture(img_path, width=PAGE_W)
                        cap = doc.add_paragraph(f'Bieu do {diagram_idx}')
                        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        cap.runs[0].font.size = Pt(10)
                        cap.runs[0].italic = True
                        cap.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
                    else:
                        p = doc.add_paragraph()
                        r = p.add_run(f'[Bieu do Mermaid {diagram_idx} - khong the render]')
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
                p = doc.add_paragraph()
                run = p.add_run(line if line else ' ')
                run.font.name = 'Courier New'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                set_para_shading(p, 'F4F4F4')
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after  = Pt(0)
            i += 1
            continue

        # Bảng
        if line.startswith('|'):
            table_rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                table_rows.append(cells)
                i += 1
            data_rows = [r for r in table_rows
                         if not all(re.match(r'^[-: ]+$', c) for c in r)]
            if not data_rows:
                continue
            max_cols = max(len(r) for r in data_rows)
            data_rows = [r + [''] * (max_cols - len(r)) for r in data_rows]
            tbl = doc.add_table(rows=len(data_rows), cols=max_cols)
            tbl.style = 'Table Grid'
            for ri, row in enumerate(data_rows):
                for ci, cell_text in enumerate(row):
                    cell = tbl.cell(ri, ci)
                    cell.paragraphs[0].clear()
                    p = cell.paragraphs[0]
                    run = p.add_run(strip_md_markup(cell_text))
                    run.font.size = Pt(11)
                    if ri == 0:
                        run.bold = True
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                        set_cell_bg(cell, '1F619E')
                    elif ri % 2 == 0:
                        set_cell_bg(cell, 'EBF4FB')
            doc.add_paragraph()
            continue

        # Horizontal rule
        if re.match(r'^---+\s*$', line):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after  = Pt(4)
            i += 1
            continue

        # Heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text  = strip_md_markup(m.group(2))
            p     = doc.add_paragraph(style=f'Heading {min(level, 4)}')
            run   = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = [COLOR_H1,COLOR_H2,COLOR_H3,COLOR_H4,COLOR_H4,COLOR_H4][level-1]
            run.font.size      = Pt([16,14,13,12,12,11][level-1])
            run.bold           = (level <= 3)
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            text = line.lstrip('> ').strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1)
            run = p.add_run(text)
            run.italic = True
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            i += 1
            continue

        # Checkbox
        if re.match(r'^-\s+\[[ xX]\]', line):
            text = re.sub(r'^-\s+\[[ xX]\]\s*', '', line)
            p = doc.add_paragraph(style='List Bullet')
            add_formatted_run(p, '[  ] ' + text)
            i += 1
            continue

        # Bullet list
        m_bullet = re.match(r'^( *)[-\*]\s+(.*)', line)
        if m_bullet:
            indent_lvl = len(m_bullet.group(1)) // 2
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.left_indent = Cm(indent_lvl * 1.0)
            add_formatted_run(p, m_bullet.group(2))
            i += 1
            continue

        # Numbered list
        if re.match(r'^\d+\.\s+', line):
            text = re.sub(r'^\d+\.\s+', '', line)
            p = doc.add_paragraph(style='List Number')
            add_formatted_run(p, text)
            i += 1
            continue

        # Math
        if line.strip().startswith('$$'):
            p = doc.add_paragraph()
            run = p.add_run(line.strip())
            run.font.name = 'Cambria Math'
            run.font.size = Pt(12)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue

        # Dòng trống
        if not line.strip():
            doc.add_paragraph()
            i += 1
            continue

        # Đoạn văn thường
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        add_formatted_run(p, line.strip())
        i += 1

def step_convert():
    print('=' * 55)
    print('BƯỚC 2: Convert MD → DOCX')
    print('=' * 55)
    print(f'  Input : {MD_OUT}')
    print(f'  Output: {DOCX_OUT}')
    print()

    doc = Document()
    set_page_setup(doc)
    for para in doc.paragraphs:
        para._element.getparent().remove(para._element)

    parse_and_write(doc, MD_OUT)

    # Thu save; neu bi khoa (Word dang mo) thi dung ten _new
    out = DOCX_OUT
    try:
        doc.save(out)
    except PermissionError:
        out = DOCX_OUT.replace('.docx', '_new.docx')
        print(f'  [WARN] File goc bi khoa. Luu sang: {out}')
        doc.save(out)

    size = os.path.getsize(out) // 1024
    print(f'\n[DONE] {out}  ({size} KB)')
    print('  => Mo file Word va dong lai neu can dung ten goc.')

# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    step_assemble()
    step_convert()
