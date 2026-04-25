# fix_ascii.py — Doi ASCII art sang Mermaid diagram va mo ta hoc thuat
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ── CH05 ──────────────────────────────────────────────────────────────────────
ch05 = r'chapters\Ch05_CHƯƠNG_3_NGHIÊN_CỨU_CHUYÊN_SÂU_—_UC06_.md'
txt = open(ch05, encoding='utf-8').read()

# 1. Thay UC04 ASCII art (lines 11-43) bang Mermaid graph
UC04_ASCII_START = '```\n┌──────────────────────────────── UC04: QUẢN LÝ CA LÀM'
UC04_ASCII_END   = '  UC04.1, 04.2, 04.5, 04.6         UC04.3, UC04.4\n```'

UC04_MERMAID = '''```mermaid
graph TD
    subgraph UC04
        UC041["UC04.1\\nTạo mẫu ca làm\\n(Create Shift Template)"]
        UC042["UC04.2\\nPhân công ca làm\\n(Assign Shift)"]
        UC043["UC04.3\\nCheck-in ca làm\\n(Employee Check-in)"]
        UC044["UC04.4\\nCheck-out ca làm\\n(Employee Check-out)"]
        UC045["UC04.5\\nTính lương tự động\\n(Calculate Salary)"]
        UC046["UC04.6\\nXem báo cáo chấm công\\n(View Report)"]
    end

    MANAGER("👔 Manager")
    EMPLOYEE("👤 Employee")

    MANAGER --- UC041
    MANAGER --- UC042
    MANAGER --- UC045
    MANAGER --- UC046
    EMPLOYEE --- UC043
    EMPLOYEE --- UC044

    UC043 -. "«extends»" .-> UC045
    UC044 -. "«extends»" .-> UC045
    UC045 -. "«extends»" .-> UC046

    style UC041 fill:#E3F2FD,stroke:#1565C0
    style UC042 fill:#E3F2FD,stroke:#1565C0
    style UC043 fill:#F3E5F5,stroke:#6A1B9A
    style UC044 fill:#F3E5F5,stroke:#6A1B9A
    style UC045 fill:#E8F5E9,stroke:#2E7D32
    style UC046 fill:#FFF3E0,stroke:#E65100
```'''

# Tim vi tri bat dau va ket thuc cua ASCII block
idx_start = txt.find(UC04_ASCII_START)
idx_end   = txt.find(UC04_ASCII_END)
if idx_start != -1 and idx_end != -1:
    txt = txt[:idx_start] + UC04_MERMAID + txt[idx_end + len(UC04_ASCII_END):]
    print('[OK] Thay UC04 ASCII -> Mermaid')
else:
    print('[WARN] Khong tim thay UC04 ASCII block')

# 2. Thay "Luong xac thuc" ASCII -> Mermaid flowchart
GPS_START = '**Luồng xác thực:**\n\n```\n[Nhân viên mở app]'
GPS_END   = '→ Khớp (≥ 90%): Ghi nhận Check-in thành công + lưu ảnh bằng chứng\n```'

GPS_MERMAID = '''**Luồng xác thực hai lớp (Two-Factor Authentication Flow):**

```mermaid
graph TD
    A("📱 Nhân viên mở app chấm công") --> B{"🛰️ GPS Geofencing\\nThiết bị trong vùng\\n≤ 100m?"}
    B -->|Không| C["❌ Từ chối\\nGhi log cảnh báo\\nThông báo Quản lý"]
    B -->|Có| D["📸 FaceID / Chụp selfie"]
    D --> E{"🤖 AI nhận diện khuôn mặt\\n≥ 90% khớp?"}
    E -->|Không khớp\\n(< 90%)| F["❌ Từ chối\\nThông báo Quản lý\\nGhi log cảnh báo"]
    E -->|Khớp\\n(≥ 90%)| G["✅ Ghi nhận Check-in\\nLưu ảnh bằng chứng mã hóa"]

    style A fill:#1565C0,color:#fff
    style C fill:#C62828,color:#fff
    style F fill:#C62828,color:#fff
    style G fill:#2E7D32,color:#fff
    style D fill:#F57F17,color:#fff
```'''

idx_start = txt.find(GPS_START)
idx_end   = txt.find(GPS_END)
if idx_start != -1 and idx_end != -1:
    txt = txt[:idx_start] + GPS_MERMAID + txt[idx_end + len(GPS_END):]
    print('[OK] Thay GPS ASCII -> Mermaid')
else:
    print('[WARN] Khong tim thay GPS ASCII block')
    # Debug
    dbg = '**Luồng xác thực:**'
    pos = txt.find(dbg)
    print(f'  "Luong xac thuc" tai: {pos}')
    if pos != -1:
        print(repr(txt[pos:pos+200]))

