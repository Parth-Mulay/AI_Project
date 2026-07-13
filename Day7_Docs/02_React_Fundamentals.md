# React Development Fundamentals

This document provides a detailed overview of the core concepts of React, a popular JavaScript library for building user interfaces. It serves as the foundation for our component architecture in the AI Meeting Notes Manager.

---

## 1. Components

Components are the building blocks of a React application. They are independent, reusable chunks of UI that combine layout, styling, and logic.

### Functional Components
In modern React, components are written as JavaScript functions that return JSX (JavaScript XML) describing what should be rendered on the screen.
```jsx
function WelcomeCard() {
    return (
        <div className="welcome-card">
            <h1>Welcome back, Priya!</h1>
            <p>Your AI Meeting Note Pipeline is active.</p>
        </div>
    );
}
```

---

## 2. JSX (JavaScript XML)

JSX is a syntax extension for JavaScript that allows you to write HTML-like structures directly within your JavaScript files. It is compiled by tools like Babel or Vite into standard JavaScript function calls (`React.createElement`).

### Key JSX Rules
1. **Return a Single Root Element**: You must wrap elements in a single parent tag (such as `<div>` or a React Fragment `<>...</>`).
2. **Close All Tags**: All tags must be explicitly closed. Self-closing tags must end with a slash (e.g., `<img />`, `<br />`, or `<Input />`).
3. **Use CamelCase for Attributes**: Since JSX compiles to JavaScript, attributes use JavaScript naming conventions (e.g., `className` instead of `class`, `onClick` instead of `onclick`, and `tabIndex` instead of `tabindex`).
4. **JavaScript Interpolation**: You can embed any valid JavaScript expression inside curly braces `{}`.
  ```jsx
  const userName = "Priya";
  return <h2>Hello, {userName.toUpperCase()}!</h2>;
  ```

---

## 3. Props (Properties)

Props are read-only inputs passed from a parent component to a child component. They allow you to reuse components with dynamic data.

### Example
```jsx
// Parent Component
function App() {
    return <StatCard label="Time Saved" value="12.5 hrs" theme="purple" />;
}

// Child Component
function StatCard(props) {
    return (
        <div className={`stat-card ${props.theme}`}>
            <span className="stat-lbl">{props.label}</span>
            <div className="stat-num">{props.value}</div>
        </div>
    );
}
```
*Note: Props are immutable. A child component must never modify its own props.*

---

## 4. State

State is an object that holds information that may change over the lifetime of a component. Unlike props, state is local and managed entirely within the component itself. When a component's state changes, the component re-renders to reflect the new data.

### Declaring and Updating State
State is declared using the `useState` hook. It returns an array with two elements: the current state value and a function to update it.
```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);

    return (
        <button onClick={() => setCount(count + 1)}>
            Count: {count}
        </button>
    );
}
```

---

## 5. Event Handling

Handling events in React is similar to handling events in vanilla HTML, with a few syntax differences:
- React events use camelCase syntax (e.g., `onClick`, `onChange`, `onSubmit`).
- Event handlers are passed as functions rather than string templates.
- You must call `event.preventDefault()` explicitly to prevent default browser behavior (such as form submits reloading the page).

### Example
```jsx
function SearchBar({ onSearch }) {
    const [query, setQuery] = useState('');

    const handleChange = (e) => {
        setQuery(e.target.value);
        onSearch(e.target.value); // Notifies parent component of change
    };

    return (
        <input 
            type="text" 
            value={query} 
            onChange={handleChange} 
            placeholder="Search meetings..." 
        />
    );
}
```

---

## 6. Conditional Rendering

In React, you can render different UI layouts depending on certain state variables or flags.

### Common Approaches
1. **If/Else Statements**: Used within component bodies before returning JSX.
2. **Ternary Operator (`condition ? trueExpress : falseExpress`)**: Used directly inside JSX for clean inline branching.
  ```jsx
  return (
      <div>
          {isRecording ? <span className="red-dot">● REC</span> : <span>Idle</span>}
      </div>
  );
  ```
