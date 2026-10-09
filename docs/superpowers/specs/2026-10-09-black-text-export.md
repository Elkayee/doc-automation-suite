# Black report text on export

The user requires report templates to export with black text only. Apply explicit 000000 font color
to document text, styles, tables, titles, captions, headings, TOC/field results, hyperlinks, headers
and footers, including inherited/theme colors in existing templates. Preserve text, fields,
typography and non-font formatting. Normalize the in-memory output document at the shared builder
save boundary; do not edit source templates or workspace chapters.

Acceptance: a colored/theme-based template must export black run/style colors, including linked text
and document parts, while its original bytes and content remain unchanged. Render a real report and
inspect every PDF text glyph color; a fix affecting only headings must fail these checks. Rebuild
and verify the Windows EXEs/ZIP so the delivered app uses the new export policy. Update PLAN.md,
TASK.md and AGENTS.md with results and existing verification limits.
