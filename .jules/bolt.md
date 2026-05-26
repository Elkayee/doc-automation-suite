## 2024-05-26 - Optimize line parsing memory usage in MarkdownUtils

**Learning:** Using `text.replace('\r\n', '\n').replace('\r', '\n').split('\n')` for large texts
forces Python to allocate massive temporary string lists, leading to memory and CPU spikes.
`io.StringIO(text, newline=None)` provides zero-allocation lazy streaming of lines and handles
universal newlines efficiently at the C level. **Action:** Use `io.StringIO(text, newline=None)`
when iterating over lines of large text blocks in Python instead of replacing line endings and
splitting the entire string into memory.
