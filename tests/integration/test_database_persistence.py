"""Integration tests for database persistence layer."""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.meeting_model import Meeting, ActionItem, Decision
from src.persistence import load_meetings, save_meetings


class TestDatabasePersistence:
    def test_load_meetings_returns_list(self):
        meetings = load_meetings()
        assert isinstance(meetings, list)

    def test_save_and_load_roundtrip(self):
        original = load_meetings()
        meeting = Meeting("Persistence Test", ["Alice"])
        meeting.add_action_item(ActionItem("Test action", "Alice"))
        meeting.add_decision(Decision("Test decision"))
        original.append(meeting)
        save_meetings(original)
        loaded = load_meetings()
        titles = [m.title for m in loaded]
        assert "Persistence Test" in titles

    def test_save_overwrites_previous(self):
        meetings = load_meetings()
        count_before = len(meetings)
        save_meetings(meetings)
        loaded = load_meetings()
        assert len(loaded) == count_before

    def test_meeting_restored_with_action_items(self):
        meetings = load_meetings()
        meeting = Meeting("AI Test", ["Bob"])
        meeting.add_action_item(ActionItem("Fix bug", "Bob", "Friday"))
        meetings.append(meeting)
        save_meetings(meetings)
        loaded = load_meetings()
        for m in loaded:
            if m.title == "AI Test":
                assert len(m.action_items) == 1
                assert m.action_items[0].description == "Fix bug"
                break
        else:
            pytest.fail("Meeting not found after persist")

    def test_meeting_restored_with_decisions(self):
        meetings = load_meetings()
        meeting = Meeting("Decision Test", ["Charlie"])
        meeting.add_decision(Decision("Use JWT", "Auth discussion"))
        meetings.append(meeting)
        save_meetings(meetings)
        loaded = load_meetings()
        for m in loaded:
            if m.title == "Decision Test":
                assert len(m.decisions) == 1
                assert m.decisions[0].description == "Use JWT"
                break
        else:
            pytest.fail("Meeting not found after persist")

    def test_meeting_with_participants_restored(self):
        meetings = load_meetings()
        participants = ["Alice", "Bob", "Charlie"]
        meeting = Meeting("Participants Test", participants)
        meetings.append(meeting)
        save_meetings(meetings)
        loaded = load_meetings()
        for m in loaded:
            if m.title == "Participants Test":
                assert len(m.participants) == 3
                assert "Alice" in m.participants
                break
        else:
            pytest.fail("Meeting not found")
