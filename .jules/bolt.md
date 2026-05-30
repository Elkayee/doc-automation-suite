## 2024-05-30 - Pre-compiling regexes in tight text-processing loops

**Learning:** Python's inline `re.sub()` calls with literal patterns (e.g., punctuation matching)
introduce measurable cache-lookup and execution overhead when run inside tight loops or heavily
executed text-normalization pipelines. **Action:** Pre-compile frequently used regular expressions
as class-level constants (`re.compile(...)`) and reuse their `.sub()` methods to bypass overhead and
improve text processing throughput.
