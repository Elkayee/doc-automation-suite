## 2024-05-22 - Pre-compile Regex in Hot Loops

**Learning:** Using `re.search()` with string literals inside a tight XML iteration loop in document
validators (`DOCXSchemaValidator`) causes redundant regex compilation and cache lookups, degrading
performance significantly for large documents. **Action:** Pre-compile regular expressions as class
or module-level constants (e.g., `WHITESPACE_START_RE = re.compile(r'^[ \t\n\r]')`) before running
intensive iterations.
