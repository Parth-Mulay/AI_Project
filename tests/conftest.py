"""Shared fixtures for all AI Meeting Notes Manager tests."""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.models.meeting_model import Meeting, Message, ActionItem, Decision, ImportantNote, Attachment


@pytest.fixture
def sample_meeting():
    meeting = Meeting("Sprint Planning", ["Alice", "Bob", "Charlie"])
    meeting.add_message(Message("Alice", "We need to complete the authentication module by Friday."))
    meeting.add_message(Message("Bob", "I agreed to adopt the new design system."))
    meeting.add_message(Message("Charlie", "Risk identified - the deployment server has limited resources."))
    meeting.add_message(Message("Alice", "I will write the migration scripts before launch."))
    meeting.add_message(Message("Bob", "We decided to use JWT for token management."))
    meeting.add_message(Message("Charlie", "We must finish the API documentation by Monday."))
    return meeting


@pytest.fixture
def empty_meeting():
    return Meeting("Empty Meeting", [])


@pytest.fixture
def meeting_with_action_items():
    meeting = Meeting("Action Review", ["Alice", "Bob"])
    meeting.add_action_item(ActionItem("Complete authentication module", "Alice", "Friday"))
    meeting.add_action_item(ActionItem("Write API documentation", "Bob", "Monday"))
    meeting.add_action_item(ActionItem("Review deployment pipeline", "Charlie", "Next Week"))
    return meeting


@pytest.fixture
def meeting_with_decisions():
    meeting = Meeting("Decision Log", ["Alice", "Bob"])
    meeting.add_decision(Decision("Use JWT for authentication", "Context: Security discussion about token management"))
    meeting.add_decision(Decision("Adopt React 18 for frontend", "Context: Frontend framework discussion"))
    return meeting


@pytest.fixture
def sample_transcript():
    return (
        "Meeting Minutes: Database Migration.\n"
        "Participants: Amit, Rahul, Priya\n"
        "Amit: We need to complete the Postgres migration by Monday.\n"
        "Rahul: I decided to approve the database schema update.\n"
        "Priya: I will write the migration scripts before launch."
    )


@pytest.fixture
def detection_service():
    from src.services.detection_service import DetectionService
    return DetectionService()


@pytest.fixture
def export_service():
    from src.services.export_service import ExportService
    return ExportService()


@pytest.fixture
def app_instance():
    from src.app import MeetingNotesApp
    return MeetingNotesApp()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from src.server import app
    return TestClient(app)


@pytest.fixture
def nlp_pipeline():
    from src.nlp.pipeline import MeetingNlpPipeline
    return MeetingNlpPipeline()
