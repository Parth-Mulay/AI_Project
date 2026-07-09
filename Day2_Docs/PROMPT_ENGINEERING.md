# Prompt Engineering for the AI Meeting Notes Manager

## Why this matters

When you work with AI tools, the quality of the output depends heavily on the quality of your prompt. A clear prompt helps the model understand the goal, the surrounding project context, and the expected result.

## The core structure of a strong prompt

A strong prompt usually includes six parts:

1. Goal
2. Context
3. Requirements
4. Constraints
5. Expected Output
6. Examples

---

## 1. Goal

The goal explains what you want the AI to do.

Example:

```text
Write a Python function that counts words in a meeting note.
```

---

## 2. Context

Context tells the AI what project it is working in.

Example:

```text
This project is called AI Meeting Notes Manager. It stores meeting notes, action items, and summaries for teams.
```

---

## 3. Requirements

Requirements describe what the solution must include.

Example:

```text
The function should count words in a note, ignore extra spaces, and return an integer.
```

---

## 4. Constraints

Constraints prevent the AI from overshooting the task.

Example:

```text
Use only basic Python. Keep the solution beginner friendly. Add comments.
```

---

## 5. Expected Output

Expected output tells the AI what format you want back.

Example:

```text
Return a short Python function with a docstring and one example usage.
```

---

## 6. Examples

Examples make the request easier to understand.

Example:

```text
Input: "Discussed launch timeline and owners"
Expected output: 6
```

---

## Bad prompt vs good prompt

### Bad prompt

```text
Write code for my project.
```

### Why it is weak

- It does not define the goal.
- It does not give project context.
- It does not explain the expected output.

### Good prompt

```text
You are helping build the AI Meeting Notes Manager. Write a beginner-friendly Python function that counts the words in a meeting note. Use only basic Python. The function should accept a string, count the words, and return an integer. Add a short docstring and one example call.
```

---

## Project-specific prompt example

### Weak version

```text
Make a Python script for my meeting app.
```

### Better version

```text
Create a small Python utility for the AI Meeting Notes Manager. The script should accept a meeting note as text and count the number of words. Keep the code simple, add comments, and use a function with a docstring.
```

---

## Why good prompts work better

Good prompts reduce guessing. They help the AI produce code that matches your project, your style, and your constraints.

---

## Suggested practice prompt

```text
I am building an AI Meeting Notes Manager. Write a Python class called MeetingNote that stores a title, content, and a list of action items. Include methods to add an action item, display the meeting, and count the action items. Use only basic Python and keep the code easy to read.
```

---

## Suggested Git commit message

```text
docs: add prompt engineering guide for day 2
```
