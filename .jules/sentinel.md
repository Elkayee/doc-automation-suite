## 2025-03-05 - Secure `lxml` Default Parser against XXE globally

**Vulnerability:** The `lxml.etree` module in both `handling-docx-files` and `xu-ly-van-phong`
components used the default XML parser which resolves external entities, exposing the application to
XML External Entity (XXE) vulnerabilities when processing OOXML format files (e.g. DOCX, PPTX).
**Learning:** `lxml` requires explicitly disabling entity resolution to be secure. When many files
or methods use `lxml.etree.parse` or `lxml.etree.fromstring`, individually patching them is
error-prone. **Prevention:** Configure a secure default parser at the module level using
`lxml.etree.set_default_parser(lxml.etree.XMLParser(resolve_entities=False))` to mitigate XXE
vulnerabilities globally across all `lxml.etree` operations in a package.
