## 2025-05-06 - Path Traversal in Workspace Config
**Vulnerability:** The DocumentAssembler allowed path traversal via `../` and absolute paths in `chapter_order` and `required_files` defined in `config.yaml`, potentially allowing malicious configuration to read files outside the designated `chapters` directory.
**Learning:** File references provided via unvalidated configuration schemas can introduce arbitrary file read vulnerabilities when appended to base directories using weak resolution.
**Prevention:** Always validate and sanitize user-provided file paths from configuration files by explicitly blocking `..` and path separator characters (`/` and `\`) when expecting simple filenames.
