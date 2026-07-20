"""Unit tests for the NLP pipeline."""

import pytest
from src.nlp.pipeline import MeetingNlpPipeline


class TestMeetingNlpPipeline:
    def test_initialization(self):
        pipeline = MeetingNlpPipeline()
        assert pipeline.cleaner is not None
        assert pipeline.segmenter is not None

    def test_process_returns_expected_keys(self, nlp_pipeline):
        text = "Alice: Hello everyone.\nBob: Hi Alice."
        result = nlp_pipeline.process(text)
        expected_keys = [
            "title", "date", "participants", "departments", "organizations",
            "speakers", "agenda", "summary", "action_items", "decisions",
            "risks", "deadlines", "recommendations", "statistics", "timeline"
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_process_empty_text(self, nlp_pipeline):
        result = nlp_pipeline.process("")
        assert result["participants"] == ["Unknown Participant"]
        assert result["statistics"]["total_messages"] == 0

    def test_extract_metadata_title_from_header(self, nlp_pipeline):
        text = "Meeting Minutes: Sprint Planning.\nParticipants: Alice."
        result = nlp_pipeline.process(text)
        assert "Sprint Planning" in result["title"]

    def test_extract_metadata_title_fallback(self, nlp_pipeline):
        text = "Short title.\nAlice: Hello."
        result = nlp_pipeline.process(text)
        assert result["title"] is not None

    def test_extract_participants_from_header(self, nlp_pipeline):
        text = "Participants: Alice, Bob, Charlie\nAlice: Hello.\nBob: Hi."
        result = nlp_pipeline.process(text)
        assert "Alice" in result["participants"]
        assert "Bob" in result["participants"]
        assert "Charlie" in result["participants"]

    def test_extract_action_items(self, nlp_pipeline):
        text = "Alice: We must complete the migration by Friday."
        result = nlp_pipeline.process(text)
        assert len(result["action_items"]) > 0

    def test_extract_decisions(self, nlp_pipeline):
        text = "Alice: We decided to adopt the new framework."
        result = nlp_pipeline.process(text)
        assert len(result["decisions"]) > 0

    def test_extract_risks(self, nlp_pipeline):
        text = "Alice: There is a risk of server downtime."
        result = nlp_pipeline.process(text)
        assert len(result["risks"]) > 0

    def test_extract_deadlines(self, nlp_pipeline):
        text = "Alice: The deadline for the project is Friday."
        result = nlp_pipeline.process(text)
        assert len(result["deadlines"]) > 0

    def test_timeline_order_preserved(self, nlp_pipeline):
        text = "Alice: First message.\nBob: Second message.\nCharlie: Third message."
        result = nlp_pipeline.process(text)
        assert len(result["timeline"]) == 3
        assert result["timeline"][0]["speaker"] == "Alice"
        assert result["timeline"][1]["speaker"] == "Bob"
        assert result["timeline"][2]["speaker"] == "Charlie"

    def test_statistics_computed(self, nlp_pipeline):
        text = "Alice: Hello.\nBob: Hi.\nCharlie: Hey."
        result = nlp_pipeline.process(text)
        stats = result["statistics"]
        assert stats["total_messages"] == 3
        assert stats["sentence_count"] == 3
        assert stats["extracted_text_length"] > 0

    def test_recommendations_generated(self, nlp_pipeline):
        text = "Alice: Hello everyone."
        result = nlp_pipeline.process(text)
        assert len(result["recommendations"]) > 0

    def test_action_items_confidence_scored(self, nlp_pipeline):
        text = "Alice: We must complete the migration by Friday."
        result = nlp_pipeline.process(text)
        if result["action_items"]:
            assert "confidence" in result["action_items"][0]

    def test_decisions_confidence_scored(self, nlp_pipeline):
        text = "Alice: We decided to adopt the new framework."
        result = nlp_pipeline.process(text)
        if result["decisions"]:
            assert "confidence" in result["decisions"][0]

    def test_risks_confidence_scored(self, nlp_pipeline):
        text = "Alice: There is a risk of server downtime."
        result = nlp_pipeline.process(text)
        if result["risks"]:
            assert "confidence" in result["risks"][0]

    def test_parse_date_none_value(self, nlp_pipeline):
        result = nlp_pipeline._parse_date(None)
        assert result is None

    def test_parse_date_empty_value(self, nlp_pipeline):
        result = nlp_pipeline._parse_date("")
        assert result is None

    def test_parse_date_valid_ymd(self, nlp_pipeline):
        result = nlp_pipeline._parse_date("2026-07-15")
        assert result is not None
        assert result.year == 2026
        assert result.month == 7
        assert result.day == 15
