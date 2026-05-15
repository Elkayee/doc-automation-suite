## 2025-05-15 - [Insecure URI construction]

**Vulnerability:** Constructing file URIs manually via string concatenation
(`'file:///' + temp_path.replace('\\', '/')`) can lead to URI parsing errors or path traversal
vulnerabilities due to missing percent-encoding (for spaces, special chars) and platform-specific
path separators. **Learning:** Python's `webbrowser.open()` is sensitive to improperly formatted
local paths. When temp paths contain user-specific or unpredictable directory names (e.g., spaces in
usernames on Windows), string concatenation creates invalid URIs, breaking functionality and
potentially allowing local file access manipulation if user input influences the temp generation.
**Prevention:** Always use `pathlib.Path(path).as_uri()` to construct proper `file://` URIs. It
handles platform-specific slashes and percent-encodes dangerous characters automatically.
