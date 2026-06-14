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

## 2025-05-18 - Avoid O(N^2) Execution in Python Regex Find Iterators
**Learning:** Slicing the entire string prefix (e.g., `text[:start]`) inside a `re.finditer` loop causes O(N) memory allocations per iteration, resulting in O(N^2) overall time complexity.
**Action:** Restrict the string slice to a fixed bounded window (e.g., `text[max(0, start - 200):start]`) and explicitly bound logic dependent on the start index when full prefix checks are not required.
