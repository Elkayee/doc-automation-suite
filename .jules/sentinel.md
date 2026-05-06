## 2026-05-06 - Path Traversal Vulnerability in TemplateConfig

**Vulnerability:** Path traversal vulnerability allowed arbitrary file read/write through the
`required_files` and `chapter_order` lists within `config.yaml`. **Learning:** `config.yaml` is a
user-editable configuration file, and its inputs (`required_files`, `chapter_order`) were
unsanitized when being passed into path construction components like `src/core/assembler.py` and
`src/core/template_manager.py`. This means a user or an attacker could potentially modify these
fields with `../` characters or absolute paths to perform malicious operations outside the intended
workspace. **Prevention:** Always validate and sanitize user-provided file paths to ensure they
don't contain `../` sequences or represent absolute paths using checks like
`Path(filename).is_absolute() or '..' in Path(filename).parts`.
