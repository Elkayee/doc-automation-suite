## 2025-05-28 - Optimize line parsing with bounded split

**Learning:** Using .split('\n') on large strings allocates memory and spends CPU processing the
entire string even if we only need the first few lines. While manual `while` loops using
`.find('\n')` can avoid this, they can be slower in Python and introduce O(L x N) complexity in
worst-case scenarios, or fail to match .split() semantics correctly on trailing newlines.
**Action:** Use Python's bounded split `.split('\n', limit)` to get the performance benefit of
lazy-like evaluation at C-speed, strictly preserving exact behavior (including trailing newline
semantics) without allocating arrays for the entire file. Always preserve preceding string
normalization like `.replace('\r\n', '\n').replace('\r', '\n')`.
