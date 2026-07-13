# Acceptance Criteria - AI Meeting Notes Manager

This document defines the formal Acceptance Criteria (AC) for each user story in [User Stories](file:///c:/New%20folder%20(3)/Day4_Docs/01_User_Stories.md). Criteria are expressed in Gherkin syntax (`Given-When-Then`) and include critical edge cases and security controls.

---

## 1. Authentication & Authorization

### US-AUTH-001: Email registration with verification
#### Scenario: Successful email registration
- **Given** the user is on the registration page
- **When** the user enters a valid corporate email address (e.g., `user@company.com`) and a strong password
- **Then** the system hashes the password using Argon2id, creates a pending account, and sends a secure, cryptographically random, one-time verification link valid for 24 hours to the email address.
#### Scenario: Registration with non-corporate or invalid email (Edge Case)
- **Given** the user is on the registration page
- **When** the user attempts to sign up with a public email domain (e.g., `gmail.com`, `yahoo.com`) or an invalid email format
- **Then** the system rejects the registration, displays an error message stating "Only corporate email domains are allowed", and does not send any verification email.

### US-AUTH-002: SSO via Google Workspace and Azure AD
#### Scenario: Successful SSO authentication
- **Given** the user's organization has SSO enabled
- **When** the user clicks "Sign in with Google Workspace" and completes OAuth2 verification
- **Then** the system authenticates the user, retrieves their organizational profile, logs the token in a secure, HttpOnly, Secure cookie, and redirects them to the team dashboard.
#### Scenario: Unconfigured SSO organization context (Edge Case)
- **Given** a user attempts to sign in via Azure AD
- **When** the user's email domain has not been configured for SSO by an IT Admin
- **Then** the system rejects the login, displays an error message: "SSO is not configured for your domain. Please register via email", and logs a security warning internally.

### US-AUTH-003: Role-based access control
#### Scenario: Access control enforcement on Admin routes
- **Given** a user with the role "Member" is logged in
- **When** the user attempts to send a `GET` or `POST` request to the Admin Dashboard endpoint `/api/v1/admin/settings`
- **Then** the system denies the request, returns an HTTP 403 Forbidden status, and logs the unauthorized access attempt.

---

## 2. Dashboard

### US-DB-001: Personalized dashboard
#### Scenario: Viewing dashboard with active meetings and pending actions
- **Given** the user is authenticated and has 8 meetings and 4 pending action items
- **When** the user views the dashboard
- **Then** the page displays exactly the 5 most recent meetings and all 4 pending action items.
#### Scenario: New user dashboard with zero items (Edge Case)
- **Given** a new user is authenticated and has no meetings or action items
- **When** the user views the dashboard
- **Then** the dashboard displays placeholders: "No recent meetings found" and "No pending actions assigned to you".

---

## 3. Meeting CRUD

### US-MTG-001: Create meetings
#### Scenario: Creating a meeting with valid metadata
- **Given** the user is logged in
- **When** the user submits the create meeting form with a title, date, and 3 participants
- **Then** the system creates the meeting record, persists the metadata in the database, and loads the live note capture interface.

### US-MTG-002: Upload content and queue transcription
#### Scenario: Successful audio file upload
- **Given** the user is on the meeting upload page
- **When** the user uploads a valid `MP3` audio file of size 15MB
- **Then** the system validates the file's magic bytes, sanitizes the filename to prevent directory traversal, saves it securely outside the web root, and adds the file to the background transcription queue.
#### Scenario: Uploading unsupported file formats or oversized files (Edge Case)
- **Given** the user is on the meeting upload page
- **When** the user attempts to upload an `EXE` file or a `WAV` file of size 120MB (exceeding the 100MB limit)
- **Then** the system immediately rejects the upload, returns an HTTP 400 Bad Request, and displays a validation error detailing the file requirements.

### US-MTG-003: Edit meeting content with versioning
#### Scenario: Editing meeting notes
- **Given** the user has edit permissions for a meeting transcript
- **When** the user modifies a paragraph of the transcript and clicks "Save"
- **Then** the system saves the new text, increments the document version number, and appends the old version to the historical audit archive.

### US-MTG-004: Delete/Archive retention policy enforcement
#### Scenario: Automatic compliance purging
- **Given** the team retention policy is set to 90 days
- **When** the automated daily cron job scans the database for meetings older than 90 days
- **Then** the system permanently deletes those meetings, their associated audio files, transcripts, and summaries, and logs a compliance record in the audit trail.

---

## 4. Meeting Search

### US-SEARCH-001: Full-text search
#### Scenario: Rapid keyword search
- **Given** the database contains 1,000 meetings
- **When** the user enters a search term "JWT token" in the search bar
- **Then** the system queries the full-text search index and returns matching records in less than 2.0 seconds.

### US-SEARCH-002: Semantic search
#### Scenario: Semantic query resolution
- **Given** the database contains meetings referencing "caching", "Redis", and "speed optimization"
- **When** the user searches semantically for "performance improvements"
- **Then** the system uses vector embeddings to rank and return the Redis and caching meetings, even if they do not contain the literal words "performance improvements".

---

## 5. AI Summary & Extraction

### US-AI-001: Trigger Anthropic Claude API for summaries & extractions
#### Scenario: Successful Anthropic summary generation
- **Given** the Anthropic API key is correctly configured in the backend environment variables
- **When** the user requests a summary for a completed transcript
- **Then** the system formats the transcript, calls the Claude API, receives the structured summary, and displays it formatted in Markdown.

### US-AI-002: Show confidence and source excerpts
#### Scenario: Displaying AI confidence score
- **Given** the AI model has extracted a list of decisions and action items
- **When** the user reviews the summary page
- **Then** the system displays a percentage confidence rating and clickable direct quotes (source excerpts) from the transcript for every extracted item.

### US-AI-003: Fallback to extractive summarizer when AI unavailable
#### Scenario: Automatic fallback on API rate-limiting or outage (Edge Case)
- **Given** the Anthropic API is currently returning an HTTP 429 Rate Limit error or is unreachable
- **When** the user triggers a summary request
- **Then** the system fails open/close safely, records a `TODO(security)` warning in logs, triggers the local extractive text summarizer, and displays the summary with a warning banner: "AI model unavailable. Using local backup summary."

### US-AI-004: Re-run summary with different prompts
#### Scenario: Regenerating summary with a technical template
- **Given** a summary has already been generated
- **When** the user selects the "Technical Details" prompt template and clicks "Regenerate"
- **Then** the system updates the prompt instructions sent to the API, regenerates the summary focusing on engineering discussions, and updates the display.

---

## 6. Action Items & Decisions

### US-ACT-001: Extract action items and suggest owners
#### Scenario: Detecting action items from transcript dialogue
- **Given** the transcript contains: "Amit: Rahul will review the API tomorrow."
- **When** the extraction service runs
- **Then** it extracts an action item: "Review the API", suggests "Rahul" as the owner, and sets the target date to tomorrow.

### US-ACT-002: Track action state and due dates
#### Scenario: Completing an action item
- **Given** a user has a pending task "Review the API" on their checklist
- **When** the user checks the checkbox next to the task
- **Then** the system changes the status to "Completed" and updates the database record timestamp.

### US-ACT-003: Send reminders via email/Slack
#### Scenario: Sending automated daily reminders
- **Given** there are pending action items due in less than 24 hours
- **When** the system scheduler runs the daily reminder job
- **Then** the system sends a notification to each assignee's email and linked Slack account.

---

## 7. Tags & Categories

### US-TAG-001: Tagging and categories for organization
#### Scenario: Categorizing a meeting
- **Given** a meeting is open
- **When** the user assigns the tags "Engineering" and "Weekly"
- **Then** the system associates these tags with the meeting and allows the user to filter meetings using these tags.

---

## 8. Export & Integration

### US-EXT-001: Export summary to PDF/DOCX
#### Scenario: Exporting to PDF
- **Given** a meeting has a generated summary and action items
- **When** the user clicks "Export to PDF"
- **Then** the backend generates a formatted PDF document, serves it with `Content-Disposition: attachment`, and prompts the user to download the file.

### US-EXT-002: Push actions to Jira/Asana
#### Scenario: Pushing tasks to Jira
- **Given** the user's account is integrated with Jira
- **When** the user clicks "Sync to Jira" for an action item
- **Then** the system creates a Jira ticket with the task description, owner, and due date, and links it back to the meeting notes.
#### Scenario: Jira API integration offline (Edge Case)
- **Given** the Jira integration API is unreachable
- **When** the user attempts to sync an action item
- **Then** the system catches the exception, displays an error message: "Failed to connect to Jira. Retrying in the background", and schedules a retry job in the dead-letter queue.

### US-EXT-003: Post highlights to Slack/Teams
#### Scenario: Posting summary highlights to Slack
- **Given** the meeting highlights are finalized
- **When** the user clicks "Post to Slack Channel"
- **Then** the system formats the notes into Slack block kit format and sends them to the configured webhook URL.

---

## 9. Profile & Settings

### US-PRF-001: User profile settings
#### Scenario: Updating profile notification settings
- **Given** a user is logged in
- **When** the user disables email notifications in their settings
- **Then** the system updates their profile configuration, and does not send emails for subsequent notifications.

### US-PRF-002: Team settings and retention policies
#### Scenario: Adjusting corporate retention settings
- **Given** the admin is on the organization settings page
- **When** the admin updates the retention period from 90 days to 30 days
- **Then** the system updates the database and schedules a clean-up job to immediately prune notes older than 30 days.

---

## 10. Notifications

### US-NOT-001: In-app and email notifications
#### Scenario: Triggering in-app alert for task assignment
- **Given** User A assigns an action item to User B
- **When** User B is active in the application
- **Then** an in-app toast notification appears instantly, and an unread notification badge is added to their notification bell.

---

## 11. Admin & Reports

### US-ADM-001: Admin dashboard for usage and logs
#### Scenario: Viewing active API key usage
- **Given** an IT Admin is logged in
- **When** the Admin visits `/admin/dashboard`
- **Then** the system displays graphs showing monthly API cost, total transcription minutes, active users, and system performance metrics.

### US-ADM-002: Audit trail for AI/fallback decisions
#### Scenario: Recording a fallback decision event
- **Given** the Anthropic API failed and the system fell back to the local summarizer
- **When** this fallback event is processed
- **Then** the system writes a permanent record into the immutable audit database table, including the timestamp, the meeting ID, the API error code, and the operator ID.

---

## 12. Reports & Analytics

### US-RPT-001: Basic team-level reports
#### Scenario: Generating team productivity report
- **Given** a team leader is logged in
- **When** the team leader runs the weekly analytics report
- **Then** the system outputs a table of statistics showing total meetings held, average meeting length, count of action items resolved, and a calculation of estimated hours saved.
