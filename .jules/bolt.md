## 2024-05-14 - Bounded splitting and fast-paths in large text checks
**Learning:** Python's unbounded `.replace(...).split('\n')` on large strings allocates a full array for the entire string, which creates an O(N) memory and performance bottleneck when parsing up to a specific line.
**Action:** Use a fast-path substring check (e.g., `if marker not in text`) combined with bounded splitting using `maxsplit` (e.g., `text.split('\n', safe_line_number)`) and targeted `.replace()` checks (e.g., `if '\r' in text`) to minimize allocations.
