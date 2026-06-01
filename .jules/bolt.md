## 2025-05-18 - Optimized whitespace regex replacements
**Learning:** Python's built-in `' '.join(text.split())` is an incredibly fast, C-optimized way to normalize whitespace, making it over 4x faster than using `re.sub(r'\s+', ' ', text).strip()`.
**Action:** Replace `re.sub(r'\s+', ' ', text).strip()` with `' '.join(text.split())` in heavily executed code paths, like Markdown normalization where it is called for every paragraph.
