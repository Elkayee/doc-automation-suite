## 2025-05-25 - O(K) Keystroke Parsers
**Learning:** Using `text.replace().split()` on full text buffers in keystroke event handlers (where a method is checked for `line_number`) leads to O(N) allocation per keystroke, causing significant latency for large documents.
**Action:** Replace full string splitting with iterative, bounded O(K) string searching (like `str.find('\n')`) that processes only up to the needed line number and avoids loading the whole document into multiple split string objects.
