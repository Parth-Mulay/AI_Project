"""
Main application class for the Meeting Notes Manager.

Orchestrates the meeting workflow, user interaction, and interactive dashboard menus.
"""

import os
import sys
from datetime import datetime
from typing import Optional, List

from models.meeting_model import Meeting, ActionItem, Decision, ImportantNote
from services.detection_service import DetectionService, SummarizationService
from services.export_service import ExportService
from utils.formatter import ConsoleFormatter, print_header, print_subheader, print_section, print_success, print_ai_insight


class MeetingNotesApp:
    """
    Main application class for managing meeting notes.

    Handles the complete interactive dashboard workflow, search, settings, and RBAC roles.
    """

    def __init__(self):
        """Initialize the application and seed demo data."""
        self.detection_service = DetectionService()
        self.export_service = ExportService()
        self.meetings: List[Meeting] = []

        # UI State Variables
        self.current_user_role = "Member"  # Can be toggled to "Admin" in Workspace settings
        self.retention_period_days = 90
        self.slack_webhooks_enabled = True
        self.mock_api_fallback = False  # If True, simulates Anthropic API timeout -> fallback summarizer
        self.notifications = [
            "Welcome to AI Meeting Notes Manager!",
            "Day 5 UI/UX Prototype is loaded and active."
        ]

        # Seed initial meeting history data for a realistic SaaS UX
        self._seed_demo_data()

    def _seed_demo_data(self) -> None:
        """Seed initial meetings in the history archive using meeting_model."""
        # Meeting 1: Completed sprint planning
        m1 = Meeting("Sprint Planning - Week 14", ["Rahul", "Priya", "Amit"])
        m1.created_at = datetime(2026, 7, 6, 10, 0, 0)
        self.detection_service.process_message(m1, "Rahul: Authentication module is completed.")
        self.detection_service.process_message(m1, "Priya: We decided to use JWT for tokens.")
        self.detection_service.process_message(m1, "Amit: Rahul will review the API tomorrow.")
        m1.summary = SummarizationService.generate_summary(m1)
        self.meetings.append(m1)

        # Meeting 2: Marketing review
        m2 = Meeting("Marketing Alignment Call", ["Brian", "Priya"])
        m2.created_at = datetime(2026, 7, 10, 14, 30, 0)
        self.detection_service.process_message(m2, "Brian: Risk identified - deployment server has limited resources.")
        self.detection_service.process_message(m2, "Priya: Need to conduct a security review before launch.")
        m2.summary = SummarizationService.generate_summary(m2)
        self.meetings.append(m2)

    def start(self) -> None:
        """Start the interactive dashboard loop."""
        while True:
            self._display_dashboard_menu()
            choice = input("\nPlease select an option (1-8): ").strip()

            if choice == "1":
                self._start_new_meeting()
            elif choice == "2":
                self._upload_audio_mock()
            elif choice == "3":
                self._view_meeting_history()
            elif choice == "4":
                self._search_meetings()
            elif choice == "5":
                self._manage_workspace()
            elif choice == "6":
                self._system_settings()
            elif choice == "7":
                self._onboarding_tour()
            elif choice == "8":
                self._display_closing()
                break
            elif not choice:
                continue
            else:
                print(ConsoleFormatter.color_text("\n⚠️ Invalid selection. Please select 1-8.", "red"))
                input("Press Enter to continue...")

    def _display_dashboard_menu(self) -> None:
        """Render the polished console dashboard menu."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.header("AI Meeting Notes Manager"))
        print(ConsoleFormatter.color_text(f"           Workspace Dashboard | Role: {self.current_user_role.upper()}", "blue"))
        print(ConsoleFormatter.SEPARATOR)
        
        # Display Statistics Grid
        meetings_count = len(self.meetings)
        pending_actions = self._get_total_pending_actions_count()
        print(f" STATS: [⏱️ Saved: {meetings_count * 2.5} hrs]  [📝 Meetings: {meetings_count}]  [🎯 Actions Pending: {pending_actions}]")
        print(ConsoleFormatter.SEPARATOR)

        # Menu List
        print(" [1] 📝 Start Live Meeting Capture")
        print(" [2] 📤 Upload Meeting Audio / Documents (Mock)")
        print(" [3] 📂 View Meeting History & Archive")
        print(" [4] 🔍 Search Past Meetings")
        print(" [5] 👥 Team Workspace & RBAC Settings")
        print(" [6] ⚙️ System Settings & Integrations")
        print(" [7] 📖 Onboarding Guide / UI-UX Tour")
        print(" [8] ❌ Exit Application")
        print(ConsoleFormatter.SEPARATOR)

        # Active Alerts/Notifications
        alert_str = self.notifications[-1] if self.notifications else "No new alerts"
        print(f" Alert Log: [🔔] {alert_str}")
        print(ConsoleFormatter.SEPARATOR)

    def _get_total_pending_actions_count(self) -> int:
        """Calculate total number of pending action items across all meetings."""
        count = 0
        for m in self.meetings:
            count += len(m.action_items)
        return count

    def _start_new_meeting(self) -> None:
        """Interactive live capture flow."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.subheader("Meeting Setup"))
        
        title = input("Enter Meeting Title: ").strip()
        while not title:
            print("Meeting title cannot be empty.")
            title = input("Enter Meeting Title: ").strip()

        participants_input = input("Enter Participants (comma separated): ").strip()
        participants = [p.strip() for p in participants_input.split(",") if p.strip()]
        if not participants:
            participants = ["Unknown"]

        # Create meeting
        meeting = Meeting(title, participants)
        self.meetings.append(meeting)
        self.notifications.append(f"Meeting '{title}' started successfully.")
        
        print_success("Meeting Started Successfully")
        print(f"\n{ConsoleFormatter.NOTEPAD} Title: {title}")
        print(f"{ConsoleFormatter.PEOPLE} Participants: {', '.join(participants)}\n")

        print(ConsoleFormatter.section("Live Meeting Notes"))
        print("Enter conversation messages (format: 'Speaker: Message'). Type 'end' to finish:\n")

        message_count = 0
        while True:
            line = input().strip()
            if line.lower() == "end":
                break
            if not line:
                continue

            message_count += 1
            # Process and detect insights in real time
            insight = self.detection_service.process_message(meeting, line)
            
            if insight["type"] == "action":
                print_ai_insight("Action Item")
            elif insight["type"] == "decision":
                print_ai_insight("Decision")
            elif insight["type"] == "note":
                print_ai_insight("Important Note")

        print_success(f"\nMeeting Ended - {message_count} messages recorded")
        
        # Compile Summary (with optional mock fallback trigger)
        if self.mock_api_fallback:
            print(ConsoleFormatter.color_text("\n⚠️ Anthropic Claude API Timed out (Simulated).", "yellow"))
            print("🤖 TODO(security): Failing close safely, activating local fallback engine...")
            meeting.summary = SummarizationService.generate_summary(meeting)
            self.notifications.append(f"Fallback summary generated for '{meeting.title}'.")
        else:
            meeting.summary = SummarizationService.generate_summary(meeting)
            self.notifications.append(f"AI Summary generated for '{meeting.title}'.")

        # Show summary outcomes immediately
        self._display_meeting_details(meeting)
        
        # Check Slack notification triggers
        if self.slack_webhooks_enabled:
            print(ConsoleFormatter.info("Highlights automatically posted to #team-sync on Slack.", "💬"))

        # Export meeting
        try:
            filepath = self.export_service.export_to_markdown(meeting)
            print_success(f"Meeting notes exported to: {filepath}")
        except Exception as e:
            print(f"Error exporting meeting: {e}")

        input("\nPress Enter to return to Dashboard...")

    def _upload_audio_mock(self) -> None:
        """Simulate file upload and verification checks."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.subheader("Upload Audio or Documents"))
        print("Supported formats: .mp3, .wav, .docx, .pdf (Max size: 100MB)\n")

        filepath = input("Enter path to file: ").strip().strip('"\'')
        if not filepath:
            print(ConsoleFormatter.color_text("Upload cancelled.", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        # Verification Checks
        extension = os.path.splitext(filepath)[1].lower()
        allowed = [".mp3", ".wav", ".docx", ".pdf"]
        
        if extension not in allowed:
            print(ConsoleFormatter.color_text(f"\n❌ Error: Unsupported file format '{extension}'.", "red"))
            print("Allowed formats are: .mp3, .wav, .docx, .pdf")
            input("\nPress Enter to return to Dashboard...")
            return

        # Mocking size validation
        size_prompt = input("Enter simulated file size in MB (e.g. 15): ").strip()
        try:
            size_mb = float(size_prompt)
        except ValueError:
            size_mb = 10.0

        if size_mb > 100:
            print(ConsoleFormatter.color_text(f"\n❌ Error: File size ({size_mb}MB) exceeds the 100MB limit.", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        # Processing state simulation
        print("\n" + ConsoleFormatter.SEPARATOR)
        print("🤖 [AI Processing] Loading File and Verifying Magic Bytes...")
        print("🤖 [AI Processing] Transcribing content using Whisper API...")
        print("🤖 [AI Processing] Extracting highlights using Claude API...")
        print(ConsoleFormatter.SEPARATOR)

        # Create simulated meeting notes based on upload
        title = f"Uploaded Meeting - {os.path.basename(filepath)}"
        meeting = Meeting(title, ["Uploader", "AI-Transcriber"])
        self.detection_service.process_message(meeting, "Uploader: We uploaded the file for documentation.")
        self.detection_service.process_message(meeting, "AI-Transcriber: Decided to approve the release notes.")
        self.detection_service.process_message(meeting, "Uploader: Priya will deploy the code by Friday.")
        meeting.summary = SummarizationService.generate_summary(meeting)
        self.meetings.append(meeting)

        print_success("Audio Processed and Synced Successfully!")
        self.notifications.append(f"Uploaded meeting '{title}' processed.")
        
        self._display_meeting_details(meeting)
        input("\nPress Enter to return to Dashboard...")

    def _view_meeting_history(self) -> None:
        """Render the meeting history archive screen."""
        while True:
            ConsoleFormatter.clear_screen()
            print(ConsoleFormatter.subheader("Meeting History Archive"))
            
            meetings = self.meetings
            if not meetings:
                print("No meetings found in the archive.")
                input("\nPress Enter to return...")
                break

            for idx, m in enumerate(meetings, 1):
                date_str = m.created_at.strftime("%Y-%m-%d %H:%M")
                print(f" [{idx}] {m.title} ({date_str}) - {len(m.messages)} messages")
            
            print(f" [0] Return to Dashboard")

            choice = input("\nSelect a meeting to view details (0 to exit): ").strip()
            if choice == "0":
                break

            try:
                sel_idx = int(choice) - 1
                if 0 <= sel_idx < len(meetings):
                    self._meeting_details_tabs_menu(meetings[sel_idx])
                else:
                    print(ConsoleFormatter.color_text("Invalid selection.", "red"))
                    input("Press Enter...")
            except ValueError:
                print(ConsoleFormatter.color_text("Invalid input. Please enter a number.", "red"))
                input("Press Enter...")

    def _meeting_details_tabs_menu(self, meeting: Meeting) -> None:
        """Simulate tab navigation for meeting details."""
        while True:
            ConsoleFormatter.clear_screen()
            print(ConsoleFormatter.subheader(f"Meeting Details: {meeting.title}"))
            print(f"Participants: {', '.join(meeting.participants)}")
            print(f"Date: {meeting.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(ConsoleFormatter.SEPARATOR)
            print(" [1] 📄 View Summary Tab")
            print(" [2] 🎯 View Action Items Checklist Tab")
            print(" [3] 🏁 View Decisions Log Tab")
            print(" [4] 📝 View Timeline & Transcript Tab")
            print(" [5] 📥 Export Options Menu")
            print(" [6] 📂 Return to Archive List")
            print(ConsoleFormatter.SEPARATOR)

            choice = input("Select a view option (1-6): ").strip()
            if choice == "1":
                ConsoleFormatter.clear_screen()
                print(ConsoleFormatter.subheader("Tab: AI Summary"))
                print(meeting.summary)
                input("\nPress Enter to return...")
            elif choice == "2":
                ConsoleFormatter.clear_screen()
                print(ConsoleFormatter.subheader("Tab: Action Items"))
                if meeting.action_items:
                    for item in meeting.action_items:
                        print(ConsoleFormatter.action_item(str(item)))
                else:
                    print("No action items identified.")
                input("\nPress Enter to return...")
            elif choice == "3":
                ConsoleFormatter.clear_screen()
                print(ConsoleFormatter.subheader("Tab: Decisions Log"))
                if meeting.decisions:
                    for decision in meeting.decisions:
                        print(ConsoleFormatter.decision(str(decision)))
                else:
                    print("No decisions recorded.")
                input("\nPress Enter to return...")
            elif choice == "4":
                ConsoleFormatter.clear_screen()
                print(ConsoleFormatter.subheader("Tab: Transcript Timeline"))
                for msg in meeting.messages:
                    print(f"**{msg.speaker}**: {msg.content}")
                input("\nPress Enter to return...")
            elif choice == "5":
                ConsoleFormatter.clear_screen()
                print(ConsoleFormatter.subheader("Export Formats"))
                print(" [1] Download as PDF")
                print(" [2] Download as DOCX")
                print(" [3] Save as Markdown File")
                print(" [4] Cancel")
                exp = input("\nSelect export type: ").strip()
                if exp in ["1", "2", "3"]:
                    try:
                        filepath = self.export_service.export_to_markdown(meeting)
                        print_success(f"Successfully generated file package. Path: {filepath}")
                    except Exception as e:
                        print(f"Export error: {e}")
                    input("\nPress Enter to continue...")
            elif choice == "6":
                break

    def _display_meeting_details(self, meeting: Meeting) -> None:
        """Display all details of a meeting directly (helper)."""
        print(ConsoleFormatter.section("Meeting Results Summary"))
        print(f"Summary:\n{meeting.summary}\n")
        print("Action Items:")
        for item in meeting.action_items:
            print(ConsoleFormatter.action_item(str(item)))
        print("\nDecisions:")
        for dec in meeting.decisions:
            print(ConsoleFormatter.decision(str(dec)))

    def _search_meetings(self) -> None:
        """Simulate search query screen."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.subheader("Search Meeting Archives"))
        
        query = input("Enter search keyword or concept: ").strip().lower()
        if not query:
            return

        print("\n🤖 Running full-text and semantic embedding search...")
        matches = []
        
        for m in self.meetings:
            match_found = False
            # Check title
            if query in m.title.lower():
                match_found = True
            # Check transcript
            for msg in m.messages:
                if query in msg.content.lower():
                    match_found = True
            
            if match_found:
                matches.append(m)

        print(f"\nFound {len(matches)} matching meeting(s):\n")
        if matches:
            for idx, m in enumerate(matches, 1):
                print(f" [{idx}] {m.title} ({m.created_at.strftime('%Y-%m-%d')})")
            
            sel = input("\nSelect a meeting number to open (or press Enter to return): ").strip()
            try:
                sel_idx = int(sel) - 1
                if 0 <= sel_idx < len(matches):
                    self._meeting_details_tabs_menu(matches[sel_idx])
            except ValueError:
                pass
        else:
            print(ConsoleFormatter.color_text("No search results found (Empty State).", "yellow"))
            input("\nPress Enter...")

    def _manage_workspace(self) -> None:
        """Workspace settings and RBAC controls."""
        while True:
            ConsoleFormatter.clear_screen()
            print(ConsoleFormatter.subheader("Team Workspace & RBAC Settings"))
            print(f"Current User: Priya | Active Role: {self.current_user_role.upper()}")
            print(ConsoleFormatter.SEPARATOR)
            print(" Workspace Members:")
            print(" - Priya (current user) | Role: Admin/Member Toggle")
            print(" - Rahul (Developer)    | Role: Member")
            print(" - Amit (Project Lead)  | Role: Admin")
            print(" - Brian (IT Compliance)| Role: Admin")
            print(ConsoleFormatter.SEPARATOR)
            print(" Options:")
            print(f" [1] Toggle active testing role (Currently: {self.current_user_role})")
            print(" [2] View organization security audit logs (ADMIN ONLY)")
            print(" [3] Return to Dashboard")
            print(ConsoleFormatter.SEPARATOR)

            choice = input("\nSelect option: ").strip()
            if choice == "1":
                self.current_user_role = "Admin" if self.current_user_role == "Member" else "Member"
                self.notifications.append(f"User role toggled to {self.current_user_role}.")
            elif choice == "2":
                if self.current_user_role != "Admin":
                    print(ConsoleFormatter.color_text("\n❌ Access Denied: Role 'Admin' required to view audit logs.", "red"))
                    input("\nPress Enter to continue...")
                else:
                    ConsoleFormatter.clear_screen()
                    print(ConsoleFormatter.subheader("Organization Security Audit Logs"))
                    print(" [2026-07-13 09:42:01] SEC-AUDIT: User login verified via Azure AD SSO.")
                    print(" [2026-07-13 09:46:12] SEC-AUDIT: Database retention sweep scheduled.")
                    print(" [2026-07-13 10:15:30] SEC-AUDIT: Role update requested.")
                    input("\nPress Enter to return...")
            elif choice == "3":
                break

    def _system_settings(self) -> None:
        """Modify compliance policies and integrations."""
        while True:
            ConsoleFormatter.clear_screen()
            print(ConsoleFormatter.subheader("System Settings & Integrations"))
            print(f" Data Retention: {self.retention_period_days} Days")
            print(f" Slack Webhook Integration: {'ENABLED' if self.slack_webhooks_enabled else 'DISABLED'}")
            print(f" API Fallback Mode (Simulate Outages): {'ACTIVE' if self.mock_api_fallback else 'INACTIVE'}")
            print(ConsoleFormatter.SEPARATOR)
            print(" Options:")
            print(" [1] Modify Data Retention Limit (ADMIN ONLY)")
            print(" [2] Toggle Slack Webhook Integration")
            print(" [3] Toggle API Fallback Outage Simulation")
            print(" [4] Return to Dashboard")
            print(ConsoleFormatter.SEPARATOR)

            choice = input("\nSelect option: ").strip()
            if choice == "1":
                if self.current_user_role != "Admin":
                    print(ConsoleFormatter.color_text("\n❌ Access Denied: Admin role required.", "red"))
                    input("Press Enter...")
                else:
                    days = input("Enter new retention period in days (e.g., 30): ").strip()
                    try:
                        self.retention_period_days = int(days)
                        print_success(f"Retention period updated to {self.retention_period_days} days.")
                        self.notifications.append(f"Retention policy adjusted to {self.retention_period_days} days.")
                    except ValueError:
                        print("Invalid integer.")
                    input("Press Enter...")
            elif choice == "2":
                self.slack_webhooks_enabled = not self.slack_webhooks_enabled
                self.notifications.append(f"Slack integration state changed.")
            elif choice == "3":
                self.mock_api_fallback = not self.mock_api_fallback
                self.notifications.append(f"API fallback state changed.")
            elif choice == "4":
                break

    def _onboarding_tour(self) -> None:
        """Guided tour explaining SaaS design and structure."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.subheader("SaaS Application Guided Tour"))
        print("Welcome to the UI/UX design showcase of the AI Meeting Notes Manager!\n")
        print("Our visual interface layout uses the Left Sidebar layout model:")
        print(" 1. Sidebar Nav: Houses Meetings Archive, Search, Settings, and Profiles.")
        print(" 2. Dashboard Home: Displays key telemetry (time saved, stats) and active action checkmarks.")
        print(" 3. Editor View: Offers interactive tab navigation (Summary, Action List, Decisions, Transcript).")
        print(" 4. Trust Badges: Every AI highlight shows the confidence level and direct source context.")
        print(" 5. Fail-Safe: Prominent fallbacks alert users if an API fails, switching to local summaries.")
        print("\nThis CLI prototype simulates this full layout workflow!")
        input("\nPress Enter to return to Dashboard...")

    def _display_closing(self) -> None:
        """Display closing message."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.header("Thank You"))
        print("Day 5 Upgraded CLI Prototype Exited Successfully.")
        print(f"\n{ConsoleFormatter.ROBOT} AI Meeting Notes Manager - Prototype v0.3.0\n")


if __name__ == "__main__":
    app = MeetingNotesApp()
    app.start()
