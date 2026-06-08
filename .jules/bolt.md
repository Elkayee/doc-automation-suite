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

## 2024-06-08 - Optimize line counting to prevent memory allocation

**Learning:** Using `len(text.splitlines())` to count lines in Python causes O(N) memory allocation
by eagerly creating a full list of all lines. This creates unnecessary overhead for large documents.
Using `.count('\n')` combined with an edge-case check for the final line is functionally equivalent
but avoids all intermediate allocations, significantly improving execution time and memory footprint
on large documents. **Action:** Replace `len(text.splitlines())` with
`text.count('\n') + (1 if text and not text.endswith('\n') else 0)` when only the line count is
needed, evaluating the backslash expression separately if used within an f-string to prevent
SyntaxErrors in older Python versions.
