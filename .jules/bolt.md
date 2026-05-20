## 2026-05-20 - Pre-compile Regex in Document Validators
**Learning:** Compiling regex patterns (like template tags or UUID checkers) inside loops or frequently called validation functions adds unnecessary execution overhead. Moving them to the module or class level prevents redundant parsing and compilation per call.
**Action:** Always pre-compile constant regex patterns at the top level of the file or class to save memory allocations and CPU cycles.
