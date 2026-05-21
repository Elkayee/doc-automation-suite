## 2024-05-24 - [Pre-compile regular expressions]
**Learning:** Pre-compiling constant regular expressions inside methods (like validators) causes redundant compilation overhead and cache lookups, especially in frequently called code paths.
**Action:** Pre-compile constant regular expressions at the module level (e.g., `PATTERN = re.compile(r'...')`) instead of inside methods or loops.
