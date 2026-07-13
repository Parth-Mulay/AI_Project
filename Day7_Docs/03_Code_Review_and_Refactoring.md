# Code Review and Refactoring Log

This document details the refactoring decisions, structural updates, and layout optimizations made when converting the vanilla prototype codebase (`app.js`, `dashboard.html`, `upload.html`) into modular, reusable React components.

---

## 1. Directory Structure Organization

### Before (Vanilla Prototype)
The prototype had files placed flatly inside `src/web/`:
- `dashboard.html`, `upload.html`, `live.html`, `settings.html`, etc.
- `app.js` (a monolithic controller of 1,000+ lines handling DOM manipulation for all views).
- `style.css` (a massive stylesheet styling every panel, chart, and modal).

### After (React Modular Component Architecture)
We structured the frontend directory logically:
```text
frontend/
├── index.html
├── vite.config.js
├── package.json
├── main.jsx
├── App.jsx
├── components/          # Reusable presentation blocks
│   ├── Button.jsx       # Standard buttons with interactive transitions
│   ├── Input.jsx        # Validation inputs, labels, and error tags
│   ├── Sidebar.jsx      # Navigation sidebar panel
│   ├── Navbar.jsx       # Top workspace navigation and notification panels
│   ├── SearchBar.jsx    # Controlled search query text field
│   ├── StatCard.jsx     # Numeric telemetry cards with SVG waves
│   ├── MeetingCard.jsx  # Individual expandable table rows
│   └── ActionItem.jsx   # Stateful checkbox listings
├── pages/               # Composite screens
│   ├── Dashboard.jsx    # Aggregate telemetry grids, charts, and tables
│   └── UploadMeeting.jsx# Controlled upload form and simulation stages
└── styles/
    ├── variables.css    # Design System variables
    └── global.css       # Layout grids, resets, and styles
```
*Rationale: Grouping elements by responsibility ensures developers can locate, edit, and audit individual modules quickly, enhancing long-term project maintainability.*

---

## 2. Shared State Uplifting & Reactive Data Flow

### Before
The prototype managed data via direct browser synchronization (`localStorage.getItem()`) and handled UI updates by manually selecting DOM elements and modifying their content properties (`document.getElementById().innerHTML = ...`). This was prone to synchronization lag and state bugs.

### After
We centralized application state in the root component `App.jsx`:
- `meetings`: A single source of truth array containing meeting items.
- `userRole`: Global active context ('Member' or 'Admin').
- `notifications`: Notifications array.
- `searchQuery`: Search string query text.

*Rationale: When a user uploads a file in the `UploadMeeting` view and triggers the AI pipeline, the output is appended to the root `meetings` state. Once they return to the `Dashboard`, the telemetry cards (Total meetings count, Time saved), SVGs (Category donut count), and the Recent Meetings lists re-render instantly to display the new item.*

---

## 3. Extracted Reusable Presentation Elements

### Button Component (`Button.jsx`)
- Replaces custom HTML markup elements. Supports design system themes (Primary CTA, Secondary outline, AI gradient action).
- Encapsulates click handler animations (reduces click scaling to `0.98` dynamically via CSS variables).

### Input Component (`Input.jsx`)
- Standardizes labeling, validation asterisks, error strings, and focus indicators.
- Employs accessibility bindings: ties labels to inputs via `htmlFor`, sets `aria-invalid` state, and points screen readers to errors using `aria-describedby`.

---

## 4. Transitioning Monolithic Logic to Declarative Rendering

### Expanding Meetings Drawer Details
- **Vanilla Approach**: Appended extra rows or toggled hidden classes by parsing indices and mapping DOM tree nodes in JavaScript arrays.
- **React Approach**: Handled locally inside `MeetingCard.jsx` using `const [expanded, setExpanded] = useState(false)`. Expanding details (summary markdown, action owner, deadlines) is controlled inline using clean conditional render statements: `{expanded && <tr>...</tr>}`.

### Checklist Board Priority Filtering
- **Vanilla Approach**: Attached click event listeners to category tabs, retrieved dataset priorities, and toggled display properties in nested lists.
- **React Approach**: Handled declaratively in `Dashboard.jsx` using a local filter state `priorityFilter`. The list is rendered in real time using:
  ```jsx
  const filteredActions = allActions.filter(action => {
      if (priorityFilter === 'all') return true;
      return action.priority.toLowerCase() === priorityFilter.toLowerCase();
  });
  ```

---

## 5. Security & Validation Hardening

1. **Secure File Upload Validations**: Added immediate pre-processing filters checking extensions (docx, pdf, txt, mp3, wav) and enforcing size limits (10MB docs, 100MB audio files) before starting submissions.
2. **XSS Shielding**: Eradicated all vulnerable manual DOM assignments (`innerHTML`). Replaced them with declarative JSX elements which auto-escape variables natively.
3. **RBAC Controls**: Tying delete buttons on meetings table rows directly to role validation tags (`userRole === 'Admin'`), ensuring destructive actions are inaccessible to general users.
