# PTIT essay covers

Authorized by the user's requests: use `dist/DocAutomationSuite-0.2.1/Cover_Ptit.docx` for essays
and offer both group and individual assignments. The supplied file is the authoritative layout
source.

Provide two choices in the existing project template selector. Keep the current `tieu_luan_nd30`
identifier for the group template; add an individual template. Preserve the source cover, its table,
logo, margins and editable Word text. Replace sample text with metadata fields. The group cover
retains five member slots from the source; the individual cover shows student name, student ID and
class. Missing required values remain missing, warn in drafts and reject final exports. Keep the
shared export core, atomic publication and explicit black text.

Existing projects remain unchanged. Build a separate local 0.2.2 distribution so the original 0.2.1
folder and supplied cover remain intact. No publication or merge.

Acceptance: create both project types, fill metadata and export real DOCX/PDF. Check that the cover
occurs once, the selected assignment type and authors are correct, the original logo bytes/table
survive and body text starts after the cover. Inspect rendered pages and the actual template
selector. Test a split Word placeholder, missing required metadata and preservation of previous
output on failure. The instruments must reject a group cover mislabeled as individual,
unfilled/stale author text, a missing logo and an altered source file. Run focused tests, the full
suite in an isolated copy, Ruff and owned Markdown/JSON formatting. Verify the new EXE from another
working directory with isolated user data and record hashes and bundled renderer paths. Frozen input
remains NOT_EVALUATED if Windows prevents input automation.
