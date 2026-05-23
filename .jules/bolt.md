## 2024-05-23 - Pre-compile Regex in Document Validators

**Learning:** Compiling regular expressions inside methods or loops in document validators
introduces redundant compilation overhead and cache lookups, causing measurable performance drops in
frequently called validation paths. **Action:** Always pre-compile constant regular expressions at
the module level (e.g., `PATTERN = re.compile(r'...')`) instead of inside function scopes,
especially in data-heavy processing or validation loops.
