# Frontend Development Fundamentals

This document provides a comprehensive guide to the core technologies and visual design patterns underpinning modern, responsive web application frontends. These principles serve as the building blocks for creating the AI Meeting Notes Manager.

---

## 1. HTML5 Semantic Structure

Semantic HTML uses tags that carry clear meaning about the enclosed content rather than just defining its visual layout. This enhances readability for developers, improves SEO indexing, and provides assistive technologies (like screen readers) with an accurate outline of the webpage structure.

### Key Semantic Layout Elements
- `<header>`: Represents introductory content, branding, or a set of navigational aids.
- `<nav>`: Defines a block of navigation links.
- `<main>`: Specifies the dominant, unique content of the `<body>`. There must only be one `<main>` per page.
- `<aside>`: Contains content that is tangentially related to the content around it (e.g., sidebars, advertising, callout boxes).
- `<section>`: Groups related content together under a single thematic heading.
- `<article>`: Encloses a self-contained composition (e.g., a forum post, magazine/newspaper article, or blog entry).
- `<footer>`: Defines a footer for its nearest ancestor sectioning content (e.g., page-level footer containing copyright, links).

### Why It Matters
Using semantic HTML ensures accessibility utilities can parse the page's structure and construct an accessibility tree. For instance, a screen reader user can skip directly to the `<main>` canvas or navigate by `<nav>` regions, avoiding tedious parsing of endless nested `<div>` blocks.

---

## 2. CSS Box Model

Every element in a web layout is rendered as a rectangular box. The CSS Box Model describes the layers of space surrounding that element.

```text
+---------------------------------------+
|                MARGIN                 |  <- External space around the element
|  +---------------------------------+  |
|  |             BORDER              |  |  <- Outline boundary of the element
|  |  +---------------------------+  |  |
|  |  |          PADDING          |  |  |  <- Internal space inside the element
|  |  |  +---------------------+  |  |  |
|  |  |  |       CONTENT       |  |  |  |  <- The actual text, image, or child elements
|  |  |  +---------------------+  |  |  |
|  |  +---------------------------+  |  |
|  +---------------------------------+  |
+---------------------------------------+
```

### Components of the Box Model
1. **Content**: The area where text and images appear.
2. **Padding**: Clear space surrounding the content, inside the border. Inherits the background color of the element.
3. **Border**: The outline boundary wrapping the padding and content.
4. **Margin**: Clear space outside the border. Separates the element from neighboring boxes. Margins of adjacent vertical boxes can collapse into a single space.

### Box-Sizing: `content-box` vs `border-box`
- `content-box` (Default): `width` and `height` apply only to the content area. Padding and borders are added to the outside, increasing the final rendered width/height of the element.
- `border-box` (Recommended): `width` and `height` apply to the entire box, including padding and borders. The content area shrinks to accommodate them, making layout calculations highly predictable.
  ```css
  * {
      box-sizing: border-box;
  }
  ```

---

## 3. CSS Flexbox (Flexible Box Layout)

Flexbox is a one-dimensional layout system designed for laying out items in a row or a column. It makes it easy to align items, distribute empty space, and handle dynamic dimensions.

### Core Concepts
Flexbox operates on a **Parent container (Flex Container)** and its **Direct children (Flex Items)**.
- **Main Axis**: The primary direction in which items are laid out (defined by `flex-direction`).
- **Cross Axis**: The axis perpendicular to the main axis.

### Essential Properties
- `display: flex;`: Turns the container into a flex container.
- `flex-direction`: Defines the main axis direction (`row`, `row-reverse`, `column`, `column-reverse`).
- `justify-content`: Aligns items along the **Main Axis** (`flex-start`, `flex-end`, `center`, `space-between`, `space-around`, `space-evenly`).
- `align-items`: Aligns items along the **Cross Axis** (`flex-start`, `flex-end`, `center`, `baseline`, `stretch`).
- `flex-wrap`: Controls whether items wrap onto multiple lines if they exceed the container size (`nowrap`, `wrap`, `wrap-reverse`).
- `gap`: Defines the spacing between flex items (both row and column gutters).

### Common Flexbox Use Cases
- Aligning items in a top navbar (horizontal row with items spread out).
- Centering items both vertically and horizontally inside a container.
- Stacking form elements vertically in a side panel.

---

## 4. CSS Grid

CSS Grid is a two-dimensional layout system designed to manage both columns and rows simultaneously. It is ideal for orchestrating large-scale page layouts, dashboards, and complex content grids.

### Core Concepts
- **Grid Container**: The parent element that declares `display: grid;`.
- **Grid Track**: The space between two adjacent grid lines (a row or a column).
- **Grid Cell**: The intersection of a grid row and a grid column (the smallest unit of grid space).
- **Grid Area**: A rectangular region composed of one or more grid cells.

