## 2025-02-27 - [Path Traversal in Config Loader]

**Vulnerability:** The configuration parsing (`TemplateConfig.load`) blindly loaded strings from
`config.yaml` files. If strings contained `../` elements (such as `required_files` or
`chapter_order`), they could resolve relative to the `chapters` directory when assembled by the
`DocumentAssembler`, allowing a path traversal that reads arbitrary files from the workspace
directory and assembles them into the exported document. **Learning:** Config files passed to
application processes must have their elements recursively checked for path manipulation sequences
if those elements intend to be used as paths by downstream systems, to prevent Local File Inclusion
(LFI) via assembled content. **Prevention:** Sanitize loaded configurations by recursively
validating all loaded nested dictionary values and arrays, verifying string elements do not contain
path traversal payloads like `..` by blocking consecutive dots inside paths. Fail immediately
explicitly with a `ValueError`.
