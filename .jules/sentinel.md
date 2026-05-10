## 2023-10-27 - [Sentinel] Prevent Path Traversal in Template Configuration
**Vulnerability:** The configuration loader in `src/core/config.py` read user-provided paths (such as `required_files`, `chapter_order`, and `docx_template`) from `config.yaml` without performing validation against relative directory climbing (`..`) or absolute path structures. This introduced a local file inclusion/path traversal vulnerability.
**Learning:** Configurations meant for workspace scaffolding or building often implicitly trust user inputs by concatenating relative strings.
**Prevention:** Implement an `is_safe_path` validator that rejects empty strings, `..`, and absolute paths, then apply it aggressively to filter all incoming configuration path entries during parsing.
