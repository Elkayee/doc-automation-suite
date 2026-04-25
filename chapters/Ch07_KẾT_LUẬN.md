## KẾT LUẬN

Báo cáo đã trình bày hệ thống Quản lý Quán Café theo chiến lược **T-shaped**: bao quát toàn bộ 6 phân hệ Use Case ở mức tổng quan, đồng thời đào sâu chuyên sâu vào **UC04 — Quản lý Ca làm việc & Chấm công** do Nguyễn Viết Tùng phụ trách.

**Tóm tắt thành quả chính:**

| **Chương** | **Nội dung**       | **Thành quả**                                                                       |
| :--------: | ------------------ | ----------------------------------------------------------------------------------- |
|  Chương 1  | Tổng quan hệ thống | Biểu đồ 6 UC, bảng FR/NFR, phân công 5 thành viên                                   |
|  Chương 2  | Kiến trúc & CSDL   | Kiến trúc 3-Tier, ERD 5 nhóm bảng, trọng tâm UC04                                   |
|  Chương 3  | Chuyên sâu UC04    | Đặc tả 5+ luồng ngoại lệ, RBAC, Payroll Engine NĐ38, Sinh trắc học GPS/FaceID, 5 BR |
|  Chương 4  | Hiện thực & SQA    | UI mockup nhân sự, 9+ Test Case chấm công/lương/RBAC, kế hoạch bảo trì              |

**Bài học cốt lõi từ UC04:**

1. **Tách Kế hoạch khỏi Thực tế:** Tách `ShiftAssignment` (kế hoạch phân ca) khỏi `Attendance` (giờ thực tế) là quyết định thiết kế then chốt — cho phép đối soát chênh lệch (đi muộn/về sớm) và kiểm toán lao động minh bạch.
2. **Business Rules ở tầng CSDL:** Đặt các ràng buộc (BR-01 đến BR-05) dưới dạng Trigger và Constraint ở tầng CSDL — đảm bảo toàn vẹn dữ liệu bất kể lỗi từ tầng ứng dụng.
3. **Chống chấm công hộ:** Kết hợp GPS Geofencing (lớp 1 — vị trí) + FaceID (lớp 2 — danh tính) tạo thành hai lớp bảo vệ hiệu quả mà không xâm phạm quyền lợi người lao động.

**Hướng phát triển tiếp theo:** Các phân hệ nâng cao (RBAC đầy đủ, AI phân ca thông minh, chấm công QR Code) đã được đặc tả tại Chương 3 — sẵn sàng để phiên bản sau triển khai mà không cần làm lại từ đầu.

---
