"""Unit tests for the domain Meeting model."""

import pytest
from src.models.meeting_model import Meeting, Message, ActionItem, Decision, ImportantNote, Attachment


class TestMessage:
    def test_message_creation(self):
        msg = Message("Alice", "Hello everyone")
        assert msg.speaker == "Alice"
        assert msg.content == "Hello everyone"
        assert msg.timestamp is not None

    def test_message_strips_whitespace(self):
        msg = Message("  Alice  ", "  Hello  ")
        assert msg.speaker == "Alice"
        assert msg.content == "Hello"

    def test_message_str(self):
        msg = Message("Alice", "Hello")
        assert str(msg) == "Alice: Hello"

    def test_message_repr(self):
        msg = Message("Alice", "Hello")
        assert "Message(" in repr(msg)
        assert "speaker='Alice'" in repr(msg)


class TestActionItem:
    def test_action_item_creation(self):
        item = ActionItem("Fix bug", "Alice", "Friday")
        assert item.description == "Fix bug"
        assert item.assigned_to == "Alice"
        assert item.due_date == "Friday"

    def test_action_item_default_assigned_to(self):
        item = ActionItem("Fix bug")
        assert item.assigned_to == "Unassigned"

    def test_action_item_default_due_date(self):
        item = ActionItem("Fix bug", "Alice")
        assert item.due_date == ""

    def test_action_item_str_with_due_date(self):
        item = ActionItem("Fix bug", "Alice", "Friday")
        assert str(item) == "Fix bug (Friday)"

    def test_action_item_str_without_due_date(self):
        item = ActionItem("Fix bug", "Alice")
        assert str(item) == "Fix bug"

    def test_action_item_to_dict(self):
        item = ActionItem("Fix bug", "Alice", "Friday")
        d = item.to_dict()
        assert d["description"] == "Fix bug"
        assert d["assigned_to"] == "Alice"
        assert d["due_date"] == "Friday"
        assert "timestamp" in d


class TestDecision:
    def test_decision_creation(self):
        dec = Decision("Use JWT", "Context: Auth discussion")
        assert dec.description == "Use JWT"
        assert dec.context == "Context: Auth discussion"

    def test_decision_default_context(self):
        dec = Decision("Use JWT")
        assert dec.context == ""

    def test_decision_str(self):
        dec = Decision("Use JWT")
        assert str(dec) == "Use JWT"

    def test_decision_to_dict(self):
        dec = Decision("Use JWT", "Context")
        d = dec.to_dict()
        assert d["description"] == "Use JWT"
        assert d["context"] == "Context"


class TestImportantNote:
    def test_note_creation(self):
        note = ImportantNote("Server is slow", "risk")
        assert note.description == "Server is slow"
        assert note.category == "risk"

    def test_note_default_category(self):
        note = ImportantNote("Remember to update docs")
        assert note.category == "note"

    def test_note_to_dict(self):
        note = ImportantNote("Server is slow", "risk")
        d = note.to_dict()
        assert d["description"] == "Server is slow"
        assert d["category"] == "risk"


class TestAttachment:
    def test_attachment_creation(self):
        att = Attachment("report.pdf", "/path/to/report.pdf", "application/pdf", 1024)
        assert att.file_name == "report.pdf"
        assert att.file_path == "/path/to/report.pdf"
        assert att.content_type == "application/pdf"
        assert att.file_size_bytes == 1024

    def test_attachment_defaults(self):
        att = Attachment("report.pdf", "/path/to/report.pdf")
        assert att.content_type is None
        assert att.file_size_bytes is None

    def test_attachment_to_dict(self):
        att = Attachment("r.pdf", "/p/r.pdf", "app/pdf", 512)
        d = att.to_dict()
        assert d["file_name"] == "r.pdf"
        assert d["file_size_bytes"] == 512


class TestMeeting:
    def test_meeting_creation(self, sample_meeting):
        assert sample_meeting.title == "Sprint Planning"
        assert len(sample_meeting.participants) == 3
        assert sample_meeting.id is not None

    def test_meeting_default_summary(self, empty_meeting):
        assert empty_meeting.summary == ""

    def test_meeting_created_at_set(self, sample_meeting):
        assert sample_meeting.created_at is not None

    def test_add_message(self, empty_meeting):
        msg = Message("Alice", "Hello")
        empty_meeting.add_message(msg)
        assert len(empty_meeting.messages) == 1
        assert empty_meeting.messages[0].speaker == "Alice"

    def test_add_action_item(self, empty_meeting):
        item = ActionItem("Fix bug", "Alice")
        empty_meeting.add_action_item(item)
        assert len(empty_meeting.action_items) == 1

    def test_add_decision(self, empty_meeting):
        dec = Decision("Use JWT")
        empty_meeting.add_decision(dec)
        assert len(empty_meeting.decisions) == 1

    def test_add_important_note(self, empty_meeting):
        note = ImportantNote("Server slow", "risk")
        empty_meeting.add_important_note(note)
        assert len(empty_meeting.important_notes) == 1

    def test_add_attachment(self, empty_meeting):
        att = Attachment("f.txt", "/p/f.txt")
        empty_meeting.add_attachment(att)
        assert len(empty_meeting.attachments) == 1

    def test_get_duration_without_end(self, sample_meeting):
        duration = sample_meeting.get_duration()
        assert "minutes" in duration

    def test_get_duration_with_end(self, sample_meeting):
        from datetime import datetime, timedelta
        sample_meeting.ended_at = sample_meeting.created_at + timedelta(hours=1)
        duration = sample_meeting.get_duration()
        assert "60" in duration

    def test_to_dict_contains_all_fields(self, sample_meeting):
        d = sample_meeting.to_dict()
        assert d["title"] == "Sprint Planning"
        assert "id" in d
        assert "participants" in d
        assert "summary" in d
        assert "messages" in d
        assert "message_count" in d
        assert "action_items" in d
        assert "decisions" in d
        assert "important_notes" in d
        assert "attachments" in d
        assert "created_at" in d
        assert "duration" in d

    def test_from_dict_roundtrip(self, sample_meeting):
        d = sample_meeting.to_dict()
        restored = Meeting.from_dict(d)
        assert restored.title == sample_meeting.title
        assert restored.id == sample_meeting.id
        assert len(restored.messages) == len(sample_meeting.messages)
        assert len(restored.action_items) == len(sample_meeting.action_items)

    def test_from_dict_creates_new_id_when_missing(self):
        restored = Meeting.from_dict({"title": "New", "participants": ["A"]})
        assert restored.id is not None
        assert restored.title == "New"

    def test_multiple_messages(self, sample_meeting):
        assert len(sample_meeting.messages) == 6

    def test_meeting_message_count_property(self, sample_meeting):
        assert len(sample_meeting.messages) == sample_meeting.to_dict()["message_count"]
