# .jules/bolt.md

## 2026-05-06 - String processing optimization

**Learning:** When searching for properties that depend on string lines (like checking if a line is
inside a block), doing `text.replace(...).split('\n')` will iterate over the entire text and
allocate an entire array of strings, which is (N)$ memory and time complexity where N is the text
length. This is particularly expensive when it's done repeatedly (e.g. for every line inside a loop
that edits multiple lines). **Action:** Next time when iterating lines up to a specific
`line_number`, try extracting substrings using `str.find('\n', start_idx)` and breaking out early
once the target line is reached. This drops the complexity to (k)$ where $ is the target line index.
