# Day 9 Task 3: Database Design and Integration

## Database Overview

The AI Meeting Notes Manager now uses a relational SQLAlchemy data model with SQLite as the default development database.

- Default connection string: `sqlite:///./meeting_notes.db`
- Configuration source: `.env`
- ORM: SQLAlchemy
- Validation/serialization layer: Pydantic schemas in `src/database/schemas.py`
- Session management: reusable session helpers in `src/database/session.py`
- Startup behavior: tables are created automatically when the FastAPI app starts

This design keeps the existing backend behavior intact while replacing file-only persistence with a normalized database structure that supports transcripts, AI outputs, participants, and uploaded files.

## Why This Schema Exists

The application does more than store a plain transcript. It needs to preserve:

- The meeting record itself
- Who participated
- What was said and in what order
- Which action items were extracted
- Which decisions were detected
- Which risks were identified
- Which files were attached to a meeting

The schema separates these concerns into related tables so each concept has a clear place, avoids duplication, and stays easy to query as the product grows.

## Entities

### `meetings`

Purpose: stores the top-level meeting record and AI-generated summary.

- Primary key: `id`
- Important fields:
  - `title`
  - `summary`
  - `started_at`
  - `ended_at`
  - `created_at`
  - `updated_at`

Why it exists:
- Every other table belongs to a meeting
- It acts as the aggregate root for the archive, transcript, AI summary, and extracted insights

### `participants`

Purpose: stores people associated with a meeting.

- Primary key: `id`
- Foreign key: `meeting_id -> meetings.id`
- Important fields:
  - `name`
  - `email`
  - `role`

Why it exists:
- Supports attendance, ownership, and future collaboration features
- Prevents repeating participant details in every transcript row or action item

### `transcripts`

Purpose: stores ordered transcript entries for a meeting.

- Primary key: `id`
- Foreign keys:
  - `meeting_id -> meetings.id`
  - `participant_id -> participants.id`
- Important fields:
  - `sequence_number`
  - `speaker_name`
  - `content`
  - `spoken_at`

Why it exists:
- Preserves the conversation timeline
- Supports transcript display, search, summarization traceability, and downstream AI analysis

### `action_items`

Purpose: stores actionable tasks extracted from the meeting.

- Primary key: `id`
- Foreign keys:
  - `meeting_id -> meetings.id`
  - `assignee_id -> participants.id`
- Important fields:
  - `description`
  - `assigned_to`
  - `due_date`
  - `status`
  - `source_excerpt`

Why it exists:
- Tracks responsibilities and follow-up work
- Links tasks back to a meeting and optionally to a participant

### `decisions`

Purpose: stores decisions detected from transcript analysis.

- Primary key: `id`
- Foreign key: `meeting_id -> meetings.id`
- Important fields:
  - `description`
  - `context`

Why it exists:
- Decisions are first-class outcomes of meetings and should be queryable separately from raw transcript text

### `risks`

Purpose: stores risks, blockers, or concerns identified during analysis.

- Primary key: `id`
- Foreign key: `meeting_id -> meetings.id`
- Important fields:
  - `description`
  - `severity`
  - `status`

Why it exists:
- Risk tracking is a core part of the current product behavior
- Separating risks from generic notes makes filtering and reporting easier

### `attachments`

Purpose: stores uploaded file metadata associated with a meeting.

- Primary key: `id`
- Foreign key: `meeting_id -> meetings.id`
- Important fields:
  - `file_name`
  - `file_path`
  - `content_type`
  - `file_size_bytes`
  - `uploaded_at`

Why it exists:
- Meetings can originate from uploaded audio or documents
- File metadata should be stored separately from transcript content

### `meeting_notes`

Purpose: stores non-risk notes preserved from the current backend flow.

- Primary key: `id`
- Foreign key: `meeting_id -> meetings.id`
- Important fields:
  - `description`
  - `category`

