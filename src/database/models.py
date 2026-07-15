"""SQLAlchemy ORM models for the AI Meeting Notes Manager."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for ORM defaults."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Shared timestamp columns used across entities."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Meeting(Base, TimestampMixin):
    """Top-level meeting aggregate containing AI-generated outputs."""

    __tablename__ = "meetings"
    __table_args__ = (
        Index("ix_meetings_title_started_at", "title", "started_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
        index=True,
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    participants: Mapped[list["Participant"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="Participant.id",
        lazy="selectin",
    )
    transcripts: Mapped[list["Transcript"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="Transcript.sequence_number",
        lazy="selectin",
    )
    action_items: Mapped[list["ActionItem"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="ActionItem.id",
        lazy="selectin",
    )
    decisions: Mapped[list["Decision"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="Decision.id",
        lazy="selectin",
    )
    risks: Mapped[list["Risk"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="Risk.id",
        lazy="selectin",
    )
    notes: Mapped[list["MeetingNote"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="MeetingNote.id",
        lazy="selectin",
    )
    attachments: Mapped[list["Attachment"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="Attachment.id",
        lazy="selectin",
    )


class Participant(Base, TimestampMixin):
    """Participant metadata for a specific meeting."""

    __tablename__ = "participants"
    __table_args__ = (
        UniqueConstraint("meeting_id", "name", name="uq_participants_meeting_name"),
        Index("ix_participants_meeting_name", "meeting_id", "name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    role: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    meeting: Mapped["Meeting"] = relationship(back_populates="participants")
    transcript_entries: Mapped[list["Transcript"]] = relationship(back_populates="participant")
    assigned_actions: Mapped[list["ActionItem"]] = relationship(back_populates="assignee")


class Transcript(Base, TimestampMixin):
    """Ordered transcript segments captured for a meeting."""

    __tablename__ = "transcripts"
    __table_args__ = (
        UniqueConstraint("meeting_id", "sequence_number", name="uq_transcripts_meeting_sequence"),
        Index("ix_transcripts_meeting_spoken_at", "meeting_id", "spoken_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    participant_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("participants.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_name: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    spoken_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    meeting: Mapped["Meeting"] = relationship(back_populates="transcripts")
    participant: Mapped[Optional["Participant"]] = relationship(back_populates="transcript_entries")


class ActionItem(Base, TimestampMixin):
    """Action items extracted from meeting discussions."""

    __tablename__ = "action_items"
    __table_args__ = (
        Index("ix_action_items_meeting_status", "meeting_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assignee_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("participants.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    due_date: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    source_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    meeting: Mapped["Meeting"] = relationship(back_populates="action_items")
    assignee: Mapped[Optional["Participant"]] = relationship(back_populates="assigned_actions")


class Decision(Base, TimestampMixin):
    """Decisions detected from meeting content."""

    __tablename__ = "decisions"
    __table_args__ = (
        Index("ix_decisions_meeting_created_at", "meeting_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    meeting: Mapped["Meeting"] = relationship(back_populates="decisions")


class Risk(Base, TimestampMixin):
    """Risks or blockers identified during meeting analysis."""

    __tablename__ = "risks"
    __table_args__ = (
        Index("ix_risks_meeting_status", "meeting_id", "status"),
        Index("ix_risks_meeting_severity", "meeting_id", "severity"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)

    meeting: Mapped["Meeting"] = relationship(back_populates="risks")


class MeetingNote(Base, TimestampMixin):
    """Non-risk notes preserved from the existing backend analysis flow."""

    __tablename__ = "meeting_notes"
    __table_args__ = (
        Index("ix_meeting_notes_meeting_category", "meeting_id", "category"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="note", index=True)

    meeting: Mapped["Meeting"] = relationship(back_populates="notes")


class Attachment(Base, TimestampMixin):
    """Attachment metadata for uploaded meeting files."""

    __tablename__ = "attachments"
    __table_args__ = (
        Index("ix_attachments_meeting_uploaded_at", "meeting_id", "uploaded_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )

    meeting: Mapped["Meeting"] = relationship(back_populates="attachments")
