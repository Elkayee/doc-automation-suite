## 2024-05-24 - bounded split optimizations

**Learning:** Using `io.StringIO` for parsing lines from a string may produce subtly different
results at the end of the string compared to `.split("\n")` (because `split` generates an empty
chunk for a trailing newline, while `StringIO` ends iteration). **Action:** Use
`.split("\n", limit)` to drastically reduce memory allocation while preserving exact compatibility
with `.split("\n")` behaviors on trailing newlines.
