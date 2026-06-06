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

## 2024-06-06 - Path Traversal in Output Files

**Vulnerability:** The `/workspaces/compile` endpoint accepted raw user strings for `md_out`,
`docx_out`, and `cache_dir`, passing them directly to `Path()` without verification. This allowed
writing to arbitrary system locations via path traversal (e.g., `../../../../etc/passwd`).
**Learning:** Even output file destinations provided by users can be weaponized if the server
process has write access. Just because a path isn't used for reading data doesn't mean it's safe to
process blindly. **Prevention:** Always validate user-provided output paths against an expected base
directory (e.g., a build folder) using secure path resolution functions like `_secure_resolve` that
verify the output path is strictly relative to the base directory.
