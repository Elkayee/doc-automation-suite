## 2024-05-24 - XML External Entity (XXE) Vulnerability

**Vulnerability:** XML External Entity (XXE) vulnerability in parsing DOCX/PPTX XML files.
**Learning:** `lxml.etree.parse` and `lxml.etree.fromstring` resolve external entities by default.
This can lead to arbitrary local file reads if an attacker provides a crafted document with a
malicious DOCTYPE definition containing an external entity (e.g., `SYSTEM "file:///etc/passwd"`).
**Prevention:** Always explicitly create an `lxml.etree.XMLParser(resolve_entities=False)` and pass
it via the `parser` keyword argument when parsing untrusted XML files using `lxml.etree.parse` or
`lxml.etree.fromstring`.
