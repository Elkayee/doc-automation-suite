## 2024-05-26 - Optimize string line parsing in large documents

**Learning:** Using `text.replace().split('\n')` creates large memory allocations and scans the
entire document. Using `io.StringIO(text, newline=None)` provides lazy, memory-efficient C-level
line iteration that handles universal newlines natively without copying strings. **Action:** When
parsing specific lines from a large string, use `io.StringIO` with `newline=None` for optimal
performance.
