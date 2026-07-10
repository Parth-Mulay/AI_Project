"""
Data models for meeting information in AI Meeting Notes Manager.

This module defines the core Meeting model that represents a meeting
and its associated metadata.
"""

from datetime import datetime
from typing import Optional, List


class Meeting:
    """
    Represents a meeting with transcript, summary, and action items.

    Attributes:
        title: Meeting title
        date: Meeting date and time
        transcript: Raw meeting transcript
        summary: AI-generated meeting summary
        action_items: List of extracted action items
        duration_minutes: Meeting duration in minutes
        participants: List of meeting participants
    """

    def __init__(
        self,
        title: str,
        date: Optional[datetime] = None,
        transcript: str = "",
        summary: str = "",
        action_items: Optional[List[str]] = None,
        duration_minutes: int = 0,
        participants: Optional[List[str]] = None
    ):
        """
        Initialize a Meeting instance.

        Args:
            title: Meeting title
            date: Meeting date (defaults to current time)
            transcript: Meeting transcript
            summary: Meeting summary
            action_items: List of action items
            duration_minutes: Meeting duration
            participants: List of participant names
        """
        self.title = title
        self.date = date or datetime.now()
        self.transcript = transcript
        self.summary = summary
        self.action_items = action_items or []
        self.duration_minutes = duration_minutes
        self.participants = participants or []
        self.created_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of the meeting."""
        return f"Meeting(title='{self.title}', date={self.date.strftime('%Y-%m-%d %H:%M:%S')})"

    def __repr__(self) -> str:
        """Return detailed representation of the meeting."""
        return (
            f"Meeting(title='{self.title}', date={self.date}, "
            f"transcript_length={len(self.transcript)}, "
            f"summary_length={len(self.summary)}, "
            f"action_items={len(self.action_items)})"
        )

    def add_action_item(self, item: str) -> None:
        """
        Add an action item to the meeting.

        Args:
            item: Action item description
        """
        if item and item not in self.action_items:
            self.action_items.append(item)

    def add_participant(self, name: str) -> None:
        """
        Add a participant to the meeting.

        Args:
            name: Participant name
        """
        if name and name not in self.participants:
            self.participants.append(name)

    def to_dict(self) -> dict:
        """
        Convert meeting to dictionary representation.

        Returns:
            Dictionary containing all meeting attributes
        """
        return {
            "title": self.title,
            "date": self.date.isoformat(),
            "transcript": self.transcript,
            "summary": self.summary,
            "action_items": self.action_items,
            "duration_minutes": self.duration_minutes,
            "participants": self.participants,
            "created_at": self.created_at.isoformat()
        }
