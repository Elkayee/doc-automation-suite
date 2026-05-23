## 2024-05-23 - Path Traversal in TemplateConfig

**Vulnerability:** The `TemplateConfig.load` method in `src/core/config.py` did not validate file paths (such as `docx_template` and `required_files`) loaded from `config.yaml`. This could allow an attacker to craft a malicious `config.yaml` with absolute paths or parent directory references (`..`), potentially enabling arbitrary file access or path traversal when the application subsequently reads or processes those paths.

**Learning:** When loading configuration files that reference other files on the filesystem, it's crucial to treat those file paths as untrusted user input and validate them explicitly, even if they are structured fields within a YAML file.

**Prevention:** Implement strict path validation on all file path fields parsed from configurations. Specifically, block absolute paths (e.g., checking for leading slashes or Windows drive letters) and reject parent directory references (`..`) to ensure paths remain constrained within the intended workspace or template directory.
