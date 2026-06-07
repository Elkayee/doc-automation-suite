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

## 2024-06-07 - O(N^2) Penalty in Iterative String Slicing

**Learning:** Slicing an unbounded prefix `text[:index]` iteratively over all words in a large
document causes O(N^2) memory allocations and massive performance degradation (e.g., capitalization
checking). **Action:** Use a bounded local window `text[max(0, index - 256):index]` when identifying
contextual structural boundaries to achieve O(N) linear time processing.
