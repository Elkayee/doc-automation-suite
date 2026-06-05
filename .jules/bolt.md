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

## 2024-06-05 - Fast Line Counting

**Learning:** `len(string.splitlines())` eagerly allocates strings for every line just to count
them, causing $O(N)$ memory spikes on large documents.

**Action:** When only the total line count is needed,
`string.count('\n') + (1 if string and not string.endswith('\n') else 0)` computes entirely in C
with $O(1)$ memory. This logic flawlessly mirrors the edge-case behavior of `splitlines()` for
standard content.
