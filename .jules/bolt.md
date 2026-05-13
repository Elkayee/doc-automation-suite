## 2024-05-30 - O(N) allocation bottleneck in parsing text line by line

**Learning:** When checking if a specific line is inside a markdown code fenced block using
`text.split('\n')` across an entire large text buffer, it unconditionally allocates memory and
performs computation for all lines, even if the target line is close to the start or if there are no
fenced blocks in the text at all. **Action:** Always prioritize fast-path structural checks (e.g.,
`if '```' not in text: return False`) and use bounded splits (e.g. `text.split('\n', limit)`) to
minimize allocations when looking up information up to a specific index or line number.
