## 2024-05-22 - [Fix path traversal in configuration loading]

**Vulnerability:** Path traversal markers (..) and absolute paths were allowed in the workspace
`config.yaml` fields, which could lead to arbitrary file access when resolving settings like image
paths or templates. **Learning:** When loading dictionary-based configurations that reference file
paths recursively, the system needs explicit validation to block absolute paths and parent directory
operators, as base directory composition discards the base directory if the right-hand side is
absolute. **Prevention:** Recursively validate loaded configuration dictionaries against
`os.path.isabs` and `..` patterns before proceeding to map them into dataclasses.
