import unittest

from src.core.markdown_utils import MarkdownUtils


class MarkdownListContinuationTests(unittest.TestCase):
    def test_continues_top_level_list_with_configured_marker(self):
        result = MarkdownUtils.get_list_continuation_for_line('- item', ['-', '+', '*'])
        self.assertEqual(result, '\n- ')

    def test_continues_nested_list_with_marker_for_level(self):
        result = MarkdownUtils.get_list_continuation_for_line('  - item', ['-', '+', '*'])
        self.assertEqual(result, '\n  + ')

    def test_exits_list_when_item_is_empty(self):
        result = MarkdownUtils.get_list_continuation_for_line('  + ', ['-', '+', '*'])
        self.assertEqual(result, '\n')

    def test_returns_none_for_non_list_line(self):
        result = MarkdownUtils.get_list_continuation_for_line('regular paragraph', ['-', '+', '*'])
        self.assertIsNone(result)

    def test_indent_list_line_updates_marker_for_new_level(self):
        result = MarkdownUtils.shift_list_line('  + item', 1, ['-', '+', '*'])
        self.assertEqual(result, '    * item')

    def test_indent_prefers_marker_level_when_indent_and_marker_disagree(self):
        result = MarkdownUtils.shift_list_line('  - item', 1, ['-', '+', '*'])
        self.assertEqual(result, '  + item')

    def test_outdent_list_line_updates_marker_for_new_level(self):
        result = MarkdownUtils.shift_list_line('    * item', -1, ['-', '+', '*'])
        self.assertEqual(result, '  + item')

    def test_outdent_top_level_list_line_stays_top_level(self):
        result = MarkdownUtils.shift_list_line('- item', -1, ['-', '+', '*'])
        self.assertEqual(result, '- item')

    def test_shift_non_list_line_returns_original(self):
        result = MarkdownUtils.shift_list_line('paragraph', 1, ['-', '+', '*'])
        self.assertEqual(result, 'paragraph')

    def test_indent_resets_noncanonical_spacing_to_standard(self):
        result = MarkdownUtils.shift_list_line('     + item', 0, ['-', '+', '*'])
        self.assertEqual(result, '  + item')

    def test_reformat_document_normalizes_lists_and_paragraphs(self):
        source = '### Tieu de\n\nDong van thu nhat\ndong van thu hai\n\n     + muc sai indent\n  - muc sai marker\n'
        expected = '### Tieu de\n\nDong van thu nhat dong van thu hai\n\n    * muc sai indent\n  + muc sai marker\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_uses_default_marker_order_when_markers_not_provided(self):
        source = '- parent\n  - child\n    - grandchild\n'
        expected = '- parent\n  + child\n    * grandchild\n'

        result = MarkdownUtils.reformat_markdown_document(source)

        self.assertEqual(result, expected)

    def test_reformat_nests_following_flat_bullets_under_label_only_parent(self):
        source = (
            '- **Thực tiễn áp dụng:**\n'
            '- Dự án sử dụng cơ chế App Router hiện đại.\n'
            '- Tính tái sử dụng được đảm bảo thông qua thư mục src/components/ui/.\n'
        )
        expected = (
            '- **Thực tiễn áp dụng:**\n'
            '  - Dự án sử dụng cơ chế App Router hiện đại.\n'
            '  - Tính tái sử dụng được đảm bảo thông qua thư mục src/components/ui/.\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_starts_new_parent_group_when_next_label_only_item_appears(self):
        source = '- **Thực tiễn áp dụng:**\n- Ví dụ con 1.\n- **Thành phần chính:**\n- Ví dụ con 2.\n'
        expected = '- **Thực tiễn áp dụng:**\n  - Ví dụ con 1.\n- **Thành phần chính:**\n  - Ví dụ con 2.\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_auto_nest_preserves_star_marker_while_only_adjusting_indent(self):
        source = '- **Thực tiễn áp dụng:**\n* Mục con giữ dấu sao.\n'
        expected = '- **Thực tiễn áp dụng:**\n    * Mục con giữ dấu sao.\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_preserves_plantuml_fence_verbatim(self):
        source = (
            '### So do\n\n'
            '```plantuml\n'
            '@startuml\n'
            'Alice -> Bob: hello\n'
            'note right\n'
            '  - must stay raw\n'
            '  + must stay raw\n'
            'end note\n'
            '@enduml\n'
            '```\n\n'
            'Doan 1\n'
            'Doan 2\n'
        )
        expected = (
            '### So do\n\n'
            '```plantuml\n'
            '@startuml\n'
            'Alice -> Bob: hello\n'
            'note right\n'
            '  - must stay raw\n'
            '  + must stay raw\n'
            'end note\n'
            '@enduml\n'
            '```\n\n'
            'Doan 1 Doan 2\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_joins_wrapped_list_item_and_normalizes_terminal_punctuation(self):
        source = (
            '- **Phù hợp với quy mô và cơ cấu tổ chức hiện đại:** Các doanh nghiệp, tập đoàn hiện nay thường hoạt\n'
            'động đa quốc gia và áp dụng mô hình làm việc từ xa (Remote/Hybrid),. Mô hình tập trung không còn phù hợp với một tổ chức có vị trí địa lý phân tán do chi phí đường truyền cao và độ trễ mạng lớn,. CSDL phân tán áp dụng nguyên lý cực đại hóa tiến trình địa phương, đưa dữ liệu về lưu trữ tại node gần với người sử dụng nhất, triệt tiêu độ trễ mạng và nâng cao trải nghiệm truy xuất thời gian thực,.\n'
        )
        expected = '- **Phù hợp với quy mô và cơ cấu tổ chức hiện đại:** Các doanh nghiệp, tập đoàn hiện nay thường hoạt động đa quốc gia và áp dụng mô hình làm việc từ xa (Remote/Hybrid). Mô hình tập trung không còn phù hợp với một tổ chức có vị trí địa lý phân tán do chi phí đường truyền cao và độ trễ mạng lớn. CSDL phân tán áp dụng nguyên lý cực đại hóa tiến trình địa phương, đưa dữ liệu về lưu trữ tại node gần với người sử dụng nhất, triệt tiêu độ trễ mạng và nâng cao trải nghiệm truy xuất thời gian thực.\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_joins_wrapped_ordered_list_item_and_normalizes_terminal_punctuation(self):
        source = '1. Mục đầu tiên bị xuống\ndòng và có lỗi dấu câu,.\n2. Mục thứ hai giữ nguyên.\n'
        expected = '1. Mục đầu tiên bị xuống dòng và có lỗi dấu câu.\n2. Mục thứ hai giữ nguyên.\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_converts_simple_inline_code_terms_to_italic_prose(self):
        source = (
            '- **Ví dụ thực tiễn:** Trong một hệ thống quản lý nhân sự đa quốc gia, bảng người dùng (`Users`) '
            'được áp dụng phân mảnh ngang nguyên thủy thành ba mảnh dựa trên điều kiện của thuộc tính khu vực '
            '(`region`). Kết quả tạo ra ba mảnh: `Users_Asia` cho khu vực Châu Á, `Users_Europe` cho Châu Âu và '
            '`Users_America` cho Châu Mỹ. Một ví dụ khác, bảng dự án `PROJ` có thể được phân mảnh ngang dựa trên '
            'thuộc tính ngân sách, tạo ra mảnh chứa các dự án có `BUDGET <= 200000` và mảnh chứa các dự án có '
            '`BUDGET > 200000`.\n'
        )
        expected = (
            '- **Ví dụ thực tiễn:** Trong một hệ thống quản lý nhân sự đa quốc gia, bảng người dùng (*Users*) '
            'được áp dụng phân mảnh ngang nguyên thủy thành ba mảnh dựa trên điều kiện của thuộc tính khu vực '
            '(*region*). Kết quả tạo ra ba mảnh: *Users Asia* cho khu vực Châu Á, *Users Europe* cho Châu Âu và '
            '*Users America* cho Châu Mỹ. Một ví dụ khác, bảng dự án *PROJ* có thể được phân mảnh ngang dựa trên '
            'thuộc tính ngân sách, tạo ra mảnh chứa các dự án có `BUDGET <= 200000` và mảnh chứa các dự án có '
            '`BUDGET > 200000`.\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_normalize_report_inline_markup_converts_relation_schema_and_strips_code_ticks(self):
        source = (
            'Quan he `PROJ1(PNO, BUDGET)` va `PROJ2(PNO, PNAME, LOC)` duoc tach rieng, '
            'nhung dieu kien `BUDGET <= 200000` van giu dang code.'
        )
        expected = (
            'Quan he *PROJ1(PNO, BUDGET)* va *PROJ2(PNO, PNAME, LOC)* duoc tach rieng, '
            'nhung dieu kien BUDGET <= 200000 van giu dang code.'
        )

        result = MarkdownUtils.normalize_report_inline_markup(source)

        self.assertEqual(result, expected)

    def test_reformat_normalizes_arbitrary_vietnamese_mid_sentence_capitalization(self):
        source = (
            'Em hãy lấy một ví dụ về CSDL Tập trung và một ví dụ về CSDL Phân tán để phân tích sự giống nhau.\n\n'
            'Triển khai thực tế: Công tác khảo sát được thực hiện. Trên cơ sở đó, Đội ngũ phát triển xây dựng '
            'tài liệu Tầm nhìn (Vision). Đồng thời, tài liệu Từ điển dự án (Glossary) cũng được thiết lập.\n'
        )
        expected = (
            'Em hãy lấy một ví dụ về CSDL tập trung và một ví dụ về CSDL phân tán để phân tích sự giống nhau.\n\n'
            'Triển khai thực tế: Công tác khảo sát được thực hiện. Trên cơ sở đó, đội ngũ phát triển xây dựng '
            'tài liệu tầm nhìn (Vision). Đồng thời, tài liệu từ điển dự án (Glossary) cũng được thiết lập.\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_keeps_uppercase_after_colon_sentence_boundary(self):
        source = 'Bước 1: phân rã truy vấn (Query Decomposition) Giai đoạn này đảm nhiệm việc đầu tiên.\n'
        expected = 'Bước 1: Phân rã truy vấn (Query Decomposition)\n\nGiai đoạn này đảm nhiệm việc đầu tiên.\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_splits_paragraph_after_english_parenthetical_before_new_capitalized_clause(self):
        source = 'Bước 1: Phân rã truy vấn (Query Decomposition) Phân tách truy vấn thành các phần nhỏ hơn để xử lý.\n'
        expected = (
            'Bước 1: Phân rã truy vấn (Query Decomposition)\n\nPhân tách truy vấn thành các phần nhỏ hơn để xử lý.\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_splits_after_bold_heading_with_english_parenthetical_before_schedule_clause(self):
        source = (
            '**Bước 4: Tối ưu hóa truy vấn cục bộ (Local Query Optimization)** Lịch trình thực thi phân tán '
            'được chuyển giao về các trạm địa phương.\n'
        )
        expected = (
            '**Bước 4: Tối ưu hóa truy vấn cục bộ (Local Query Optimization)**\n\n'
            'Lịch trình thực thi phân tán được chuyển giao về các trạm địa phương.\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_normalizes_comma_period_before_markdown_closer(self):
        source = (
            '**1. Phân mảnh ngang (Horizontal Fragmentation)** Phân mảnh ngang là quá trình chia các bộ '
            '(dòng) của một quan hệ thành các tập con logic khác biệt nhau,.**\n'
        )
        expected = (
            '**1. Phân mảnh ngang (Horizontal Fragmentation)**\n\n'
            'Phân mảnh ngang là quá trình chia các bộ (dòng) của một quan hệ thành các tập con logic khác biệt nhau.**\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, expected)

    def test_reformat_preserves_dotted_inline_code_identifiers(self):
        source = (
            '- **Thực tiễn áp dụng:**\n'
            '  - **Xác thực (Authentication):** Ứng dụng tích hợp dịch vụ Firebase Authentication '
            '(thông qua `firebase.ts`) để cung cấp tính năng đăng nhập nhanh bằng tài khoản Google (SSO).\n'
            '  - **Giao tiếp máy chủ:** Lớp `apiClient.ts` gửi yêu cầu đến máy chủ Backend '
            '(tại địa chỉ `thanhvtapp.ddns.net`).\n'
        )

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertIn('`firebase.ts`', result)
        self.assertIn('`apiClient.ts`', result)
        self.assertIn('`thanhvtapp.ddns.net`', result)
        self.assertNotIn('`firebase. Ts`', result)
        self.assertNotIn('`apiClient. Ts`', result)
        self.assertNotIn('`thanhvtapp. Ddns. Net`', result)

    def test_reformat_preserves_capitalization_for_bold_member_heading_list_item(self):
        source = '- **Nguyễn Viết Tùng (Lập trình Frontend - UI/UX)**\n'

        result = MarkdownUtils.reformat_markdown_document(source, ['-', '+', '*'])

        self.assertEqual(result, source)

    def test_detects_line_inside_fenced_block(self):
        text = '### So do\n\n```plantuml\n@startuml\nAlice -> Bob: hello\n```\n'

        self.assertTrue(MarkdownUtils.is_line_inside_fenced_block(text, 4))
        self.assertFalse(MarkdownUtils.is_line_inside_fenced_block(text, 1))

    def test_normalize_pasted_markdown_preserves_plantuml_block(self):
        source = '```plantuml\n@startuml\nAlice -> Bob: hello\nnote right\n  - keep this\nend note\n@enduml\n```\n'

        result = MarkdownUtils.normalize_pasted_markdown(source)

        self.assertEqual(result, source)

    def test_normalize_pasted_markdown_converts_unicode_bullets_and_wrapped_lines(self):
        source = (
            'Phan mem quan ly gui xe duoc mo ta nhu sau:\n'
            '▪ Moi bai xe co ma bai, ten bai, suc chua toi da, loai xe ho tro (xe may, o\n'
            'to), mo ta.\n'
            '▪ Phi gui xe duoc tinh theo thoi gian:\n'
            '✓ Duoi 2 gio: gia co dinh\n'
            '✓ Tren 2 gio: tinh theo gio\n'
            '▪ Neu mat ve, khach phai tra phi phat co dinh.6\n'
            'Thuc hien module.\n'
        )
        expected = (
            'Phan mem quan ly gui xe duoc mo ta nhu sau:\n\n'
            '- Moi bai xe co ma bai, ten bai, suc chua toi da, loai xe ho tro (xe may, o to), mo ta.\n'
            '- Phi gui xe duoc tinh theo thoi gian:\n'
            '  - Duoi 2 gio: gia co dinh\n'
            '  - Tren 2 gio: tinh theo gio\n'
            '- Neu mat ve, khach phai tra phi phat co dinh.\n\n'
            '6. Thuc hien module.\n'
        )

        result = MarkdownUtils.normalize_pasted_markdown(source)

        self.assertEqual(result, expected)

    def test_normalize_pasted_markdown_normalizes_mid_sentence_vietnamese_capitalization(self):
        source = (
            'Triển khai thực tế: Công tác khảo sát được thực hiện để làm rõ nhu cầu của chủ đầu tư.\n'
            'Trên cơ sở đó, Đội ngũ phát triển xây dựng tài liệu Tầm nhìn (Vision) nhằm xác lập mục tiêu cốt lõi.\n'
        )
        expected = (
            'Triển khai thực tế: Công tác khảo sát được thực hiện để làm rõ nhu cầu của chủ đầu tư. '
            'Trên cơ sở đó, đội ngũ phát triển xây dựng tài liệu tầm nhìn (Vision) nhằm xác lập mục tiêu cốt lõi.\n'
        )

        result = MarkdownUtils.normalize_pasted_markdown(source)

        self.assertEqual(result, expected)

    def test_is_line_inside_fenced_block_when_line_is_outside(self):
        text = "```\ncode\n```\noutside"
        self.assertFalse(MarkdownUtils.is_line_inside_fenced_block(text, 4))

    def test_is_line_inside_fenced_block_when_line_is_inside(self):
        text = "```\ncode\n```\noutside"
        self.assertTrue(MarkdownUtils.is_line_inside_fenced_block(text, 2))

    def test_is_line_inside_fenced_block_when_line_is_fence_start(self):
        text = "```\ncode\n```\noutside"
        self.assertFalse(MarkdownUtils.is_line_inside_fenced_block(text, 1))

    def test_is_line_inside_fenced_block_when_line_is_fence_end(self):
        text = "```\ncode\n```\noutside"
        self.assertFalse(MarkdownUtils.is_line_inside_fenced_block(text, 3))


if __name__ == '__main__':
    unittest.main()
