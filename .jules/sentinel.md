## 2024-05-27 - Disable external entity resolution in lxml

**Vulnerability:** The application uses `lxml.etree.parse()` to read XML files in `base.py` without
disabling entity resolution, which is enabled by default. This makes the application vulnerable to
XML External Entity (XXE) attacks if it parses untrusted XML. **Learning:** Default configurations
of XML parsers like `lxml` are often insecure by default (resolving external entities).
**Prevention:** Always disable entity resolution globally when using `lxml` via
`lxml.etree.set_default_parser(lxml.etree.XMLParser(resolve_entities=False))` or pass a secure
parser instance explicitly to `parse()` and `fromstring()`.
