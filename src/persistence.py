"""SQLAlchemy-backed persistence helpers for Meeting objects.

The existing FastAPI server still works with the in-memory/legacy `Meeting`
domain model, so this module acts as the bridge between that model and the new
relational database schema. A legacy JSON file is only used as a one-time
bootstrap source if database tables exist but no records have been stored yet.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from typing import List, Optional

from .database import (
    ActionItem as DbActionItem,
    Attachment as DbAttachment,
    Decision as DbDecision,
    Meeting as DbMeeting,
    MeetingNote as DbMeetingNote,
    Participant as DbParticipant,
    Risk as DbRisk,
    Transcript as DbTranscript,
    initialize_database,
    session_scope,
)
from .models.meeting_model import (
    ActionItem,
    Attachment,
    Decision,
    ImportantNote,
    Meeting,
    Message,
)

LEGACY_DB_FILE = os.path.join(os.path.dirname(__file__), "data", "meetings.json")
_lock = threading.Lock()

initialize_database()


def _apply_timestamps(record, timestamp: Optional[datetime]) -> None:
    """Copy a legacy timestamp onto a SQLAlchemy record when available."""
    if timestamp is None:
        return
    record.created_at = timestamp
    record.updated_at = timestamp


def _normalize_participant_name(name: Optional[str]) -> Optional[str]:
    """Normalize participant names used across legacy and relational models."""
    if not name:
        return None
    cleaned = name.strip()
    return cleaned or None


def _load_legacy_json_meetings() -> List[Meeting]:
    """Load meetings from the former JSON store if it still exists."""
    if not os.path.exists(LEGACY_DB_FILE):
        return []

    try:
        with open(LEGACY_DB_FILE, "r", encoding="utf-8") as file_pointer:
            data = json.load(file_pointer)
        return [Meeting.from_dict(item) for item in data]
    except Exception:
        return []


def _ensure_participant(
    db_meeting: DbMeeting,
    participants_by_name: dict[str, DbParticipant],
    name: Optional[str],
    timestamp: Optional[datetime] = None,
) -> Optional[DbParticipant]:
    """Return the participant row for the supplied name, creating it if needed."""
    normalized_name = _normalize_participant_name(name)
    if normalized_name is None:
        return None

    participant_key = normalized_name.casefold()
    if participant_key in participants_by_name:
        return participants_by_name[participant_key]

    for existing_participant in db_meeting.participants:
        if existing_participant.name.casefold() == participant_key:
            participants_by_name[participant_key] = existing_participant
            return existing_participant

    participant = DbParticipant(name=normalized_name)
    _apply_timestamps(participant, timestamp or db_meeting.started_at)
    participants_by_name[participant_key] = participant
    db_meeting.participants.append(participant)

    return participant


def _legacy_meeting_to_orm(meeting: Meeting) -> DbMeeting:
    """Convert the legacy Meeting model into the SQLAlchemy meeting aggregate."""
    db_meeting = DbMeeting(
        id=meeting.id,
        title=meeting.title,
        summary=meeting.summary,
        started_at=meeting.created_at,
        ended_at=meeting.ended_at,
    )
    _apply_timestamps(db_meeting, meeting.created_at)
    if meeting.ended_at is not None:
        db_meeting.updated_at = meeting.ended_at

    participants_by_name: dict[str, DbParticipant] = {}
    for participant_name in meeting.participants:
        _ensure_participant(db_meeting, participants_by_name, participant_name, meeting.created_at)

    for sequence_number, message in enumerate(meeting.messages, start=1):
        participant = _ensure_participant(
            db_meeting,
            participants_by_name,
            message.speaker,
            message.timestamp,
        )
        transcript = DbTranscript(
            sequence_number=sequence_number,
            speaker_name=message.speaker or "Unknown",
            content=message.content,
            spoken_at=message.timestamp,
            participant=participant,
        )
        _apply_timestamps(transcript, message.timestamp)
        db_meeting.transcripts.append(transcript)

    for item in meeting.action_items:
        assignee_name = _normalize_participant_name(item.assigned_to)
        if assignee_name == "Unassigned":
            assignee_name = None

        assignee = _ensure_participant(
            db_meeting,
            participants_by_name,
            assignee_name,
            item.timestamp,
        )
        action_item = DbActionItem(
            description=item.description,
            assigned_to=assignee_name,
            due_date=item.due_date or None,
            status="pending",
            assignee=assignee,
        )
        _apply_timestamps(action_item, item.timestamp)
        db_meeting.action_items.append(action_item)

    for decision in meeting.decisions:
        db_decision = DbDecision(
            description=decision.description,
            context=decision.context or None,
        )
        _apply_timestamps(db_decision, decision.timestamp)
        db_meeting.decisions.append(db_decision)

    for note in meeting.important_notes:
        note_category = (note.category or "note").strip().lower()
        if note_category == "risk":
            risk = DbRisk(
                description=note.description,
                severity="medium",
                status="open",
            )
            _apply_timestamps(risk, note.timestamp)
            db_meeting.risks.append(risk)
            continue

        meeting_note = DbMeetingNote(
            description=note.description,
            category=note_category,
        )
        _apply_timestamps(meeting_note, note.timestamp)
        db_meeting.notes.append(meeting_note)

    for attachment in meeting.attachments:
        db_attachment = DbAttachment(
            file_name=attachment.file_name,
            file_path=attachment.file_path,
            content_type=attachment.content_type,
            file_size_bytes=attachment.file_size_bytes,
            uploaded_at=attachment.uploaded_at,
        )
        _apply_timestamps(db_attachment, attachment.uploaded_at)
        db_meeting.attachments.append(db_attachment)

    return db_meeting


def _orm_meeting_to_legacy(db_meeting: DbMeeting) -> Meeting:
    """Convert a SQLAlchemy meeting aggregate back into the legacy Meeting model."""
    legacy_meeting = Meeting(
        title=db_meeting.title,
        participants=[participant.name for participant in db_meeting.participants],
    )
    legacy_meeting.id = db_meeting.id
    legacy_meeting.summary = db_meeting.summary
    legacy_meeting.created_at = db_meeting.started_at
    legacy_meeting.ended_at = db_meeting.ended_at
    legacy_meeting.messages = []
    legacy_meeting.action_items = []
    legacy_meeting.decisions = []
    legacy_meeting.important_notes = []
    legacy_meeting.attachments = []

    for transcript in db_meeting.transcripts:
        message = Message(transcript.speaker_name, transcript.content)
        message.timestamp = transcript.spoken_at or transcript.created_at
        legacy_meeting.messages.append(message)

    for db_action in db_meeting.action_items:
        action_item = ActionItem(
            description=db_action.description,
            assigned_to=db_action.assigned_to,
            due_date=db_action.due_date or "",
        )
        action_item.timestamp = db_action.created_at
        legacy_meeting.action_items.append(action_item)

    for db_decision in db_meeting.decisions:
        decision = Decision(
            description=db_decision.description,
            context=db_decision.context or "",
        )
        decision.timestamp = db_decision.created_at
        legacy_meeting.decisions.append(decision)

    important_notes: list[ImportantNote] = []

    for db_note in db_meeting.notes:
        note = ImportantNote(
            description=db_note.description,
            category=db_note.category,
        )
        note.timestamp = db_note.created_at
        important_notes.append(note)

    for db_risk in db_meeting.risks:
        risk_note = ImportantNote(
            description=db_risk.description,
            category="risk",
        )
        risk_note.timestamp = db_risk.created_at
        important_notes.append(risk_note)

    legacy_meeting.important_notes = sorted(
        important_notes,
        key=lambda note: note.timestamp,
    )

    for db_attachment in db_meeting.attachments:
        attachment = Attachment(
            file_name=db_attachment.file_name,
            file_path=db_attachment.file_path,
            content_type=db_attachment.content_type,
            file_size_bytes=db_attachment.file_size_bytes,
        )
        attachment.uploaded_at = db_attachment.uploaded_at
        legacy_meeting.attachments.append(attachment)

    return legacy_meeting


def load_meetings() -> List[Meeting]:
    """Load meetings from SQLite, importing the legacy JSON archive once if needed."""
    with _lock:
        with session_scope() as db:
            stored_meetings = (
                db.query(DbMeeting)
                .order_by(DbMeeting.started_at.desc(), DbMeeting.id.desc())
                .all()
            )
            if stored_meetings:
                return [_orm_meeting_to_legacy(meeting) for meeting in stored_meetings]

            legacy_meetings = _load_legacy_json_meetings()
            for legacy_meeting in legacy_meetings:
                db.add(_legacy_meeting_to_orm(legacy_meeting))
            return legacy_meetings


def save_meetings(meetings: List[Meeting]) -> None:
    """Replace stored meetings with the supplied in-memory meeting list."""
    with _lock:
        with session_scope() as db:
            existing_meetings = db.query(DbMeeting).all()
            for existing_meeting in existing_meetings:
                db.delete(existing_meeting)
            db.flush()

            for meeting in meetings:
                db.add(_legacy_meeting_to_orm(meeting))
