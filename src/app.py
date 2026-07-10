"""
Main application class for the Meeting Notes Manager.

Orchestrates the meeting workflow and user interaction.
"""

from typing import Optional
from models.meeting_model import Meeting
from services.detection_service import DetectionService, SummarizationService
from services.export_service import ExportService
from utils.formatter import ConsoleFormatter, print_header, print_subheader, print_section, print_success, print_ai_insight


class MeetingNotesApp:
    """
    Main application class for managing meeting notes.

    Handles the complete workflow from meeting creation to export.
    """

    def __init__(self):
        """Initialize the application."""
        self.current_meeting: Optional[Meeting] = None
        self.detection_service = DetectionService()
        self.export_service = ExportService()

    def start(self) -> None:
        """Start the application and run the main workflow."""
        self._display_welcome()
        self._start_new_meeting()
        self._collect_meeting_notes()
        self._display_meeting_summary()
        self._export_meeting()
        self._display_closing()

    def _display_welcome(self) -> None:
        """Display welcome message."""
        print(ConsoleFormatter.header("AI Meeting Notes Manager"))
        print(ConsoleFormatter.color_text(
            "Intelligent meeting assistant powered by AI\n",
            "blue"
        ))

    def _start_new_meeting(self) -> None:
        """Get meeting details and start a new meeting."""
        print(ConsoleFormatter.subheader("Meeting Setup"))

        # Get meeting title
        title = input("Enter Meeting Title: ").strip()
        while not title:
            print("Meeting title cannot be empty.")
            title = input("Enter Meeting Title: ").strip()

        # Get participants
        participants_input = input("Enter Participants (comma separated): ").strip()
        participants = [p.strip() for p in participants_input.split(",") if p.strip()]

        if not participants:
            participants = ["Unknown"]

        # Create meeting
        self.current_meeting = Meeting(title, participants)
        print_success("Meeting Started Successfully")
        print(f"\n{ConsoleFormatter.NOTEPAD} Title: {title}")
        print(f"{ConsoleFormatter.PEOPLE} Participants: {', '.join(participants)}\n")

    def _collect_meeting_notes(self) -> None:
        """Collect meeting notes from user input."""
        print(ConsoleFormatter.section("Live Meeting Notes"))
        print("Enter meeting conversations (type 'end' to finish):\n")

        message_count = 0

        while True:
            line = input()

            if line.lower().strip() == "end":
                break

            if not line.strip():
                continue

            message_count += 1

            # Process the message and detect insights
            insight = self.detection_service.process_message(self.current_meeting, line)

            # Display AI insight if detected
            if insight["type"] == "action":
                print_ai_insight("Action Item")
            elif insight["type"] == "decision":
                print_ai_insight("Decision")
            elif insight["type"] == "note":
                print_ai_insight("Important Note")

        print_success(f"\nMeeting Ended - {message_count} messages recorded\n")

    def _display_meeting_summary(self) -> None:
        """Display comprehensive meeting summary."""
        print(ConsoleFormatter.section("Meeting Summary"))

        # Generate and display summary
        summary = SummarizationService.generate_summary(self.current_meeting)
        print(summary)

        # Display action items
        print(ConsoleFormatter.section("Action Items"))
        if self.current_meeting.action_items:
            for item in self.current_meeting.action_items:
                print(ConsoleFormatter.action_item(str(item)))
        else:
            print("No action items identified.")

        # Display decisions
        print(ConsoleFormatter.section("Decisions Made"))
        if self.current_meeting.decisions:
            for decision in self.current_meeting.decisions:
                print(ConsoleFormatter.decision(str(decision)))
        else:
            print("No decisions recorded.")

        # Display important notes
        print(ConsoleFormatter.section("Important Notes"))
        if self.current_meeting.important_notes:
            for note in self.current_meeting.important_notes:
                print(ConsoleFormatter.note(
                    str(note),
                    note.category
                ))
        else:
            print("No important notes.")

        # Display statistics
        print(ConsoleFormatter.section("Meeting Statistics"))
        self._display_statistics()

    def _display_statistics(self) -> None:
        """Display meeting statistics."""
        meeting = self.current_meeting

        print(f"{ConsoleFormatter.DOCUMENT} Meeting Title: {meeting.title}")
        print(f"{ConsoleFormatter.PEOPLE} Participants: {len(meeting.participants)}")
        print(f"  {', '.join(meeting.participants)}")
        print(f"\n{ConsoleFormatter.NOTEPAD} Total Messages: {len(meeting.messages)}")
        print(f"{ConsoleFormatter.TARGET} Action Items Found: {len(meeting.action_items)}")
        print(f"{ConsoleFormatter.CHECKMARK} Decisions Found: {len(meeting.decisions)}")
        print(f"{ConsoleFormatter.WARNING} Important Notes: {len(meeting.important_notes)}")
        print(f"\n{ConsoleFormatter.CLOCK} Duration: {meeting.get_duration()}")
        print(f"{ConsoleFormatter.CLOCK} Timestamp: {meeting.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def _export_meeting(self) -> None:
        """Export meeting notes to file."""
        print(ConsoleFormatter.section("Export"))

        try:
            filepath = self.export_service.export_to_markdown(self.current_meeting)
            print_success(f"Meeting exported to: {filepath}")
        except Exception as e:
            print(f"Error exporting meeting: {e}")

    def _display_closing(self) -> None:
        """Display closing message."""
        print(ConsoleFormatter.section("Thank You"))
        print("Meeting notes have been saved successfully!")
        print(f"\n{ConsoleFormatter.ROBOT} AI Meeting Notes Manager\n")

