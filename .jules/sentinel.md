## 2024-05-30 - Fix XXE vulnerability in lxml XML parsers

**Vulnerability:** Use of `lxml.etree.parse` or `lxml.etree.fromstring` without explicitly disabling
entity resolution makes the application vulnerable to XML External Entity (XXE) attacks. Default
`lxml` behavior resolves external entities, allowing path traversal or DoS when parsing unverified
XML. **Learning:** For extensive codebases, rather than patching every single parser invocation,
`lxml` allows configuring a safe global default parser using
`lxml.etree.set_default_parser(lxml.etree.XMLParser(resolve_entities=False))`. This ensures security
across all `lxml.etree` methods. **Prevention:** Always configure
`XMLParser(resolve_entities=False)` globally or on a per-parse basis when dealing with XML files
like OOXML.