Why it exists:
- The current backend already distinguishes important notes from action items and decisions
- This table keeps those notes normalized without forcing every note to be treated as a risk

## Relationships

- One `meeting` has many `participants`
- One `meeting` has many `transcripts`
- One `meeting` has many `action_items`
- One `meeting` has many `decisions`
- One `meeting` has many `risks`
- One `meeting` has many `meeting_notes`
- One `meeting` has many `attachments`
- One `participant` can be linked to many `transcripts`
- One `participant` can be assigned to many `action_items`

Cascade behavior:

- Deleting a meeting deletes its dependent participants, transcripts, action items, decisions, risks, notes, and attachments
- If a participant is removed, related transcript/action references are set to `NULL` rather than deleting the content

## Primary Keys

- `meetings.id` uses a UUID string
- All child tables use integer surrogate primary keys

Reasoning:

- UUIDs work well for top-level meeting identifiers that may be surfaced in APIs or exports
- Integer keys keep related child tables simple and efficient

## Foreign Keys

- `participants.meeting_id -> meetings.id`
- `transcripts.meeting_id -> meetings.id`
- `transcripts.participant_id -> participants.id`
- `action_items.meeting_id -> meetings.id`
- `action_items.assignee_id -> participants.id`
- `decisions.meeting_id -> meetings.id`
- `risks.meeting_id -> meetings.id`
- `meeting_notes.meeting_id -> meetings.id`
- `attachments.meeting_id -> meetings.id`

## Indexing Strategy

Indexes were added where the backend is likely to filter or sort:

- Meeting title and start time
- Participant lookup by meeting and name
- Transcript ordering and timestamp access
- Action item status by meeting
- Risk status and severity by meeting
- Attachment upload time by meeting

Unique constraints were also added for:

- Participant name uniqueness within a meeting
- Transcript sequence uniqueness within a meeting

## Pydantic Schema Coverage

Each major entity includes matching schemas for:

- `Create`
- `Update`
- `Response`

These are located in `src/database/schemas.py` and prepare the backend for future database-backed service or API operations without implementing CRUD in this task.

## Integration Notes

The backend now includes:

- Environment-based database configuration in `src/database/database.py`
- A reusable `SessionLocal` and `get_db()` dependency in `src/database/session.py`
- SQLAlchemy models in `src/database/models.py`
- Pydantic schemas in `src/database/schemas.py`
- Automatic table creation during FastAPI startup in `src/server.py`
- SQLAlchemy-backed persistence bridging in `src/persistence.py`

The persistence layer keeps the existing backend behavior while storing data in SQLite. If the older JSON archive file exists, it is used once to seed the database when the tables are empty.

## Simple ER Diagram

```text
meetings
  PK id
  |
  |--< participants
  |     PK id
  |     FK meeting_id -> meetings.id
  |
  |--< transcripts
  |     PK id
  |     FK meeting_id -> meetings.id
  |     FK participant_id -> participants.id
  |
  |--< action_items
  |     PK id
  |     FK meeting_id -> meetings.id
  |     FK assignee_id -> participants.id
  |
  |--< decisions
  |     PK id
  |     FK meeting_id -> meetings.id
  |
  |--< risks
  |     PK id
  |     FK meeting_id -> meetings.id
  |
  |--< meeting_notes
  |     PK id
  |     FK meeting_id -> meetings.id
  |
  |--< attachments
        PK id
        FK meeting_id -> meetings.id
```

## How the Schema Supports the Product

This schema supports the AI Meeting Notes Manager by giving each meeting artifact a proper relational home:

- uploads map to attachments
- transcript processing maps to ordered transcript rows
- summaries live on the meeting record
- action extraction maps to action items
- decision detection maps to decisions
- risk detection maps to risks
- archive/history maps to the meetings table and related children

That foundation makes future search, filtering, analytics, and collaboration features much easier to build without redesigning storage again.
