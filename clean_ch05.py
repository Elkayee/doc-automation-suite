# clean_ch05.py — Xoa heading trung, giu lai heading 3.x, xoa noi dung lap
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'chapters\Ch05_CHƯƠNG_3_NGHIÊN_CỨU_CHUYÊN_SÂU_—_UC06_.md'

with open(SRC, encoding='utf-8') as f:
    raw = f.read()

lines = raw.splitlines()
out = []
i = 0
# Cac heading cu can xoa (khi gap heading 3.x/4.x/5.x tru heading 3.x)
OLD_H3 = re.compile(r'^### ([45]\.\d)')   # ### 4.x hoac ### 5.x
OLD_H4 = re.compile(r'^#### ([45]\.\d)')  # #### 4.x hoac #### 5.x
NEW_H3 = re.compile(r'^### 3\.')           # ### 3.x -> giu lai

# Xoa dong "### 3.5. Co che Cham cong Sinh trac hoc" lan thu 2 (trung)
# Xoa dong code block mo ``` bi con lai sau khi xoa heading 3.5
# Thuat toan: duyet tung dong, neu gap OLD_H3/H4 thi bo, kem theo noi dung lap sau no

skip_until_next_h3 = False
seen_h3 = set()
seen_content_blocks = {}

# Pass 1: loai heading trung va noi dung bi lap (dung hash)
cleaned = []
i = 0
while i < len(lines):
    line = lines[i]

    # Neu la heading cu (4.x, 5.x) -> skip dong nay
    if OLD_H3.match(line) or OLD_H4.match(line):
        i += 1
        continue

    # Xu ly truong hop "### 3.5. Co che..." roi thay la code block mo lon ```
    # (do script cu copy nham: doan 3.5 chi co 1 dong ``` roi het)
    # -> giu lai nhung skip dong ``` don le ngay sau heading
    if line.strip() == '```' and i > 0:
        # Kiem tra dong truoc co phai la heading khong
        prev = cleaned[-1].strip() if cleaned else ''
        if prev.startswith('###') or prev == '':
            # Co the la ``` mo bi lap - kiem tra dong tiep theo
            if i + 1 < len(lines) and (lines[i+1].startswith('###') or lines[i+1] == ''):
                i += 1
                continue

    cleaned.append(line)
    i += 1

# Pass 2: xoa khoi noi dung hoan toan lap (giu lan dau, bo lan sau)
# Chien luoc: hash tung "block" giua cac heading, neu trung -> skip
final = []
blocks = []
cur_block = []
cur_heading = None

for line in cleaned:
    if line.startswith('### ') or line.startswith('#### '):
        if cur_heading is not None:
            blocks.append((cur_heading, cur_block))
        cur_heading = line
        cur_block = []
    else:
        cur_block.append(line)

if cur_heading is not None:
    blocks.append((cur_heading, cur_block))

seen_headings = {}
for heading, block in blocks:
    content_hash = hash('\n'.join(block).strip()[:200])  # hash 200 ky tu dau
    heading_key = heading.strip()

    # Neu heading nay da xuat hien voi cung noi dung -> skip
    if heading_key in seen_headings:
        if seen_headings[heading_key] == content_hash:
            continue  # Lap hoan toan -> bo
    seen_headings[heading_key] = content_hash
    final.append(heading)
    final.extend(block)

result = '\n'.join(final)

# Fix tieu de chuong cho dung
result = result.replace(
    '## CHƯƠNG 3: NGHIÊN CỨU CHUYÊN SÂU — UC06: QUẢN LÝ NHÂN SỰ, PHÂN QUYỀN & CHẤM CÔNG',
    '## CHƯƠNG 3: NGHIÊN CỨU CHUYÊN SÂU — UC04: QUẢN LÝ CA LÀM VIỆC, CHẤM CÔNG & PHÂN QUYỀN'
)
result = result.replace(
    '> **Trái tim của báo cáo — Chiếm ~50%.** Chương này trình bày toàn bộ phân tích nghiệp vụ, thiết kế hành vi, quy tắc kinh doanh và cơ chế bảo mật của phân hệ Nhân sự do Nguyễn Viết Tùng phụ trách. Nội dung hợp nhất cả chấm công (UC04 cũ) và quản lý tài khoản/RBAC (UC07 cũ) thành một phân hệ nhất quán.',
    '> **Trái tim của báo cáo — Chiếm ~50%.** Chương này đặc tả đầy đủ nghiệp vụ, thiết kế hành vi, quy tắc kinh doanh và cơ chế bảo mật của phân hệ **UC04** do **Nguyễn Viết Tùng** phụ trách, bao gồm: phân công ca, check-in/out sinh trắc học, tính lương đa biến NĐ38 và phân quyền RBAC.'
)

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(result)

lines_out = len(result.splitlines())
print(f'[OK] {SRC}: {lines_out} dong (tu {len(lines)})')
