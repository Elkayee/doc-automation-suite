# split_chapters.py
# Chia file bao cao chinh thanh tung chapter rieng biet

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

src = open('Bao_Cao_Tieu_Luan_NMCNPM.md', encoding='utf-8').read()
lines = src.split('\n')

# Tim cac dau muc cap 2 (##)
sections = []
current_title = 'header'
current_start = 0

for i, line in enumerate(lines):
    if line.startswith('## ') and i > 0:
        sections.append((current_title, current_start, i - 1))
        slug = line.lstrip('#').strip()
        slug = slug[:40]
        current_title = slug
        current_start = i

sections.append((current_title, current_start, len(lines) - 1))

os.makedirs('chapters', exist_ok=True)

BAD_CHARS = '\\/:*?"<>|'
def sanitize(s):
    for c in BAD_CHARS:
        s = s.replace(c, '')
    return s.replace(' ', '_')

for idx, (title, start, end) in enumerate(sections):
    content = '\n'.join(lines[start:end + 1])
    fname = os.path.join('chapters', f'Ch{idx:02d}_{sanitize(title)[:40]}.md')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    n = end - start + 1
    print(f'  [{idx:02d}] {os.path.basename(fname)}  ({n} dong)')

print(f'\n[OK] Da tao {len(sections)} file chapter trong thu muc chapters/')
