"""A simple meeting note demo for the AI Meeting Notes Manager.

This file shows how to create a meeting note, add action items,
and display the note information.
"""


class MeetingNote:
    """Represent a meeting note with a title, content, and action items."""

    def __init__(self, title, content):
        """Initialize the meeting note with a title and content."""
        self.title = title
        self.content = content
        self.action_items = []

    def add_action_item(self, item):
        """Add a new action item to the meeting note."""
        self.action_items.append(item)

    def display_meeting(self):
        """Print the meeting title, content, and action items."""
        print(f"Meeting: {self.title}")
        print(f"Content: {self.content}")
        print("Action Items:")
        for item in self.action_items:
            print(f"- {item}")

    def count_action_items(self):
        """Return the number of action items in the meeting note."""
        return len(self.action_items)


# Create a meeting note
meeting = MeetingNote("Client Review", "Discussed launch timeline and risks")

# Add action items
meeting.add_action_item("Send final proposal")
meeting.add_action_item("Schedule follow-up")

# Display the meeting details
meeting.display_meeting()

# Count action items
print(f"Total action items: {meeting.count_action_items()}")
