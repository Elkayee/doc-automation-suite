## 2024-05-08 - [Path Traversal in Configuration Parsing]

**Vulnerability:** The configuration parser (`TemplateConfig.load`) blindly accepted file paths from
`required_files`, `chapter_order`, and `docx_template` without sanitization. An attacker controlling
the config.yaml file could include `..` or absolute paths in these configurations to perform path
traversal and read or overwrite files outside the expected workspace. **Learning:** Even when
reading configurations that seem internal (e.g., templates), any user-controlled inputs that dictate
file system access must be sanitized to prevent directory traversal attacks. **Prevention:** Always
validate file paths provided via external inputs. Reject or fallback to safe defaults for any path
containing sequence like `..`, `/` or `\\` before appending to base directories.
