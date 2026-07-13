# Figma AI Prompt & Prototyping Notes

This document provides a production-ready **Figma AI Prompt** to generate the first interactive mockup of the AI Meeting Notes Manager, alongside list recommendations for free Figma resources and animation trigger guidelines.

---

## 1. Copy-Paste Figma AI Prompt

To bootstrap the visual prototype in Figma, copy the detailed prompt below and paste it directly into the Figma AI Design Generator or similar LLM-driven UI design agents:

```text
Design a high-fidelity modern SaaS application dashboard for "AI Meeting Notes Manager" on a 1440x900 viewport. Use a sleek, minimalist dark-mode-first theme resembling Linear or Notion.

Color Palette:
- Main background: Deep Navy Black (#0B0F19)
- Surface panels and sidebar: Dark Gray-Blue (#161E2E)
- Divider borders: Thin Slate Gray (#243249)
- Typography primary: Cool White (#F3F4F6)
- Typography secondary: Slate Gray (#9CA3AF)
- Primary interactive accent: Vivid Blue (#3F83F8)
- AI Highlights: Vibrant Lavender (#8B5CF6)
- Status green (Success): (#10B981)
- Status yellow (Warning): (#F59E0B)

Layout Structure:
1. Fixed Left Sidebar (Width 240px, Background #161E2E):
   - Top: Clean, minimalist logo with white icon and bold brand text "AI NOTES"
   - Navigation links with clean 20px Feather Icons (Search, Dashboard, Meetings Archive, Workspace, System Settings)
   - Active state navigation link highlighted in Vivid Blue (#3F83F8)
   - Bottom: Minimalist user profile tag showing user name "Priya" and email domain "priya@company.com"

2. Top Global Bar (Height 64px, background #0B0F19):
   - Center: Floating search box with shortcut hint "Ctrl + K"
   - Right: Notification Bell icon with a red circle badge indicator and user profile avatar dropdown

3. Main Scrollable Content Area (Background #0B0F19, Margin 32px):
   - Top Header Section: Large page title "Workspace Dashboard" in Outfit Font (700 bold, size 28px). Beneath it, secondary subtitle "Real-time AI meeting notes and action items tracker"
   - Stats Row: Three horizontal container cards side-by-side:
     - Card A: "Time Saved This Week" -> Text Value "12.5 hrs" in large Bold font, supporting green text "+15% vs last week"
     - Card B: "Meetings Analyzed" -> Text Value "24 total", supporting text "99.9% AI summary uptime"
     - Card C: "Actions Completion" -> Text Value "88% complete" with a thin circular green progress ring UI
   - Main Grid (Two columns layout: 8-columns left, 4-columns right):
     - Left Column Widget: "Recent Meetings" list card. Shows a table of 3 recent meetings. Columns: Meeting Title, Date, Participants (Avatars stacked), Status Tag. Items:
       1. "Sprint Planning - Week 15" | July 13, 2026 | 4 avatars | Status "Analyzed" (purple badge)
       2. "Marketing & Content Sync" | July 11, 2026 | 3 avatars | Status "Completed" (green badge)
       3. "Client Feedback Review" | July 10, 2026 | 2 avatars | Status "Failed - Used Fallback" (amber badge)
     - Right Column Widget: "My Pending Action Items" checklist card. Contains list of checkboxes:
       - [ ] "Review new database API schema" (Due: Tomorrow | Assigned: Rahul)
       - [ ] "Deploy performance caching to staging" (Due: Friday | Assigned: Priya)
       - [ ] "Verify WCAG 2.1 accessibility constraints" (Due: ASAP | Assigned: Priya)

Ensure all elements are pixel-aligned on an 8px grid, with 6px border-radius on elements and 1.5px divider lines. No 3D shadows, keep UI flat, enterprise-grade, and premium.
```

---

## 2. Recommended Free Figma Community Resources

To maintain a 100% free workflow, build your Figma file using only these official, free components and plugins:

