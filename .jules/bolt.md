## 2026-05-31 - String Split for Fast Whitespace Normalization

**Learning:** `re.sub(r'\s+', ' ', text.replace('\xa0', ' ')).strip()` takes ~5x longer than
`' '.join(text.split())` due to regex engine overhead and multiple passes. Both methods output an
identical result since `.split()` without arguments normalizes all whitespace (including newlines
and non-breaking spaces like `\xa0`). **Action:** Replace `re.sub` whitespace normalization with
`' '.join(text.split())` where all whitespace (including newlines) is meant to be collapsed. For
targeted whitespace collapse (e.g. only space/tab) use a precompiled regex to avoid functional
regression.
