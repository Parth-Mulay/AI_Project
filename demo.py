"""
Demo script showcasing the AI Meeting Notes Manager prototype.

This script demonstrates all features without requiring interactive input.

Run with: python demo.py
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.meeting_model import Meeting
from services.detection_service import DetectionService, SummarizationService
from services.export_service import ExportService
from utils.formatter import ConsoleFormatter, print_header, print_subheader, print_section, print_success, print_ai_insight


def run_demo():
    """Run a demonstration of the Meeting Notes Manager."""
    
    # Display welcome
    print(ConsoleFormatter.header("AI Meeting Notes Manager"))
    print(ConsoleFormatter.color_text("Working Prototype - Rule-Based Intelligence Demo\n", "blue"))

    # Create a meeting
    print(ConsoleFormatter.subheader("Meeting Setup"))
    meeting = Meeting("Sprint Planning - Week 15", ["Rahul", "Priya", "Amit", "Brian"])
    print_success("Meeting Started Successfully")
    print(f"\n{ConsoleFormatter.NOTEPAD} Title: Sprint Planning - Week 15")
    print(f"{ConsoleFormatter.PEOPLE} Participants: {', '.join(meeting.participants)}\n")

    # Initialize services
    detection_service = DetectionService()
    export_service = ExportService()

    # Demo messages with insights
    demo_messages = [
        "Rahul: Authentication module is completed.",
        "Priya: We need to finish the dashboard by Friday.",
        "Amit: Rahul will review the API tomorrow.",
        "Priya: We decided to use JWT for token management.",
        "Brian: Risk identified - deployment server has limited resources.",
        "Rahul: Approved the new database schema.",
        "Amit: Important reminder - backup the production data before deployment.",
        "Priya: Should we add caching to improve performance?",
        "Brian: Need to conduct a security review before launch.",
    ]

    # Collect meeting notes
    print(ConsoleFormatter.section("Live Meeting Notes"))
    print("Processing meeting conversation with AI insights:\n")

    for message in demo_messages:
        print(f"  {message}")

        # Process message and detect insights
        insight = detection_service.process_message(meeting, message)

        # Display AI insight if detected
        if insight["type"] == "action":
            print(f"  {ConsoleFormatter.ai_insight('Action Item')}\n")
        elif insight["type"] == "decision":
            print(f"  {ConsoleFormatter.ai_insight('Decision')}\n")
        elif insight["type"] == "note":
            print(f"  {ConsoleFormatter.ai_insight('Important Note')}\n")

    print_success(f"Meeting Ended - {len(meeting.messages)} messages processed\n")

    # Display meeting summary
    print(ConsoleFormatter.section("Meeting Summary"))
    summary = SummarizationService.generate_summary(meeting)
    print(summary)

    # Display action items
    print(ConsoleFormatter.section("Action Items"))
    if meeting.action_items:
        for item in meeting.action_items:
            print(ConsoleFormatter.action_item(str(item)))
    else:
        print("No action items identified.")

    # Display decisions
    print(ConsoleFormatter.section("Decisions Made"))
    if meeting.decisions:
        for decision in meeting.decisions:
            print(ConsoleFormatter.decision(str(decision)))
    else:
        print("No decisions recorded.")

    # Display important notes
    print(ConsoleFormatter.section("Important Notes"))
    if meeting.important_notes:
        for note in meeting.important_notes:
            print(ConsoleFormatter.note(str(note), note.category))
    else:
        print("No important notes.")

    # Display statistics
    print(ConsoleFormatter.section("Meeting Statistics"))
    print(f"{ConsoleFormatter.DOCUMENT} Meeting Title: {meeting.title}")
    print(f"{ConsoleFormatter.PEOPLE} Participants: {len(meeting.participants)}")
    print(f"  {', '.join(meeting.participants)}")
    print(f"\n{ConsoleFormatter.NOTEPAD} Total Messages: {len(meeting.messages)}")
    print(f"{ConsoleFormatter.TARGET} Action Items Found: {len(meeting.action_items)}")
    print(f"{ConsoleFormatter.CHECKMARK} Decisions Found: {len(meeting.decisions)}")
    print(f"{ConsoleFormatter.WARNING} Important Notes: {len(meeting.important_notes)}")
    print(f"\n{ConsoleFormatter.CLOCK} Duration: {meeting.get_duration()}")
    print(f"{ConsoleFormatter.CLOCK} Timestamp: {meeting.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Export meeting
    print(ConsoleFormatter.section("Export"))
    try:
        filepath = export_service.export_to_markdown(meeting)
        print_success(f"Meeting exported to: {filepath}")
        
        # Display file contents
        print(f"\n{ConsoleFormatter.DOCUMENT} File Preview:\n")
        with open(filepath, 'r') as f:
            content = f.read()
            # Show first 500 characters
            preview = content[:500] + "..." if len(content) > 500 else content
            print(preview)
    except Exception as e:
        print(f"Error exporting meeting: {e}")

    # Display closing
    print(ConsoleFormatter.section("Demo Complete"))
    print("✓ All features demonstrated successfully!")
    print(f"\n{ConsoleFormatter.ROBOT} AI Meeting Notes Manager - Prototype v0.2.0\n")
    print("Key Features Demonstrated:")
    print("  ✓ Live meeting note-taking")
    print("  ✓ Real-time AI insight detection (action items, decisions, notes)")
    print("  ✓ Rule-based intelligence (no APIs required)")
    print("  ✓ Automatic summary generation")
    print("  ✓ Meeting statistics")
    print("  ✓ Professional Markdown export")
    print("\nUsage: python src/main.py\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
