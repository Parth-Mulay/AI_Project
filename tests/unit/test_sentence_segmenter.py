"""Unit tests for the SentenceSegmenter."""

import pytest
from src.nlp.sentence_segmenter import SentenceSegmenter


class TestSentenceSegmenter:
    def setup_method(self):
        self.segmenter = SentenceSegmenter()

    def test_segment_empty_text(self):
        result = self.segmenter.segment("")
        assert result == []

    def test_segment_single_line(self):
        result = self.segmenter.segment("Alice: Hello World")
        assert len(result) == 1
        assert result[0][0] == "Alice"
        assert result[0][1] == "Hello World"

    def test_segment_unknown_speaker(self):
        result = self.segmenter.segment("Just a line")
        assert result[0][0] == "Unknown"

    def test_segment_splits_sentences(self):
        result = self.segmenter.segment("Alice: Hello. How are you?")
        assert len(result) >= 2

    def test_segment_skips_empty_lines(self):
        result = self.segmenter.segment("Alice: Hello.\n\n\nBob: Hi.")
        assert len(result) == 2

    def test_segment_multiple_lines(self):
        text = "Alice: First.\nBob: Second.\nCharlie: Third."
        result = self.segmenter.segment(text)
        assert len(result) == 3
        assert result[0][0] == "Alice"
        assert result[1][0] == "Bob"
        assert result[2][0] == "Charlie"

    def test_segment_long_speaker_name(self):
        result = self.segmenter.segment("A" * 31 + ": Hello")
        assert result[0][0] == "Unknown"

    def test_segment_speaker_with_non_alpha(self):
        result = self.segmenter.segment("Alice123: Hello")
        assert result[0][0] == "Unknown"

    def test_segment_preserves_content(self):
        result = self.segmenter.segment("Alice: This is a test message.")
        assert result[0][1] == "This is a test message."

    def test_segment_exclamation_sentence_split(self):
        result = self.segmenter.segment("Alice: Go! Now!")
        assert len(result) == 2

    def test_segment_question_sentence_split(self):
        result = self.segmenter.segment("Alice: Ready? Go!")
        assert len(result) == 2
