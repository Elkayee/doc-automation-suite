## 2024-10-30 - Optimize `is_line_inside_fenced_block`

**Learning:** `text.replace('\r\n', '\n').replace('\r', '\n').split('\n')` creates severe memory and
computation overhead on large strings, specifically because it replaces and splits the entire text
even when processing up to a specific, early `line_number`. **Action:** Use bounded limits
(`text.split('\n', limit)`) to minimize allocations, wrap `replace` with a fast-path substring check
(`if '\r' in text:`), and prioritize an initial `if marker not in text: return` to skip processing
entirely if possible. Be sure to handle the final chunk of the bounded split array (using
`line.split('\n', 1)[0]`), as it contains the remainder of the text.
