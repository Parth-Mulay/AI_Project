"""Basic Python examples for the AI Meeting Notes Manager project.

This file demonstrates simple Python concepts using meeting-note examples.
"""

# Variables
meeting_title = "Weekly Product Sync"
summary_ready = False
participant_count = 4

# Lists
action_items = ["Send follow-up email", "Review roadmap", "Schedule demo"]

# Dictionaries
meeting_record = {
    "title": meeting_title,
    "summary": "Discussed roadmap, launch timeline, and customer feedback.",
    "action_items": action_items,
    "participants": participant_count,
}

# Loops
for item in action_items:
    print(f"Action item: {item}")

# Functions

def format_meeting_title(title):
    """Return a cleaned meeting title in title case."""
    return title.strip().title()


# Classes
class MeetingNote:
    """Simple model for a meeting note."""

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.action_items = []

    def add_action_item(self, item):
        """Add a new action item to the meeting note."""
        self.action_items.append(item)

    def show_summary(self):
        """Return a short description of the meeting note."""
        return f"{self.title}: {self.content}"


meeting = MeetingNote("Design Review", "Reviewed UI and backend plan")
meeting.add_action_item("Share updated wireframes")

print(format_meeting_title(meeting_title))
print(meeting.show_summary())
print(meeting.action_items)
