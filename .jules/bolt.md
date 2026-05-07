## 2024-05-07 - Avoid full split for line checks
**Learning:** Checking properties of a single line by performing `text.split('\n')` creates O(N) memory allocation and O(N) execution overhead by processing the whole file.
**Action:** Use string find logic (`text.find('\n', start_idx)`) combined with a fast-path condition (e.g., `if '```' not in text: return False`) to short circuit early, converting an O(N) allocation into an O(1) memory approach.
