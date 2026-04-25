# build_tshape_report.py
# Doc file bao cao goc, trich xuat theo dong, ghep lai thanh bao cao T-shaped moi

import re

SRC = "Bao_Cao_Tieu_Luan_NMCNPM.md"
DST = "Bao_Cao_TShape_UC4.md"

# Doc toan bo file goc
with open(SRC, encoding="utf-8") as f:
    raw = f.read()

lines = raw.split("\n")

def get_lines(start, end):
    """Lay tu dong start den end (1-indexed, inclusive)."""
    return "\n".join(lines[start - 1 : end])

# ============================================================
# XAY DUNG NOI DUNG BAO CAO MOI
# ============================================================
parts = []

# ---- TRANG BIA & LOI MO DAU --------------------------------
parts.append("""\
# TIỂU LUẬN: KHẢO SÁT, PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG QUẢN LÝ QUÁN CAFÉ

**Môn học:** Nhập môn Công nghệ phần mềm  
**Phạm vi nghiên cứu chuyên sâu:** Quản lý Ca làm việc và Chấm công (UC04)  
**Thành viên phụ trách UC04:** Nguyễn Viết Tùng  
**Chiến lược báo cáo:** T-shaped — Bao quát toàn hệ thống, đào sâu UC04

---

## LỜI MỞ ĐẦU
""")
# Lay loi mo dau tu file goc (dong 12)
parts.append(get_lines(12, 13))

parts.append("""
---

## MỞ ĐẦU: KẾ HOẠCH QUẢN LÝ DỰ ÁN (SPMP TÓM TẮT)
""")
# Phan phân bổ nhiem vu (dong 52-93)
parts.append(get_lines(52, 93))

# ---- CHUONG 1: TONG QUAN (10%) ----------------------------
parts.append("""
---

## CHƯƠNG 1: TỔNG QUAN HỆ THỐNG VÀ PHÂN CÔNG NHÓM

> **Mục tiêu chương:** Trình bày bức tranh toàn cảnh của hệ thống — 5 phân hệ Use Case, kiến trúc tổng thể và phân công nhóm. Phần này chiếm ~10% báo cáo.

### 1.1. Bối cảnh và Tầm nhìn Dự án
""")
# Lay muc tieu du an (dong 18-27)
parts.append(get_lines(18, 27))

parts.append("""
### 1.2. Biểu đồ Use Case Tổng quát — Phạm vi 5 Phân hệ
""")
# Lay bieu do UC tong quat (dong 165-213)
parts.append(get_lines(165, 213))

parts.append("""
### 1.3. Bảng Tóm tắt Chức năng Toàn Hệ thống

| **UC** | **Phân hệ** | **Chức năng cốt lõi** | **Người phụ trách** | **Mức độ chi tiết trong báo cáo này** |
|--------|-------------|----------------------|---------------------|---------------------------------------|
| UC01 | Thực đơn & Đồ uống | CRUD sản phẩm, nhóm, topping, công thức pha chế | Bảo | Tóm tắt |
| UC02 | Đơn hàng & Bàn | Tạo/sửa đơn, quản lý trạng thái bàn theo thời gian thực | Thành | Tóm tắt |
| UC03 | Thanh toán & Hóa đơn | Xử lý thanh toán đa kênh, in hóa đơn nhiệt | Thành | Tóm tắt |
| UC05 | Kho & Nguyên liệu | Nhập kho, trừ tồn theo công thức, cảnh báo ngưỡng | Nguyễn Quang Đạo | Tóm tắt |
| UC07 | Báo cáo & Cửa hàng | Thống kê doanh thu, top sản phẩm, quản lý chi nhánh | Hồng Nhung | Tóm tắt |
| **UC06** | **Nhân sự & Chấm công** | **Hồ sơ NV, phân ca, GPS check-in/out, tính lương NĐ38** | **Nguyễn Viết Tùng** | **⭐ Phân tích chuyên sâu (Chương 3)** |

### 1.4. Yêu cầu Chức năng và Phi chức năng (Tóm tắt)
""")
# Lay bang FR (dong 199-250)
parts.append(get_lines(199, 250))

