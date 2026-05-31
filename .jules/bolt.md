## 2026-05-31 - Fast String Whitespace Normalization

**Learning:** When collapsing consecutive spaces, tabs, or newlines in a Python string,
`' '.join(text.split())` is approximately 5x faster than using the regular expression
`re.sub(r'\s+', ' ', text).strip()`. This difference is magnified inside frequently executed loops
or recursive parsing routines. Be aware that `.split()` collapses _all_ whitespace, including
newlines, so it is a direct replacement for regex patterns that do the same.

**Action:** Replace inline instances of `re.sub(r'\s+', ' ', text).strip()` with
`' '.join(text.split())` in hot paths such as string normalization blocks inside parsing loops.
