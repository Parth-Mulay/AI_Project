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

    def _extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            if not text.strip():
                raise ValueError("The document is empty.")
            return text
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"The document is corrupted or unreadable. Details: {e}")

    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from docx using zipfile and xml parsing (no dependencies)."""
        import zipfile
        import xml.etree.ElementTree as ET
        try:
            if not zipfile.is_zipfile(file_path):
                raise ValueError("The document is corrupted or unreadable.")
            with zipfile.ZipFile(file_path) as z:
                if "word/document.xml" not in z.namelist():
                    raise ValueError("The document is corrupted or not a valid Word file.")
                try:
                    xml_content = z.read("word/document.xml")
                except RuntimeError as re_err:
                    if "encrypted" in str(re_err).lower() or "password" in str(re_err).lower():
                        raise ValueError("The document is password protected and cannot be read.")
                    raise ValueError(f"The document is corrupted or unreadable. Details: {re_err}")
                root = ET.fromstring(xml_content)
                texts = []
                for elem in root.iter():
                    if elem.tag.endswith("}t") or elem.tag == "t":
                        if elem.text:
                            texts.append(elem.text)
                extracted = " ".join(texts).strip()
                if not extracted:
                    raise ValueError("The document is empty.")
                return extracted
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"The document is corrupted or unreadable. Details: {e}")

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from pdf using regex stream parsing (no dependencies)."""
        import re
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            if b"/Encrypt" in content or b"/encrypt" in content:
                raise ValueError("The document is password protected and cannot be read.")
            matches = re.findall(rb"\(([^)]*)\)", content)
            texts = []
            for m in matches:
                try:
                    text = m.decode("utf-8", errors="ignore")
                    text = text.replace("\\(", "(").replace("\\)", ")")
                    if text.strip():
                        texts.append(text)
                except Exception:
                    pass
            extracted = " ".join(texts).strip()
            if not extracted:
                raise ValueError("The document is empty.")
            return extracted
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"The document is corrupted or unreadable. Details: {e}")

    def _extract_text_from_audio(self, file_path: str) -> str:
        """Transcribe and extract text from audio file."""
        from audio.transcriber import AudioTranscriber
        try:
            transcriber = AudioTranscriber()
            text = transcriber.transcribe(file_path)
            if not text.strip():
                raise ValueError("The document is empty.")
            return text
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"The document is corrupted or unreadable. Details: {e}")

    def _upload_audio_mock(self) -> None:
        """Simulate file upload, run validation pipeline, and extract actual AI insights."""
        ConsoleFormatter.clear_screen()
        print(ConsoleFormatter.subheader("Upload Audio or Documents"))
        print("Supported formats: .mp3, .wav, .docx, .pdf, .txt")
        print("Max limits: 100MB for audio, 10MB for text/documents\n")

        filepath = input("Enter path to file: ").strip().strip('"\'')
        if not filepath:
            print(ConsoleFormatter.color_text("Upload cancelled.", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        # 1. Validation Checks: Exist check
        if not os.path.exists(filepath):
            print(ConsoleFormatter.color_text(f"\n❌ Error: File not found at path '{filepath}'.", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        # 2. Validation Checks: Extension check
        extension = os.path.splitext(filepath)[1].lower()
        allowed = [".mp3", ".wav", ".docx", ".pdf", ".txt"]
        
        if extension not in allowed:
            print(ConsoleFormatter.color_text(f"\n❌ Error: Unsupported file format '{extension}'.", "red"))
            print("Allowed formats are: .mp3, .wav, .docx, .pdf, .txt")
            input("\nPress Enter to return to Dashboard...")
            return

        # 3. Validation Checks: Size limit check
        try:
            file_size_bytes = os.path.getsize(filepath)
            file_size_mb = file_size_bytes / (1024 * 1024)
        except Exception as e:
            print(ConsoleFormatter.color_text(f"\n❌ Error: The document is corrupted or unreadable. Details: {e}", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        is_audio = extension in [".mp3", ".wav"]
        max_limit_mb = 100.0 if is_audio else 10.0
        if file_size_mb > max_limit_mb:
            print(ConsoleFormatter.color_text(f"\n❌ Error: File size ({file_size_mb:.2f}MB) exceeds the limit of {max_limit_mb}MB.", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        # 4. Processing stages animation
        import time
        print("\n🤖 [AI Processing] Reading document...")
        time.sleep(0.2)

        try:
            if extension == ".txt":
                text = self._extract_text_from_txt(filepath)
            elif extension == ".docx":
                text = self._extract_text_from_docx(filepath)
            elif extension == ".pdf":
                text = self._extract_text_from_pdf(filepath)
            else:
                text = self._extract_text_from_audio(filepath)
        except ValueError as ve:
            print(ConsoleFormatter.color_text(f"\n❌ Error: {ve}", "red"))
            input("\nPress Enter to return to Dashboard...")
            return
        except Exception as e:
            print(ConsoleFormatter.color_text(f"\n❌ Error: The document is corrupted or unreadable. Details: {e}", "red"))
            input("\nPress Enter to return to Dashboard...")
            return

        print("🤖 [AI Processing] Extracting text...")
        time.sleep(0.2)

        # Create dynamically populated Meeting
        title = f"Uploaded Document - {os.path.basename(filepath)}"
        meeting = Meeting(title, ["Unknown"])
        
        print("🤖 [AI Processing] Analyzing meeting...")
        time.sleep(0.2)
        print("🤖 [AI Processing] Generating summary...")
        time.sleep(0.2)
        print("🤖 [AI Processing] Extracting action items...")
        time.sleep(0.2)

        # Dynamic AI Pipeline Run
        self.detection_service.analyze_document(meeting, text)
        self.meetings.append(meeting)

        print("🤖 [AI Processing] Completed.")
        time.sleep(0.1)
        print_success("Document Processed Successfully!")
        self.notifications.append(f"Processed file '{title}' successfully.")
        
        self._display_meeting_details(meeting)
        
        # Export meeting notes
        try:
            exp_path = self.export_service.export_to_markdown(meeting)
            print_success(f"Meeting notes exported to: {exp_path}")
        except Exception as e:
            print(f"Export failed: {e}")
            
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
