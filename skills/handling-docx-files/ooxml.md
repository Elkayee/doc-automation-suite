# OOXML XML Reference

Manual XML manipulation for advanced DOCX editing.

## Editing Workflow

### Step 1: Unpack

```bash
python scripts/office/unpack.py document.docx unpacked/
```

Extracts XML, pretty-prints, merges adjacent runs, and converts smart quotes to XML entities (`&#x201C;` etc.) so they survive editing. Use `--merge-runs false` to skip run merging.

### Step 2: Edit XML

Edit files in `unpacked/word/`.

**Use "Claude" as the author** for tracked changes and comments, unless the user explicitly requests use of a different name.

**CRITICAL: Use smart quotes for new content.** When adding text with apostrophes or quotes, use XML entities to produce smart quotes:

```xml
<!-- Use these entities for professional typography -->
<w:t>Here’s a quote: “Hello”</w:t>
```

| Entity     | Character                     |
| ---------- | ----------------------------- |
| `&#x2018;` | ‘ (left single)               |
| `&#x2019;` | ’ (right single / apostrophe) |
| `&#x201C;` | “ (left double)               |
| `&#x201D;` | ” (right double)              |

**Adding comments:** Use `comment.py` to handle boilerplate across multiple XML files (text must be pre-escaped XML):

```bash
python scripts/comment.py unpacked/ 0 "Comment text"
```

### Step 3: Pack

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

Validates with auto-repair, condenses XML, and creates DOCX. Use `--validate false` to skip.

---

## XML Schema Reference

### Element Order in `<w:pPr>`

`<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` last.

### Tracked Changes

**Insertion:**

```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**Deletion:**

```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**Deleting entire paragraphs:** Add `<w:del/>` inside `<w:pPr><w:rPr>` to ensure the paragraph mark itself is deleted.

### Comments markers

`<w:commentRangeStart>` and `<w:commentRangeEnd>` are siblings of `<w:r>`, never inside `<w:r>`.

```xml
<w:commentRangeStart w:id="0"/>
<w:r><w:t>commented text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

### Images Reference

1. Add image to `word/media/`
2. Add relation to `word/_rels/document.xml.rels`
3. Add content type to `[Content_Types].xml`
4. Reference in `document.xml` using `<w:drawing>`.
