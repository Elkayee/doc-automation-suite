## 2024-05-29 - Optimize regex compilation in MarkdownUtils

**Learning:** `re.sub` compiles the regular expression pattern each time it's called unless it's
available in the internal cache. For patterns used heavily in tight loops (like `r'\s+'` used
repeatedly in `reformat_markdown_document` and `normalize_pasted_markdown`), pre-compiling the regex
as a class attribute avoids repeated cache lookups and compilation overhead, resulting in a
measurable performance improvement for large strings. **Action:** Replace inline
`re.sub(r'\s+', ...)` calls in heavily used functions with a pre-compiled `WHITESPACE_RE.sub(...)`
constant defined at the class level.
