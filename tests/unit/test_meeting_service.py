"""Unit tests for the MeetingService."""

from datetime import datetime, timedelta

import pytest
from src.models.meeting import Meeting
from src.services.meeting_service import MeetingService


class TestMeetingService:
    def test_initialization(self):
        service = MeetingService()
        assert service.meetings == []
        assert service.summarizer is not None
        assert service.action_extractor is not None

    def test_create_meeting(self):
        service = MeetingService()
        meeting = service.create_meeting("Test Meeting", ["Alice", "Bob"])
        assert meeting.title == "Test Meeting"
        assert len(service.get_all_meetings()) == 1

    def test_create_meeting_with_defaults(self):
        service = MeetingService()
        meeting = service.create_meeting("Default Meeting")
        assert meeting.title == "Default Meeting"
        assert meeting.participants == []
        assert meeting.date is not None

    def test_get_meeting_by_title_found(self):
        service = MeetingService()
        service.create_meeting("Sprint Planning", ["Alice"])
        meeting = service.get_meeting_by_title("Sprint Planning")
        assert meeting is not None
        assert meeting.title == "Sprint Planning"

    def test_get_meeting_by_title_case_insensitive(self):
        service = MeetingService()
        service.create_meeting("Sprint Planning", ["Alice"])
        meeting = service.get_meeting_by_title("sprint planning")
        assert meeting is not None

    def test_get_meeting_by_title_not_found(self):
        service = MeetingService()
        result = service.get_meeting_by_title("Nonexistent")
        assert result is None

    def test_get_all_meetings_empty(self):
        service = MeetingService()
        assert service.get_all_meetings() == []

    def test_get_all_meetings_returns_all(self):
        service = MeetingService()
        service.create_meeting("Meeting 1")
        service.create_meeting("Meeting 2")
        assert len(service.get_all_meetings()) == 2

    def test_process_meeting_no_transcript(self):
        service = MeetingService()
        meeting = service.create_meeting("Test")
        service.process_meeting(meeting)
        assert meeting.summary == ""

    def test_process_meeting_with_transcript(self):
        service = MeetingService()
        meeting = service.create_meeting("Test")
        meeting.transcript = "Alice: We need to discuss the project plan."
        service.process_meeting(meeting)
        assert meeting.summary is not None

    def test_get_meetings_by_date(self):
        service = MeetingService()
        today = datetime.now()
        m1 = service.create_meeting("Today Meeting", date=today)
        yesterday = today - timedelta(days=1)
        m2 = service.create_meeting("Yesterday Meeting", date=yesterday)
        today_meetings = service.get_meetings_by_date(today)
        assert m1 in today_meetings
        assert m2 not in today_meetings

    def test_get_meetings_by_participant(self):
        service = MeetingService()
        m1 = service.create_meeting("Meeting 1", participants=["Alice", "Bob"])
        m2 = service.create_meeting("Meeting 2", participants=["Charlie"])
        alice_meetings = service.get_meetings_by_participant("Alice")
        assert m1 in alice_meetings
        assert m2 not in alice_meetings

    def test_get_meetings_by_participant_case_insensitive(self):
        service = MeetingService()
        m1 = service.create_meeting("Meeting", participants=["Alice"])
        result = service.get_meetings_by_participant("alice")
        assert m1 in result

    def test_update_meeting_transcript(self):
        service = MeetingService()
        meeting = service.create_meeting("Test")
        service.update_meeting_transcript(meeting, "Alice: New transcript content.")
        assert meeting.transcript == "Alice: New transcript content."

    def test_delete_meeting_success(self):
        service = MeetingService()
        meeting = service.create_meeting("Test")
        result = service.delete_meeting(meeting)
        assert result is True
        assert len(service.get_all_meetings()) == 0

    def test_delete_meeting_not_found(self):
        service = MeetingService()
        meeting = Meeting("Test")
        result = service.delete_meeting(meeting)
        assert result is False

    def test_get_statistics_empty(self):
        service = MeetingService()
        stats = service.get_statistics()
        assert stats["total_meetings"] == 0
        assert stats["total_participants"] == 0
        assert stats["total_action_items"] == 0
        assert stats["latest_meeting"] is None

    def test_get_statistics_with_meetings(self):
        service = MeetingService()
        service.create_meeting("Meeting 1", participants=["Alice", "Bob"])
        service.create_meeting("Meeting 2", participants=["Charlie"])
        stats = service.get_statistics()
        assert stats["total_meetings"] == 2
        assert stats["total_participants"] == 3
        assert stats["latest_meeting"] is not None
