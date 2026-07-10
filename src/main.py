"""
Entry point for AI Meeting Notes Manager application.

This is the main script that starts the application and demonstrates
the initialized architecture.

Run with: python main.py
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app import MeetingNotesManager


def main():
    """Main function to start the application."""
    try:
        # Create and start the application
        manager = MeetingNotesManager()
        manager.start()

        # Display service status
        print("\nService Status:")
        status = manager.get_service_status()
        for service, state in status.items():
            print(f"  • {service}: {state}")

        # Optional: Uncomment to test meeting creation
        # meeting = manager.meeting_service.create_meeting(
        #     title="Team Standup",
        #     participants=["Alice", "Bob", "Charlie"]
        # )
        # print(f"\nTest meeting created: {meeting}")

    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
