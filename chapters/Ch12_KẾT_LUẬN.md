## KẾT LUẬN

Bài tiểu luận này đã trình bày một cách có hệ thống và toàn diện toàn bộ vòng đời phát triển phần mềm (SDLC) cho Hệ thống Quản lý Quán Café, áp dụng nhất quán các phương pháp luận và công cụ chuẩn mực của ngành Công nghệ phần mềm.

**Tóm tắt thành quả chính:**

| **Chương** | **Giai đoạn SDLC** | **Thành quả chính** |
| --- | --- | --- |
| Chương 1 | Khảo sát & Đặc tả | 12 Yêu cầu chức năng (FR), 6 Yêu cầu phi chức năng (NFR), Ma trận rủi ro |
| Chương 2 | Phân tích & Thiết kế | Class Diagram 5 nhóm lớp, ERD chuẩn 3NF, Sequence/State Diagram, Kiến trúc 3-Tier |
| Chương 3 | Hiện thực & SQA | Tech Stack, Clean Code Pipeline, Tháp kiểm thử, 10+ Test Case, Kế hoạch bảo trì 4 loại |
| Chương 4 | Nghiên cứu UC04 | Đặc tả đầy đủ 5 luồng ngoại lệ, ERD 4 bảng nhân sự, 5 Business Rules, 9 Test Case |

**Bài học rút ra:** Quá trình thực hiện dự án khẳng định một nguyên lý căn bản trong kỹ nghệ phần mềm: _"Đầu tư vào giai đoạn đặc tả và thiết kế tốt sẽ giảm thiểu đáng kể chi phí sửa lỗi ở giai đoạn sau."_ Cụ thể, việc xây dựng Business Rule BR-01 (ngăn ca chồng chéo) bằng Database Trigger thay vì chỉ kiểm tra ở tầng ứng dụng là một quyết định thiết kế có tầm nhìn, đảm bảo toàn vẹn dữ liệu bất kể lỗi từ phía ứng dụng.

**Hướng phát triển tiếp theo:** Hệ thống hiện tại được xây dựng cho mô hình một chi nhánh. Để mở rộng lên quy mô chuỗi (multi-branch), cần nghiên cứu chuyển đổi sang kiến trúc microservices và bổ sung cơ chế đồng bộ dữ liệu phân tán — đây là bài toán nghiên cứu cho học phần Kiến trúc Phần mềm ở các cấp độ cao hơn.
