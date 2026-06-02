## 2024-12-05 - Avoid str.replace().split() memory allocation in Python
**Learning:** Using `text.replace('\r\n', '\n').replace('\r', '\n').split('\n', limit)` on large strings still allocates the entire modified string in memory before the split happens. This causes O(N) memory allocation on every keystroke in a UI, leading to significant latency.
**Action:** Use a lazily evaluated regular expression iterator (`re.finditer(r'\r\n|\r|\n', text)`) to slice lines iteratively, preventing full-document memory allocation while correctly identifying lines with multiple line ending formats.
