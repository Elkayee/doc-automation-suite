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

## 2024-06-16 - Fast paths and early breaks in regex iteration

**Learning:** Using `re.finditer` over a large document is lazy, but still evaluates the entire text
if the loop processes every line. For line-specific queries (like checking state at `line_number`),
evaluating past the target line is a massive waste of resources. Additionally, string inclusion
(`'```' in text`) is an extremely fast C-level operation that can completely bypass regex evaluation
when the feature (code fences) is unused. **Action:** Always add fast path string inclusion checks
before regex loops if the pattern requires a specific static string, and aggressively early-break
from `finditer` loops once the required target state (like reaching `line_number`) is achieved.
