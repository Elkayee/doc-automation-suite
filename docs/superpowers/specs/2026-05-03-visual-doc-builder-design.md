# Visual Doc Builder Design

## Overview
A high-fidelity, interactive document editing and building application for the `doc-automation-suite`. It integrates the fragmented chapters into a cohesive IDE-like experience with real-time Word-style pagination.

## Architecture: Three-Pane IDE
The application will be a Tkinter-based dashboard with three main components:

### 1. Navigator (Left Pane)
- **Purpose:** Content hierarchy and navigation.
- **Features:**
    - Real-time file system monitoring of the `chapters/` directory.
    - Drag-and-drop reordering of chapters.
    - Status indicators (e.g., unsaved changes).

### 2. Editor (Center Pane)
- **Purpose:** Direct text modification.
- **Features:**
    - Focused Markdown editing.
    - Syntax highlighting for Markdown elements (headers, tables, images).
    - Auto-save to underlying `.md` files.

### 3. Visualizer (Right Pane)
- **Purpose:** Real-time Word-style visualization.
- **Technology:** Embedded browser (`tkinterweb`) using **CSS Paged Media**.
- **Features:**
    - Virtual A4 pages with margins, drop shadows, and page numbers.
    - Multi-page layout simulation.
    - Zoom support (50% - 200%).
    - **Scroll Sync:** Bi-directional synchronization between editor line and preview element.

## Components & Data Flow
1. **File System:** The source of truth remains the `.md` files in `chapters/`.
2. **Assembler:** Combines chapters into a single stream for the Visualizer.
3. **CSS Engine:** Injects A4 styling and Word-like formatting (fonts, spacing, table borders).
4. **Toolbar:** Quick actions for inserting tables, images, and triggering the DOCX build pipeline.

## Success Criteria
- [ ] User can navigate between all chapters via a sidebar.
- [ ] Changes in the editor appear in the visualizer within 800ms (debounced).
- [ ] Visualizer shows discrete pages (A4 size).
- [ ] One-click export to a finalized `.docx` file.

## Risks & Mitigations
- **Risk:** Large documents slowing down the preview.
- **Mitigation:** Debounced rendering and incremental updates to the DOM.
- **Risk:** Tkinterweb dependency issues on some platforms.
- **Mitigation:** Fallback to a simplified non-paginated view or standard web browser launch.
