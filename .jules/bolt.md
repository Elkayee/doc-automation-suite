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

## 2024-06-07 - Avoid allocating lists when counting lines

**Learning:** Using `len(text.splitlines())` to simply count the number of lines causes O(N) memory
allocation because it eagerly creates an intermediate list of all lines. For large documents, this
can allocate megabytes of memory. **Action:** Use
`text.count('\n') + (1 if text and not text.endswith('\n') else 0)` to count lines without memory
allocation. It is virtually instantaneous and uses O(1) memory.
