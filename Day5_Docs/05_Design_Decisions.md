# Design Decisions Rationale - AI Meeting Notes Manager

This document records the design decisions and UX choices made for the **AI Meeting Notes Manager** SaaS application. These justifications are grounded in user research (from Day 3) and product constraints.

---

## 1. Visual Theme: Sleek Dark Mode First

### Decision
The platform utilizes a cool-toned dark theme (`#0B0F19` background, `#161E2E` card surfaces, and `#3F83F8` blue accents).
### Rationale
- **Target Persona Context:** Our primary target user personas (Software Engineers, Tech Leads, and Project Managers from [USER_PERSONAS.md](file:///c:/New%20folder%20(3)/Day1_Docs/USER_PERSONAS.md)) spend 8+ hours a day in dark-themed terminals, code editors (VS Code), and productivity tools (Linear). A dark dashboard provides visual continuity and minimizes eye strain.
- **Brand Perception:** A dark theme balanced with neon-lavender AI highlights (`#8B5CF6`) creates a premium, high-quality, and modern AI aesthetic.

---

## 2. Navigation Layout: Left Sidebar + Fluid Content Canvas

### Decision
A fixed left sidebar layout (`240px` width) for application-level navigation, with horizontal tab splits on detail pages.
### Rationale
- **SaaS Layout Standards:** Sidebars are the established navigation paradigm in Linear, Slack, and Notion, lowering cognitive friction for new users.
- **Hierarchy Separation:** Separating the global workspace settings, system configurations, and archives (in the sidebar) from the current meeting details (in the main content window) keeps the screen uncluttered.

---

## 3. UI Trust and Explainability (Confidence & Source Excerpts)

### Decision
Placing AI confidence score badges and clickable source excerpts directly inline with each summary point and action item.
### Rationale
- **Mitigating Hallucinations:** User research indicated that users are skeptical of AI summaries due to fear of hallucination. By placing the direct quote (source excerpt) with a link to the transcript line range *directly beneath* the item, users can verify accuracy in one click, establishing strong product trust.
- **Statistical Safety:** Instead of displaying an abstract statistic, color-coded badges (Green, Amber, Red) provide immediate, scan-friendly indicators of confidence.

---

## 4. Availability & Fallback Visibility

### Decision
A prominent yellow/amber warning banner appears at the top of the meeting summary view if the system had to fall back to the local extractive summarizer due to API outage.
### Rationale
- **System Transparency:** Users must know when they are looking at a rule-based extractive summary rather than a full generative synthesis. The banner provides transparency without blocking access to the meeting notes.
- **Graceful Degradation:** Rather than showing an error screen and preventing access (failing close on UI but failing open on data), the fallback banner lets the user read the notes immediately while explaining the limitation.

---

## 5. Workspace Context & Role Modifiers

### Decision
A quick-toggle in the user workspace settings that allows switching views between "Admin" and "Member" roles during testing.
### Rationale
- **UX Validation:** Administrators configuration settings (like global retention sweeps or API key management) are hidden for standard members. The toggle allows QA testers and recruiters to easily verify permission-enforced layouts without creating separate accounts.
