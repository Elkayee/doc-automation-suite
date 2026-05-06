## 2025-02-24 - [Avoid Unbounded `.split()` on Large Text Editor Buffers]

**Learning:** Frequent UI actions (like typing 'Return' or 'Shift+Tab') called
`MarkdownUtils.is_line_inside_fenced_block` on the entire editor content. In large documents, doing
an unbounded `.split('\n')` creates thousands of small string allocations and tanks performance even
when checking early lines. **Action:** When inspecting lines in large text blobs, always use a fast
path (`if substr not in text: return`) and bounded splits (`text.split('\n', limit)`) to minimize
memory allocation overhead.
