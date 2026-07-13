# MVP Design Decisions – AI Meeting Notes Manager

## Executive Summary

This document details the prioritization framework and design decisions for the AI Meeting Notes Manager. Using MoSCoW prioritization and product trade-off analysis, we identified the core features implemented in our working prototype, the capabilities deferred as planned enhancements, and intentionally out-of-scope items. Each decision is justified by user research, competitor evaluations, and technical feasibility.

---

## 1. Prioritization Framework: MoSCoW Method

We categorized capabilities using the MoSCoW method to establish a robust MVP scope while defining a clear development roadmap:

| Category | Criteria | Impact on MVP |
|----------|----------|---------------|
| **Must Have** | Required for product viability; solves the core user problem. | Essential for initial release. |
| **Should Have** | Adds significant user value but the application can function without it. | High-priority planned enhancement. |
| **Could Have** | Nice-to-have capabilities; improves experience but not critical. | Deferred backlog. |
| **Won't Have** | Explicitly out of scope; not required for initial validation. | Excluded from near-term roadmap. |

---

## 2. Feature Breakdown: Implemented vs. Planned

### 2.1 Current Prototype (MUST HAVE Features)

These features are fully implemented and verified in the current prototype:

#### 2.1.1 Meeting Creation & Management
- **Description:** Initialize meetings with metadata (title and participants).
- **Justification:** Establishes context for note organization and indexing.
- **Implementation Status:** Fully implemented.

#### 2.1.2 Live Note Capture
- **Description:** Simulates note-taking via real-time text input (speaker and message dialogue).
- **Justification:** Eliminates early transcription dependencies and runs fully offline.
- **Implementation Status:** Fully implemented.

#### 2.1.3 Automatic Action Item Extraction
- **Description:** Parse dialogue using deterministic keyword matching (e.g., "will", "should", "needs to") to extract tasks, attribute owners, and recognize deadlines.
- **Justification:** Addresses the primary user pain point (scattered action items and unclear ownership) without API latency or cost.
- **Implementation Status:** Fully implemented.

#### 2.1.4 Decision Detection & Logging
- **Description:** Extract and log choices made during meetings using decision indicators (e.g., "decided", "agreed", "approved").
- **Justification:** Addresses the key pain point of historical context loss and prevents re-litigating choices.
- **Implementation Status:** Fully implemented.

#### 2.1.5 Important Notes & Risk Capture
- **Description:** Tag and categorize crucial reminders, risks, or blockers (using keywords like "risk", "blocker", "reminder").
- **Justification:** Essential for project managers and tech leads coordinating risk registers.
- **Implementation Status:** Fully implemented.

#### 2.1.6 Meeting Summary Generation
- **Description:** Compiles a concise overview of meeting outcomes by prioritizing sentences containing extracted action items, decisions, and risks.
- **Justification:** Provides quick visibility for asynchronous team alignment.
- **Implementation Status:** Fully implemented.

#### 2.1.7 Markdown Export
- **Description:** Generates structured Markdown files with formatted tables, summaries, and action checklists.
- **Justification:** Platform-agnostic format that integrates into standard wikis or version-control systems (such as Git).
- **Implementation Status:** Fully implemented.

#### 2.1.8 Polished Console UI
- **Description:** Formatted command-line interface with Unicode indicators and clear separators for improved usability.
- **Justification:** Enhances readability and demonstrates product quality during validation.
- **Implementation Status:** Fully implemented.

---

### 2.2 Planned Enhancements (SHOULD HAVE & COULD HAVE Features)

These capabilities are planned for future development phases:

#### 2.2.1 Searchable Meeting Archive (Should Have)
- **Description:** Store meetings in a local indexing layer to allow semantic queries of past choices.
- **Justification:** Allows team members to retrieve historical context (e.g., "why PostgreSQL was chosen") without scrolling through files.
- **Implementation Status:** Planned enhancement.

#### 2.2.2 In-Meeting Editing (Should Have)
- **Description:** Edit extracted items dynamically during live capture rather than post-export.
- **Justification:** Improves accuracy by correcting extraction errors on the fly.
- **Implementation Status:** Planned enhancement.

#### 2.2.3 Communication Integrations (Should Have)
- **Description:** Push markdown summaries automatically to team chat channels.
- **Justification:** Meets teams where they work, reducing administrative distribution steps.
- **Implementation Status:** Planned enhancement.

#### 2.2.4 Audio Transcription (Could Have)
- **Description:** Integrate audio recording and speech-to-text models (such as the Whisper API).
- **Justification:** Supports hands-free capture for fast-paced discussions.
- **Implementation Status:** Planned enhancement.

