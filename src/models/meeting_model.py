"""
Data models for the Meeting Notes Manager prototype.

Defines the core data structures used throughout the application.
"""

from datetime import datetime
from typing import List, Optional


class Message:
    """
    Represents a single message during a meeting.

    Attributes:
        speaker: Name of the person speaking
        content: Message content
        timestamp: When the message was recorded
    """

    def __init__(self, speaker: str, content: str):
        """Initialize a message."""
        self.speaker = speaker.strip()
        self.content = content.strip()
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.speaker}: {self.content}"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"Message(speaker='{self.speaker}', timestamp={self.timestamp})"


class ActionItem:
    """
    Represents an action item extracted from the meeting.

    Attributes:
        description: Description of the action item
        assigned_to: Person assigned to complete the task
        due_date: When the task is due
        detected_line: The line that triggered the detection
    """

    def __init__(self, description: str, assigned_to: Optional[str] = None, due_date: str = ""):
        """Initialize an action item."""
        self.description = description
        self.assigned_to = assigned_to or "Unassigned"
        self.due_date = due_date
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        """Return string representation."""
        if self.due_date:
            return f"{self.description} ({self.due_date})"
        return self.description

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "description": self.description,
            "assigned_to": self.assigned_to,
            "due_date": self.due_date,
            "timestamp": self.timestamp.isoformat()
        }


class Decision:
    """
    Represents a decision made during the meeting.

    Attributes:
        description: Description of the decision
        context: Context in which the decision was made
    """

    def __init__(self, description: str, context: str = ""):
        """Initialize a decision."""
        self.description = description
        self.context = context
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        """Return string representation."""
        return self.description

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "description": self.description,
            "context": self.context,
            "timestamp": self.timestamp.isoformat()
        }


class ImportantNote:
    """
    Represents an important note from the meeting.

    Attributes:
        description: Description of the note
        category: Category (risk, issue, blocker, reminder)
    """

    def __init__(self, description: str, category: str = "note"):
        """Initialize an important note."""
        self.description = description
        self.category = category
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        """Return string representation."""
        return self.description

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "description": self.description,
            "category": self.category,
            "timestamp": self.timestamp.isoformat()
        }


class Meeting:
    """
    Represents a meeting with all its components.

    Attributes:
        id: Unique identifier for the meeting
        title: Meeting title
        participants: List of participant names
        messages: List of messages during the meeting
        action_items: List of detected action items
        decisions: List of detected decisions
        important_notes: List of important notes
        summary: Summary of the meeting
    """

    def __init__(self, title: str, participants: List[str]):
        """Initialize a meeting."""
        import uuid
        self.id = str(uuid.uuid4())
        self.title = title
        self.participants = participants
        self.messages: List[Message] = []
        self.action_items: List[ActionItem] = []
        self.decisions: List[Decision] = []
        self.important_notes: List[ImportantNote] = []
        self.summary = ""
        self.created_at = datetime.now()
        self.ended_at: Optional[datetime] = None

    def add_message(self, message: Message) -> None:
        """Add a message to the meeting."""
        self.messages.append(message)

    def add_action_item(self, item: ActionItem) -> None:
        """Add an action item."""
        self.action_items.append(item)

    def add_decision(self, decision: Decision) -> None:
        """Add a decision."""
        self.decisions.append(decision)

    def add_important_note(self, note: ImportantNote) -> None:
        """Add an important note."""
        self.important_notes.append(note)

    def get_duration(self) -> str:
        """Get the duration of the meeting."""
        if not self.ended_at:
            end_time = datetime.now()
        else:
            end_time = self.ended_at

        duration = end_time - self.created_at
        minutes = duration.total_seconds() / 60
        return f"{int(minutes)} minutes"

    def to_dict(self) -> dict:
        """Convert meeting to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "participants": self.participants,
            "summary": self.summary,
            "messages": [{"speaker": m.speaker, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in self.messages],
            "message_count": len(self.messages),
            "action_items": [item.to_dict() for item in self.action_items],
            "decisions": [d.to_dict() for d in self.decisions],
            "important_notes": [n.to_dict() for n in self.important_notes],
            "created_at": self.created_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration": self.get_duration()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Meeting':
        """Create a Meeting instance from a dictionary."""
        import uuid
        title = data.get("title", "Untitled")
        participants = data.get("participants", [])
        meeting = cls(title, participants)
        meeting.id = data.get("id", str(uuid.uuid4()))
        meeting.summary = data.get("summary", "")
        
        if "created_at" in data:
            meeting.created_at = datetime.fromisoformat(data["created_at"])
        if "ended_at" in data and data["ended_at"]:
            meeting.ended_at = datetime.fromisoformat(data["ended_at"])
            
        for m_data in data.get("messages", []):
            msg = Message(m_data["speaker"], m_data["content"])
            if "timestamp" in m_data:
                msg.timestamp = datetime.fromisoformat(m_data["timestamp"])
            meeting.messages.append(msg)
            
        for a_data in data.get("action_items", []):
            item = ActionItem(
                description=a_data["description"],
                assigned_to=a_data.get("assigned_to"),
                due_date=a_data.get("due_date", "")
            )
            if "timestamp" in a_data:
                item.timestamp = datetime.fromisoformat(a_data["timestamp"])
            meeting.action_items.append(item)
            
        for d_data in data.get("decisions", []):
            dec = Decision(
                description=d_data["description"],
                context=d_data.get("context", "")
            )
            if "timestamp" in d_data:
                dec.timestamp = datetime.fromisoformat(d_data["timestamp"])
            meeting.decisions.append(dec)
            
        for n_data in data.get("important_notes", []):
            note = ImportantNote(
                description=n_data["description"],
                category=n_data.get("category", "note")
            )
            if "timestamp" in n_data:
                note.timestamp = datetime.fromisoformat(n_data["timestamp"])
            meeting.important_notes.append(note)
            
        return meeting
