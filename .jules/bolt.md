## 2025-02-28 - Optimize line splitting during fenced code block check

**Learning:** Checking line numbers or markers on large text blocks using
`text.replace('\r\n', '\n').replace('\r', '\n').split('\n')` creates severe memory allocations
because it duplicates the entire string in memory as an array. This causes an unnecessary O(N)
penalty and memory bloat. **Action:** Replace full string splitting with iterative substring
searching using `str.find('\n', start_idx)` coupled with line-by-line checks. This preserves
original strings and dramatically decreases processing overhead.
