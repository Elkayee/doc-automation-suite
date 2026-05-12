## 2024-05-12 - Prevent Path Traversal in Project Template Creation

**Vulnerability:** The `TemplateConfig.load` method loaded `config.yaml` values (`docx_template`,
`required_files`, `chapter_order`) and instantiated the config object without sanitizing file paths,
allowing arbitrary path traversal (`../`) when the config is later used to write or assemble files.
**Learning:** Config YAML loading must not blindly trust file paths referenced in the data payload,
especially when the application writes or reads files relative to those paths during project
assembly. **Prevention:** Always validate all path strings extracted from untrusted or external
configuration files against path traversal sequences (e.g., `'..' in str(path)`) before they are
stored or processed. Explicitly reject invalid configurations rather than attempting to silently
sanitize them.
