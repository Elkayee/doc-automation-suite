## 2026-05-24 - Optimizing Line Parsing Memory Allocation

**Learning:** In string parsing functions that only need to process lines up to a certain index
(like checking if line N is in a fenced block), using a full `.split('\n')` on large files causes
unnecessary O(L) list memory allocation. However, trying to use `io.StringIO` introduces trailing
newline edge cases that break backwards compatibility.

**Action:** Use `.split('\n', limit)` to bound memory allocation while strictly preserving
bug-for-bug compatibility with standard `split()` behavior (including handling of trailing empty
strings). Always preserve existing `\r\n` and `\r` replacement logic before splitting to avoid
regressions.
