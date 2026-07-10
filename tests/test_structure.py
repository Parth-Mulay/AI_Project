"""
Test suite for AI Meeting Notes Manager architecture.

This module contains unit tests to verify that the project
structure and imports are working correctly.
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_imports():
    """Test that all major modules can be imported successfully."""
    # Core modules
    from config import PROJECT_NAME, PROJECT_VERSION
    from app import MeetingNotesManager

    # Service modules
    from services.meeting_service import MeetingService
    from services.export_service import ExportService

    # AI modules
    from ai.summarizer import MeetingSummarizer
    from ai.action_items import ActionItemExtractor
    from ai.prompts import MEETING_SUMMARY_PROMPT

    # Audio modules
    from audio.transcriber import AudioTranscriber
    from audio.audio_utils import AudioUtils

    # Model modules
    from models.meeting import Meeting

    # Utility modules
    from utils.logger import app_logger, setup_logger
    from utils.file_handler import create_directory, save_file, read_file

    assert PROJECT_NAME == "AI Meeting Notes Manager"
    assert PROJECT_VERSION == "0.1.0"


def test_application_initialization():
    """Test that the application initializes successfully."""
    from app import MeetingNotesManager

    manager = MeetingNotesManager()
    assert manager is not None
    assert manager.meeting_service is not None
    assert manager.export_service is not None
    assert manager.audio_transcriber is not None
    assert manager.summarizer is not None
    assert manager.action_extractor is not None


def test_meeting_creation():
    """Test that meetings can be created."""
    from models.meeting import Meeting
    from datetime import datetime

    meeting = Meeting(
        title="Test Meeting",
        participants=["Alice", "Bob"]
    )

    assert meeting.title == "Test Meeting"
    assert len(meeting.participants) == 2
    assert isinstance(meeting.date, datetime)


def test_meeting_service():
    """Test meeting service operations."""
    from services.meeting_service import MeetingService

    service = MeetingService()
    meeting = service.create_meeting(
        title="Test Meeting",
        participants=["Alice"]
    )

    assert meeting is not None
    assert meeting.title == "Test Meeting"

    retrieved = service.get_meeting_by_title("Test Meeting")
    assert retrieved is not None
    assert retrieved.title == "Test Meeting"


def test_audio_utils():
    """Test audio utility functions."""
    from audio.audio_utils import AudioUtils

    # Test format support
    assert AudioUtils.is_supported_format("test.mp3")
    assert AudioUtils.is_supported_format("test.wav")
    assert not AudioUtils.is_supported_format("test.txt")

    # Test format list
    formats = AudioUtils.get_supported_formats_list()
    assert len(formats) > 0
    assert ".mp3" in formats


def test_export_service():
    """Test export service initialization."""
    from services.export_service import ExportService

    service = ExportService()
    assert service.is_format_supported("markdown")
    assert service.is_format_supported("pdf")
    assert service.is_format_supported("docx")
    assert not service.is_format_supported("invalid")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
