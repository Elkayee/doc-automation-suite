## 2025-05-18 - Fast-path text checks over manual splits

**Learning:** For large documents, Python's `str.split('\n')` forces full array allocation overhead
even when limiting string size via slicing isn't an option. **Action:** Use an O(1) fast-path
substring check (e.g., `marker not in text`) combined with `split(marker, limit)` rather than
unbounded splits.
