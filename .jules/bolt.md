## 2024-05-18 - Pre-compile Regex Patterns in Loop/Repeated Methods

**Learning:** Instantiating `re.compile()` inside frequently called methods (like
`_remove_template_tags_from_text_nodes` running per node or `validate_uuid_ids` running per file)
adds redundant compilation overhead. **Action:** Always move `re.compile()` patterns to module-level
constants to ensure they are compiled only once, optimizing performance without impacting
readability.
