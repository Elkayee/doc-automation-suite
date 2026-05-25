## 2025-05-25 - Tkinter Empty States and Affordances

**Learning:** Tkinter listboxes don't have built-in empty states, which can make them look broken.
Adding placeholders with a distinct color (like gray) and checking for that color in event handlers
creates a robust empty state pattern. Additionally, Tkinter elements often lack modern web-like
hover affordances; setting the global button cursor via `option_add('*TButton*cursor', 'hand2')`
greatly improves discoverability. **Action:** Always implement explicit empty states for listboxes
and ensure interactive elements have appropriate cursor feedback in Tkinter applications.
