# Token Cost and Prompt Optimization

## What are tokens?

Tokens are small pieces of text that models read and generate. A word is often split into one or more tokens.

Example:

```text
"meeting notes" may be counted as two or more tokens depending on the model.
```

## Why tokens matter

Models process tokens, and the number of tokens affects:

- speed
- cost
- memory usage

## Context window

The context window is the maximum amount of text a model can consider at one time.

If your prompt is too long, the model may not fit everything in the window.

## Prompt size

A larger prompt usually means more tokens. This can increase cost and reduce efficiency.

## Output size

Large outputs also use more tokens. If you ask for a long explanation or a very large code block, the cost increases.

## Cost optimization tips

- Keep prompts clear and focused
- Give only the necessary context
- Ask for short answers when possible
- Trim repeated information
- Use smaller examples when possible

## Small vs large models

- Small models are cheaper and faster
- Large models are more capable but more expensive

Use a small model for simple tasks such as:

- rewriting a short function
- fixing minor code issues
- summarizing notes

Use a larger model for:

- complex architecture tasks
- advanced reasoning
- multi-step code generation

## Prompt trimming

Remove unnecessary details from your prompt. Keep the important goal, context, and constraints.

## Context trimming

Only include the project context that helps the model. Too much context can waste tokens and confuse the output.

## Caching

Caching means reusing previous responses for repeated requests. This can reduce cost when the same task is requested multiple times.

## Beginner-friendly example

### Expensive prompt

```text
Please explain everything about my project, all features, all requirements, and all code patterns before writing a Python function.
```

### Better prompt

```text
I am building an AI Meeting Notes Manager. Write a Python function that counts words in a meeting note.
```

## Key lesson

Good prompts are not just clear; they are also efficient.

---

## Suggested Git commit message

```text
docs: add token cost and prompt optimization guide
```