### Essential Properties
- `grid-template-columns` / `grid-template-rows`: Defines the structure of columns and rows using values, percentages, or the fractional unit (`fr`).
  ```css
  /* Creates a 3-column layout where the center column takes twice the space */
  grid-template-columns: 1fr 2fr 1fr;
  ```
- `gap` (or `grid-gap`): Sets gutters between grid tracks.
- `grid-column` / `grid-row`: Directs a child grid item to span multiple columns or rows.
  ```css
  /* Directs item to span from grid column line 1 to line 3 */
  grid-column: 1 / 3;
  ```
- `align-content` & `justify-content`: Coordinates alignment of tracks inside the container.

---

## 5. Responsive Design & Media Queries

Responsive Web Design (RWD) ensures that web layouts adapt fluidly to varying screen dimensions (mobile, tablet, desktop) and orientations.

### Key Practices
1. **Fluid Grids**: Avoid hardcoded widths (like `width: 960px;`). Use relative units (like percentages, `vw` / `vh`, or `fr`).
2. **Flexible Images**: Prevent images/media from overflowing their containers.
  ```css
  img {
      max-width: 100%;
      height: auto;
  }
  ```
3. **Viewport Meta Tag**: Instructs the browser to scale the layout to the viewport's physical pixels.
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  ```

### CSS Media Queries
Media queries apply blocks of CSS rules only when specific condition filters (such as screen width) are met.
- **Mobile-First Approach**: Write base styles for mobile screens first, and add styling for larger viewports inside media queries.
  ```css
  /* Base styles apply to mobile (default) */
  .container {
      padding: 16px;
  }

  /* Applied to screens 768px wide and above (Tablet) */
  @media (min-width: 768px) {
      .container {
          padding: 24px;
      }
  }

  /* Applied to screens 1024px wide and above (Desktop) */
  @media (min-width: 1024px) {
      .container {
          padding: 32px;
      }
  }
  ```

---

## 6. CSS Custom Properties (CSS Variables)

CSS Variables are custom values defined by developers that can be reused throughout a stylesheet. They simplify theme switches, spacing grids, and style audits.

### Declaring and Using Variables
Variables are declared inside a CSS selector (often `:root` for global scope) and prefix-named with two hyphens (`--`).
```css
:root {
    --color-primary: #3F83F8;
    --color-background: #0B0F19;
    --font-heading: 'Outfit', sans-serif;
    --radius-md: 8px;
}

.card {
    background-color: var(--color-background);
    border-radius: var(--radius-md);
    font-family: var(--font-heading);
}
```

### Benefits
- **Maintainability**: Changing a design system color or border-radius token only requires editing a single line in `:root`.
- **Dynamic Manipulation**: Can be overridden dynamically on specific classes or adjusted via JavaScript (e.g., dark mode vs. light mode toggles).

---

## 7. Web Accessibility (a11y) Basics

Web accessibility ensures that websites can be used by everyone, including people with physical, sensory, cognitive, or situational impairments. We aim for WCAG 2.1 AA Compliance.

### Core Guidelines
1. **Color Contrast**: Text must stand out against its background. WCAG AA requires a contrast ratio of at least `4.5:1` for normal text and `3:1` for large text.
2. **Keyboard Navigation**: Users should be able to navigate all interactive features using only the `Tab`, `Enter`, `Space`, and Arrow keys. Focus rings must be clearly visible:
  ```css
  button:focus-visible, input:focus-visible {
      outline: 2px solid var(--color-accent-blue);
      outline-offset: 2px;
  }
  ```
3. **Semantic Markup**: Avoid using generic tags like `<div>` or `<span>` for buttons or interactive elements. Use `<button>` or `<input>` to ensure the browser exposes correct accessibility traits out of the box.
4. **ARIA (Accessible Rich Internet Applications)**: Supplementary HTML attributes that clarify element purposes to assistive tech when HTML is insufficient.
  - `aria-label`: Describes an icon-only button (e.g., `aria-label="Upload document"` on a button with only a cloud icon).
  - `aria-expanded`: Signals whether a drawer/modal is open or closed.
  - `aria-live`: Tells screen readers to announce dynamic content updates immediately (e.g., validation alerts or upload progress logs).

---

## 8. Component-Based UI Principles

Modern frontends are built using a component-based model. Instead of writing single, long HTML documents, interfaces are broken down into self-contained, modular blocks.

### Core Principles
- **Encapsulation**: A component packages its own structure (HTML), style (CSS), and logic (JS) together, isolated from other UI blocks.
- **Reusability**: Write once, reuse multiple times. For example, a single `<Button>` component can render different text, colors, and handle click events across various pages.
- **Single Responsibility Principle (SRP)**: Each component should do one thing well. A `StatCard` should display a metric, a `SearchBar` should handle search input, and a `Sidebar` should manage navigations.
- **Composition**: Larger pages are assembled by composing smaller components (e.g., the `Dashboard` page is built out of `Sidebar`, `Navbar`, and several `StatCard` and `MeetingCard` components).