3. **Logical AND Operator (`condition && expression`)**: Renders the expression only if the condition evaluates to true.
  ```jsx
  return (
      <div>
          {hasError && <div className="error-message">⚠️ Validation failed</div>}
      </div>
  );
  ```

---

## 7. Lists & Keys

When rendering lists of elements, you use the standard JavaScript `.map()` method to loop over arrays and output JSX elements.

### The `key` Attribute
You MUST provide a unique, stable `key` string attribute to each item in the list. This helps React identify which items have changed, been added, or been removed, ensuring optimal DOM update performance.
```jsx
const meetings = [
    { id: "m1", title: "Sprint Sync" },
    { id: "m2", title: "Marketing Catchup" }
];

return (
    <ul>
        {meetings.map((meeting) => (
            <li key={meeting.id}>{meeting.title}</li>
        ))}
    </ul>
);
```
*Avoid using array indices as keys if the list items can be reordered, deleted, or inserted, as it can cause rendering bugs.*

---

## 8. Hooks (useState, useEffect)

Hooks are built-in functions that let functional components hook into React state and lifecycle features.

### 8.1 `useState`
Allows components to track state variables. (See Section 4).

### 8.2 `useEffect`
Enables functional components to perform side effects (such as fetching data, manipulating the DOM, setting timers, or subscribing to events) in response to changes.
```jsx
import { useEffect, useState } from 'react';

function LocalizedClock() {
    const [time, setTime] = useState(new Date().toLocaleTimeString());

    useEffect(() => {
        // Setup side effect (timer)
        const timer = setInterval(() => {
            setTime(new Date().toLocaleTimeString());
        }, 1000);

        // Cleanup function (runs when component unmounts or before re-running effect)
        return () => clearInterval(timer);
    }, []); // Empty dependency array means this runs only once on mount

    return <div>Current Time: {time}</div>;
}
```

---

## 9. Component Communication

### Parent to Child (Downward)
Data is passed from parent to child via **Props**.

### Child to Parent (Upward)
A parent passes a **Callback function** as a prop to the child. The child calls this function, passing data back up as arguments.
```jsx
// Parent
function Parent() {
    const handleChildEvent = (data) => {
        console.log("Data from child:", data);
    };

    return <Child onSubmit={handleChildEvent} />;
}

// Child
function Child({ onSubmit }) {
    return <button onClick={() => onSubmit("Hello Parent!")}>Click Me</button>;
}
```

---

## 10. Folder Structure

For production frontends, files are organized logically by function and responsibility:
```text
frontend/
├── index.html          # Web page wrapper entrypoint
├── vite.config.js      # Bundler settings
├── package.json        # Dependencies list
├── components/         # Reusable presentation blocks
│   ├── Button.jsx
│   ├── Input.jsx
│   ├── Sidebar.jsx
│   └── Navbar.jsx
├── pages/              # Composite layout structures representing screens
│   ├── Dashboard.jsx
│   └── UploadMeeting.jsx
└── styles/             # Application-wide stylesheets
    ├── variables.css   # Color & spacing tokens
    └── global.css      # Core resets and global setups
```

---

## 11. Best Practices

1. **Keep Components Small and Focused**: A component should ideally do one thing. If it becomes too complex, split it into smaller sub-components.
2. **Lifting State Up**: If multiple components need access to the same state, lift that state up to their closest common ancestor and pass it down via props.
3. **Keep State Minimal**: Do not store values in state that can be computed from existing state or props.
4. **Use Strict Types and Handlers**: Ensure inputs are fully controlled. Always validate inputs before updating state or submitting forms to prevent corrupted data or security slips.
5. **Always Clean Up Effects**: Return clean-up functions in `useEffect` to clear active subscriptions, intervals, or event listeners and avoid memory leaks.
