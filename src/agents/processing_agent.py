"""Agent 2: Processing & Extraction Agent.

Responsible for deep feature extraction, line-by-line keyword/NLP analysis,
speaker identification, action item detection, and decision logging.
"""

from typing import Any, Dict, List, Set
from .base_agent import BaseAgent
from ..utils.keyword_detector import KeywordDetector


class ProcessingExtractionAgent(BaseAgent):
    """
    Agent 2 - Processing & Extraction Agent.

    Parses sanitized meeting lines to extract speakers, action items, decisions, notes, and topics.
    """

    def __init__(self):
        super().__init__(
            name="Agent-2:ProcessingExtraction",
            role="Extracts speakers, raw action items, decisions, notes, and topics from sanitized lines.",
        )

    def process(self, context: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
        sanitized_lines: List[str] = context.get("sanitized_lines", [])

        if not sanitized_lines:
            logs.append("Warning: Received empty sanitized lines array.")

        messages: List[Dict[str, str]] = []
        raw_action_items: List[Dict[str, Any]] = []
        raw_decisions: List[Dict[str, Any]] = []
        raw_notes: List[Dict[str, Any]] = []
        speakers: Set[str] = set()

        for idx, line in enumerate(sanitized_lines):
            speaker, content = KeywordDetector.extract_speaker(line)
            assigned_speaker = speaker if speaker else "Presenter"
            speakers.add(assigned_speaker)

            messages.append({"speaker": assigned_speaker, "content": content, "line_no": idx + 1})

            # Detect action items
            action_result = KeywordDetector.detect_action_item(content)
            if action_result:
                action_text, due_date = action_result
                owner = self._resolve_action_owner(content, assigned_speaker)
                raw_action_items.append({
                    "description": action_text,
                    "owner": owner,
                    "due_date": due_date or "TBD",
                    "raw_context": content,
                })

            # Detect decisions
            decision_result = KeywordDetector.detect_decision(content)
            if decision_result:
                raw_decisions.append({
                    "description": decision_result,
                    "context": f"Line {idx+1}: {content[:60]}",
                })

            # Detect important notes
            note_result = KeywordDetector.detect_important_note(content)
            if note_result:
                note_text, category = note_result
                raw_notes.append({
                    "description": note_text,
                    "category": category or "General",
                })

        # Extract dominant topics / keywords
        topics = self._extract_topics(sanitized_lines)

        logs.append(
            f"Extracted {len(messages)} messages, {len(raw_action_items)} action items, "
            f"{len(raw_decisions)} decisions, and {len(raw_notes)} notes from {len(speakers)} speakers."
        )

        return {
            "messages": messages,
            "speakers": sorted(list(speakers)),
            "raw_action_items": raw_action_items,
            "raw_decisions": raw_decisions,
            "raw_notes": raw_notes,
            "extracted_topics": topics,
        }

    @staticmethod
    def _resolve_action_owner(content: str, assigned_speaker: str) -> str:
        """Prefer the speaker when the extracted owner is just a pronoun or missing."""
        owner = KeywordDetector.extract_owner(content)
        if not owner:
            return assigned_speaker

        generic_owners = {"i", "we", "someone", "team"}
        if owner.strip().lower() in generic_owners:
            return assigned_speaker

        return owner

    @staticmethod
    def _extract_topics(lines: List[str]) -> List[str]:
        """Simple keyword frequency based topic extraction."""
        common_words = {"the", "and", "to", "a", "of", "in", "is", "it", "that", "for", "on", "was", "with", "as", "at", "by", "an", "be", "this", "which", "or", "from"}
        freq: Dict[str, int] = {}
        for line in lines:
            words = line.lower().split()
            for w in words:
                cleaned = "".join(c for c in w if c.isalnum())
                if len(cleaned) > 3 and cleaned not in common_words:
                    freq[cleaned] = freq.get(cleaned, 0) + 1

        sorted_topics = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [t[0].capitalize() for t in sorted_topics[:5]]
