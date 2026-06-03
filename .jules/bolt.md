## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.

## 2025-02-24 - Avoid `splitlines()` for memory-efficient line iteration

**Learning:** In Python, `str.splitlines()` eagerly allocates a full list of all lines in memory.
Wrapping it in a generator expression like `(line for line in text.splitlines())` does _not_
mitigate this overhead because the list is fully constructed before the generator yields anything.
**Action:** For truly memory-efficient, lazy line iteration over large strings, use a regex iterator
like `re.finditer(r'\n', text)` to slice lines dynamically without allocating the entire document in
memory.

## 2025-02-24 - Prefer `str.split()` over regex for whitespace normalization

**Learning:** `re.sub(r'\s+', ' ', text).strip()` is significantly slower (often 3x-5x) than the
idiomatic `' '.join(text.split())`, which utilizes highly optimized C-level string methods to
collapse all whitespace without regex engine overhead. **Action:** Always prefer
`' '.join(text.split())` for standard whitespace normalization unless boundary newlines must
specifically be preserved.
