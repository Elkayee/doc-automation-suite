## 2024-05-09 - Fast-path code fence optimization

**Learning:** In `src/core/markdown_utils.py`, `is_line_inside_fenced_block` split an entire
markdown string up to its end `text.replace('\r\n', '\n').replace('\r', '\n').split('\n')`. For huge
strings being processed in a loop, unbounded list allocation scales as O(N^2) memory footprint and
time delay over a document loop. **Action:** Always start strings scans with an O(1) quick-check
like `if marker not in text: return False`. Bounding line processing with `text.split('\n', limit)`
also constrains heap allocations safely when quick checks fail.
