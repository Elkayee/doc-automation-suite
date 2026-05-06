## 2026-05-06 - Pre-compiling regexes in tight loops
**Learning:** Even though Python caches compiled regular expressions internally when using `re.search` and `re.fullmatch`, the overhead of function calls and cache lookups can be significant when executed inside a tight loop (e.g. iterating over every word in a large document).
**Action:** When a method containing regular expressions is called frequently, always extract them into class-level or module-level pre-compiled regex objects (`re.compile`) to maximize performance.
