# Requirement Gap Analysis - AI Meeting Notes Manager

This document reviews the existing documentation (Days 1–3) to identify gaps, ambiguities, security vulnerabilities, validation omissions, unhandled edge cases, and missing business rules. It proposes actionable improvements for the implementation phase.

---

## 1. Missing Requirements

### Gap 1.1: Password Reset & Account Recovery Flow
- **Description:** [FUNCTIONAL_REQUIREMENTS.md](file:///c:/New%20folder%20(3)/Day1_Docs/FUNCTIONAL_REQUIREMENTS.md) specifies email registration (`FR-AUTH-001`), but does not define a flow for users who forget their passwords.
- **Impact:** High. Users will be locked out of accounts permanently, leading to support overhead and poor UX.
- **Proposed Improvement:** Add `FR-AUTH-004: Password Reset Workflow`. Implement a "Forgot Password" flow that emails a cryptographically signed, short-lived (15 minutes), single-use token to allow the user to reset their password securely.

### Gap 1.2: Session Invalidation & Logout
- **Description:** No functional requirement defines session management lifecycle operations (logging out, invalidating active sessions, and clearing tokens).
- **Impact:** High. Users cannot terminate their sessions, which presents a security risk on shared devices.
- **Proposed Improvement:** Add `FR-AUTH-005: Session Invalidation`. Implement a logout endpoint that deletes client-side session cookies on the server, clears client-side memory state, and redirects the browser to the login screen.

### Gap 1.3: User-Initiated Account Deletion (GDPR Right to Be Forgotten)
- **Description:** While compliance with GDPR/CCPA is listed in Non-Functional Requirements (`NFR-PRIV-002`), there is no corresponding functional interface for user-initiated account deletion.
- **Impact:** Medium. Compliance audits will fail if users have no self-service mechanism to purge their data.
- **Proposed Improvement:** Add `FR-PRF-003: Account Self-Deletion`. Allow users to request permanent account deletion, which triggers soft deletion followed by a hard purge of all associated meetings, files, and PII after a 30-day grace period.

---

## 2. Ambiguous Requirements

### Gap 2.1: Definition of AI "Unavailability" and Fallback Logic
- **Description:** `FR-AI-003` specifies a "fallback to extractive summarizer when AI unavailable." It does not define what triggers this fallback.
- **Impact:** High. The system could hang or crash if it waits indefinitely for a timed-out API call.
- **Proposed Improvement:** Define "Unavailable" as:
  1. A network connection timeout exceeding 10 seconds.
  2. Anthropic API response code `429` (Rate Limit) or `5xx` (Server Error) after 3 automated retry attempts using exponential backoff.
  The fallback should run a deterministic local TextRank algorithm to parse the transcript and extract the top 20% highest-scoring sentences based on term frequency.

### Gap 2.2: Generative AI "Confidence Scores"
- **Description:** `FR-AI-002` specifies showing "confidence and source excerpts" for summaries. LLMs do not natively return standard statistical confidence scores for generated summaries.
- **Impact:** Medium. Developers might implement arbitrary or fabricated confidence scores, misleading users.
- **Proposed Improvement:** Define confidence calculations based on rule-based validation of source excerpts:
  - If the summary item has a direct, exact-string match in the transcript, the confidence is **High (>=90%)**.
  - If it is semantically matched (distance < threshold) but has no direct quote, the confidence is **Medium (70-89%)**.
  - Otherwise, show **Low (50-69%)**.

### Gap 2.3: Semantic Search Indexing Details
- **Description:** `FR-SEARCH-002` mentions "semantic search using embeddings" but does not detail indexing timing.
- **Impact:** Medium. High database load and latency if embeddings are calculated on every search query.
- **Proposed Improvement:** Specify that semantic search will use a local vector store (e.g., pgvector or ChromaDB). Embeddings must be generated using a lightweight sentence embedding model (e.g., `all-MiniLM-L6-v2`) in a background worker *immediately* when a meeting transcript is finalized or edited, never on-demand during a search query.

---

## 3. Security Gaps

### Gap 3.1: Session Token Storage Vulnerability
- **Description:** Current documentation does not specify where session tokens are stored, leaving developers to store them in `localStorage`, exposing them to XSS token theft.
- **Impact:** Critical. Session hijacking is highly feasible if XSS occurs.
- **Proposed Improvement:** Enforce that all authentication tokens must be stored in secure, `HttpOnly`, `Secure`, `SameSite=Lax` cookies, blocking JavaScript access entirely.

### Gap 3.2: Cross-Site Request Forgery (CSRF) Mitigation
- **Description:** There is no requirement for CSRF protection on state-changing actions (creating/deleting meetings, updating settings).
- **Impact:** High. Users could be tricked into deleting meeting notes via malicious third-party links.
- **Proposed Improvement:** Implement anti-CSRF tokens for all POST/PUT/DELETE API endpoints. If cookies are used for authentication, require double-submit cookie validation.

### Gap 3.3: Data Isolation & Multi-Tenancy
- **Description:** The functional requirements do not define how multi-tenant isolation is enforced in the database.
- **Impact:** Critical. A user guessing a UUID or meeting ID of another organization must not be able to retrieve data.
- **Proposed Improvement:** Every SQL query fetching meeting data MUST contain a tenant ID filter (e.g., `WHERE tenant_id = :current_user_tenant_id`). Implement Row-Level Security (RLS) in the PostgreSQL database layer as a second line of defense.

---

## 4. Validation Gaps

### Gap 4.1: File Upload Security Limits
- **Description:** `FR-MTG-002` permits uploading text, audio, docx, and pdf files but does not specify file size and type validation bounds.
- **Impact:** High. Threat of Denial of Service (DoS) from massive files, and remote code execution if malicious scripts are uploaded.
- **Proposed Improvement:**
  - **Size Limits:** Enforce maximum limits of 10MB for text/docs, and 100MB for audio files.
  - **Type Validation:** Validate the uploaded file using server-side magic byte analysis (e.g., verifying `FF FB` for MP3, `%PDF` for PDF), rather than relying on the client-provided file extension.
  - **Sanitization:** Strip directory traversal paths (`../`, `..\`) from filenames using `path.basename()` before writing to disk.

### Gap 4.2: Input Sanitization
- **Description:** User input (like manual comments or title changes) is saved to the database without validation.
- **Impact:** High (XSS / SQL Injection).
- **Proposed Improvement:** Sanitize all text fields using HTML entity encoding before rendering them on the frontend, and enforce prepared statements/ORMs for all database queries.

---

## 5. Edge Cases

### Gap 5.1: Concurrent Document Edits
- **Description:** `FR-MTG-003` allows versioned edits, but does not define what happens if two users edit a transcript or summary simultaneously.
- **Impact:** Medium. Users may overwrite each other's changes, leading to data loss.
- **Proposed Improvement:** Implement a document locking mechanism. When a user begins editing, the meeting resource is marked as "locked" in the database for 15 minutes, preventing other users from editing. Alternatively, implement a Last-Write-Wins (LWW) conflict resolution strategy and alert the user if a newer version is saved while they are editing.

### Gap 5.2: Network Outages During Audio Uploads
- **Description:** High network latency or connection drops during a 100MB file upload will cause the request to fail.
- **Impact:** Medium. Frustrated users who have to restart long uploads.
- **Proposed Improvement:** Implement chunked uploads (e.g., using Tus protocol or client-side file slicing) allowing the application to resume uploads from the last successful chunk.

---

## 6. Business Rule Gaps

### Gap 6.1: Default Retention Configurations
- **Description:** `FR-MTG-004` references retention policy enforcement but lacks default definitions.
- **Impact:** Low. Inconsistent data deletion across clients.
- **Proposed Improvement:** Establish default business rules:
  - Default retention: **90 days** for standard accounts, **365 days** for enterprise accounts.
  - Retention policies are configured at the team/organization level by an Admin and cannot be overridden by individual Members.

### Gap 6.2: API Rate Limits and Tier Constraints
- **Description:** The system triggers costly external APIs (Anthropic, transcription services) without bounding user-level consumption.
- **Impact:** High (Unexpected API bills).
- **Proposed Improvement:** Implement user-level and tenant-level limits:
  - Standard User: Limit to 10 hours of audio transcription and 100 AI summarizations per month.
  - Enterprise User: Custom limits configured via the Admin Dashboard.
