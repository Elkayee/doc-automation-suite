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

## 2024-06-09 - Optimize Line Counting

**Learning:** Using `len(text.splitlines())` just to count lines eagerly allocates a full list of
all lines in memory. For large strings,
`text.count('\n') + (1 if text and not text.endswith('\n') else 0)` is ~10x faster and avoids the
O(N) memory allocation overhead, while exactly reproducing `splitlines()` behavior regarding
trailing newlines. **Action:** Prefer `.count('\n')` with trailing newline compensation over
`.splitlines()` when only the total number of lines is required.
