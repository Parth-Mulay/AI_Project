# Code Review for the Day 2 Practice Scripts

## Reviewed files

- [Day2_Docs/word_counter.py](word_counter.py)
- [Day2_Docs/my_version.py](my_version.py)
- [Day2_Docs/meeting_notes_demo.py](meeting_notes_demo.py)

## Review summary

The generated code is simple, readable, and beginner friendly. It follows the goal of practicing Python fundamentals for the AI Meeting Notes Manager.

## Improvement 1: Better function names

The first version used a general name such as `count_text`. A more descriptive name like `count_words_in_note` is clearer because it explains the purpose immediately.

### Why this is better

Better names make the code easier to read and reduce confusion when the project grows.

## Improvement 2: Better comments

The code should explain why a function exists, not only what it does. Short comments above each function help a beginner understand the design choice.

### Why this is better

Comments support learning and make the code easier to maintain later.

## Improvement 3: Better formatting

Spacing, blank lines, and consistent indentation improve readability. This is especially important when multiple functions are used together.

### Why this is better

Readable code is easier to review, debug, and extend.

## Improvement 4: Stronger structure

A small helper function can improve clarity when the script performs more than one task. For example, one function can count words while another can format the result for display.

### Why this is better

Clear structure makes the logic easier to test and reuse.

---

## Final thought

The main goal of the Day 2 practice is not to write perfect code. The goal is to learn how to read, explain, and improve code deliberately.

---

## Suggested Git commit message

```text
refactor: improve day 2 practice scripts readability
```
