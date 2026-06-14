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

## 2026-06-14 - Optimize Prefix Checking Using Boundaries

**Learning:** Re-slicing long prefixes dynamically (e.g., `text[:start]`) inside heavily repeated
code causes massive O(N) memory churn. Replacing it naively with a bounded slice
`text[max(0, start - N):start]` can cause functional regressions if the original checks relied on
evaluating the full string's properties (like counting newlines in trailing whitespace or fully
matching a structural regex). **Action:** Use a backwards character loop for localized trailing
space checks (like counting newlines), and use the `pattern.fullmatch(string, 0, endpos)` method on
pre-compiled regexes to evaluate patterns over long prefixes without allocating intermediate
strings.
