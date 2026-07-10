"""
Main application module for AI Meeting Notes Manager.

This module contains the core MeetingNotesManager class that orchestrates
all the major components of the application.
"""

from utils.logger import app_logger
from services.meeting_service import MeetingService
from services.export_service import ExportService
from audio.transcriber import AudioTranscriber
from ai.summarizer import MeetingSummarizer
from ai.action_items import ActionItemExtractor
import config


class MeetingNotesManager:
    """
    Main application class for AI Meeting Notes Manager.

    Orchestrates all major components including transcription,
    summarization, action item extraction, and export services.
    """

    def __init__(self):
        """Initialize the MeetingNotesManager application."""
        app_logger.info("=" * 50)
        app_logger.info("AI Meeting Notes Manager")
        app_logger.info(f"Version: {config.PROJECT_VERSION}")
        app_logger.info(f"Author: {config.PROJECT_AUTHOR}")
        app_logger.info("=" * 50)

        # Initialize core services
        self.meeting_service = MeetingService()
        self.export_service = ExportService()
        self.audio_transcriber = AudioTranscriber()
        self.summarizer = MeetingSummarizer()
        self.action_extractor = ActionItemExtractor()

        app_logger.info("All services initialized successfully")

    def start(self) -> None:
        """
        Start the application and display initialization message.

        This method is called when the application starts and displays
        a professional startup message indicating the architecture is ready.
        """
        self._display_startup_message()
        app_logger.info("Application started and ready for use")

    def _display_startup_message(self) -> None:
        """Display the startup message with architecture status."""
        startup_message = f"""
{'=' * 60}

{'AI MEETING NOTES MANAGER'.center(60)}

Architecture Initialized Successfully

Day 3 Product Thinking Completed

{'=' * 60}

Initialized Modules:

✓ Audio Processing (Transcriber)
✓ AI Summarization (MeetingSummarizer)
✓ Action Item Extraction (ActionItemExtractor)
✓ Meeting Management (MeetingService)
✓ Export Services (PDF, Markdown, DOCX)
✓ Logging & Utilities

{'=' * 60}

Status: Ready for Development

Version: {config.PROJECT_VERSION}
Author: {config.PROJECT_AUTHOR}

Project: {config.PROJECT_DESCRIPTION}

{'=' * 60}
"""
        print(startup_message)
        app_logger.info("Startup message displayed")

    def get_service_status(self) -> dict:
        """
        Get the status of all services.

        Returns:
            Dictionary containing the status of each service
        """
        return {
            "project_name": config.PROJECT_NAME,
            "version": config.PROJECT_VERSION,
            "author": config.PROJECT_AUTHOR,
            "meeting_service": "active",
            "export_service": "active",
            "audio_transcriber": "active",
            "summarizer": "active",
            "action_extractor": "active"
        }

    def shutdown(self) -> None:
        """Gracefully shutdown the application."""
        app_logger.info("Shutting down AI Meeting Notes Manager")
        print("\nAI Meeting Notes Manager shutting down...")
        app_logger.info("=" * 50)
        app_logger.info("Application closed")
