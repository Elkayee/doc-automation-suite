## 2025-02-14 - Prevent Path Traversal in Configuration Loading

**Vulnerability:** Path traversal risks existed due to configuration structures (e.g.,
`required_files`) from `config.yaml` not being validated for absolute paths or `..` sequences.
**Learning:** When loading dictionary-based configurations that define file system access (like
template builders), relying solely on `yaml.safe_load` is insufficient to prevent arbitrary file
access if those variables are passed directly into path combinations. **Prevention:** Apply a
recursive input validator to configuration dictionaries to strictly block absolute paths (across
platforms) and parent directory references (`..`) before parsing them into application state.
