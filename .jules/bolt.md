## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.

## 2024-06-03 - Optimize Python Whitespace Normalization

**Learning:** Using `str.split()` combined with `' '.join()` is significantly faster (~5.5x) than
`re.sub(r'\s+', ' ', text).strip()` for collapsing whitespace in Python, bypassing regex compilation
and engine overhead. **Action:** Prefer `' '.join(text.split())` over `re.sub` for normalizing
whitespace when exact space/tab/newline distinctions aren't required.

## 2024-06-13 - Bounding Context Slices in Regex Loops
**Learning:** Slicing the entire prefix of a large document (`text[:start]`) repeatedly inside a regex search loop (`re.finditer`) forces Python to allocate massive intermediate strings every iteration, resulting in severe O(N^2) performance degradation on large inputs.
**Action:** Always bound string slicing to a fixed context window (e.g., `text[max(0, start - 200):start]`) when only local backward context is required for parsing decisions. Ensure fullmatch bounds are logically gated (`if start <= 200:`) to preserve functionality.
