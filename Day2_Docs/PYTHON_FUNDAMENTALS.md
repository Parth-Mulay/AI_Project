# Day 2 Task 1 — Python Fundamentals for the AI Meeting Notes Manager

## Goal

Today we will refresh the Python building blocks that will matter most for the AI Meeting Notes Manager project. The focus is not memorizing syntax alone; it is learning how to model real project data clearly and safely.

## Why this matters for the project

The project will need to manage things like:
- meeting titles
- note content
- action items
- AI-generated summaries
- participant names
- decision records

Python is a strong fit because it makes it easy to represent these as variables, lists, dictionaries, functions, and classes.

---

## 1. Variables

A variable stores information so we can reuse it later.

```python
meeting_title = "Sprint Planning"
summary_length = 180
is_ai_enabled = True
```

### Example in the project
```python
meeting_title = "Weekly Product Sync"
notes_text = "Discussed roadmap, customer feedback, and launch timeline."
summary_ready = False
```

### Why this matters

Variables help us keep the app state clear. For example, `summary_ready` tells us whether the AI summary has been generated yet.

---

## 2. Loops

Loops let us repeat actions over a collection of items.

```python
action_items = ["Send follow-up email", "Update roadmap", "Review budget"]

for item in action_items:
    print(item)
```

### Example in the project
```python
participants = ["Aisha", "Ben", "Carla"]

for participant in participants:
    print(f"Processing notes for {participant}")
```

### Why this matters

Meeting notes often contain many action items, reminders, or participants. Loops make it easy to process each one without writing repetitive code.

---

## 3. Functions

Functions help us group reusable logic into a named block.

```python
def format_meeting_title(title):
    return title.strip().title()

print(format_meeting_title("  weekly product sync  "))
```

### Example in the project
```python
def extract_keywords(notes_text):
    words = notes_text.lower().split()
    return words

sample_notes = "AI summary decisions action items"
print(extract_keywords(sample_notes))
```

### Why this matters

A good project structure uses functions to avoid duplication. If the app needs to clean titles, extract keywords, or create summaries in multiple places, functions keep the logic consistent.

---

## 4. Lists

A list stores ordered items.

```python
action_items = ["Send email", "Review draft", "Book meeting"]
print(action_items[0])
```

### Example in the project
```python
meeting_tags = ["product", "planning", "launch"]
meeting_tags.append("ai")
print(meeting_tags)
```

### Why this matters

Lists are ideal for collections such as action items, tags, or participant names.

---

## 5. Dictionaries

A dictionary stores data as key-value pairs.

```python
meeting = {
    "title": "Weekly Product Sync",
    "participants": ["Aisha", "Ben"],
    "action_items": 3
}

print(meeting["title"])
```

### Example in the project
```python
meeting_record = {
    "title": "Client Review",
    "summary": "Discussed roadmap and risks.",
    "action_items": ["Send proposal", "Schedule follow-up"],
    "ai_enabled": True
}

print(meeting_record["summary"])
```

### Why this matters

Dictionaries are very useful for modeling structured meeting data. A meeting record is easier to reason about when it is stored as a dictionary instead of many unrelated variables.

---

## 6. Classes

A class defines a blueprint for objects.

```python
class MeetingNote:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.action_items = []

    def add_action_item(self, item):
        self.action_items.append(item)

    def show_summary(self):
        return f"{self.title}: {self.content}"
```

### Example in the project
```python
class MeetingNote:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.action_items = []

    def add_action_item(self, item):
        self.action_items.append(item)

    def get_action_count(self):
        return len(self.action_items)

note = MeetingNote("Design Review", "Discussed UI changes")
note.add_action_item("Share mockups")
print(note.get_action_count())
```

### Why this matters

Classes are helpful when we want to model a real-world object with behavior. A meeting note can naturally be treated as an object with a title, content, action items, and methods to work with them.

---

## 7. A small combined example

Here is a simple example that combines several concepts for the project:

```python
class MeetingNote:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.action_items = []

    def add_action_item(self, item):
        self.action_items.append(item)

    def get_action_items(self):
        return self.action_items

note = MeetingNote("Standup", "Reviewed blockers and next steps")
note.add_action_item("Send deployment update")
note.add_action_item("Follow up with QA")

print(note.title)
print(note.get_action_items())
```

### What this teaches

- a class groups related behavior
- a list stores multiple action items
- a method keeps the object logic organized

---

## 8. Key takeaways

For the AI Meeting Notes Manager, these Python concepts map to the product like this:

- Variables: store the meeting title, summary text, or AI status
- Loops: process many participants or action items
- Functions: clean titles, parse notes, or extract keywords
- Lists: track action items or tags
- Dictionaries: represent structured meeting records
- Classes: model a meeting note as an object with behavior

---

## 9. Practice exercise

Try to write a small Python snippet from memory that:
1. creates a meeting note object
2. adds two action items
3. prints the title and action items

You do not need to send the answer yet. We will use this as a bridge into the next lesson.

---

## Suggested Git commit message

```text
docs: add day 2 python fundamentals notes
```

## Suggested repository organization

A simple structure for the repository could be:

```text
Day2_Docs/
  PYTHON_FUNDAMENTALS.md
```

This keeps Day 2 learning materials separate from the Day 1 product discovery docs.
