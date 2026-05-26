## 2024-05-24 - [Fix XXE vulnerability in lxml]
**Vulnerability:** [XML parsing with default lxml settings allows External Entity Resolution (XXE), which could read local files or trigger SSRF]
**Learning:** [The lxml parser resolves external entities by default. In OOXML files, this is not needed and poses a high security risk.]
**Prevention:** [Explicitly configure a secure parser using lxml.etree.set_default_parser(lxml.etree.XMLParser(resolve_entities=False))]
