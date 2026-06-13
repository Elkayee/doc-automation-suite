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

## 2024-06-13 - Fix Arbitrary File Write via Unvalidated Output Paths

**Vulnerability:** The `/workspaces/compile` API endpoint accepted optional `md_out`, `docx_out`,
and `cache_dir` parameters and converted them directly to `Path` objects. This allowed attackers to
provide absolute paths (e.g., `/etc/passwd`) or relative path traversal strings (`../../`), leading
to arbitrary file writes. **Learning:** Using `Path(user_input)` does not safely bind the path to a
base directory. If `user_input` is an absolute path, Python's `pathlib` will override the base path
completely. **Prevention:** Always validate user-provided paths using a secure resolution function
(like `_secure_resolve`) that ensures the final path remains relative to the intended base directory
(e.g., `resolved.is_relative_to(base_dir)`), even for output files.
