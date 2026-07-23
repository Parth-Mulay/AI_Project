"""
Service for processing and analyzing meeting content.

Handles detection of insights and generation of summaries.
"""

import hashlib
import copy
import threading
from collections import OrderedDict
from typing import List, Set
from ..models.meeting_model import Meeting, ActionItem, Decision, ImportantNote, Message
from ..utils.keyword_detector import KeywordDetector
from backend.ai.llm_service import AISummaryService
from backend.ai.rag import LocalRagPipeline
from backend.core.logging import get_logger

logger = get_logger(__name__)


class DetectionService:
    """
    Service for detecting insights from meeting content.

    Uses rule-based keyword matching to identify action items, decisions, and notes.
    """

    _MAX_CACHE_SIZE = 100

    def __init__(self):
        """Initialize the detection service."""
        self.detected_insights = {"actions": [], "decisions": [], "notes": []}
        self._analysis_cache = OrderedDict()
        self._cache_lock = threading.Lock()

    def process_message(self, meeting: Meeting, line: str) -> dict:
        """
        Process a single message line from the meeting.

        Detects action items, decisions, and important notes.

        Returns: {"type": "action" | "decision" | "note" | None, "content": str}
        """
        if not line.strip():
            logger.debug("Skipped empty meeting line")
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

    def _get_cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _get_cached_result(self, cache_key: str):
        with self._cache_lock:
            if cache_key in self._analysis_cache:
                self._analysis_cache.move_to_end(cache_key)
                logger.debug("Analysis cache hit for key %s", cache_key[:12])
                return copy.deepcopy(self._analysis_cache[cache_key])
            return None

    def _set_cached_result(self, cache_key: str, result: dict) -> None:
        with self._cache_lock:
            self._analysis_cache[cache_key] = copy.deepcopy(result)
            if len(self._analysis_cache) > self._MAX_CACHE_SIZE:
                self._analysis_cache.popitem(last=False)

    def analyze_document(self, meeting: Meeting, text: str) -> None:
        """
        Analyze the full text of an uploaded document using the advanced NLP pipeline.

        Extracts participants, timeline, action items, decisions, and risks dynamically.
        Populates all attributes directly on the Meeting object.
        """
        if not text.strip():
            meeting.summary = "Empty document."
            logger.warning("Document analysis skipped because the text was empty")
            return

        cache_key = self._get_cache_key(text)
        cached = self._get_cached_result(cache_key)
        if cached is not None:
            logger.info("Using cached analysis result for %s", meeting.title)
            nlp_result = cached
        else:
            from ..nlp.pipeline import MeetingNlpPipeline
            pipeline = MeetingNlpPipeline()
            logger.info("Analyzing document for meeting %s", meeting.title)
            nlp_result = pipeline.process(text, debug_mode=True)
            self._set_cached_result(cache_key, nlp_result)

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

        meeting.summary = nlp_result["summary"]
        logger.info("Document analysis completed for %s", meeting.title)


class SummarizationService:
    """
    Service for generating meeting summaries.

    Uses rule-based approach to extract key points.
    """

    _MAX_CHARS = 5000

    @staticmethod
    def _truncate_text(text: str, max_chars: int = None) -> str:
        if max_chars is None:
            max_chars = SummarizationService._MAX_CHARS
        if len(text) <= max_chars:
            return text
        truncated = text[:max_chars]
        last_period = truncated.rfind(".")
        if last_period > max_chars // 2:
            return text[: last_period + 1]
        last_space = truncated.rfind(" ")
        if last_space > max_chars // 2:
            return text[:last_space]
        return truncated

    @staticmethod
    def generate_summary(meeting: Meeting) -> str:
        """
        Generate a summary of the meeting.

        Uses the existing rule-based summarizer by default and only consults the
        AI service when it is available and useful.
        """
        if not meeting.messages:
            return "No meeting content to summarize."

        key_sentences = SummarizationService._extract_key_sentences(meeting)

        if not key_sentences:
            return "Meeting conducted with focus on ongoing tasks and discussions."

        summary = "Key points discussed:\n\n"
        for i, sentence in enumerate(key_sentences, 1):
            summary += f"• {sentence}\n"

        try:
            join_text = "\n".join([message.content for message in meeting.messages if message.content])
            join_text = SummarizationService._truncate_text(join_text)
            if len(join_text) > 40:
                service = AISummaryService()
                result = service.generate_summary(join_text)
                if result.get("source") == "llm":
                    return result["summary"]
        except Exception as exc:
            logger.debug("AI summary unavailable, using fallback: %s", exc)

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
