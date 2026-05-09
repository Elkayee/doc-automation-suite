## 2024-05-24 - Unbounded string splitting in markdown parsing

**Learning:** When parsing text up to a specific line, unbounded `text.replace(...).split('\n')`
allocates a full array for the entire string, creating memory and computation overhead on large text
buffers. **Action:** Avoid manual iterative `str.find('\n')` loops as they are slower in Python;
instead, use a fast-path substring check (`if marker not in text: return`) combined with bounded
splitting using `maxsplit` (e.g., `text.split('\n', safe_line_number)`).
