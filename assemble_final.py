# assemble_final.py  — Gop cac chapter thanh 1 file cuoi
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

CH_DIR = 'chapters'
OUT    = 'Bao_Cao_Tieu_Luan_NMCNPM.md'

# Lay danh sach tat ca chapter theo thu tu ten file (Ch00..Ch07)
all_files = sorted(glob.glob(os.path.join(CH_DIR, 'Ch0*.md')))

# Loai bo Ch08, Ch09 (da gop vao Ch07)
keep = [f for f in all_files if not os.path.basename(f).startswith('Ch08') 
                              and not os.path.basename(f).startswith('Ch09')]

parts = []
for fp in keep:
    content = open(fp, encoding='utf-8').read().strip()
    parts.append(content)
    lines = len(content.splitlines())
    print(f'  [OK] {os.path.basename(fp)} ({lines} dong)')

final = '\n\n'.join(parts)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(final)

kb = len(final.encode('utf-8')) // 1024
total = len(final.splitlines())
print(f'\n[DONE] {OUT}: {total} dong, {kb} KB, {len(keep)} chapters')
