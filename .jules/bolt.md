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

## 2024-05-24 - Fast-path substring check to prevent unnecessary regex iteration

**Learning:** In string processing functions that iterate over line endings via regex (`finditer`),
documents without target patterns (like code block backticks ` ``` `) still incur high iteration
overhead. **Action:** Always add a fast-path substring check (e.g., `if '```' not in text`) before
entering the iterator to skip processing completely when the target token is absent, achieving near
O(1) performance for the common negative case.
