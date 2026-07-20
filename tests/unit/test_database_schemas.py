"""Unit tests for Pydantic database schemas."""

from datetime import datetime

import pytest
from src.database.schemas import (
    MeetingCreate,
    MeetingUpdate,
    MeetingResponse,
    ParticipantCreate,
    ParticipantResponse,
    ActionItemCreate,
    ActionItemResponse,
    DecisionCreate,
    DecisionResponse,
    RiskCreate,
    RiskResponse,
    MeetingNoteCreate,
    MeetingNoteResponse,
    TranscriptCreate,
    TranscriptResponse,
    AttachmentCreate,
    AttachmentResponse,
    ORMModel,
)


class TestORMModel:
    def test_orm_model_config(self):
        config = ORMModel.model_config
        assert config is not None


class TestParticipantSchemas:
    def test_participant_create(self):
        p = ParticipantCreate(name="Alice", email="alice@example.com", role="Developer")
        assert p.name == "Alice"
        assert p.email == "alice@example.com"

    def test_participant_create_minimal(self):
        p = ParticipantCreate(name="Bob")
        assert p.name == "Bob"
        assert p.email is None

    def test_participant_response_has_id(self):
        p = ParticipantResponse(
            id=1, meeting_id="m1", name="Alice",
            created_at=datetime.now(), updated_at=datetime.now()
        )
        assert p.id == 1


class TestActionItemSchemas:
    def test_action_item_create_defaults(self):
        item = ActionItemCreate(description="Fix bug")
        assert item.status == "pending"
        assert item.assigned_to is None

    def test_action_item_create_full(self):
        item = ActionItemCreate(
            description="Fix bug", assigned_to="Alice",
            due_date="Friday", status="in_progress"
        )
        assert item.assigned_to == "Alice"
        assert item.status == "in_progress"

    def test_action_item_response(self):
        item = ActionItemResponse(
            id=1, meeting_id="m1", description="Fix bug",
            created_at=datetime.now(), updated_at=datetime.now()
        )
        assert item.description == "Fix bug"


class TestDecisionSchemas:
    def test_decision_create(self):
        d = DecisionCreate(description="Use JWT", context="Auth discussion")
        assert d.description == "Use JWT"
        assert d.context == "Auth discussion"

    def test_decision_create_minimal(self):
        d = DecisionCreate(description="Use JWT")
        assert d.context is None


class TestRiskSchemas:
    def test_risk_create_defaults(self):
        r = RiskCreate(description="Server failure")
        assert r.severity == "medium"
        assert r.status == "open"

    def test_risk_create_custom(self):
        r = RiskCreate(description="Server failure", severity="high", status="mitigated")
        assert r.severity == "high"
        assert r.status == "mitigated"


class TestMeetingNoteSchemas:
    def test_note_create_defaults(self):
        n = MeetingNoteCreate(description="Important note")
        assert n.category == "note"

    def test_note_create_custom(self):
        n = MeetingNoteCreate(description="Risk note", category="risk")
        assert n.category == "risk"


class TestTranscriptSchemas:
    def test_transcript_create(self):
        t = TranscriptCreate(
            sequence_number=1, speaker_name="Alice",
            content="Hello everyone"
        )
        assert t.sequence_number == 1
        assert t.speaker_name == "Alice"
        assert t.content == "Hello everyone"


class TestAttachmentSchemas:
    def test_attachment_create(self):
        a = AttachmentCreate(
            file_name="test.pdf", file_path="/path/to/test.pdf",
            content_type="application/pdf", file_size_bytes=1024
        )
        assert a.file_name == "test.pdf"
        assert a.file_size_bytes == 1024


class TestMeetingSchemas:
    def test_meeting_create_defaults(self):
        m = MeetingCreate(title="Sprint Planning")
        assert m.summary == ""
        assert m.participants == []
        assert m.transcripts == []

    def test_meeting_create_with_nested(self):
        m = MeetingCreate(
            title="Sprint Planning",
            participants=[ParticipantCreate(name="Alice")]
        )
        assert len(m.participants) == 1

    def test_meeting_update_allows_partial(self):
        m = MeetingUpdate(title="Updated Title")
        assert m.title == "Updated Title"
        assert m.summary is None

    def test_meeting_response_has_id(self):
        m = MeetingResponse(
            id="m1", title="Meeting",
            created_at=datetime.now(), updated_at=datetime.now()
        )
        assert m.id == "m1"
