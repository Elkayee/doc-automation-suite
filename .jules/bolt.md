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

## 2024-06-11 - Avoid splitlines() for line counting

**Learning:** In Python, `str.splitlines()` eagerly allocates a full list of all lines in memory.
When needing only the line count of a string,
`text.count('\n') + (1 if text and not text.endswith('\n') else 0)` is significantly faster (around
5x speedup) as it avoids allocating an intermediate list. This exact formula is necessary to prevent
functional regressions because `splitlines()` drops the trailing newline. **Action:** Replace
`len(text.splitlines())` with the count formula when only the line count is needed, ensuring not to
use backslashes directly in f-strings for pre-3.12 compatibility.
