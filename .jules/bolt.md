## 2024-05-18 - [O(N^2) Bottleneck in Markdown Parser]
**Learning:** Found an O(N^2) bottleneck in `src/core/markdown_utils.py` where `_sentence_start_kind` performed slow `re.search` and `re.fullmatch` across the entire document prefix, taking over 6 seconds for just 4000 sentences.
**Action:** Always slice string prefixes (`text[:start][-150:]`) before running regex checks for punctuation or structural rules in long documents. This drops processing time from O(N^2) down to linear O(N), bringing the same 4000 sentences down to <0.1s.