1. **Icons Library:**
   - **Plugin:** *Feather Icons* or *Phosphor Icons* (Install via Figma Community. Both are completely open-source, modern, and outline-based, fitting SaaS styles perfectly).
   - Use standard `20px` scale with a `1.5px` stroke weight for general UI, and `16px` scale inside badges and tags.
2. **UI Kit & Components:**
   - **Template:** *Untitled UI (Free Version)* or *Figma Ant Design System (Free Version)*.
   - Utilize their pre-built layout files to extract standard buttons, input fields, checkboxes, and avatar groups.
3. **Typography:**
   - Standard Google Fonts (Inter & Outfit). Ensure they are synced to your system or loaded natively in the Figma web browser.
4. **Device Layout Frames:**
   - Desktop: *MacBook Pro 14"* (1512 x 982) or *Desktop (1440 x 900)*.
   - Tablet: *iPad Pro 11"* (834 x 1194).
   - Mobile: *iPhone 14 & 15 Pro* (393 x 852).

---

## 3. Figma Prototype & Interaction Specifications

To prepare the Figma design for developer handoff, apply these interactive prototyping behaviors:

| Interaction Element | Trigger | Animation Type | Visual Transition Details |
|---|---|---|---|
| **Sidebar Menu Item** | Hover | Instant | Background color transitions from transparent to `#161E2E` (Opacity 40%). |
| **Primary CTA Button** | Hover | Smart Animate (150ms) | Color shifts from `#3F83F8` to a slightly deeper blue; cursor changes to Pointer. |
| **Notification Bell** | Click | Smart Animate (200ms) | Notification panel slides in from the right edge (`ease-out`). |
| **Search (Ctrl+K)** | Click / Key | Dissolve (100ms) | Semi-transparent dark overlay fades in; search text box enters focus state. |
| **Live Record Waveform**| Loop (1000ms) | Smart Animate | Visual audio waves cycle between scale heights (`0.5` to `1.2`) to mimic active recording. |
| **Interactive Checkbox**| Click | Smart Animate (100ms) | Box border changes to `#3F83F8` (Blue) and a checkmark dissolves into place. |
| **AI Summary Tab Toggle**| Click | Smart Animate (150ms) | Active Tab underline moves smoothly; Tab panel content dissolves. |

---

## 4. Implemented Day 5 Figma Integration Prototype Specifications

We have fully integrated the Figma layout design into the prototype web interface located in `src/web/`. Below are the implementation highlights pushed to remote GitHub today:

### 1. Vector & Chart Mockup Integrations (Native HTML/SVG)
Instead of static images or standard browser presets, we built native SVG graphics directly into the HTML to match Figma's visual specifications:
- **Time Saved Sparklines:** Micro curved wave vectors rendering trend offsets.
- **Time Saved Trend Line Chart:** Curated gradient area fill under a high-fidelity spline curved path (`M 50 100 Q 100 95...`) with hover-triggered absolute tooltips.
- **Meetings by Category Donut Chart:** A segment-based donut circle using standard SVG stroke-dasharray properties to build sector percentages for Engineering, Marketing, Operations, and HR categories.
- **Completion Dial Ring:** An 88% completed concentric SVG path tracking pending vs. finished tasks.

### 2. Typographic & Vector Upgrade (Google Material Symbols)
To ensure the interface feels modern, sleek, and premium (matching standard Linear / Stripe dashboards):
- Imported Google's `Material Symbols Outlined` icons to replace primitive system emojis in headers, navigators, toggles, badges, and upload status pipelines.
- Standardized icons to `20px` inside navigation cards and `14px` inside metadata badges with vertical-align alignment controls.

### 3. Navigation & Interaction Updates
- **Block Anchor Sidebar:** Transformed list-item menu placeholders into direct inline-flex `<a>` block anchors, removing standard hyperlink underlines and ensuring the entire menu button is clickable.
- **Spin Loader Animations:** Defined custom CSS `@keyframes spin` in `style.css` so that the synchronization icons spin during drag-and-drop file ingestion stages.
- **Stateful LocalStorage Sync:** Synced active workspace meetings list, notifications lists, system settings, and RBAC user roles in browser storage, allowing modifications to update across pages in real time.

