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

## 2024-06-12 - Bounded Slice inside Iteration Loop

**Learning:** Using `text[:start]` inside an iteration loop like `re.finditer` over a very large
document creates O(N^2) memory and performance overhead by allocating increasingly large strings.
**Action:** Use a bounded slice like `text[max(0, start - 200):start]` to restrict copying to only
the local context required, but always bound original structural `re.fullmatch` checks to
`if start <= 200:` to prevent false negatives when the entire prefix was structurally required.
