## 2024-05-30 - Replace Regex Whitespace Normalization with String Methods

**Learning:** In heavily executed text parsing loops (like Markdown processing), using
`re.sub(r'\s+', ' ', text).strip()` for basic whitespace normalization is significantly slower (up
to 5-6x) than using built-in string methods like `' '.join(text.split())`. This is because
`.split()` without arguments intrinsically handles collapsing all consecutive whitespace (spaces,
tabs, newlines, etc.) and stripping leading/trailing whitespace, bypassing the overhead of regex
execution entirely.

**Action:** When normalizing whitespace to single spaces, always prefer `' '.join(text.split())`
over regex substitution, especially in loops parsing large documents. For joining and normalizing a
list of strings, `' '.join(' '.join(parts).split())` is extremely fast and clean.
