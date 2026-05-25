## 2025-05-25 - Prevent XXE via Default XML Parsers

**Vulnerability:** lxml.etree standard parsers were used, allowing XML external entity resolution
which could lead to XXE. **Learning:** When using lxml for document parsing (like docx/pptx),
default parsers are dangerous. **Prevention:** Use lxml.etree.XMLParser(resolve_entities=False) and
apply via lxml.etree.set_default_parser()
