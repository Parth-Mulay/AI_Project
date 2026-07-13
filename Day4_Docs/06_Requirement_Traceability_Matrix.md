# Requirement Traceability Matrix (RTM) - AI Meeting Notes Manager

This matrix provides end-to-end traceability from original Functional Requirement IDs to their respective User Stories, Acceptance Criteria, UI Screens, Backend Modules, Database tables, Priorities, and current Implementation Status.

| Requirement ID | Requirement Description | User Story ID | Acceptance Criteria ID | Future Screen | Future Backend Module | Future Database Entity | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| **FR-AUTH-001** | Email Registration with Verification | `US-AUTH-001` | `AC-AUTH-001` | Register / Sign Up | Authentication Service | `users` (table) | **Must** | Planned |
| **FR-AUTH-002** | SSO via Google Workspace & Azure AD | `US-AUTH-002` | `AC-AUTH-002` | Login | SSO / OAuth Client | `users`, `user_sso` | **Should** | Planned |
| **FR-AUTH-003** | Role-Based Access Control (RBAC) | `US-AUTH-003` | `AC-AUTH-003` | Admin / Member Settings | Authorization Middleware | `users.role` (column) | **Must** | Planned |
| **FR-DB-001** | Personalized Dashboard | `US-DB-001` | `AC-DB-001` | Dashboard | Dashboard API Service | `meetings`, `action_items` | **Must** | Planned |
| **FR-MTG-001** | Create Meetings | `US-MTG-001` | `AC-MTG-001` | Create Meeting Modal | Meeting Management Service | `meetings` | **Must** | Implemented (Prototype) |
| **FR-MTG-002** | Upload Content & Queue Transcription | `US-MTG-002` | `AC-MTG-002` | Meeting Details (Upload) | Audio / Document Upload Service | `uploaded_files` | **Must** (Text)<br>**Should** (Audio) | Implemented (Text)<br>Planned (Audio) |
| **FR-MTG-003** | Edit Meeting Content (Versioning) | `US-MTG-003` | `AC-MTG-003` | Interactive Transcript Editor | Versioning / Revision Service | `meeting_versions` | **Should** | Planned |
| **FR-MTG-004** | Delete / Archive Retention Purge | `US-MTG-004` | `AC-MTG-004` | Organization Compliance | Retention Policy Daemon | `meetings` (cascade delete) | **Should** | Planned |
| **FR-SEARCH-001** | Full-Text Search (<2s) | `US-SEARCH-001` | `AC-SEARCH-001` | Search Page | Full-Text Search Engine | `meetings` (indexed) | **Must** | Planned |
| **FR-SEARCH-002** | Semantic Search via Embeddings | `US-SEARCH-002` | `AC-SEARCH-002` | Search Page (Semantic Toggle)| Semantic Vector Search Service | `meeting_embeddings` | **Could** | Planned |
| **FR-AI-001** | Trigger Anthropic Summaries API | `US-AI-001` | `AC-AI-001` | Meeting Details (Summary View) | Claude AI Client Service | `meetings.summary` | **Must** | Planned |
| **FR-AI-002** | AI Confidence & Excerpt Display | `US-AI-002` | `AC-AI-002` | Meeting Details (AI Highlights) | AI Excerpt Alignment Engine | `meeting_highlights` | **Should** | Planned |
| **FR-AI-003** | Local Extractive Fallback Summarizer | `US-AI-003` | `AC-AI-003` | Meeting Details (Summary View) | Local TextRank Summarizer | `meetings.summary` | **Must** | Implemented (Prototype) |
| **FR-AI-004** | Re-run Summary with Custom Prompts | `US-AI-004` | `AC-AI-004` | Template Manager Panel | AI Prompt Template Service | `prompt_templates` | **Could** | Planned |
| **FR-ACT-001** | Extract Action Items & Suggest Owners | `US-ACT-001` | `AC-ACT-001` | Meeting Details (Actions list) | AI Action Item Extractor | `action_items` | **Must** | Implemented (Prototype) |
| **FR-ACT-002** | Track Action State & Due Dates | `US-ACT-002` | `AC-ACT-002` | Dashboard Checklist / Board | Task Workflow Manager | `action_items` | **Must** | Implemented (Prototype) |
| **FR-ACT-003** | Send Reminders via Slack / Email | `US-ACT-003` | `AC-ACT-003` | Notification Settings | Scheduler / Notification Engine| `action_reminders` | **Should** | Planned |
| **FR-TAG-001** | Tagging & Categories | `US-TAG-001` | `AC-TAG-001` | Tag Manager Modal | Categorization & Tagging Service| `tags`, `meeting_tags` | **Should** | Planned |
| **FR-EXT-001** | Export to PDF / DOCX | `US-EXT-001` | `AC-EXT-001` | Meeting Details (Export Dropdown)| Document Generation Service | N/A (In-Memory Stream) | **Must** | Implemented (Prototype) |
| **FR-EXT-002** | Push Actions to Jira / Asana | `US-EXT-002` | `AC-EXT-002` | Integrations Center | Integration Connector API | `integration_tokens` | **Could** | Planned |
| **FR-EXT-003** | Post Highlights to Slack / Teams | `US-EXT-003` | `AC-EXT-003` | Share Dialog | External Webhook Dispatcher | `integration_webhooks` | **Should** | Planned |
| **FR-PRF-001** | User Profile Preferences | `US-PRF-001` | `AC-PRF-001` | Profile Page | User Preferences Service | `users` (preferences JSON) | **Could** | Planned |
| **FR-PRF-002** | Team Settings & Retention Configuration| `US-PRF-002` | `AC-PRF-002` | Admin Console (Compliance) | Organization Settings Service | `organizations` | **Should** | Planned |
| **FR-NOT-001** | In-app & Email notifications | `US-NOT-001` | `AC-NOT-001` | Dashboard Notification Bell | Notification Dispatcher Broker | `notifications` | **Should** | Planned |
| **FR-ADM-001** | Admin Dashboard Usage Logs | `US-ADM-001` | `AC-ADM-001` | IT Admin Portal | Usage Statistics Service | `system_metrics` | **Could** | Planned |
| **FR-ADM-002** | Audit Trail for AI / Fallback Events | `US-ADM-002` | `AC-ADM-002` | IT Admin Portal (Audits Panel) | Audit Logging Service | `audit_trail` | **Should** | Planned |
| **FR-RPT-001** | Team-Level Reports & Analytics | `US-RPT-001` | `AC-RPT-001` | Reports Tab | Analytics Engine Service | `meetings` / `action_items` | **Could** | Planned |
