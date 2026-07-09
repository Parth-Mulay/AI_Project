# Explain Then Generate

## Why understanding matters more than copying

Copying code from AI tools can help you move quickly, but it can also create confusion. If you do not understand how the code works, you may struggle to fix bugs or improve it later.

## Bad prompt

```text
Write Python code for my project.
```

### Why it is weak

- It gives no clear goal.
- It does not explain the context.
- It does not say what the code should do.

## Better prompt

```text
I am building the AI Meeting Notes Manager. Write a Python function that counts the words in a meeting note. Use simple code, add comments, and explain the logic in plain English before the code.
```

### Why it is better

- It states the project clearly.
- It explains the task.
- It asks for an explanation first.

## Explain then generate workflow

1. Understand the requirement.
2. Describe the logic in plain English.
3. Ask the AI to generate code.
4. Review the code carefully.
5. Rewrite the logic in your own words.

## Example workflow for this project

### Step 1: Explain the idea

```text
We need a function that accepts a meeting note string and returns the number of words in it.
```

### Step 2: Generate code

```python
def count_words_in_note(note_text):
    return len(note_text.split())
```

### Step 3: Review the code

Ask questions such as:

- What does `split()` do?
- Why is `len()` used?
- What happens if the note contains extra spaces?

## Key lesson

Understanding the idea first makes AI-generated code easier to trust, edit, and reuse.

---

## Suggested Git commit message

```text
docs: add explain-then-generate guidance
```