#### 2.2.5 LLM Refinement (Could Have)
- **Description:** Utilize language models to refine extraction and summarize indirect dialogue.
- **Justification:** Improves accuracy for complex grammar patterns.
- **Implementation Status:** Planned enhancement.

#### 2.2.6 Jira and GitHub Connections (Could Have)
- **Description:** Automatically convert action items into issue tracker tickets.
- **Justification:** Streamlines software engineering workflows.
- **Implementation Status:** Planned enhancement.

---

### 2.3 Out-of-Scope (WON'T HAVE Features)

These capabilities are explicitly excluded from the current roadmap:
- **Real-Time Video Recording:** Excluded due to high storage, streaming infrastructure, and consent compliance overhead.
- **Native Mobile Applications:** Deferred; desktop web and command-line interfaces are the primary workspaces for the target segments.
- **Advanced Meeting Analytics:** Metrics like speaker engagement and talk-time velocity are deferred until documentation capture is fully validated.

---

## 3. Capability Priority Table

| Feature | Primary User Benefit | Implementation Complexity | Priority | Status |
|---------|---------------------|---------------------------|----------|--------|
| Meeting Creation | Organizes notes by session | Low | Must Have | Current Prototype |
| Live Note Capture | Simple, offline-ready input | Low | Must Have | Current Prototype |
| Action Extraction | Resolves task ownership ambiguity | Medium | Must Have | Current Prototype |
| Decision Logging | Retains organizational memory | Low | Must Have | Current Prototype |
| Risk Capture | Identifies project blockers early | Low | Must Have | Current Prototype |
| Summary Generation | Concise executive overview | Medium | Must Have | Current Prototype |
| Markdown Export | Universal file compatibility | Low | Must Have | Current Prototype |
| Polished UI | Clean, readable terminal output | Low | Must Have | Current Prototype |
| Searchable Archive | Quick retrieval of past context | Medium | Should Have | Planned Enhancement |
| In-Meeting Editing | Real-time correction of highlights | Medium | Should Have | Planned Enhancement |
| Chat Integration | Automatic outcome distribution | Medium | Should Have | Planned Enhancement |
| Audio Transcription | Hands-free note capture | High | Could Have | Planned Enhancement |
| LLM Refinement | Contextual grammar handling | Medium | Could Have | Planned Enhancement |
| Task Tracker Sync | Automated ticket generation | Medium | Could Have | Planned Enhancement |
| Calendar Sync | Joins meetings automatically | High | Could Have | Planned Enhancement |

---

## 4. Deferral Trade-Off Analysis

### 4.1 Audio Transcription
- **Trade-off:** Including transcription increases setup complexity, external API costs, and network dependencies. Deferring it allows us to isolate and validate our core value: automated extraction of outcomes.
- **Decision:** Validate the rule-based extraction logic using text input first. Introduce speech-to-text models once the core extraction UX is verified.

### 4.2 LLM Refinement
- **Trade-off:** Generative AI models handle semantic nuances but run the risk of hallucinating outcomes and require recurring API costs.
- **Decision:** Use deterministic, rule-based keywords as the baseline. This ensures explainable extractions. LLM refinement will be added as an optional enhancement step.

### 4.3 Task Tracker Integrations
- **Trade-off:** Direct integrations (e.g., Jira API) depend on platform-specific authentication and setups, limiting initial portability.
- **Decision:** Export to standard Markdown, which is universally copy-paste friendly. Build direct API integrations after user validation.

---

## 5. Prototype Validation

The current prototype demonstrates the technical and functional viability of our design decisions:
- **Standard Library Execution:** Validates that key insights can be parsed locally without external library installations or runtime fees.
- **Keyword Processing:** Verifies that a rule-based parser can identify action items, decisions, and risks in dialogue.
- **Format Portability:** Demonstrates that Markdown files serve as a flexible, versionable documentation format.

---

## 6. Research References

- **Resource:** *Inspired: How to Create Products Customers Love* by Marty Cagan (Silicon Valley Product Group)
  - **Why Consulted:** To structure product prioritization around user value and viability risks.
  - **How It Influenced:** Guided the decision to defer high-cost integrations (such as Whisper or Jira) until the core value of automated extraction was validated.
- **Resource:** *The Lean Product Playbook* by Dan Olsen
  - **Why Consulted:** To apply MoSCoW prioritization metrics to the feature backlog.
  - **How It Influenced:** Helped establish a clean separation between essential prototype features (P0) and future growth vectors (P1/P2).

---

## 7. Conclusion

MVP design decisions prioritize the core value of structured meeting extraction over technical integrations. By implementing a local, standard-library prototype, we validate user workflows and extraction utility before incurring operational costs or integration dependencies.

---

**Document Status:** Refinement Completed  
**Date:** 2026-07-10  
**Version:** 1.1
