# UI Screen Traceability Matrix

This document provides a trace mapping between the **Day 5 UI/UX Screens/Component States** and the **Day 4 User Stories and Requirement IDs**, verifying that our interface designs cover 100% of the functional scope.

---

## Screen-to-Requirement Mapping Matrix

| Screen / Component ID | Screen Name | Mapped User Story ID | Mapped Functional Requirement ID | Design Coverage & Verification Check |
|---|---|---|---|---|
| **SCR-001** | Splash Screen | `N/A (System Init)` | `NFR-UX-001` | Onboarding progress and quick launch feedback loop. |
| **SCR-002** | Login Screen | `US-AUTH-002` | `FR-AUTH-002` | Features Azure AD / Google Workspace SSO login buttons. |
| **SCR-003** | Sign Up Screen | `US-AUTH-001` | `FR-AUTH-001` | Standard registration inputs with email verification triggers. |
| **SCR-004** | Forgot Password | `N/A (Gap Fix)` | `FR-AUTH-004` (Backlog) | Recovery request token trigger input form. |
| **SCR-005** | Dashboard Home | `US-DB-001` | `FR-DB-001` | Lists 5 most recent meetings and personal action items. |
| **SCR-006** | Live Recording | `US-MTG-002` | `FR-MTG-002` | Real-time waveform display and live audio capture interface. |
| **SCR-007** | Upload Audio | `US-MTG-002` | `FR-MTG-002` | Drag-and-drop file uploader (supports WAV, MP3, PDF, DOCX). |
| **SCR-008** | AI Processing | `US-AI-001` | `FR-AI-001` | Visual spinner/status tracker while AI is compiling summary. |
| **SCR-009** | Meeting Summary | `US-AI-001`, `US-AI-002`| `FR-AI-001`, `FR-AI-002` | Displays markdown summaries, confidence ratings, and excerpts. |
| **SCR-010** | Action Items Tab | `US-ACT-001`, `US-ACT-002`| `FR-ACT-001`, `FR-ACT-002` | Interactive checkbox task tracking with owner and due dates. |
| **SCR-011** | Decisions Tab | `US-ACT-001` | `FR-ACT-001` | Ordered list of decisions logged from keyword matching. |
| **SCR-012** | Meeting Timeline | `US-MTG-003` | `FR-MTG-003` | Chronologically indexed list of messages and version history. |
| **SCR-013** | Search Page | `US-SEARCH-001`, `US-SEARCH-002`| `FR-SEARCH-001`, `FR-SEARCH-002`| Full-text and semantic embedding concept search results. |
| **SCR-014** | Meeting History | `US-TAG-001` | `FR-TAG-001` | General archive showing tags, categories, and filters. |
| **SCR-015** | Team Workspace | `US-AUTH-003` | `FR-AUTH-003` | User directory displaying roles (Admin vs. Member modifiers). |
| **SCR-016** | Notifications Bell | `US-NOT-001` | `FR-NOT-001` | Slide-out overlay showing mentions, assignments, and summary ready states. |
| **SCR-017** | User Profile | `US-PRF-001` | `FR-PRF-001` | Personal preferences and avatar configurations. |
| **SCR-018** | System Settings | `US-PRF-002` | `FR-PRF-002` | Admin compliance configs (retention policies and integrations). |
| **SCR-019** | Export Options | `US-EXT-001` | `FR-EXT-001` | PDF, DOCX, and raw Markdown download overlays. |
| **SCR-020** | Empty State | `US-DB-001` | `FR-DB-001` | Actionable placeholders for empty lists or dashboards. |
| **SCR-021** | Error Fallback | `US-AI-003` | `FR-AI-003` | Banner indicating fallback summarizer is active. |
| **SCR-022** | Success Banner | `US-EXT-002`, `US-EXT-003`| `FR-EXT-002`, `FR-EXT-003`| Positive confirmation indicators (e.g., "Slack Synced"). |
