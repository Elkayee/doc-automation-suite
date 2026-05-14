## 2024-10-27 - Insecure File URI Construction
**Vulnerability:** Constructing local file URIs using string concatenation (`'file:///' + path.replace('\\', '/')`) fails to percent-encode reserved characters and leaves the application vulnerable to URI parsing errors or potential path traversal issues on certain platforms.
**Learning:** Manual URL/URI generation for file paths is error-prone and can lead to security vulnerabilities or unexpected behavior when file paths contain spaces, `#`, `?`, or other URL-reserved characters.
**Prevention:** Always use `pathlib.Path(file_path).as_uri()` in Python when passing local file paths to tools like `webbrowser.open` to ensure cross-platform safety and correct URI percent-encoding.
