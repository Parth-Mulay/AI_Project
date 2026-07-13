# AI Code Review and Corrective Log

This document reviews three critical security, architectural, and accessibility mistakes that a naive AI generator would get wrong when building the AI Meeting Notes Manager frontend, explaining why they are incorrect, how we solved them, and the engineering best practices to follow.

---

## 1. Vulnerability to XSS via Insecure Markdown Rendering

### Problem
When displaying AI-extracted summaries or meeting transcripts containing markdown formatting (such as `## Executive Summary` or bold lists), standard AI generators often attempt to render the formatted strings by binding them directly to React's `dangerouslySetInnerHTML` attribute:
```jsx
// Vulnerable AI Implementation
<div dangerouslySetInnerHTML={{ __html: meeting.summary }} />
```

### Why It Was Incorrect
Relying on raw rendering options bypasses React's built-in auto-escaping security layers. If an attacker inputs a malicious script or vector payload inside the meeting notes (e.g., `<img src=x onerror=alert(document.cookie)>`), the browser will execute it when the card is expanded, leading to Cross-Site Scripting (XSS) attacks.

### How It Was Fixed
We stripped raw formatting symbols and mounted the text using React's safe, auto-escaped text bindings:
```jsx
// Secure React Implementation
<p style={{ whiteSpace: 'pre-line' }}>
  {meeting.summary ? meeting.summary.replace(/##\s+/g, '').replace(/-\s+/g, '• ') : ''}
</p>
```
For complex HTML rendering requirements, we document that the application MUST use `DOMPurify.sanitize()` to sanitize input before passing it to any HTML mounting sink:
```jsx
import DOMPurify from 'dompurify';
// ...
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(meeting.summary) }} />
```

### Best Practice
Treat all data retrieved from databases, files, or external APIs as untrusted. Never use unsafe rendering APIs without running a robust sanitizer first.

---

## 2. Insecure Client-Side RBAC Authorization Check

### Problem
Naive AI models frequently check user authorization levels (e.g., whether the user is a `Member` or `Admin`) by reading a raw string directly from `localStorage` or checking state variables without validating them on the backend. They might display or execute actions like deleting a meeting card based solely on this client side value.

### Why It Was Incorrect
Client-side state can be easily manipulated by anyone using standard browser developer tools (e.g., executing `localStorage.setItem('role', 'Admin')` in the console). Additionally, client storage is vulnerable to theft via script injection.

### How It Was Fixed
We isolated the active user role strictly in React's component memory state (`App.jsx`), preventing unauthorized global storage edits. More importantly, we added comments noting that client-side role validation is purely for visual presentation (e.g., hiding/showing the Delete button in `MeetingCard.jsx`), and must be backed by server-side verification:
```jsx
// Server-Side Verification TODO Note
// TODO(security): The backend API endpoint must check the user's session cookie
// and enforce role validation before processing any deletion commands.
```

### Best Practice
Never rely on the client for security checks. The frontend should only adjust the interface for convenience, while the backend API must validate permissions on every single state-changing request.

---

## 3. Lack of Accessibility (a11y) in Custom Checkboxes and Upload Zones

### Problem
AIs often build custom components (like the custom checklist checkboxes or the drag-and-drop file upload area) using simple, unstyled `<div>` tags without keyboard listeners or semantic descriptors:
```jsx
// Inaccessible AI Implementation
<div className="checkbox" onClick={toggleCheckbox}>
  {checked && "✔"}
</div>
```

### Why It Was Incorrect
Unstyled `<div>` blocks are invisible to screen readers, which cannot identify them as interactive controls. Furthermore, keyboard-only users cannot tab to or interact with these controls because they lack focus selectors and keyboard handlers, failing WCAG 2.1 AA guidelines.

### How It Was Fixed
We upgraded custom interactive elements with focus attributes, keyboard listeners, and role descriptors:
```jsx
// Accessible React Checkbox
<div 
  className="chk-box-wrap" 
  onClick={onToggle} 
  role="checkbox" 
  aria-checked={isChecked}
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onToggle();
    }
  }}
>
  <div className={`checkbox-custom ${isChecked ? 'checked' : ''}`}>
    {isChecked && <span className="check-symbol">✓</span>}
  </div>
</div>
```
We also added `tabIndex={0}`, keyboard focus outlines, and `aria-live="polite"` tags to the file upload container to announce loading and success updates to assistive technologies.

### Best Practice
Ensure all interactive elements are reachable via the `Tab` key and can be activated using `Enter` or `Space`. Always accompany custom controls with appropriate ARIA roles and state indicators.
