## 2024-05-24 - Tkinter Listbox Empty States

**Learning:** Empty `tk.Listbox` widgets offer no visual feedback and can appear broken to users.
Implementing a visible empty state improves clarity and UX.

**Action:** Insert a placeholder string (e.g., "(Chua co du an nao)") into the listbox and set its
color to gray (`listbox.itemconfig(0, foreground='gray')`). Update event handlers to ignore
selections where `itemcget(idx, 'foreground') == 'gray'` to prevent errors.

## 2024-05-28 - Staying Focused

**Learning:** When making micro-UX enhancements, it's easy to get distracted by unrelated CI
failures or outdated dependencies in the repository. Trying to fix these out-of-scope issues can
lead to accidental dependency changes (e.g., mixing up JS/Python ecosystems) and noisy pull
requests.

**Action:** Strictly isolate UX changes. Ignore unrelated failing tests or CI deprecation warnings
unless explicitly tasked with resolving them. Keep the PR focused solely on the visual or
interactive improvement.
