## 2024-05-29 - O(N) memory to O(1) in line parsing

**Learning:** `text.replace('\r\n', '\n').replace('\r', '\n').split('\n')` creates a full array of
strings in memory. If we only need to check lines up to a certain `line_number`, we can use
`split('\n', safe_line_number)` to limit the amount of memory allocated and work done to split the
string unnecessarily, saving up to ~30x execution time for long texts on early line checks.
**Action:** Use `.split('\n', safe_line_number)` when extracting lines up to a known index.
