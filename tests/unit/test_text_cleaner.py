"""Unit tests for the TextCleaner."""

import pytest
from src.nlp.text_cleaner import TextCleaner


class TestTextCleaner:
    def setup_method(self):
        self.cleaner = TextCleaner()

    def test_clean_empty_string(self):
        result = self.cleaner.clean("")
        assert result == ""

    def test_clean_whitespace_only(self):
        result = self.cleaner.clean("   ")
        assert result == ""

    def test_clean_normalizes_whitespace(self):
        result = self.cleaner.clean("Hello    World")
        assert result == "Hello World"

    def test_clean_strips_lines(self):
        result = self.cleaner.clean("  Hello  \n  World  ")
        assert "Hello" in result
        assert "World" in result

    def test_clean_collapses_duplicate_punctuation(self):
        result = self.cleaner.clean("Hello!! World??")
        assert "Hello" in result
        assert "World" in result

    def test_clean_removes_unwanted_symbols(self):
        result = self.cleaner.clean("Hello $%^ World")
        assert "Hello" in result
        assert "World" in result

    def test_clean_preserves_speaker_label(self):
        result = self.cleaner.clean("Alice: Hello World")
        assert result == "Alice: Hello World"

    def test_clean_preserves_dates(self):
        result = self.cleaner.clean("Meeting on 2026-07-15")
        assert "2026-07-15" in result

    def test_clean_preserves_slash(self):
        result = self.cleaner.clean("Alice/Bob: Update")
        assert "Alice/Bob" in result

    def test_clean_removes_html_tags(self):
        result = self.cleaner.clean("<p>Hello</p>")
        assert result == "pHello/p"

    def test_clean_multiple_lines_preserved(self):
        result = self.cleaner.clean("Line 1.\nLine 2.\nLine 3.")
        lines = result.split("\n")
        assert len(lines) == 3

    def test_clean_collapses_tabs(self):
        result = self.cleaner.clean("Hello\t\tWorld")
        assert "Hello World" in result
