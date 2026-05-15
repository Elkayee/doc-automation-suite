## 2025-05-15 - [Critical] Path Traversal in Configuration Files

**Vulnerability:** The application was not validating file paths extracted from `config.yaml` (`docx_template`, `required_files`, `chapter_order`, and items within `settings`). This allowed paths containing `..` to point to potentially sensitive files outside the workspace directory.

**Learning:** When loading configuration files that reference other files in a restricted scope (like a template directory or workspace), all paths must be explicitly sanitized to block parent directory references (`..`).

**Prevention:** Ensure explicit string checks against `..` for all path-like configuration values, applying recursive validation over complex structures like dictionaries and lists if needed, and explicitly fail with errors (e.g., `ValueError`) instead of silently modifying inputs.
