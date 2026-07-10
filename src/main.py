"""
Entry point for the AI Meeting Notes Manager application.

Run with: python src/main.py
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app import MeetingNotesApp


def main():
    """Main entry point."""
    try:
        app = MeetingNotesApp()
        app.start()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

