"""
Meeting service module for AI Meeting Notes Manager.

This module provides the MeetingService class that handles
business logic for meeting management, processing, and analysis.
"""

from datetime import datetime
from typing import List, Optional

from ..models.meeting import Meeting
from ai.summarizer import MeetingSummarizer
from ai.action_items import ActionItemExtractor
from utils.logger import app_logger


class MeetingService:
    """
    Service class for managing meeting operations.

    Handles creation, processing, and retrieval of meetings
    with associated analysis and summaries.
    """

    def __init__(self):
        """Initialize the MeetingService."""
        self.meetings: List[Meeting] = []
        self.summarizer = MeetingSummarizer()
        self.action_extractor = ActionItemExtractor()
        app_logger.info("MeetingService initialized")

    def create_meeting(
        self,
        title: str,
        participants: Optional[List[str]] = None,
        date: Optional[datetime] = None
    ) -> Meeting:
        """
        Create a new meeting.

        Args:
            title: Meeting title
            participants: List of participant names
            date: Meeting date

        Returns:
            Created Meeting instance
        """
        meeting = Meeting(
            title=title,
            date=date or datetime.now(),
            participants=participants or []
        )
        self.meetings.append(meeting)
        app_logger.info(f"Meeting created: {title}")
        return meeting

    def process_meeting(self, meeting: Meeting) -> None:
        """
        Process a meeting with transcript.

        Args:
            meeting: Meeting instance to process
        """
        if not meeting.transcript:
            app_logger.warning(f"Meeting {meeting.title} has no transcript")
            return

        app_logger.info(f"Processing meeting: {meeting.title}")

        # Generate summary
        meeting.summary = self.summarizer.summarize(meeting.transcript)

        # Extract action items
        action_items = self.action_extractor.extract(meeting.transcript)
        meeting.action_items = action_items

        app_logger.info(f"Meeting {meeting.title} processed successfully")

    def get_meeting_by_title(self, title: str) -> Optional[Meeting]:
        """
        Retrieve a meeting by title.

        Args:
            title: Meeting title

        Returns:
            Meeting instance or None if not found
        """
        for meeting in self.meetings:
            if meeting.title.lower() == title.lower():
                return meeting
        return None

    def get_all_meetings(self) -> List[Meeting]:
        """
        Get all meetings.

        Returns:
            List of all meetings
        """
        return self.meetings

    def get_meetings_by_date(self, target_date: datetime) -> List[Meeting]:
        """
        Get meetings from a specific date.

        Args:
            target_date: Target date

        Returns:
            List of meetings on the target date
        """
        return [
            m for m in self.meetings
            if m.date.date() == target_date.date()
        ]

    def get_meetings_by_participant(self, participant: str) -> List[Meeting]:
        """
        Get all meetings with a specific participant.

        Args:
            participant: Participant name

        Returns:
            List of meetings with this participant
        """
        return [
            m for m in self.meetings
            if participant.lower() in [p.lower() for p in m.participants]
        ]

    def update_meeting_transcript(self, meeting: Meeting, transcript: str) -> None:
        """
        Update a meeting's transcript.

        Args:
            meeting: Meeting instance
            transcript: New transcript text
        """
        meeting.transcript = transcript
        self.process_meeting(meeting)
        app_logger.info(f"Meeting transcript updated: {meeting.title}")

    def delete_meeting(self, meeting: Meeting) -> bool:
        """
        Delete a meeting.

        Args:
            meeting: Meeting instance to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            self.meetings.remove(meeting)
            app_logger.info(f"Meeting deleted: {meeting.title}")
            return True
        except ValueError:
            app_logger.warning(f"Meeting not found: {meeting.title}")
            return False

    def get_statistics(self) -> dict:
        """
        Get statistics about meetings.

        Returns:
            Dictionary with meeting statistics
        """
        return {
            "total_meetings": len(self.meetings),
            "total_participants": len(set(p for m in self.meetings for p in m.participants)),
            "total_action_items": sum(len(m.action_items) for m in self.meetings),
            "latest_meeting": max([m.date for m in self.meetings]).isoformat() if self.meetings else None
        }
