# diagnose.py — Tim code fence mat can bang trong file MD
import sys
sys.stdout.reconfigure(encoding='utf-8')

lines = open('Bao_Cao_Tieu_Luan_NMCNPM.md', encoding='utf-8').readlines()

FENCE = '```'
in_code = False
issues = []
open_at = None

for i, raw in enumerate(lines, 1):
    l = raw.strip()
    if l.startswith(FENCE):
        if not in_code:
            in_code = True
            open_at = i
            lang = l[3:].strip()
            # print(f'  OPEN  L{i:4d}  lang="{lang}"')
        else:
            in_code = False
            # print(f'  CLOSE L{i:4d}')
            open_at = None

if in_code:
    issues.append(f'[!] Code fence MO tai L{open_at} CHUA DONG (EOF)')

# Tim cac doan text co ** hoac - o trong code block (biet hieu sai)
in_code2 = False
open2 = 0
for i, raw in enumerate(lines, 1):
    l = raw.strip()
    if l.startswith(FENCE):
        if not in_code2:
            in_code2 = True
            open2 = i
        else:
            in_code2 = False
    elif in_code2 and (l.startswith('**') or l.startswith('- **') or l.startswith('### ')):
        issues.append(f'  [?] L{i:4d}: markdown inside code block (mo tai L{open2}): {l[:60]}')

if not issues:
    print('[OK] Tat ca code fence can bang, khong co van de.')
else:
    for iss in issues:
        print(iss)

# Dem tong so fence
total_open = sum(1 for raw in lines if raw.strip().startswith(FENCE) and raw.strip() != FENCE)
total_close = sum(1 for raw in lines if raw.strip() == FENCE)
total_named = sum(1 for raw in lines if raw.strip().startswith(FENCE) and len(raw.strip()) > 3)
print(f'\nThong ke fence:')
print(f'  Tong dong bat dau voi ``` : {total_open + total_close}')
print(f'  Fence co ten lang         : {total_named}')
print(f'  Fence dong (``` don)      : {total_close}')
