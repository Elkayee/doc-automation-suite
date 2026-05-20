## 2024-05-20 - Prevent Path Traversal in Config

**Vulnerability:** Arbitrary file read/write vulnerability exists when parsing `config.yaml` files
inside `TemplateConfig.load`, allowing arbitrary paths like `../` or absolute paths like
`/etc/passwd` to be loaded and used in template generation. **Learning:** User-provided
configurations (even static files) that reference other files must be sanitized recursively to
prevent them from reading or writing outside intended directories. **Prevention:** Added a recursive
`_validate_no_path_traversal` check that explicitly blocks parent directory (`..`) references and
absolute paths (`os.path.isabs`) in all configuration values before they are parsed into dataclass
attributes.
