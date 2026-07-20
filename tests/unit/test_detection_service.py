"""Unit tests for the DetectionService."""

import pytest
from src.models.meeting_model import Meeting, Message, ActionItem, Decision
from src.services.detection_service import DetectionService, SummarizationService


class TestProcessMessage:
    def test_skip_empty_line(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        result = detection_service.process_message(meeting, "")
        assert result["type"] is None
        assert len(meeting.messages) == 0

    def test_skip_whitespace_line(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        result = detection_service.process_message(meeting, "   ")
        assert result["type"] is None

    def test_creates_message(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        detection_service.process_message(meeting, "Alice: Hello everyone")
        assert len(meeting.messages) == 1
        assert meeting.messages[0].speaker == "Alice"
        assert meeting.messages[0].content == "Hello everyone"

    def test_detects_action_item(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        result = detection_service.process_message(meeting, "Alice will fix the bug by Friday")
        assert result["type"] == "action"
        assert len(meeting.action_items) == 1

    def test_detects_decision(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        result = detection_service.process_message(meeting, "Alice: We decided to use JWT")
        assert result["type"] == "decision"
        assert len(meeting.decisions) == 1

    def test_detects_important_note(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        result = detection_service.process_message(meeting, "Alice: There is a risk of server failure")
        assert result["type"] == "note"
        assert len(meeting.important_notes) == 1

    def test_unknown_speaker_default(self, detection_service):
        meeting = Meeting("Test", ["Unknown"])
        detection_service.process_message(meeting, "Just a message without speaker")
        assert meeting.messages[0].speaker == "Unknown"

    def test_no_duplicate_action_items(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        detection_service.process_message(meeting, "Alice: I will fix the bug")
        detection_service.process_message(meeting, "Alice: I will fix the bug")
        assert len(meeting.action_items) == 1

    def test_no_duplicate_decisions(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        detection_service.process_message(meeting, "Alice: We decided to use JWT")
        detection_service.process_message(meeting, "Alice: We decided to use JWT")
        assert len(meeting.decisions) == 1

    def test_no_duplicate_notes(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        detection_service.process_message(meeting, "Alice: Risk identified")
        detection_service.process_message(meeting, "Alice: Risk identified")
        assert len(meeting.important_notes) == 1

    def test_message_still_added_even_if_duplicate(self, detection_service):
        meeting = Meeting("Test", ["Alice"])
        detection_service.process_message(meeting, "Alice: I will fix the bug")
        detection_service.process_message(meeting, "Alice: I will fix the bug")
        assert len(meeting.messages) == 2


class TestAnalyzeDocument:
    def test_analyze_empty_text(self, detection_service):
        meeting = Meeting("Test", ["Unknown"])
        detection_service.analyze_document(meeting, "")
        assert meeting.summary == "Empty document."

    def test_analyze_whitespace_text(self, detection_service):
        meeting = Meeting("Test", ["Unknown"])
        detection_service.analyze_document(meeting, "   ")
        assert meeting.summary == "Empty document."

    def test_analyze_participants_extracted(self, detection_service):
        meeting = Meeting("Test", ["Unknown"])
        text = "Alice: Hello\nBob: Hi"
        detection_service.analyze_document(meeting, text)
        assert len(meeting.participants) > 0

    def test_analyze_adds_messages(self, detection_service):
        meeting = Meeting("Test", ["Unknown"])
        text = "Alice: Hello\nBob: Hi there"
        detection_service.analyze_document(meeting, text)
        assert len(meeting.messages) > 0

    def test_analyze_clears_previous_data(self, detection_service):
        meeting = Meeting("Test", ["Unknown"])
        meeting.add_action_item(ActionItem("Old item", "Alice"))
        meeting.add_decision(Decision("Old decision"))
        text = "Alice: Let's discuss new things"
        detection_service.analyze_document(meeting, text)
        assert len(meeting.action_items) == 0


class TestSummarizationService:
    def test_empty_messages_returns_placeholder(self):
        meeting = Meeting("Test", ["Alice"])
        summary = SummarizationService.generate_summary(meeting)
        assert summary == "No meeting content to summarize."

    def test_summary_contains_messages_content(self, sample_meeting):
        summary = SummarizationService.generate_summary(sample_meeting)
        assert "authentication module" in summary or "API documentation" in summary or "JWT" in summary

    def test_summary_includes_key_sentences(self, sample_meeting):
        sample_meeting.add_action_item(ActionItem("Review the deployment plan", "Alice", "Friday"))
        sample_meeting.add_decision(Decision("Adopt microservices architecture"))
        summary = SummarizationService.generate_summary(sample_meeting)
        assert "Review the deployment plan" in summary
        assert "microservices" in summary

    def test_summary_format_uses_bullets(self, sample_meeting):
        summary = SummarizationService.generate_summary(sample_meeting)
        assert "Key points discussed" in summary

    def test_extract_key_sentences_max_limit(self, sample_meeting):
        sentences = SummarizationService._extract_key_sentences(sample_meeting, max_sentences=3)
        assert len(sentences) <= 3