# ---- CHUONG 2: KIEN TRUC & CSDL (15%) --------------------
parts.append("""
---

## CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC VÀ CƠ SỞ DỮ LIỆU

> **Mục tiêu chương:** Trình bày kiến trúc triển khai 3 tầng và ERD tập trung vào nhóm bảng UC04 (Nhân sự). Chiếm ~15% báo cáo.

### 2.1. Kiến trúc Triển khai 3 Tầng (Three-Tier Architecture)
""")
# Lay kien truc 3 tier (dong 420-474)
parts.append(get_lines(420, 474))

parts.append("""
### 2.2. Tổng quan Lược đồ CSDL — Nhóm Bảng Toàn Hệ thống

Hệ thống gồm **5 nhóm bảng** tương ứng với 5 phân hệ UC, đều chuẩn hóa 3NF:

| **Nhóm bảng** | **Bảng chính** | **UC sử dụng** |
|---|---|---|
| Thực đơn | `do_uong`, `nhom_do_uong`, `topping`, `cong_thuc` | UC01 |
| Giao dịch | `hoa_don`, `hoa_don_chi_tiet`, `ban`, `khu_vuc` | UC02, UC03 |
| Kho | `nguyen_lieu`, `nhap_kho`, `canh_bao_kho` | UC05 |
| Báo cáo | `bao_cao_doanh_thu`, `chi_phi`, `danh_sach_cua_hang` | UC07 |
| **Nhân sự** *(trọng tâm)* | **`nhan_vien`, `tai_khoan`, `shift_template`, `shift`, `shift_assignment`, `attendance`** | **UC06** |

> **Snapshot nguyên tắc:** Trường `luong_gio_tai_thoi_diem` trong bảng `bang_luong_chi_tiet` được lưu cứng tại kỳ tính lương — đảm bảo lịch sử tài chính không bị ảnh hưởng khi mức lương thay đổi.

### 2.3. ERD Chi tiết — Nhóm Bảng Nhân sự (UC06)
""")
# Lay ERD nhan su UC04 (dong 951-994)
parts.append(get_lines(951, 1006))

# ---- CHUONG 3: CHUYEN SAU UC04 (50%) ---------------------
parts.append("""
---

## CHƯƠNG 3: NGHIÊN CỨU CHUYÊN SÂU — UC06: QUẢN LÝ NHÂN SỰ, PHÂN QUYỀN & CHẤM CÔNG

> **Trái tim của báo cáo — Chiếm ~50%.** Chương này trình bày toàn bộ phân tích nghiệp vụ, thiết kế hành vi, quy tắc kinh doanh và cơ chế bảo mật của phân hệ Nhân sự do Nguyễn Viết Tùng phụ trách. Nội dung hợp nhất cả chấm công (UC04 cũ) và quản lý tài khoản/RBAC (UC07 cũ) thành một phân hệ nhất quán.
""")

parts.append("""
### 3.1. Biểu đồ Use Case Chi tiết UC06
""")
# Bieu do UC04 chi tiet (dong 765-802)
parts.append(get_lines(765, 803))

parts.append("""
### 3.2. Quản lý Tài khoản và Phân quyền RBAC

> Quyền truy cập hệ thống là tiền điều kiện của mọi luồng nghiệp vụ trong UC06. Phân hệ RBAC được tích hợp trực tiếp vào đây thay vì để riêng.
""")
# Lay noi dung RBAC tu chuong 5 (dong 1151-1250)
parts.append(get_lines(1151, 1250))

parts.append("""
### 3.3. Đặc tả Use Case Chi tiết — Check-in và Check-out
""")
# Dac ta UC04.3 (dong 807-840)
parts.append(get_lines(807, 860))

parts.append("""
### 3.4. Xử lý Ngoại lệ Thông minh
""")
# Shift swapping + Quen checkout (dong 862-913)
parts.append(get_lines(862, 913))

parts.append("""
### 3.5. Cơ chế Chấm công Sinh trắc học — Triệt tiêu Chấm công Hộ
""")
# Sinh trac hoc (dong 896-913) — da trong 3.4, lay tu 914
parts.append(get_lines(894, 945))

