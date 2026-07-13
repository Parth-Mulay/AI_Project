# User Stories - AI Meeting Notes Manager

This document maps all functional requirements defined in [FUNCTIONAL_REQUIREMENTS.md](file:///c:/New%20folder%20(3)/Day1_Docs/FUNCTIONAL_REQUIREMENTS.md) to professional User Stories. Each story describes the target user, the desired capability, and the value it delivers.

---

## 1. Authentication & Authorization

### US-AUTH-001 (Maps to FR-AUTH-001)
- **Role/Actor:** User (Meeting Participant / Organizer)
- **User Story:**
  - **As a** new user,
  - **I want** to register an account using my corporate email address and verify it via a secure verification link,
  - **So that** I can securely access the platform and ensure only authorized team members can sign up.

### US-AUTH-002 (Maps to FR-AUTH-002)
- **Role/Actor:** User, IT Admin
- **User Story:**
  - **As a** corporate employee,
  - **I want** to sign in using Single Sign-On (SSO) via Google Workspace or Azure Active Directory,
  - **So that** I don't have to manage another set of credentials and can automatically inherit my organization's security policies and team context.

### US-AUTH-003 (Maps to FR-AUTH-003)
- **Role/Actor:** Admin, Member
- **User Story:**
  - **As a** team administrator,
  - **I want** to assign granular roles (Admin vs. Member) to my team members,
  - **So that** sensitive meeting notes and configuration settings are protected and restricted to authorized personnel only.

---

## 2. Dashboard

### US-DB-001 (Maps to FR-DB-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** busy team member,
  - **I want** a personalized dashboard that displays my 5 most recent meetings and an aggregated list of my pending action items,
  - **So that** I can quickly catch up on recent work and understand what requires my immediate attention.

---

## 3. Meeting CRUD

### US-MTG-001 (Maps to FR-MTG-001)
- **Role/Actor:** User (Organizer)
- **User Story:**
  - **As a** meeting organizer,
  - **I want** to create a new meeting entry by providing metadata like title, date, time, and participants,
  - **So that** my meeting notes are properly indexed and associated with the correct team context.

### US-MTG-002 (Maps to FR-MTG-002)
- **Role/Actor:** User (Organizer)
- **User Story:**
  - **As a** meeting organizer,
  - **I want** to upload text, audio (MP3, WAV, M4A), docx, or PDF files and have them queued for transcription,
  - **So that** I don't have to transcribe conversations manually.

### US-MTG-003 (Maps to FR-MTG-003)
- **Role/Actor:** User (Member)
- **User Story:**
  - **As a** meeting participant,
  - **I want** to edit the meeting transcript or AI-generated summaries and track these edits as separate versions,
  - **So that** we can correct any transcription errors while maintaining a history of changes.

### US-MTG-004 (Maps to FR-MTG-004)
- **Role/Actor:** User, IT Admin
- **User Story:**
  - **As a** compliance officer,
  - **I want** meeting records to be deleted or archived automatically based on our organization's data retention policies,
  - **So that** our organization remains compliant with data privacy regulations (e.g., GDPR, CCPA).

---

## 4. Meeting Search

### US-SEARCH-001 (Maps to FR-SEARCH-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** team member,
  - **I want** to perform full-text searches across meeting titles, bodies, and summaries with results returning in less than 2 seconds,
  - **So that** I can instantly find specific mentions or keywords from past discussions.

### US-SEARCH-002 (Maps to FR-SEARCH-002)
- **Role/Actor:** User
- **User Story:**
  - **As a** project manager,
  - **I want** to perform semantic searches on past meeting concepts (e.g., searching for "database decisions" even if those exact words aren't in the notes),
  - **So that** I can retrieve relevant context across a long history of discussions.

---

## 5. AI Summary & Extraction

### US-AI-001 (Maps to FR-AI-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** project stakeholder,
  - **I want** the system to automatically trigger the Anthropic Claude API to generate a structured meeting summary and key highlights from the transcript,
  - **So that** I can review a meeting's outcome in minutes without reading the entire transcript.

### US-AI-002 (Maps to FR-AI-002)
- **Role/Actor:** User
- **User Story:**
  - **As a** detail-oriented user,
  - **I want** the system to display confidence scores and source excerpts next to each AI-extracted detail,
  - **So that** I can verify the accuracy of the summary and trust the system's output.

### US-AI-003 (Maps to FR-AI-003)
- **Role/Actor:** User
- **User Story:**
  - **As a** user,
  - **I want** the system to automatically fall back to a local extractive summarizer if the Anthropic API is unavailable or rate-limited,
  - **So that** my productivity is not disrupted by external API outages.

### US-AI-004 (Maps to FR-AI-004)
- **Role/Actor:** User
- **User Story:**
  - **As a** meeting organizer,
  - **I want** to re-run the summary extraction with customized prompt templates (e.g., "technical focus" vs. "executive overview"),
  - **So that** the generated output fits the specific style and needs of my target audience.

---

## 6. Action Items & Decisions

### US-ACT-001 (Maps to FR-ACT-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** project manager,
  - **I want** the system to automatically extract action items and suggest potential owners from the meeting participant list,
  - **So that** follow-up tasks are documented and assigned immediately after the meeting.

### US-ACT-002 (Maps to FR-ACT-002)
- **Role/Actor:** User (Task Owner / Manager)
- **User Story:**
  - **As a** task owner,
  - **I want** to track the state (Pending, In Progress, Completed) and due dates of my assigned action items,
  - **So that** I can stay on top of my commitments and show my progress to the team.

### US-ACT-003 (Maps to FR-ACT-003)
- **Role/Actor:** User
- **User Story:**
  - **As a** task creator,
  - **I want** the system to automatically send action-item reminders to assignees via email or Slack,
  - **So that** deadlines are not missed and team accountability is maintained.

---

## 7. Tags & Categories

### US-TAG-001 (Maps to FR-TAG-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** user with many meetings,
  - **I want** to tag and categorize meetings (e.g., "Sprint Planning", "Retro", "Client Call"),
  - **So that** I can filter, organize, and find meetings based on their category.

---

## 8. Export & Integration

### US-EXT-001 (Maps to FR-EXT-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** meeting organizer,
  - **I want** to export the structured meeting notes and summary into a PDF or DOCX file,
  - **So that** I can share them with external clients or stakeholders who do not have access to the system.

### US-EXT-002 (Maps to FR-EXT-002)
- **Role/Actor:** User (Developer / PM)
- **User Story:**
  - **As a** software engineer,
  - **I want** to push extracted action items directly to Jira or Asana as tasks,
  - **So that** I can manage my work in our team's central tracking tool without manual duplication.

### US-EXT-003 (Maps to FR-EXT-003)
- **Role/Actor:** User
- **User Story:**
  - **As a** team leader,
  - **I want** to post meeting highlights and summaries directly to Slack or Microsoft Teams channels,
  - **So that** our wider team remains aligned on meeting decisions asynchronously.

---

## 9. Profile & Settings

### US-PRF-001 (Maps to FR-PRF-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** registered user,
  - **I want** to manage my profile details, preferences, and default notification options,
  - **So that** the application fits my personal workflow and layout preference.

### US-PRF-002 (Maps to FR-PRF-002)
- **Role/Actor:** Admin
- **User Story:**
  - **As a** tenant administrator,
  - **I want** to configure global team settings and corporate retention policies (e.g., delete meeting notes after 90 days),
  - **So that** we adhere to organization-wide compliance mandates.

---

## 10. Notifications

### US-NOT-001 (Maps to FR-NOT-001)
- **Role/Actor:** User
- **User Story:**
  - **As a** user,
  - **I want** to receive in-app and email notifications when I am assigned a task, mentioned in a decision, or when a meeting summary is ready,
  - **So that** I am notified of important events in real time.

---

## 11. Admin & Reports

### US-ADM-001 (Maps to FR-ADM-001)
- **Role/Actor:** Admin
- **User Story:**
  - **As an** IT administrator,
  - **I want** an admin dashboard showing usage statistics (e.g., active users, transcription hours used) and system logs,
  - **So that** I can monitor system usage, API token consumption, and audit operations.

### US-ADM-002 (Maps to FR-ADM-002)
- **Role/Actor:** Admin
- **User Story:**
  - **As a** compliance auditor,
  - **I want** a detailed audit trail of all AI summary runs, manual corrections, and fallback activations,
  - **So that** we can review system behavior and trace decisions when data discrepancies arise.

---

## 12. Reports & Analytics

### US-RPT-001 (Maps to FR-RPT-001)
- **Role/Actor:** User (Manager / Admin)
- **User Story:**
  - **As a** team lead,
  - **I want** basic team-level reports (e.g., meeting frequency, time saved, action item completion rate),
  - **So that** I can evaluate team productivity and the ROI of using the meeting manager.