open(ch05, 'w', encoding='utf-8').write(txt)
print(f'[OK] Ch05: {len(txt.splitlines())} dong')

# ── CH06 ──────────────────────────────────────────────────────────────────────
ch06 = r'chapters\Ch06_CHƯƠNG_4_HIỆN_THỰC_HÓA_VÀ_ĐẢM_BẢO_CHẤT_.md'
txt6 = open(ch06, encoding='utf-8').read()

# 3. Thay Code Quality Pipeline ASCII -> Mermaid flowchart
PIPELINE_START = '```\nQuy trình kiểm soát mã nguồn'
PIPELINE_END   = 'Style check    Bug detect    Code smell      Peer review\n```'

PIPELINE_MERMAID = '''```mermaid
graph LR
    A["✍️ Viết code"] --> B["🔍 Checkstyle\\nStyle check"]
    B --> C["🐛 SpotBugs\\nBug detect"]
    C --> D["📊 SonarLint\\nCode smell"]
    D --> E["👥 Code Review\\nPeer review"]
    E --> F["✅ Merge\\nvào develop"]

    style A fill:#37474F,color:#fff
    style B fill:#1565C0,color:#fff
    style C fill:#C62828,color:#fff
    style D fill:#E65100,color:#fff
    style E fill:#4527A0,color:#fff
    style F fill:#2E7D32,color:#fff
```'''

idx_start = txt6.find(PIPELINE_START)
idx_end   = txt6.find(PIPELINE_END)
if idx_start != -1 and idx_end != -1:
    txt6 = txt6[:idx_start] + PIPELINE_MERMAID + txt6[idx_end + len(PIPELINE_END):]
    print('[OK] Thay Pipeline ASCII -> Mermaid')
else:
    print('[WARN] Khong tim thay Pipeline ASCII block')
    dbg = 'Quy trình kiểm soát'
    pos = txt6.find(dbg)
    print(f'  Found at: {pos}')

# 4. Thay UI Mockup Login -> mo ta hoc thuat
LOGIN_START = '```\n┌──────────────────────────────────────────────┐\n│          🍵  CAFÉ MANAGEMENT SYSTEM'
LOGIN_END   = '└──────────────────────────────────────────────┘\n```'

LOGIN_DESC = '''> **Màn hình Đăng nhập (Login Screen):** Giao diện tối giản gồm hai trường nhập liệu (_Tên đăng nhập_ và _Mật khẩu_) cùng nút _ĐĂNG NHẬP_. Hệ thống áp dụng cơ chế **khóa tài khoản tạm thời 5 phút** sau 3 lần sai liên tiếp và **bắt buộc đổi mật khẩu** ở lần đăng nhập đầu tiên.'''

idx_start = txt6.find(LOGIN_START)
idx_end   = txt6.find(LOGIN_END)
if idx_start != -1 and idx_end != -1:
    txt6 = txt6[:idx_start] + LOGIN_DESC + txt6[idx_end + len(LOGIN_END):]
    print('[OK] Thay Login mockup -> mo ta hoc thuat')
else:
    print('[WARN] Khong tim thay Login mockup')

# 5. Bug tracking workflow ASCII -> danh sach hoc thuat
BUG_START = '```\nPhát hiện lỗi → Ghi nhận vào Issue Tracker'
BUG_END   = '→ Review & Test lại → Merge & Deploy → Đóng Issue\n```'

BUG_DESC = '''Quy trình xử lý lỗi được thực hiện tuần tự qua **6 bước**:

1. **Phát hiện lỗi** — Người dùng hoặc tester ghi nhận lỗi
2. **Ghi nhận** — Tạo Issue trên GitHub Issues kèm mô tả, ảnh chụp màn hình
3. **Phân loại** — Đánh giá mức độ: *Critical* (ảnh hưởng dữ liệu) / *Major* / *Minor*
4. **Phân công xử lý** — Assign cho thành viên phụ trách, fix trên nhánh `hotfix/`
5. **Review & Test lại** — Peer review + chạy unit test trước khi merge
6. **Merge & Đóng Issue** — Deploy và đóng Issue trên GitHub'''

idx_start = txt6.find(BUG_START)
idx_end   = txt6.find(BUG_END)
if idx_start != -1 and idx_end != -1:
    txt6 = txt6[:idx_start] + BUG_DESC + txt6[idx_end + len(BUG_END):]
    print('[OK] Thay Bug tracking ASCII -> mo ta hoc thuat')
else:
    print('[WARN] Khong tim thay Bug tracking ASCII')

open(ch06, 'w', encoding='utf-8').write(txt6)
print(f'[OK] Ch06: {len(txt6.splitlines())} dong')
