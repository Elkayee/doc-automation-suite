## 2026-05-07 - Optimize is_line_inside_fenced_block
**Learning:** Using `text.replace('\r\n', '\n').replace('\r', '\n').split('\n')` creates O(N) memory allocations across an entire text buffer and traverses the whole buffer, which is extremely expensive for large markdown files, especially when doing iterative checks (e.g. looking up if a specific line is inside a fence).
**Action:** Replace string splits with iterative `str.find('\n', start_idx)` calls to avoid array allocations and allow breaking out of the parsing loop early as soon as the target line is reached.
