# Delete Project Feature Design

## Overview
Add the ability to delete a project from the Dashboard's "Recent Projects" list.

## UI Changes
- Modify the area above the projects listbox in `src/ui/dashboard.py`.
- Wrap the "Du an gan day" label in a horizontal `ttk.Frame`.
- Add a "Xoa Du An" (Delete Project) button next to the label, aligned to the right.

## Logic Changes
- Add a new method `delete_selected_project(self)`.
- When the delete button is clicked:
  1. Check if a project is selected in `self.projects_list`. If not, show an error message.
  2. Get the name of the selected project.
  3. Show a confirmation dialog: "Ban co chac chan muon xoa du an '{name}' khong? Hanh dong nay khong the hoan tac."
  4. If the user confirms (Yes), use `shutil.rmtree` to permanently delete the project folder from `self.workspaces_dir`.
  5. Call `self.refresh_projects()` to update the listbox.
  6. Show a success message.
  7. Handle any potential exceptions (e.g., file in use) with an error dialog.

## Dependencies
- Requires `shutil` for recursive directory deletion.
- Requires `tkinter.messagebox` for confirmation and error dialogs (already imported).