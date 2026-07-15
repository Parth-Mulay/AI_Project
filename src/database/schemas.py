"""Pydantic schemas for future database-backed API operations."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict
except ImportError:  # pragma: no cover - Pydantic v1 compatibility.
    ConfigDict = None


class ORMModel(BaseModel):
    """Base schema configured for SQLAlchemy ORM serialization."""

    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:  # pragma: no cover - Pydantic v1 compatibility.
        class Config:
            orm_mode = True


class ParticipantBase(BaseModel):
    """Shared participant fields."""

    name: str
    email: Optional[str] = None
    role: Optional[str] = None


class ParticipantCreate(ParticipantBase):
    """Schema for creating a participant."""


class ParticipantUpdate(BaseModel):
    """Schema for updating a participant."""

    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class ParticipantResponse(ORMModel, ParticipantBase):
    """Participant payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class TranscriptBase(BaseModel):
    """Shared transcript fields."""

    sequence_number: int
    speaker_name: str
    content: str
    participant_id: Optional[int] = None
    spoken_at: Optional[datetime] = None


class TranscriptCreate(TranscriptBase):
    """Schema for creating a transcript segment."""


class TranscriptUpdate(BaseModel):
    """Schema for updating a transcript segment."""

    sequence_number: Optional[int] = None
    speaker_name: Optional[str] = None
    content: Optional[str] = None
    participant_id: Optional[int] = None
    spoken_at: Optional[datetime] = None


class TranscriptResponse(ORMModel, TranscriptBase):
    """Transcript payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class ActionItemBase(BaseModel):
    """Shared action item fields."""

    description: str
    assigned_to: Optional[str] = None
    assignee_id: Optional[int] = None
    due_date: Optional[str] = None
    status: str = "pending"
    source_excerpt: Optional[str] = None


class ActionItemCreate(ActionItemBase):
    """Schema for creating an action item."""


class ActionItemUpdate(BaseModel):
    """Schema for updating an action item."""

    description: Optional[str] = None
    assigned_to: Optional[str] = None
    assignee_id: Optional[int] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    source_excerpt: Optional[str] = None


class ActionItemResponse(ORMModel, ActionItemBase):
    """Action item payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class DecisionBase(BaseModel):
    """Shared decision fields."""

    description: str
    context: Optional[str] = None


class DecisionCreate(DecisionBase):
    """Schema for creating a decision."""


class DecisionUpdate(BaseModel):
    """Schema for updating a decision."""

    description: Optional[str] = None
    context: Optional[str] = None


class DecisionResponse(ORMModel, DecisionBase):
    """Decision payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class RiskBase(BaseModel):
    """Shared risk fields."""

    description: str
    severity: str = "medium"
    status: str = "open"


class RiskCreate(RiskBase):
    """Schema for creating a risk."""


class RiskUpdate(BaseModel):
    """Schema for updating a risk."""

    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None


class RiskResponse(ORMModel, RiskBase):
    """Risk payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class MeetingNoteBase(BaseModel):
    """Shared note fields."""

    description: str
    category: str = "note"


class MeetingNoteCreate(MeetingNoteBase):
    """Schema for creating a meeting note."""


class MeetingNoteUpdate(BaseModel):
    """Schema for updating a meeting note."""

    description: Optional[str] = None
    category: Optional[str] = None


class MeetingNoteResponse(ORMModel, MeetingNoteBase):
    """Meeting note payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class AttachmentBase(BaseModel):
    """Shared attachment fields."""

    file_name: str
    file_path: str
    content_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    uploaded_at: Optional[datetime] = None


class AttachmentCreate(AttachmentBase):
    """Schema for creating an attachment."""


class AttachmentUpdate(BaseModel):
    """Schema for updating attachment metadata."""

    file_name: Optional[str] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    uploaded_at: Optional[datetime] = None


class AttachmentResponse(ORMModel, AttachmentBase):
    """Attachment payload returned from the database."""

    id: int
    meeting_id: str
    created_at: datetime
    updated_at: datetime


class MeetingBase(BaseModel):
    """Shared meeting fields."""

    title: str
    summary: str = ""
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class MeetingCreate(MeetingBase):
    """Schema for creating a meeting with nested records."""

    participants: list[ParticipantCreate] = Field(default_factory=list)
    transcripts: list[TranscriptCreate] = Field(default_factory=list)
    action_items: list[ActionItemCreate] = Field(default_factory=list)
    decisions: list[DecisionCreate] = Field(default_factory=list)
    risks: list[RiskCreate] = Field(default_factory=list)
    notes: list[MeetingNoteCreate] = Field(default_factory=list)
    attachments: list[AttachmentCreate] = Field(default_factory=list)


class MeetingUpdate(BaseModel):
    """Schema for updating a meeting."""

    title: Optional[str] = None
    summary: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class MeetingResponse(ORMModel, MeetingBase):
    """Meeting payload returned from the database."""

    id: str
    created_at: datetime
    updated_at: datetime
    participants: list[ParticipantResponse] = Field(default_factory=list)
    transcripts: list[TranscriptResponse] = Field(default_factory=list)
    action_items: list[ActionItemResponse] = Field(default_factory=list)
    decisions: list[DecisionResponse] = Field(default_factory=list)
    risks: list[RiskResponse] = Field(default_factory=list)
    notes: list[MeetingNoteResponse] = Field(default_factory=list)
    attachments: list[AttachmentResponse] = Field(default_factory=list)
