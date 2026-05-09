## 2025-02-18 - Optimize unbounded string splitting in Markdown parsing

**Learning:** When parsing text up to a specific line number (like in
`is_line_inside_fenced_block`), using an unbounded `text.split('\n')` on large documents allocates a
full array for the entire string, which creates a severe memory and computation bottleneck (O(N) for
the whole text). **Action:** Always optimize string parsing functions that only need to process a
prefix by:

1. Adding a fast-path substring check (e.g., `if '```' not in text: return False`) to avoid any
   allocation if the structural marker isn't even present.
2. Using the `maxsplit` parameter in `split()` (e.g., `text.split('\n', safe_line_number)`) to bound
   the processing to only the necessary portion of the text, preventing full-document allocations.
