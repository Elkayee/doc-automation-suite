## 2024-05-30 - Listbox Empty States

**Learning:** Using `insert` to add a dummy string for a Listbox empty state creates false
affordances, as the user might try to interact with or select the "empty" text as if it were a real
list item. **Action:** Always implement empty states by wrapping the Listbox in a dedicated
container Frame, and toggling visibility between the Listbox and a dedicated Label using
`pack_forget()` and `pack()`.
