"""Unit tests for the KeywordDetector service."""

import pytest
from src.utils.keyword_detector import KeywordDetector


class TestExtractSpeaker:
    def test_extracts_speaker_and_content(self):
        speaker, content = KeywordDetector.extract_speaker("Alice: Hello everyone")
        assert speaker == "Alice"
        assert content == "Hello everyone"

    def test_no_speaker_returns_empty(self):
        speaker, content = KeywordDetector.extract_speaker("Just a statement")
        assert speaker == ""
        assert content == "Just a statement"

    def test_empty_line_returns_empty(self):
        speaker, content = KeywordDetector.extract_speaker("")
        assert speaker == ""
        assert content == ""

    def test_multiple_colons_only_splits_first(self):
        speaker, content = KeywordDetector.extract_speaker("Alice: Note: This is a test")
        assert speaker == "Alice"
        assert content == "Note: This is a test"


class TestDetectActionItem:
    def test_detects_will_keyword(self):
        result = KeywordDetector.detect_action_item("Alice will fix the bug")
        assert result is not None
        assert "Alice will fix the bug" in result[0]

    def test_detects_need_to_keyword(self):
        result = KeywordDetector.detect_action_item("We need to update the docs")
        assert result is not None

    def test_detects_should_keyword(self):
        result = KeywordDetector.detect_action_item("We should review the PR")
        assert result is not None

    def test_detects_must_keyword(self):
        result = KeywordDetector.detect_action_item("We must complete this by Friday")
        assert result is not None

    def test_detects_assign_keyword(self):
        result = KeywordDetector.detect_action_item("I assign this task to Alice")
        assert result is not None

    def test_removes_trailing_period(self):
        result = KeywordDetector.detect_action_item("Alice will fix the bug.")
        assert result is not None
        assert result[0].endswith("bug") is True

    def test_no_match_returns_none(self):
        result = KeywordDetector.detect_action_item("The weather is nice today.")
        assert result is None

    def test_empty_line_returns_none(self):
        result = KeywordDetector.detect_action_item("")
        assert result is None

    def test_detects_due_date_friday(self):
        result = KeywordDetector.detect_action_item("Alice will fix the bug by Friday")
        assert result is not None
        assert result[1] == "Friday"

    def test_detects_due_date_monday(self):
        result = KeywordDetector.detect_action_item("We need to deploy by Monday")
        assert result is not None
        assert result[1] == "Monday"

    def test_detects_asap(self):
        result = KeywordDetector.detect_action_item("We must fix this ASAP")
        assert result is not None
        assert result[1] == "ASAP"


class TestDetectDecision:
    def test_detects_decided(self):
        result = KeywordDetector.detect_decision("We decided to use JWT")
        assert result is not None
        assert "decided to use JWT" in result

    def test_detects_approved(self):
        result = KeywordDetector.detect_decision("The committee approved the budget")
        assert result is not None

    def test_detects_agreed(self):
        result = KeywordDetector.detect_decision("We agreed on the timeline")
        assert result is not None

    def test_detects_confirmed(self):
        result = KeywordDetector.detect_decision("We confirmed the meeting date")
        assert result is not None

    def test_no_match_returns_none(self):
        result = KeywordDetector.detect_decision("The weather is nice")
        assert result is None

    def test_removes_trailing_period(self):
        result = KeywordDetector.detect_decision("We decided to proceed.")
        assert result is not None
        assert result.endswith("proceed") is True


class TestDetectImportantNote:
    def test_detects_risk(self):
        result = KeywordDetector.detect_important_note("There is a risk of server failure")
        assert result is not None
        assert result[1] == "risk"

    def test_detects_issue(self):
        result = KeywordDetector.detect_important_note("There is an issue with deployment")
        assert result is not None
        assert result[1] == "issue"

    def test_detects_blocker(self):
        result = KeywordDetector.detect_important_note("This is a blocker for the release")
        assert result is not None

    def test_detects_reminder(self):
        result = KeywordDetector.detect_important_note("Reminder: update the docs")
        assert result is not None

    def test_no_match_returns_none(self):
        result = KeywordDetector.detect_important_note("The weather is nice")
        assert result is None


class TestExtractOwner:
    def test_extracts_name_will_pattern(self):
        owner = KeywordDetector.extract_owner("Alice will fix the bug")
        assert owner == "Alice"

    def test_extracts_name_should_pattern(self):
        owner = KeywordDetector.extract_owner("Alice should fix the bug")
        assert owner == "Alice"

    def test_extracts_assign_to_pattern(self):
        owner = KeywordDetector.extract_owner("Assign to Bob the task")
        assert owner == "Bob"

    def test_no_match_returns_none(self):
        owner = KeywordDetector.extract_owner("The bug needs to be fixed")
        assert owner is None


class TestGetInsightsCount:
    def test_returns_counts(self):
        counts = KeywordDetector.get_insights_count("Alice will fix the bug by Friday")
        assert isinstance(counts, dict)
        assert "actions" in counts
        assert "decisions" in counts
        assert "notes" in counts

    def test_action_item_detected(self):
        counts = KeywordDetector.get_insights_count("Alice will fix the bug")
        assert counts["actions"] == 1

    def test_decision_detected(self):
        counts = KeywordDetector.get_insights_count("We decided to proceed")
        assert counts["decisions"] == 1

    def test_note_detected(self):
        counts = KeywordDetector.get_insights_count("Risk of server failure")
        assert counts["notes"] == 1

    def test_no_insights(self):
        counts = KeywordDetector.get_insights_count("The weather is nice")
        assert counts["actions"] == 0
        assert counts["decisions"] == 0
        assert counts["notes"] == 0
