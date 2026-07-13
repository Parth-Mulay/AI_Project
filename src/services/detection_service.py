"""
Service for processing and analyzing meeting content.

Handles detection of insights and generation of summaries.
"""

from typing import List, Set
from models.meeting_model import Meeting, ActionItem, Decision, ImportantNote, Message
from utils.keyword_detector import KeywordDetector


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
        Analyze the full text of an uploaded document.

        Extracts participants, transcript timeline, action items, decisions,
        risks, next steps, deadlines, and generates an executive summary.

        Populates all attributes directly on the Meeting object.
        """
        if not text.strip():
            meeting.summary = "Empty document."
            return

        import re

        # 1. Extract Participants
        participants = []
        # Check for explicit participants lines
        for line in text.split('\n'):
            line_strip = line.strip()
            match = re.match(r'(?i)^participants\s*:\s*(.*)', line_strip)
            if match:
                names = match.group(1).split(',')
                for name in names:
                    name_clean = name.strip()
                    if name_clean and name_clean not in participants:
                        participants.append(name_clean)

        # Check for speaker lines: "Name: message"
        for line in text.split('\n'):
            line_strip = line.strip()
            if ":" in line_strip:
                part0, part1 = line_strip.split(":", 1)
                part0 = part0.strip()
                if 0 < len(part0) < 30 and re.match(r'^[A-Za-z\s]+$', part0) and part0.lower() not in [
                    "http", "https", "note", "warning", "error", "info", "date", "time", "summary", "decision", "action"
                ]:
                    if part0 not in participants:
                        participants.append(part0)

        if not participants:
            participants = ["Document Reader"]

        meeting.participants = participants

        # 2. Add Messages (Timeline)
        # Parse text line by line to build transcript messages
        for line in text.split('\n'):
            line_strip = line.strip()
            if not line_strip:
                continue

            speaker, content = KeywordDetector.extract_speaker(line_strip)
            if speaker and speaker in participants:
                meeting.add_message(Message(speaker, content))
            else:
                meeting.add_message(Message("Document Content", line_strip))

        # 3. Sentence Splitting
        # Split text into sentences for granular insight extraction
        raw_sentences = re.split(r'[.!?](?=\s|$)', text)
        sentences = []
        for s in raw_sentences:
            s_clean = s.strip().replace('\n', ' ').strip()
            if s_clean:
                sentences.append(s_clean)

        # 4. Extract Action Items
        action_keywords = ["will", "must", "should", "need to", "action", "follow-up", "deadline", "assign", "responsible", "task"]
        for sent in sentences:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in action_keywords):
                # Detect Owner
                owner = "Unassigned"
                for p in participants:
                    if p.lower() in sent_lower:
                        owner = p
                        break
                if owner == "Unassigned":
                    assign_match = re.search(r'(?i)assign(?:ed)? to\s+([A-Z][a-z]+)', sent)
                    if assign_match:
                        owner = assign_match.group(1)
                    else:
                        will_match = re.search(r'\b([A-Z][a-z]+)\s+(?:will|should|must|needs to)\b', sent)
                        if will_match:
                            owner = will_match.group(1)

                # Detect Deadline
                deadline = ""
                deadline_match = re.search(r'(?i)(?:by|before|due|deadline)\s+([A-Za-z0-9\s\-]{2,25}?)(?:\.|$|,|\s+and)', sent)
                if deadline_match:
                    deadline = deadline_match.group(1).strip()
                elif "tomorrow" in sent_lower:
                    deadline = "Tomorrow"
                elif "next week" in sent_lower:
                    deadline = "Next week"
                elif "friday" in sent_lower:
                    deadline = "Friday"

                action_item = ActionItem(sent, owner, deadline)
                if not self._is_duplicate_action(meeting, action_item):
                    meeting.add_action_item(action_item)

        # 5. Extract Decisions
        decision_keywords = ["approved", "agreed", "decided", "accepted", "confirmed", "rejected", "resolved"]
        for sent in sentences:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in decision_keywords):
                decision = Decision(sent, f"Context: {sent[:40]}...")
                if not self._is_duplicate_decision(meeting, decision):
                    meeting.add_decision(decision)

        # 6. Extract Risks / Notes
        risk_keywords = ["risk", "issue", "blocker", "concern", "problem", "critical", "warning"]
        for sent in sentences:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in risk_keywords):
                note = ImportantNote(sent, "risk")
                if not self._is_duplicate_note(meeting, note):
                    meeting.add_important_note(note)

        # 7. Extract Next Steps
        next_steps = []
        next_keywords = ["next step", "future", "upcoming", "later", "action plan", "milestone"]
        for sent in sentences:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in next_keywords):
                next_steps.append(sent)

        # 8. Extract Deadlines list
        deadlines_list = []
        deadline_kws = ["deadline", "due", "by tomorrow", "by friday", "by monday", "by march 2027", "timeline", "target date"]
        for sent in sentences:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in deadline_kws):
                deadlines_list.append(sent)

        # 9. Generate Executive Summary & Key Discussion Points
        intro_sentences = []
        for sent in sentences:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in ["meeting", "discussed", "focus", "align", "goal", "vision"]):
                intro_sentences.append(sent)
                if len(intro_sentences) >= 3:
                    break

        if len(intro_sentences) < 3:
            for sent in sentences:
                if sent not in intro_sentences:
                    intro_sentences.append(sent)
                    if len(intro_sentences) >= 3:
                        break

        executive_summary = " ".join(intro_sentences)

        discussion_points = []
        for sent in sentences:
            sent_lower = sent.lower()
            is_key = any(kw in sent_lower for kw in ["decided", "approved", "agreed", "will", "must", "should", "risk", "issue", "blocker"])
            if is_key and sent not in intro_sentences:
                discussion_points.append(sent)
                if len(discussion_points) >= 5:
                    break

        if not discussion_points:
            discussion_points = [sent for sent in sentences if sent not in intro_sentences][:3]

        # 10. Format and Assign Summary
        summary_parts = []
        summary_parts.append(f"## Executive Summary\n{executive_summary}\n")

        if discussion_points:
            summary_parts.append("## Key Discussion Points")
            for pt in discussion_points:
                summary_parts.append(f"- {pt}")
            summary_parts.append("")

        if meeting.important_notes:
            summary_parts.append("## Risks")
            for r in meeting.important_notes:
                summary_parts.append(f"- {r.description}")
            summary_parts.append("")

        if next_steps:
            summary_parts.append("## Next Steps")
            for ns in next_steps:
                summary_parts.append(f"- {ns}")
            summary_parts.append("")

        if deadlines_list:
            summary_parts.append("## Deadlines")
            for dl in deadlines_list:
                summary_parts.append(f"- {dl}")
            summary_parts.append("")

        meeting.summary = "\n".join(summary_parts).strip()


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
