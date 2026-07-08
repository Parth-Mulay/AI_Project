# FUNCTIONAL REQUIREMENTS (SRS)

Each feature below contains: Requirement ID, Description, Priority, Actors, Preconditions, Postconditions, Acceptance Criteria.

## 1. Authentication & Authorization

FR-AUTH-001
- Description: Email registration with verification
- Priority: High
- Actors: User
- Preconditions: None
- Postconditions: Account created; verification sent
- Acceptance: User activates account via verification link

FR-AUTH-002
- Description: SSO via Google Workspace and Azure AD
- Priority: High
- Actors: User, IT Admin
- Preconditions: Org has SSO configured
- Postconditions: User authenticated with team context
- Acceptance: User logs in via SSO and is assigned to team

FR-AUTH-003
- Description: Role-based access control
- Priority: High
- Actors: Admin, Member
- Preconditions: Team exists
- Postconditions: Access restrictions enforced
- Acceptance: Admin assigns roles; UI enforces permissions

## 2. Dashboard
FR-DB-001: Personalized dashboard (High) — shows recent meetings and pending actions; must display 5 most recent meetings and pending actions list.

## 3. Meeting CRUD
FR-MTG-001: Create meetings (High) — persists metadata.
FR-MTG-002: Upload content (High) — supports text, audio, docx, pdf; queues transcription.
FR-MTG-003: Edit meeting content (Medium) — versioned edits.
FR-MTG-004: Delete/Archive (Medium) — retention policy enforcement.

## 4. Meeting Search
FR-SEARCH-001: Full-text search across title, body, summaries (High) — results in <2s.
FR-SEARCH-002: Semantic search using embeddings (Medium).

## 5. AI Summary & Extraction
FR-AI-001: Trigger Anthropic API for summaries & extractions (High).
FR-AI-002: Show confidence and source excerpts (High).
FR-AI-003: Fallback to extractive summarizer when AI unavailable (High).
FR-AI-004: Re-run summary with different prompts (Medium).

## 6. Action Items & Decisions
FR-ACT-001: Extract action items and suggest owners (High).
FR-ACT-002: Track action state and due dates (High).
FR-ACT-003: Send reminders via email/Slack (Medium).

## 7. Tags & Categories
FR-TAG-001: Tagging and categories for organization (Medium).

## 8. Export & Integration
FR-EXT-001: Export summary to PDF/DOCX (High).
FR-EXT-002: Push actions to Jira/Asana (Medium).
FR-EXT-003: Post highlights to Slack/Teams (Medium).

## 9. Profile & Settings
FR-PRF-001: User profile (Low).
FR-PRF-002: Team settings including retention (High).

## 10. Notifications
FR-NOT-001: In-app and email notifications for actions (Medium).

## 11. Admin & Reports
FR-ADM-001: Admin dashboard for usage and logs (Medium).
FR-ADM-002: Audit trail for AI/fallback decisions (High).

## 12. Reports & Analytics
FR-RPT-001: Basic team-level reports (Low).

(Notes: Each FR maps to backlog items, estimated in later phases.)

(End of Functional Requirements)
