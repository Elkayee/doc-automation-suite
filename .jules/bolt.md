## 2024-05-23 - Fast-path Substring Checks

**Learning:** Chaining string `replace()` calls on large text buffers (e.g.
`text.replace('\r\n', '\n').replace('\r', '\n')`) performs unnecessary full-string buffer traversals
even when the target characters are absent. **Action:** When chaining `str.replace()` calls, wrap
the operation in a fast-path substring check (e.g. `if '\r' in text:`) to bypass unnecessary Python
method overhead and buffer traversals when the characters are not present.
