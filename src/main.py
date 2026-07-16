"""
Entry point for the AI Meeting Notes Manager application.

Run with: python src/main.py
"""

import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.app import MeetingNotesApp
from backend.core.logging import get_logger

logger = get_logger(__name__)


def main():
    """Main entry point."""
    try:
        logger.info("Starting MeetingNotesApp")
        app = MeetingNotesApp()
        app.start()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception("Application crashed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

