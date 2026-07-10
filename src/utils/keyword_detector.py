"""
Keyword-based detection service for meeting intelligence.

Uses rule-based keyword matching to detect action items, decisions, and important notes.
"""

import re
from typing import Tuple, Optional


class KeywordDetector:
    """
    Detects action items, decisions, and important notes using keyword matching.

    This rule-based approach simulates AI intelligence without using external APIs.
    """

    # Keywords for action items
    ACTION_KEYWORDS = {
        "will": [],
        "need to": [],
        "should": [],
        "must": [],
        "assign": [],
        "complete": [],
        "finish": [],
        "build": [],
        "review": [],
        "approve": [],
        "by friday": ["due_date"],
        "by monday": ["due_date"],
        "by today": ["due_date"],
        "by tomorrow": ["due_date"],
        "next week": ["due_date"],
        "eow": ["due_date"],
        "asap": ["due_date"],
        "urgent": ["due_date"],
    }

    # Keywords for decisions
    DECISION_KEYWORDS = {
        "decided": [],
        "approved": [],
        "agreed": [],
        "finalized": [],
        "confirmed": [],
        "accepted": [],
        "resolved": [],
        "implemented": [],
        "adopted": [],
        "selected": [],
    }

    # Keywords for important notes
    IMPORTANT_NOTE_KEYWORDS = {
        "risk": ["risk"],
        "issue": ["issue"],
        "blocker": ["blocker"],
        "problem": ["issue"],
        "concern": ["issue"],
        "reminder": ["reminder"],
        "note": ["note"],
        "important": ["note"],
        "critical": ["risk"],
        "urgent": ["risk"],
    }

    @staticmethod
    def extract_speaker(line: str) -> Tuple[str, str]:
        """
        Extract speaker and content from a line.

        Format: "Speaker: Content"
        """
        if ":" in line:
            parts = line.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        return "", line

    @staticmethod
    def detect_action_item(line: str) -> Optional[Tuple[str, Optional[str]]]:
        """
        Detect if a line contains an action item.

        Returns: (action_item_description, due_date) or None
        """
        line_lower = line.lower()

        # Check for action keywords
        for keyword in KeywordDetector.ACTION_KEYWORDS.keys():
            if keyword in line_lower:
                # Extract due date if present
                due_date = KeywordDetector._extract_due_date(line_lower)

                # Clean up the action item text
                action_text = line.strip()
                if action_text.endswith("."):
                    action_text = action_text[:-1]

                return action_text, due_date

        return None

    @staticmethod
    def detect_decision(line: str) -> Optional[str]:
        """
        Detect if a line contains a decision.

        Returns: decision_description or None
        """
        line_lower = line.lower()

        # Check for decision keywords
        for keyword in KeywordDetector.DECISION_KEYWORDS.keys():
            if keyword in line_lower:
                decision_text = line.strip()
                if decision_text.endswith("."):
                    decision_text = decision_text[:-1]
                return decision_text

        return None

    @staticmethod
    def detect_important_note(line: str) -> Optional[Tuple[str, str]]:
        """
        Detect if a line contains an important note.

        Returns: (note_description, category) or None
        """
        line_lower = line.lower()

        # Check for important note keywords
        for keyword, categories in KeywordDetector.IMPORTANT_NOTE_KEYWORDS.items():
            if keyword in line_lower:
                note_text = line.strip()
                if note_text.endswith("."):
                    note_text = note_text[:-1]

                category = categories[0] if categories else "note"
                return note_text, category

        return None

    @staticmethod
    def _extract_due_date(line_lower: str) -> Optional[str]:
        """Extract due date from a line."""
        due_date_patterns = {
            "by friday": "Friday",
            "by monday": "Monday",
            "by today": "Today",
            "by tomorrow": "Tomorrow",
            "next week": "Next Week",
            "eow": "End of Week",
            "asap": "ASAP",
            "urgent": "Urgent",
        }

        for pattern, date_text in due_date_patterns.items():
            if pattern in line_lower:
                return date_text

        return None

    @staticmethod
    def extract_owner(line: str) -> Optional[str]:
        """
        Try to extract who is assigned to the action item.

        Looks for patterns like "Name will...", "Assign to Name", etc.
        """
        # Pattern: "Name will do X"
        match = re.match(r"^(\w+)\s+will\s+", line, re.IGNORECASE)
        if match:
            return match.group(1)

        # Pattern: "Assign to Name"
        match = re.search(r"assign\s+to\s+(\w+)", line, re.IGNORECASE)
        if match:
            return match.group(1)

        # Pattern: "Name should do X"
        match = re.match(r"^(\w+)\s+should\s+", line, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    @staticmethod
    def get_insights_count(line: str) -> dict:
        """
        Get counts of different insight types in a line.

        Returns: {"actions": count, "decisions": count, "notes": count}
        """
        count = {
            "actions": 1 if KeywordDetector.detect_action_item(line) else 0,
            "decisions": 1 if KeywordDetector.detect_decision(line) else 0,
            "notes": 1 if KeywordDetector.detect_important_note(line) else 0,
        }
        return count
