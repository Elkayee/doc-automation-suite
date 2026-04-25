# fix_headings.py — Sua lai heading cho Ch05 va Ch06
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ===== CH05: them ## heading, doi UC06->UC04, xoa duplicate headings =====
ch05_path = r'chapters\Ch05_CHƯƠNG_3_NGHIÊN_CỨU_CHUYÊN_SÂU_—_UC06_.md'

with open(ch05_path, encoding='utf-8') as f:
    txt = f.read()

# 1. Them heading ## truoc dong dau tien
header = """## CHƯƠNG 3: NGHIÊN CỨU CHUYÊN SÂU — UC04: QUẢN LÝ CA LÀM VIỆC, CHẤM CÔNG & PHÂN QUYỀN

> **Trái tim của báo cáo — Chiếm ~50%.** Đặc tả đầy đủ nghiệp vụ UC04 do **Nguyễn Viết Tùng** phụ trách: phân công ca, check-in/out sinh trắc học, tính lương đa biến NĐ38 và phân quyền RBAC.

"""
txt = header + txt

# 2. Fix cac heading con: doi UC06 -> UC04 trong heading
txt = txt.replace('### 3.1. Biểu đồ Use Case Chi tiết UC06',
                  '### 3.1. Biểu đồ Use Case Chi tiết UC04')
txt = txt.replace('### 3.2. Quản lý Tài khoản và Phân quyền RBAC',
                  '### 3.2. Quản lý Tài khoản, Phân quyền RBAC và Onboarding')
txt = txt.replace('### 3.3. Đặc tả Use Case Chi tiết — Check-in và Check-out',
                  '### 3.3. Đặc tả Use Case — Check-in, Check-out và Tính lương')
# Cac heading 3.8 den 3.10 da ok
txt = txt.replace('### 3.8. Biểu đồ Tuần tự (Sequence Diagram) — Luồng Check-in',
                  '### 3.8. Biểu đồ Tuần tự — Luồng Check-in (Sequence Diagram)')
txt = txt.replace('### 3.9. Biểu đồ Hoạt động (Activity Diagram) — Quy trình Chấm công Toàn luồng',
                  '### 3.9. Biểu đồ Hoạt động — Quy trình Chấm công (Activity Diagram)')
txt = txt.replace('### 3.10. Biểu đồ Hoạt động — Quy trình Onboarding Nhân viên Mới',
                  '### 3.10. Biểu đồ Hoạt động — Quy trình Onboarding Nhân viên Mới (Activity Diagram)')

with open(ch05_path, 'w', encoding='utf-8') as f:
    f.write(txt)
print(f'[OK] Ch05: {len(txt.splitlines())} dong')

# ===== CH06: Giu heading 4.x, xoa heading 3.x/5.x cu =====
ch06_path = r'chapters\Ch06_CHƯƠNG_4_HIỆN_THỰC_HÓA_VÀ_ĐẢM_BẢO_CHẤT_.md'

with open(ch06_path, encoding='utf-8') as f:
    lines = f.readlines()

OLD_H = re.compile(r'^(###|####) [35]\.')   # heading 3.x, 5.x cu -> xoa
result = []
i = 0
while i < len(lines):
    line = lines[i]
    # Xoa heading cu 3.x va 5.x
    if OLD_H.match(line):
        i += 1
        continue
    # Fix heading trung "### 4.4. Test Case — UC06" -> bo vi co "### 4.5." sau do
    if line.strip() == '### 4.4. Test Case — UC06: Check-in / Check-out':
        # Merge vao 4.4 chuan
        i += 1
        continue
    result.append(line)
    i += 1

txt6 = ''.join(result)

# Doi ten heading cho chuan
txt6 = txt6.replace('### 4.1. Ngăn xếp Công nghệ và Tiêu chuẩn Lập trình',
                    '### 4.1. Ngăn xếp Công nghệ và Tiêu chuẩn Lập trình (Tech Stack)')
txt6 = txt6.replace('### 4.3. Mô hình Tháp Kiểm thử (Testing Pyramid)',
                    '### 4.3. Mô hình Tháp Kiểm thử và Chiến lược SQA')
txt6 = txt6.replace('### 4.4. Test Case — UC06: Check-in / Check-out',
                    '### 4.4. Test Case — UC04: Check-in / Check-out')
txt6 = txt6.replace('### 4.5. Kiểm thử Use Case UC04',
                    '### 4.5. Test Case — Tính lương và Phân quyền RBAC')
txt6 = txt6.replace('### 4.5. Test Case — Tính lương và Phân quyền',
                    '')  # xoa heading trung
txt6 = txt6.replace('### 4.6. Kế hoạch SQA và Bảo trì',
                    '### 4.6. Kế hoạch SQA và Bảo trì (Maintenance Plan)')

with open(ch06_path, 'w', encoding='utf-8') as f:
    f.write(txt6)
print(f'[OK] Ch06: {len(txt6.splitlines())} dong')
