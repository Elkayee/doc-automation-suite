## 2026-05-23 - [Path Traversal in Config Paths]
**Vulnerability:** The configuration loader blindly trusted file paths (e.g., `docx_template`, `required_files`) from `config.yaml`, enabling path traversal and arbitrary file access.
**Learning:** Combining a base directory with an absolute path via `pathlib` discards the base directory, giving attacker arbitrary read access on the system.
**Prevention:** Explicitly validate path values to block absolute paths (`/`, `C:\`, etc.) and parent directory references (`..`).
