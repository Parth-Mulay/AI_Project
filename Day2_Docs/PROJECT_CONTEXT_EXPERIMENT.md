# Project Context Experiment

## Why this experiment matters

AI tools respond better when they receive project context. Without context, the model may generate generic answers. With context, it can tailor the output to your real product needs.

---

## Without Context Prompt

```text
Write a Python function that processes text.
```

### Likely output

The AI may produce a generic function that does not match your app structure or your user needs.

---

## With Context Prompt

```text
I am building an AI Meeting Notes Manager. Write a Python function that counts the words in a meeting note. The note may contain action items, meeting summaries, and participant names. Keep the code beginner friendly and add comments.
```

### Likely output

The AI will produce a more relevant function because it understands that the text belongs to a meeting notes system.

---

## Comparison

| Prompt Type | Result |
| --- | --- |
| Without context | Generic and less useful |
| With context | More relevant, project-aware, and easier to adapt |

---

## Why context improves AI-generated code

Context improves the result because it helps the model:

- understand the domain
- choose better variable names
- avoid irrelevant features
- match the project vocabulary
- produce code that is easier to integrate

For the AI Meeting Notes Manager, context matters because the system deals with more than plain text. It handles summaries, action items, and meeting records.

---

## Key lesson

When you ask AI for code, give it:

- the product name
- the problem you are solving
- the expected input and output
- the coding style you want

---

## Suggested Git commit message

```text
docs: add project context experiment notes
```
