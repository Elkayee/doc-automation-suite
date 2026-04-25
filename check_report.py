# check_report.py — kiem tra header va mermaid diagram
import sys
sys.stdout.reconfigure(encoding='utf-8')

lines = open('Bao_Cao_Tieu_Luan_NMCNPM.md', encoding='utf-8').readlines()

# 1. Header
print('=== HEADER (20 dong dau) ===')
for i, l in enumerate(lines[:20], 1):
    print(f'L{i:3d}: {l.rstrip()}')

# 2. Mermaid diagrams
print()
print('=== MERMAID DIAGRAMS ===')
in_mermaid = False
idx = 0
start_line = 0
buf = []
FENCE = '```'

for i, l in enumerate(lines, 1):
    stripped = l.strip()
    if stripped == FENCE + 'mermaid':
        in_mermaid = True
        idx += 1
        start_line = i
        buf = []
    elif in_mermaid and stripped == FENCE:
        in_mermaid = False
        diagram_type = buf[0].strip() if buf else '?'
        print(f'  [{idx:02d}] L{start_line:4d}-{i:4d}  type="{diagram_type}"  ({len(buf)} dong code)')
    elif in_mermaid:
        buf.append(stripped)

print(f'\nTong cong: {idx} Mermaid diagram(s)')
