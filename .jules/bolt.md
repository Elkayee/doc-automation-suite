## 2024-05-24 - Unbounded string splitting anti-pattern with text limits

**Learning:** When parsing markdown, operations like `text.split('\n')` without a limit on text up
to a specific line (e.g., `is_line_inside_fenced_block`) will unnecessarily allocate memory and
process the entire document even if the target line is near the beginning. Unbounded replace
operations (`text.replace...`) before the split make this worse. A fast path check like
`if '```' not in text: return False` is highly effective when the target token isn't present.
**Action:** Use a fast path check when the target substring might not exist. If a line limit is
known, use `maxsplit` (e.g., `text.split('\n', safe_line_number)`) instead of splitting the entire
string, preventing O(N) allocation on large strings when only evaluating up to a limit.
