## 2025-02-24 - Optimizing large string line splitting

**Learning:** Using `text.replace('\r\n', '\n').split('\n')` on large documents causes catastrophic
full-string memory allocation and severe performance regressions (O(N) operations over large text).
**Action:** Replace manual replacements and splits with `io.StringIO(text, newline=None)` for highly
optimized, lazy C-level line iteration that handles universal newlines efficiently without
allocating new full strings.