parts.append("""
### 3.6. Payroll Engine Đa biến — Tuân thủ NĐ 38/2022/NĐ-CP
""")
# Payroll engine (dong 917-944)
parts.append(get_lines(917, 1006))

parts.append("""
### 3.7. Business Rules và Ràng buộc Nghiệp vụ
""")
# BR UC04 (dong 997-1005) + BR NS tu ch5 (dong 1371-1383)
parts.append(get_lines(997, 1006))
parts.append("\n**Business Rules bổ sung — Quản lý Tài khoản:**\n")
parts.append(get_lines(1371, 1383))

parts.append("""
### 3.8. Biểu đồ Tuần tự (Sequence Diagram) — Luồng Check-in
""")
# Sequence diagram tu ch5 (dong 1237-1275)
parts.append(get_lines(1237, 1275))

parts.append("""
### 3.9. Biểu đồ Hoạt động (Activity Diagram) — Quy trình Chấm công Toàn luồng
""")
# Activity diagram (dong 1009-1056)
parts.append(get_lines(1009, 1057))

parts.append("""
### 3.10. Biểu đồ Hoạt động — Quy trình Onboarding Nhân viên Mới
""")
# Onboarding activity (dong 1276-1313)
parts.append(get_lines(1276, 1314))

# ---- CHUONG 4: HIEN THUC & SQA (25%) ---------------------
parts.append("""
---

## CHƯƠNG 4: HIỆN THỰC HÓA VÀ ĐẢM BẢO CHẤT LƯỢNG (SQA)

> **Mục tiêu chương:** Chứng minh hệ thống chạy được và không có bug. Tập trung vào giao diện và test case của phân hệ Nhân sự/Chấm công. Chiếm ~25%.

### 4.1. Ngăn xếp Công nghệ và Tiêu chuẩn Lập trình
""")
# Tech stack + code quality (dong 589-630)
parts.append(get_lines(589, 630))

parts.append("""
### 4.2. Thiết kế Giao diện — Màn hình Nhân sự và Chấm công

#### 4.2.1. Màn hình Đăng nhập

```
┌──────────────────────────────────────────────┐
│          🍵  CAFÉ MANAGEMENT SYSTEM          │
│                                              │
│   Tên đăng nhập: [_________________________]│
│   Mật khẩu:      [_________________________]│
│                                              │
│              [  ĐĂNG NHẬP  ]                 │
│                                              │
│   Phiên bản 1.0.0   |  © 2025 CaféSoft     │
└──────────────────────────────────────────────┘
```

_Sau 3 lần đăng nhập sai: tài khoản bị khoá tạm 5 phút. Lần đầu đăng nhập bắt buộc đổi mật khẩu._

#### 4.2.2. Màn hình Dashboard Nhân viên — Chấm công

```
┌──────────── DASHBOARD NHÂN VIÊN ───────────────────┐
│  👤 Nguyễn Viết Tùng  |  Ca: 08:00 – 17:00         │
│  📍 Vị trí: Trong vùng cho phép (GPS ✅)            │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │   🟢  [   CHECK-IN   ]   ⏰ 07:58            │   │
│  │   ⬜  [   CHECK-OUT  ]   (chưa kích hoạt)   │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  📅 LỊCH LÀM VIỆC TUẦN NÀY:                         │
│  ┌───────┬──────────────┬────────────┬──────────┐   │
│  │ Ngày  │ Ca           │ Trạng thái │ Giờ công │   │
│  ├───────┼──────────────┼────────────┼──────────┤   │
│  │ T2    │ 08:00–17:00  │ ✅ Đúng giờ│ 8.0h     │   │
│  │ T3    │ 08:00–17:00  │ ⚠️ Đến muộn│ 7.8h     │   │
│  │ T4    │ 12:00–21:00  │ ⏳ Hôm nay │ —        │   │
│  └───────┴──────────────┴────────────┴──────────┘   │
│                                                     │
│  💰 Tổng giờ tháng: 142.5h  |  Ước lương: 3.56M   │
└─────────────────────────────────────────────────────┘
```

#### 4.2.3. Màn hình Quản lý Nhân viên (dành cho Manager)

```
┌──────────────── QUẢN LÝ NHÂN VIÊN ────────────────────────┐
│  [+ Thêm NV]  [🔍 Tìm kiếm]  [📊 Báo cáo chuyên cần]      │
├──────┬────────────────┬──────────┬──────────┬─────────────┤
│  ID  │ Họ tên         │ Vai trò  │ Trạng thái│ Hành động  │
├──────┼────────────────┼──────────┼──────────┼─────────────┤
│  001 │ Nguyễn V. Tùng │ CASHIER  │ 🟢 Đang làm│ [Sửa][Khoá]│
│  002 │ Trần Thị B     │ WAITER   │ ⏸ Nghỉ phép│ [Sửa][Khoá]│
│  003 │ Lê Văn C       │ MANAGER  │ 🟢 Đang làm│ [Sửa]      │
└──────┴────────────────┴──────────┴──────────┴─────────────┘
```

### 4.3. Mô hình Tháp Kiểm thử (Testing Pyramid)
""")
# Testing pyramid (dong 633-651)
parts.append(get_lines(633, 651))

