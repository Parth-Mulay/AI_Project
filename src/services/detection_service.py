"""
Service for processing and analyzing meeting content.

Handles detection of insights and generation of summaries.
"""

from typing import List, Set
from ..models.meeting_model import Meeting, ActionItem, Decision, ImportantNote, Message
from ..utils.keyword_detector import KeywordDetector


class DetectionService:
    """
    Service for detecting insights from meeting content.

    Uses rule-based keyword matching to identify action items, decisions, and notes.
    """

    def __init__(self):
        """Initialize the detection service."""
        self.detected_insights = {"actions": [], "decisions": [], "notes": []}

    def process_message(self, meeting: Meeting, line: str) -> dict:
        """
        Process a single message line from the meeting.

        Detects action items, decisions, and important notes.

        Returns: {"type": "action" | "decision" | "note" | None, "content": str}
        """
        if not line.strip():
            return {"type": None, "content": ""}

        # Extract speaker and content
        speaker, content = KeywordDetector.extract_speaker(line)

        # Create and add message to meeting
        message = Message(speaker if speaker else "Unknown", content)
        meeting.add_message(message)

        # Detect insights
        insight = {"type": None, "content": ""}

        # Check for action items
        action_result = KeywordDetector.detect_action_item(content)
        if action_result:
            action_text, due_date = action_result
            owner = KeywordDetector.extract_owner(content)

            action_item = ActionItem(action_text, owner, due_date or "")

            # Avoid duplicates
            if not self._is_duplicate_action(meeting, action_item):
                meeting.add_action_item(action_item)
                insight["type"] = "action"
                insight["content"] = action_text

        # Check for decisions
        if not insight["type"]:
            decision_result = KeywordDetector.detect_decision(content)
            if decision_result:
                decision = Decision(decision_result, f"Context: {content[:50]}...")

                # Avoid duplicates
                if not self._is_duplicate_decision(meeting, decision):
                    meeting.add_decision(decision)
                    insight["type"] = "decision"
                    insight["content"] = decision_result

        # Check for important notes
        if not insight["type"]:
            note_result = KeywordDetector.detect_important_note(content)
            if note_result:
                note_text, category = note_result
                note = ImportantNote(note_text, category)

                # Avoid duplicates
                if not self._is_duplicate_note(meeting, note):
                    meeting.add_important_note(note)
                    insight["type"] = "note"
                    insight["content"] = note_text

        return insight

    @staticmethod
    def _is_duplicate_action(meeting: Meeting, new_action: ActionItem) -> bool:
        """Check if action item already exists."""
        for existing in meeting.action_items:
            if existing.description.lower() == new_action.description.lower():
                return True
        return False

    @staticmethod
    def _is_duplicate_decision(meeting: Meeting, new_decision: Decision) -> bool:
        """Check if decision already exists."""
        for existing in meeting.decisions:
            if existing.description.lower() == new_decision.description.lower():
                return True
        return False

    @staticmethod
    def _is_duplicate_note(meeting: Meeting, new_note: ImportantNote) -> bool:
        """Check if note already exists."""
        for existing in meeting.important_notes:
            if existing.description.lower() == new_note.description.lower():
                return True
        return False

    def analyze_document(self, meeting: Meeting, text: str) -> None:
        """
        Analyze the full text of an uploaded document using the advanced NLP pipeline.

        Extracts participants, timeline, action items, decisions, and risks dynamically.
        Populates all attributes directly on the Meeting object.
        """
        if not text.strip():
            meeting.summary = "Empty document."
            return

        from ..nlp.pipeline import MeetingNlpPipeline
        pipeline = MeetingNlpPipeline()
        
        # Always run with debug_mode=True to output the Developer Debug Log (Step 14)
        nlp_result = pipeline.process(text, debug_mode=True)

        # Clear existing meeting data to prevent caching / history bleed (Step 12)
        meeting.participants = nlp_result["participants"]
        meeting.messages = []
        meeting.action_items = []
        meeting.decisions = []
        meeting.important_notes = []

        # Populate timeline (messages)
        for msg in nlp_result["timeline"]:
            meeting.add_message(Message(msg["speaker"], msg["content"]))

        # Populate action items
        for action in nlp_result["action_items"]:
            meeting.add_action_item(ActionItem(
                description=action["task"],
                assigned_to=action["owner"],
                due_date=action["deadline"]
            ))

        # Populate decisions
        for decision in nlp_result["decisions"]:
            meeting.add_decision(Decision(
                description=decision["decision"],
                context=decision["context"]
            ))

        # Populate risks (important_notes of category 'risk')
        for risk in nlp_result["risks"]:
            meeting.add_important_note(ImportantNote(
                description=risk["description"],
                category="risk"
            ))

        # Set summary
        meeting.summary = nlp_result["summary"]


class SummarizationService:
    """
    Service for generating meeting summaries.

    Uses rule-based approach to extract key points.
    """

    @staticmethod
    def generate_summary(meeting: Meeting) -> str:
        """
        Generate a summary of the meeting.

        Extracts key points from messages containing important keywords.
        """
        if not meeting.messages:
            return "No meeting content to summarize."

        # Extract key sentences
        key_sentences = SummarizationService._extract_key_sentences(meeting)

        if not key_sentences:
            return "Meeting conducted with focus on ongoing tasks and discussions."

        # Create summary
        summary = "Key points discussed:\n\n"
        for i, sentence in enumerate(key_sentences, 1):
            summary += f"• {sentence}\n"

        return summary.strip()

    @staticmethod
    def _extract_key_sentences(meeting: Meeting, max_sentences: int = 5) -> List[str]:
        """
        Extract important sentences from meeting messages.

        Prioritizes sentences that contain action items or decisions.
        """
        key_sentences: Set[str] = set()

        # Add sentences with action items
        for action in meeting.action_items:
            key_sentences.add(action.description)

        # Add sentences with decisions
        for decision in meeting.decisions:
            key_sentences.add(decision.description)

        # Add sentences with important notes
        for note in meeting.important_notes:
            key_sentences.add(note.description)

        # If not enough sentences, add some from messages
        if len(key_sentences) < max_sentences:
            for message in meeting.messages:
                if len(message.content) > 20:  # Skip very short messages
                    key_sentences.add(f"{message.speaker}: {message.content}")

                if len(key_sentences) >= max_sentences:
                    break

        return list(key_sentences)[:max_sentences]
