## 2026-05-09 - Markdown Utility Parsing Bottleneck

**Learning:** In string parsing methods like `is_line_inside_fenced_block`, replacing character sets
and splitting by newlines without a `maxsplit` argument processes the entire file contents
unnecessarily, causing O(N) allocation and slowdowns, particularly on huge markdown files where you
only want to know about early lines. **Action:** Always add early exits (e.g.,
`if '```' not in text: return False`) to completely skip allocations when elements don't exist.
Apply `maxsplit` arguments (`text.split('\n', limit)`) when parsing strings line-by-line where only
the first N lines are needed.
