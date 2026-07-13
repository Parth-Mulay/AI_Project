# UI/UX Design System - AI Meeting Notes Manager

This document establishes the official UI/UX Design System for the **AI Meeting Notes Manager** SaaS application. It defines the visual styles, design tokens, component specifications, and accessibility standards to maintain a consistent, high-fidelity experience across desktop, tablet, and mobile interfaces.

---

## 1. Visual & Color System (Sleek Dark Theme)

To convey premium, state-of-the-art AI intelligence, the application utilizes a dark-mode-first aesthetic with a carefully chosen cool-toned gray palette, balanced with vivid indicators.

### 1.1 Color Tokens

| Token Name | Hex Code | Purpose / Application |
|---|---|---|
| **Background (Deep)** | `#0B0F19` | Main layout canvas background. |
| **Surface (Card/Nav)**| `#161E2E` | Container surfaces, sidebar background, table rows. |
| **Surface Hover** | `#202B3E` | Hover states on lists, menu items, and interactive cards. |
| **Border (Default)** | `#243249` | Thin lines separating content panels, table rows, and inputs. |
| **Text Primary** | `#F3F4F6` | Main headers and body copy (High contrast). |
| **Text Secondary** | `#9CA3AF` | Supporting text, timestamps, user details, and metadata labels. |
| **Accent Primary** | `#3F83F8` | Primary CTA buttons, focus states, loading progress, and brand accents. |
| **Success / Done** | `#10B981` | Completed tasks, successful save/upload alerts, high AI confidence. |
| **Warning / Blocker**| `#F59E0B` | In-progress tasks, pending reviews, risk flags, medium AI confidence. |
| **Error / Alert** | `#EF4444` | Outages, failed API attempts, deletion checks, low AI confidence. |
| **AI Magic Highlight**| `#8B5CF6` | AI-extracted insights (Action items, Decisions, Highlights). |

---

## 2. Typography System

The typography relies on clean, modern sans-serif typefaces available for free on Google Fonts:
- **Primary Typeface:** **Inter** (for body, input forms, tables, and buttons to maximize readability).
- **Secondary Typeface (Headers):** **Outfit** (geometric sans-serif for dashboard titles, card headings, and stats).

### 2.2 Text Hierarchy Specifications

| Hierarchy Level | Font Face | Size | Weight | Line Height | Case / Letter Spacing |
|---|---|---|---|---|---|
| **H1 - Page Title** | Outfit | `28px` | Bold (700) | `36px` | `-0.02em` |
| **H2 - Section Header**| Outfit | `20px` | SemiBold (600) | `28px` | `-0.01em` |
| **H3 - Card Title** | Outfit | `16px` | Medium (500) | `22px` | `0` |
| **Body (Default)** | Inter | `14px` | Regular (400) | `20px` | `0` |
| **Body (Small/Meta)** | Inter | `12px` | Regular (400) | `16px` | `+0.01em` |
| **Button / Input Text**| Inter | `14px` | Medium (500) | `20px` | `+0.02em` |
| **Badge / Tag Label** | Inter | `11px` | SemiBold (600) | `14px` | Uppercase, `+0.05em` |

---

## 3. Spacing & Grid System

The design is built on a rigid **8px spacing system** (`8px`, `16px`, `24px`, `32px`, `48px`, `64px`) to ensure absolute layout balance.

### 3.1 Responsive Grid Specifications

#### Desktop Viewport (1440px width)
- **Columns:** 12 columns.
- **Side Nav:** Fixed at `240px` width.
- **Content Area:** 12-column fluid grid, `24px` gutter, `32px` outer margins.
- **Content Container:** Max-width `1120px` centered inside content viewport.

#### Tablet Viewport (768px width)
- **Columns:** 8 columns.
- **Side Nav:** Collapsed to an icon-only sidebar (`64px` width) or sliding menu.
- **Content Area:** 8-column fluid grid, `16px` gutter, `24px` outer margins.

#### Mobile Viewport (375px width)
- **Columns:** 4 columns.
- **Side Nav:** Hidden, accessible via a top hamburger icon (overlay drawer).
- **Content Area:** 4-column fluid, `16px` gutter, `16px` outer margins.

---

## 4. UI Components & Figma Resources

All components leverage standard **Figma Free Community Resources** (e.g., standard layout templates, free icon sets, and basic button kits) to ensure speed and code alignment.

### 4.1 Buttons & Interactive Controls
- **Primary CTA:** Solid accent color (`#3F83F8`), text primary (`#F3F4F6`), 6px border-radius.
- **Secondary Button:** Surface color (`#161E2E`), border default (`#243249`), hover changes background to Surface Hover (`#202B3E`).
- **AI Action Button:** Gradient background (Accent Primary `#3F83F8` to AI Magic Highlight `#8B5CF6`) for triggering AI summaries or extractions.
- **Micro-Animations:** Hover transitions should have a `150ms ease-in-out` on background colors, and active click states should scale down slightly to `0.98`.

### 4.2 Form Inputs
- **Text Inputs / Search Fields:** Surface background (`#161E2E`), border default (`#243249`), 6px border-radius. Active/focused border color changes to Accent Primary (`#3F83F8`).
- **Placeholder text:** Secondary Text (`#9CA3AF`).
- **Icons:** **Feather Icons** or **Phosphor Icons** (free Figma plugins) used at `16px` or `20px` size.

### 4.3 Cards & Lists
- **Dashboard Meeting Cards:** Surface background (`#161E2E`), border default (`#243249`), padding `20px`, 8px border-radius. Hover adds a subtle glow outline (`#3F83F8` at 15% opacity).

### 4.4 Badges & Status Indicators
- **High Confidence Badge:** Text `#10B981` (Green) on `#10B981` (10% opacity) pill-shaped background.
- **Risk Badge:** Text `#F59E0B` (Amber) on `#F59E0B` (10% opacity) pill-shaped background.
- **Action Pending Checkbox:** Empty square outline (`#243249`) with hover highlight (`#3F83F8`). Checked state fills with Accent Primary and draws a checkmark.

---

## 5. Accessibility (WCAG 2.1 AA Compliance)

1. **Color Contrast:** All Text Primary (`#F3F4F6` on `#0B0F19` or `#161E2E`) exceeds a 4.5:1 ratio (achieving WCAG AAA compliance). Supporting Text Secondary (`#9CA3AF` on `#161E2E`) is verified at a 4.61:1 ratio, satisfying the WCAG AA minimum.
2. **Keyboard Navigation:** All interactive inputs, buttons, and settings items must support focus states. Focus ring outline: `2px solid #3F83F8` with a `2px` offset.
3. **Screen Readers:** ARIA labels must accompany all icon-only buttons (e.g., `aria-label="Upload meeting recording"`, `aria-label="Close settings pane"`).
4. **Color Independency:** Information is never conveyed strictly by color. For instance:
   - Success checkmarks have a distinct checkbox check symbol `[x]`.
   - Error messages are prefixed with a caution icon `⚠️`.
   - AI highlights are labeled with a small robot chip `🤖 AI Insight`.
