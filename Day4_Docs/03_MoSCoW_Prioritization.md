# MoSCoW Prioritization - AI Meeting Notes Manager

This document presents a comprehensive MoSCoW (Must Have, Should Have, Could Have, Won't Have) prioritization of all 26 functional requirements from [FUNCTIONAL_REQUIREMENTS.md](file:///c:/New%20folder%20(3)/Day1_Docs/FUNCTIONAL_REQUIREMENTS.md). Each classification is justified by product research, technical feasibility, and business value.

---

## Prioritization Summary Table

| Requirement ID | Requirement Description | MoSCoW Priority | Business & Product Justification |
|----------------|-------------------------|-----------------|----------------------------------|
| **FR-AUTH-001**| Email Registration & Verification | **Must Have** | Required to secure user accounts in a multi-tenant environment. |
| **FR-AUTH-002**| SSO via Google/Azure AD | **Should Have** | Crucial for enterprise adoption, but users can sign up using corporate email domains in the MVP. |
| **FR-AUTH-003**| Role-Based Access Control | **Must Have** | Essential to prevent regular members from viewing or modifying restricted meetings or admin settings. |
| **FR-DB-001**  | Personalized Dashboard | **Must Have** | Core user landing page showing the 5 most recent meetings and personal action items; critical for daily UX. |
| **FR-MTG-001** | Create Meetings | **Must Have** | Primary flow entry point; metadata setup is required to initialize notes. |
| **FR-MTG-002** | Upload Content & Queue Transcription| **Must Have** (Text/Docs)<br>**Should Have** (Audio) | Text, DOCX, and PDF uploads are lightweight and simple. Audio requires transcription models (Whisper) which introduce latency and cost. |
| **FR-MTG-003** | Edit Meeting Content (Versioning) | **Should Have** | Users need to correct transcription errors, but they can work around this in the MVP by exporting to Markdown. |
| **FR-MTG-004** | Delete/Archive Retention Compliance | **Should Have** | Essential for data compliance (GDPR/CCPA), but can be handled manually in the early launch phase. |
| **FR-SEARCH-001**| Full-Text Search (<2s) | **Must Have** | Essential for navigating high volumes of meeting notes efficiently. |
| **FR-SEARCH-002**| Semantic Search (Embeddings) | **Could Have** | Adds high value for conceptual queries but introduces significant backend complexity and database cost. |
| **FR-AI-001**  | Anthropic Claude Summary API | **Must Have** | The core value proposition of the product; provides high-quality structured summaries. |
| **FR-AI-002**  | Confidence Scores & Source Excerpts | **Should Have** | Crucial for user trust and checking AI hallucinations, but summaries are readable without it. |
| **FR-AI-003**  | Local Extractive Fallback Summarizer| **Must Have** | Vital to guarantee service availability and offline capabilities if external APIs go down. |
| **FR-AI-004**  | Re-run Summary with Custom Prompts | **Could Have** | Nice-to-have personalization feature, but a single optimized default prompt is sufficient for launch. |
| **FR-ACT-001** | Extract Action Items & Owners | **Must Have** | Solves the primary administrative pain point: tracking who is responsible for what. |
| **FR-ACT-002** | Track Action State & Due Dates | **Must Have** | Required for accountability; enables the dashboard's task checklist function. |
| **FR-ACT-003** | Send Reminders via Email/Slack | **Should Have** | Boosts follow-up rates, but users can view their action items directly on the dashboard. |
| **FR-TAG-001** | Tagging & Categories | **Should Have** | Useful for organizing notes once teams accumulate dozens of meetings, but not blocking on Day 1. |
| **FR-EXT-001** | Export to PDF/DOCX | **Must Have** | Necessary to share notes with clients or external stakeholders who lack platform accounts. |
| **FR-EXT-002** | Push Actions to Jira/Asana | **Could Have** | Improves developer workflow, but copy-pasting exported Markdown is an acceptable MVP workaround. |
| **FR-EXT-003** | Post Highlights to Slack/Teams | **Should Have** | Meets teams where they work; supports asynchronous coordination. |
| **FR-PRF-001** | User Profile Management | **Could Have** | Default configurations are acceptable for initial validation; customization is a fast follow. |
| **FR-PRF-002** | Team Settings & Global Retention | **Should Have** | Required for configuring tenant-wide compliance and details. |
| **FR-NOT-001** | In-app & Email Notifications | **Should Have** | Important for engagement, but the dashboard task checklist serves as a passive notification hub. |
| **FR-ADM-001** | Admin Dashboard (Usage Logs) | **Could Have** | Only needed by system administrators; backend database logs can be used during early stages. |
| **FR-ADM-002** | Audit Trail for AI/Fallback Decisions| **Should Have** | Essential for system debugging and compliance validation. |
| **FR-RPT-001** | Team-Level Reports & Analytics | **Could Have** | Shows ROI to management, but does not affect the core day-to-day meeting workflow. |

---

## Priority Classification Rationale

### 1. Must Have (MVP Core)
These features are critical to resolving the primary user pain points identified in [USER_JOURNEY.md](file:///c:/New%20folder%20(3)/Day1_Docs/USER_JOURNEY.md) and [01_Product_Ideation_Research.md](file:///c:/New%20folder%20(3)/Day3_Docs/01_Product_Ideation_Research.md). Without them, the product is non-viable.
- **AI Summary & Action Item Extraction (FR-AI-001, FR-AI-003, FR-ACT-001, FR-ACT-002):** These represent the core value proposition. Fallback mechanisms guarantee uptime.
- **Data Entry & Management (FR-MTG-001, FR-DB-001, FR-SEARCH-001, FR-EXT-001):** Users must be able to input, search, and export their notes.
- **Fundamental Security (FR-AUTH-001, FR-AUTH-003):** Multi-tenant notes must be isolated and secured from unauthorized access from Day 1.

### 2. Should Have (High-Priority Enhancements)
These features add massive user and business value, but the application remains functional without them. They are scheduled for the post-MVP release.
- **Audio Upload & Transcription (FR-MTG-002 part):** Crucial for hands-free operations, but text-based capture is our baseline MVP input (established in `PROTOTYPE.md`).
- **Integrations & Reminders (FR-EXT-003, FR-ACT-003, FR-NOT-001):** Slack notifications and email reminders drive engagement but can be deferred.
- **Explainability & Auditing (FR-AI-002, FR-ADM-002):** Showing AI confidence scores and logging fallback decisions are important for enterprise trust, but do not block note creation.

### 3. Could Have (Backlog)
These are nice-to-have capabilities that provide convenience but are not core to the product's function.
- **Integrations with Jira/Asana (FR-EXT-002):** High complexity due to distinct APIs and authentication setups.
- **Semantic Search (FR-SEARCH-002):** Adds value but is a secondary search type that requires vector databases.
- **Analytics & Usage Reports (FR-RPT-001, FR-ADM-001):** Helpful for enterprise scaling, but not needed during initial validation.

### 4. Won't Have (Out of Scope for Near-Term Roadmap)
- **Real-Time Video Recording:** Heavy infrastructure costs, storage overhead, and complex privacy compliance.
- **Native Mobile Apps:** Deferred; users primarily consume and manage meeting notes on desktop screens (established in [04_MVP_Design_Decisions.md](file:///c:/New%20folder%20(3)/Day3_Docs/04_MVP_Design_Decisions.md)).