parts.append("""
### 4.4. Test Case — UC06: Check-in / Check-out
""")
# Test case UC04 (dong 1061-1080)
parts.append(get_lines(1061, 1080))

parts.append("""
### 4.5. Test Case — Tính lương và Phân quyền
""")
# Test case luong (dong 1073-1080) + RBAC (dong 1392-1405)
parts.append(get_lines(1073, 1080))
parts.append("\n**Test Case — Phân quyền RBAC:**\n")
parts.append(get_lines(1392, 1406))

parts.append("""
### 4.6. Kế hoạch SQA và Bảo trì
""")
# SQA plan (dong 721-755)
parts.append(get_lines(721, 756))

# ---- KET LUAN & TAI LIEU THAM KHAO -----------------------
parts.append("""
---

## KẾT LUẬN

Báo cáo đã trình bày hệ thống Quản lý Quán Café theo chiến lược **T-shaped**: bao quát toàn bộ 5 phân hệ UC ở mức tổng quan, đồng thời đào sâu chuyên sâu vào **UC06 — Nhân sự & Chấm công**.

**Tóm tắt thành quả chính:**

| **Chương** | **Nội dung** | **Thành quả** |
|---|---|---|
| Chương 1 | Tổng quan hệ thống | Biểu đồ UC 6 phân hệ, bảng FR/NFR, phân công nhóm |
| Chương 2 | Kiến trúc & CSDL | Kiến trúc 3-Tier, ERD 5 nhóm bảng, trọng tâm nhân sự |
| Chương 3 | Chuyên sâu UC06 | Đặc tả 5+ luồng ngoại lệ, RBAC, Payroll Engine NĐ38, Sinh trắc học, 5 BR |
| Chương 4 | Hiện thực & SQA | UI mockup nhân sự, 9+ Test Case chấm công/lương/RBAC, kế hoạch bảo trì |

**Bài học cốt lõi:** Tách biệt `ShiftAssignment` (kế hoạch) khỏi `Attendance` (thực tế) là quyết định thiết kế then chốt — cho phép đối soát, phát hiện sai lệch và kiểm toán lao động minh bạch. Kết hợp GPS Geofencing + FaceID tạo thành hai lớp chống chấm công hộ hiệu quả mà không xâm phạm quyền lợi người lao động.

---

## TÀI LIỆU THAM KHẢO
""")
# Tai lieu tham khao (dong 1459-1467)
parts.append(get_lines(1459, 1467))

# ============================================================
# XUAT FILE
# ============================================================
output = "\n".join(parts)
with open(DST, "w", encoding="utf-8") as f:
    f.write(output)

print(f"[OK] Da tao file: {DST}")
print(f"     So dong: {len(output.splitlines())}")
print(f"     Kich thuoc: {len(output.encode('utf-8')) // 1024} KB")
