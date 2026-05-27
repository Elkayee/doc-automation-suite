## 2024-05-27 - Optimize large string parsing in line-by-line checks

**Learning:** Parsing large markdown files string by replacing newlines
(`str.replace('\r\n', '\n').split('\n')`) can cause severe memory allocations and slow down line
iteration loops if we only need a few lines. Furthermore, iterating over lines looking for block
starts (like code fences) can be short-circuited if the block marker isn't in the string at all.
**Action:** Use an early return `if '```' not in text:` to skip line-by-line checks entirely for
files without code blocks. For the fallback, use `io.StringIO(text, newline=None)` instead of string
replace/split for lazy, C-level optimized line parsing.
