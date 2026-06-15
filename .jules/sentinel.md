## 2026-05-04 - Path Traversal Vulnerability in Template Configuration

**Vulnerability:** Path traversal vulnerability allowed reading arbitrary files by specifying paths
like `../../etc/passwd` in `docx_template` and `required_files` inside `config.yaml`. The
`template_id` in `TemplateManager.create_project` was also vulnerable to path traversal.

**Learning:** When reading files specified in YAML configurations or accepting directory names as
input (like `template_id`), user inputs must be validated to prevent traversing outside the intended
directories (`..` or absolute paths).

**Prevention:** Always validate that paths from configurations do not contain `..` and are not
absolute paths before using them in file operations. Ensure that directory IDs do not contain path
separators (`/` or `\`).

## 2024-06-02 - Fix Path Traversal in API

**Vulnerability:** The API endpoints `/workspaces/create` and `/workspaces/compile` allowed
directory traversal by directly concatenating user input (`req.name`, `req.workspace_name`) with the
base directory without verification. **Learning:** `Path.resolve()` combined with
`Path.is_relative_to()` is a clean and robust way to verify that an untrusted sub-path resolves
strictly within an expected base directory in Python. Wait, I should also remember to never commit
dummy exploit files. **Prevention:** Always validate and normalize external path inputs against the
expected base directory boundaries before using them in file operations.

## 2024-06-02 - Fix Arbitrary File Write in API compilation

**Vulnerability:** The API endpoint `/workspaces/compile` allowed an arbitrary file write via path
traversal. User-provided paths for `md_out`, `docx_out`, and `cache_dir` were directly passed to
`Path` without validation, allowing an attacker to write compiled documents or create cache
directories in arbitrary locations on the host system (e.g., `/tmp` or `/etc/`). **Learning:** Even
when reading configuration or writing outputs in endpoints, all user-provided file paths must be
strictly bounded to the intended base directories. `Path` objects in Python will resolve to absolute
paths directly if the user provides an absolute path string, completely ignoring the base directory
concatenation. **Prevention:** Always use internal path resolution and validation methods like
`_secure_resolve` to confirm that all dynamically generated paths from user input reside strictly
within safe workspace boundaries before executing any file I/O operations.
