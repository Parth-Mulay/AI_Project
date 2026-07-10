# MVP Design Decisions – AI Meeting Notes Manager

## Executive Summary

This document details the prioritization framework and design decisions for the AI Meeting Notes Manager MVP. Using MoSCoW prioritization and product trade-offs analysis, we identified the core feature set necessary for MVP launch (Phase 1), features deferred to Phase 2, and intentionally out-of-scope capabilities. Each decision is justified by user research, competitive analysis, and technical feasibility.

---

## 1. Prioritization Framework: MoSCoW Method

### 1.1 MoSCoW Definitions

| Category | Criteria | Impact on MVP |
|----------|----------|---------------|
| **Must Have** | Required for product viability; without it, MVP doesn't solve core problem | Blocks launch if missing |
| **Should Have** | Important for user satisfaction; adds significant value but MVP works without | Launch after MVP if high-impact |
| **Could Have** | Nice-to-have; improves experience but not critical | Backlog for later phases |
| **Won't Have** | Explicitly deferred; not needed for MVP success | Documented for future phases |

### 1.2 Feature Categorization

---

## 2. MVP Features – Detailed Breakdown

### 2.1 MUST HAVE – Phase 1 Core Features

#### 2.1.1 Meeting Creation & Management

**Feature:** Create meeting with title and participants

| Dimension | Details |
|-----------|---------|
| **Reason** | Provides context for later extraction and export |
| **Business Value** | Enables structured output (not just transcript) |
| **Implementation Complexity** | Low (simple data model) |
| **Priority** | P0 – Core |
| **User Benefit** | All personas (organizes notes by meeting) |
| **Status** | ✅ Implemented |

**Justification:**
- Without meeting context (participants, title), extraction loses relevance
- User research: All personas mentioned needing meeting metadata
- Competitive gap: Otter, Fireflies auto-record but don't structure context
- Low effort: Simple Python data model

---

#### 2.1.2 Live Meeting Note Capture

**Feature:** Text input during meeting; capture speaker + message

| Dimension | Details |
|-----------|---------|
| **Reason** | Primary input method (easier than audio for MVP) |
| **Business Value** | No transcription dependency; works offline |
| **Implementation Complexity** | Low (CLI input loop) |
| **Priority** | P0 – Core |
| **User Benefit** | All personas (flexible input) |
| **Status** | ✅ Implemented |

**Justification:**
- Audio transcription adds complexity (Whisper API, processing time)
- Text input is simpler, more reliable for MVP
- Phase 2 enhancement: add audio transcription
- User research: Some teams prefer manual notes (async, controlled)
- Competitive advantage: Text + extraction faster than audio + transcription

---

#### 2.1.3 Automatic Action Item Extraction

**Feature:** Detect action items from meeting transcript

**Extraction Method:** Rule-based keyword matching
- Keywords: "will", "need to", "should", "must", "by Friday", "tomorrow", "ASAP", etc.
- Speaker extraction: "Alice will review API" → Owner: Alice
- Due date detection: "by Friday", "tomorrow", "ASAP"

| Dimension | Details |
|-----------|---------|
| **Reason** | Core problem identified in user research (scattered action items) |
| **Business Value** | Saves ~30 minutes/week of manual item identification |
| **Implementation Complexity** | Medium (regex + NLP preprocessing) |
| **Priority** | P0 – Core |
| **User Benefit** | Emma (PM): Ownership clarity; Carlos (EM): Follow-up ease; Nina: Time savings |
| **Status** | ✅ Implemented |

**Justification:**
- User research: Action item clarity ranked #1 pain point (9/10)
- Competitive gap: Otter requires manual extraction; Fireflies unreliable (~50% accuracy)
- Keyword-based approach: Fast, transparent, no API cost
- Hybrid future: LLM refinement in Phase 2 if needed

**Trade-off Considered:**
- LLM-based extraction (more flexible) vs. Rule-based (simpler, transparent)
- Decision: Rule-based MVP for reliability; LLM as Phase 2 enhancement

---

#### 2.1.4 Decision Detection & Logging

**Feature:** Extract decisions made during meeting

**Extraction Method:** Keyword matching
- Keywords: "decided", "approved", "agreed", "finalized", "confirmed", "accepted", "resolved"
- Capture decision as-is (preserve wording)
- Optional: timestamp and decision maker

| Dimension | Details |
|-----------|---------|
| **Reason** | Second-highest pain point: "Did we actually decide this?" |
| **Business Value** | Historical record for retrospectives; prevents re-litigating decisions |
| **Implementation Complexity** | Low (similar to action items) |
| **Priority** | P0 – Core |
| **User Benefit** | Emma: Decision reference; Carlos: Architectural memory; Nina: Client deliverables |
| **Status** | ✅ Implemented |

**Justification:**
- User research: 70% report uncertainty on past decisions
- No competitor effectively captures decisions (Otter, Fireflies skip this)
- Simple keyword-based approach sufficient for MVP
- Future enhancement: Preserve decision context (alternatives considered, trade-offs)

---

#### 2.1.5 Important Notes / Risk Capture

**Feature:** Flag risks, blockers, and reminders

**Extraction Method:** Keyword matching
- Keywords: "risk", "issue", "blocker", "problem", "reminder", "critical", "urgent"
- Categorize: RISK, ISSUE, BLOCKER, REMINDER

| Dimension | Details |
|-----------|---------|
| **Reason** | Safety-critical for high-risk meetings (product, engineering, compliance) |
| **Business Value** | Prevents overlooked risks; ensures escalation |
| **Implementation Complexity** | Low (keyword + category assignment) |
| **Priority** | P0 – Core |
| **User Benefit** | Carlos (EM): Unblocks teams; Nina: Client risk documentation |
| **Status** | ✅ Implemented |

**Justification:**
- User research: Carlos mentioned "risk management" as decision factor
- Regulatory/compliance need: Risk capture is non-negotiable for regulated industries
- Low effort: Same pattern as action items + decisions
- Differentiator: Competitors don't categorize risks separately

---

#### 2.1.6 Meeting Summary Generation

**Feature:** Auto-generate summary of key points

**Method:** Extract 5-7 key sentences (heuristic: sentences with actions, decisions, risks)

| Dimension | Details |
|-----------|---------|
| **Reason** | One-page summary for busy users (executives, consultants) |
| **Business Value** | Saves read time; provides executive overview |
| **Implementation Complexity** | Medium (heuristic-based sentence ranking) |
| **Priority** | P0 – Core |
| **User Benefit** | Emma: Executive reviews; Nina: Client summaries; Carlos: Onboarding |
| **Status** | ✅ Implemented |

**Justification:**
- User research: All personas value executive summary (especially for async participation)
- Competitive gap: Otter summaries are too generic; Fireflies unreliable
- MVP approach: Heuristic-based (important sentences = those with actions/decisions/risks)
- Phase 2 enhancement: LLM refinement for better readability

---

#### 2.1.7 Markdown Export

**Feature:** Generate Markdown file with all extracted data

**Export Contents:**
- Meeting metadata (title, date, participants, duration)
- Summary
- Full transcript
- Action items (checkbox format)
- Decisions made
- Important notes (categorized)
- Statistics (message count, item counts)

| Dimension | Details |
|-----------|---------|
| **Reason** | Enable integration with existing workflows (Git, Jira, Notion, email) |
| **Business Value** | Portable, version-controllable, future-proof |
| **Implementation Complexity** | Low (string formatting) |
| **Priority** | P0 – Core |
| **User Benefit** | All personas (integration with their tools) |
| **Status** | ✅ Implemented |

**Justification:**
- Competitive advantage: Otter, Fireflies export to proprietary formats; we use Markdown (portable)
- User research: Integration is top adoption barrier; Markdown solves this
- Enables future automation: Markdown → Jira (Zapier), Notion (import), email
- Searchable: Users can grep past meetings in Git

---

#### 2.1.8 Professional Console UI

**Feature:** Formatted terminal output with:
- Unicode icons (✓, •, 🤖, 📝, 📊, ⏰, 👥, ⚠️)
- Section headers with separators
- Color output (where supported)
- Real-time feedback ("🤖 AI Insight: ✓ Action Item Detected")

| Dimension | Details |
|-----------|---------|
| **Reason** | User perception of polish; professional appearance |
| **Business Value** | Increases credibility; enjoyable to use |
| **Implementation Complexity** | Low (formatting utilities) |
| **Priority** | P0 – Core (quality bar) |
| **User Benefit** | Nina: Professional appearance; all: pleasant UX |
| **Status** | ✅ Implemented |

**Justification:**
- User research: Fathom noted "beautiful UI drives adoption"
- Low effort: Formatting only, no logic required
- Differentiator: CLI tools often look dated; polished UI sets us apart
- Real-time feedback: "AI Insight detected" messages improve perceived intelligence

---

### 2.2 SHOULD HAVE – Phase 1.5 (Post-MVP)

These features add significant value but MVP works without them.

#### 2.2.1 Searchable Meeting Archive

**Feature:** Store meetings + enable searching past decisions

| Dimension | Details |
|-----------|---------|
| **Reason** | "When did we decide X?" is common query; prevents re-litigating |
| **Business Value** | Organizational memory; reduces decision churn |
| **Implementation Complexity** | Medium (local database or Git search) |
| **Priority** | P1 – High value |
| **User Benefit** | Carlos: Onboarding efficiency; Emma: Executive reviews |
| **Estimated Effort** | 2-3 days |
| **Phase 2 Timeline** | Add after MVP launch |

**Justification:**
- User research: Carlos repeatedly mentioned need to find past decisions
- MVP MVP: File export sufficient for Phase 1 (can search exported Markdown)
- Phase 1.5: Add SQLite database or Git integration for semantic search

**Phase 1 Workaround:** Markdown files in Git → `git log --grep="decision"` works for now

---

#### 2.2.2 Inline Editing During Meeting

**Feature:** Edit/refine action items while meeting is ongoing

| Dimension | Details |
|-----------|---------|
| **Reason** | Reduce post-meeting editing (capture accuracy in real-time) |
| **Business Value** | Faster meeting close-out; fewer post-meeting messages |
| **Implementation Complexity** | Medium (interactive CLI) |
| **Priority** | P1 – Nice-to-have |
| **User Benefit** | Emma, Carlos: Less follow-up work |
| **Estimated Effort** | 3-4 days |
| **Phase 2 Timeline** | Add in Phase 1.5 |

**Justification:**
- Nice-to-have: MVP works without this (edit Markdown file after)
- Low barrier to user flow: Post-export editing acceptable for Phase 1
- Phase 1.5 enhancement: In-meeting edits improve experience

---

#### 2.2.3 Slack Integration (Basic)

**Feature:** Post meeting summary to Slack channel automatically

| Dimension | Details |
|-----------|---------|
| **Reason** | Meet users where they work (Slack) |
| **Business Value** | Increases visibility; drives action item completion |
| **Implementation Complexity** | Medium (Slack API, webhooks) |
| **Priority** | P1 – High value for teams using Slack |
| **User Benefit** | All personas (especially distributed teams) |
| **Estimated Effort** | 2-3 days |
| **Phase 2 Timeline** | Add in Phase 1.5 |

**Justification:**
- User research: Fireflies integration with Slack noted as valuable
- MVP workaround: Manual copy-paste from Markdown acceptable for Phase 1
- Phase 1.5: Automate for convenience

---

### 2.3 COULD HAVE – Phase 2+ (Advanced Features)

Nice-to-have features; high implementation cost relative to value for MVP.

#### 2.3.1 Audio Transcription (Whisper API)

**Feature:** Record meeting audio → auto-transcribe

| Dimension | Details |
|-----------|---------|
| **Reason** | Reduce typing burden for note-taker |
| **Business Value** | Faster capture; suitable for fast-paced meetings |
| **Implementation Complexity** | High (Whisper API, audio processing, latency) |
| **Priority** | P2 – Phase 2 |
| **Cost** | $0.02 per minute (for Whisper) |
| **User Benefit** | Emma, Carlos: Hands-free note-taking |
| **Estimated Effort** | 5-7 days |
| **Phase 2 Timeline** | Q3 2026 (after MVP validation) |

**Rationale for Deferral:**
- Adds complexity without solving core problem (extraction, not capture)
- Users can take text notes for MVP (acceptable friction for Phase 1)
- Phase 2: Add Whisper API integration once MVP proven

---

#### 2.3.2 LLM-Enhanced Extraction (GPT-4)

**Feature:** Use GPT-4 to refine action item extraction

| Dimension | Details |
|-----------|---------|
| **Reason** | Handle edge cases; improve summary quality |
| **Business Value** | Fewer false positives; better comprehension |
| **Implementation Complexity** | Medium (API integration, prompt engineering) |
| **Priority** | P2 – Phase 2 enhancement |
| **Cost** | ~$0.10 per meeting (variable) |
| **User Benefit** | Improved accuracy; better summaries |
| **Estimated Effort** | 3-4 days |
| **Phase 2 Timeline** | Q3 2026 (after rule-based validation) |

**Rationale for Deferral:**
- Rule-based MVP sufficient for launch
- Hybrid approach: Keep rule-based as foundation, use LLM for refinement
- Validates demand before incurring API costs
- Prevents lock-in to OpenAI API

---

#### 2.3.3 Jira Integration

**Feature:** Automatically create Jira tickets from action items

| Dimension | Details |
|-----------|---------|
| **Reason** | Reduce manual ticket creation |
| **Business Value** | Workflow integration for engineering teams |
| **Implementation Complexity** | Medium (Jira API, auth) |
| **Priority** | P2 – Phase 2 |
| **User Benefit** | Carlos (EM): Faster ticket creation |
| **Estimated Effort** | 3-4 days |
| **Phase 2 Timeline** | Q3 2026 (after MVP validation) |

**Rationale for Deferral:**
- Not all teams use Jira (Notion, Linear, GitHub Projects users excluded)
- Markdown export + manual paste sufficient for MVP
- Phase 2: Add Jira plugin (or generic webhook approach)

---

#### 2.3.4 Calendar Integration

**Feature:** Auto-read Zoom/Teams meeting link → record automatically

| Dimension | Details |
|-----------|---------|
| **Reason** | Reduce manual meeting setup |
| **Business Value** | Workflow convenience |
| **Implementation Complexity** | High (calendar APIs, permissions) |
| **Priority** | P2 – Nice-to-have |
| **User Benefit** | Convenience (not critical) |
| **Estimated Effort** | 4-5 days |
| **Phase 2 Timeline** | Q3 2026 (low priority) |

**Rationale for Deferral:**
- Users can paste meeting link manually for MVP
- Low ROI relative to effort
- Calendar integration is nice-to-have, not critical

---

#### 2.3.5 Mobile App

**Feature:** iOS/Android app for mobile note-taking

| Dimension | Details |
|-----------|---------|
| **Reason** | Capture notes on-the-go |
| **Business Value** | Accessibility, convenience |
| **Implementation Complexity** | Very High (separate codebases) |
| **Priority** | P3 – Phase 3+ |
| **User Benefit** | Low (primary use is sync meetings at desk) |
| **Estimated Effort** | 15-20 days |
| **Phase 2 Timeline** | Q4 2026+ (after web MVP) |

**Rationale for Deferral:**
- Most meetings are Zoom/Teams at desk (laptop)
- Low user demand (not mentioned in interviews)
- Very high effort for low ROI
- Web version sufficient for Phase 1-2

---

#### 2.3.6 Compliance Features (Audit Trails, Retention)

**Feature:** Audit log of who viewed/edited notes; retention policies

| Dimension | Details |
|-----------|---------|
| **Reason** | Required for healthcare, finance, legal sectors |
| **Business Value** | Market expansion to regulated industries |
| **Implementation Complexity** | Medium (audit logging, encryption) |
| **Priority** | P2 – Phase 2 (new use case) |
| **User Benefit** | Nina, regulated teams: Risk management |
| **Estimated Effort** | 5-7 days |
| **Phase 2 Timeline** | Q3 2026 (after SMB validation) |

**Rationale for Deferral:**
- MVP targets SMB (product, engineering, consulting)
- Compliance features add complexity without MVP user benefit
- Phase 2: Add after proving SMB market fit

---

### 2.4 WON'T HAVE – Explicitly Out of Scope

These features are intentionally deferred. Not on roadmap for 2026.

#### 2.4.1 Real-Time Video/Audio Recording

**Why Not:** Requires infrastructure (storage, streaming), licensing issues (two-party consent)

**Alternative:** Markdown text input during meeting (sufficient for MVP)

---

#### 2.4.2 Multilingual Support

**Why Not:** MVP targets English-speaking teams; translation adds complexity

**Alternative:** Phase 2 enhancement using translation APIs

---

#### 2.4.3 Custom Workflows / Workflow Automation

**Why Not:** Over-complicates MVP; no-code platforms (Zapier) can automate if needed

**Alternative:** Clean API in Phase 2 enables integrations

---

#### 2.4.4 Analytics & Insights

**Why Not:** Requires 6+ months of data; not MVP requirement

**Features Include:**
- Meeting frequency trends
- Decision velocity analysis
- Participant engagement metrics
- Blockers over time

**Alternative:** Phase 3+ (post-validation)

---

## 3. Feature Priority Table (Complete Summary)

| Feature | Reason | Business Value | Complexity | Priority | Phase |
|---------|--------|---|---|---|---|
| Meeting Setup | Context for extraction | High | Low | P0 | 1 |
| Live Input | Primary input method | High | Low | P0 | 1 |
| Action Extraction | Core problem | High | Medium | P0 | 1 |
| Decision Detection | Historical record | High | Low | P0 | 1 |
| Risk Capture | Safety-critical | High | Low | P0 | 1 |
| Summary Generation | Executive overview | High | Medium | P0 | 1 |
| Markdown Export | Portability | High | Low | P0 | 1 |
| Console UI | Professional appearance | Medium | Low | P0 | 1 |
| Search Archive | Find past decisions | High | Medium | P1 | 1.5 |
| In-Meeting Editing | Reduce post-work | Medium | Medium | P1 | 1.5 |
| Slack Integration | Meet users where they work | High | Medium | P1 | 1.5 |
| Audio Transcription | Hands-free capture | Medium | High | P2 | 2 |
| LLM Enhancement | Improve accuracy | Medium | Medium | P2 | 2 |
| Jira Integration | Reduce manual work | Medium | Medium | P2 | 2 |
| Calendar Sync | Setup convenience | Low | High | P2 | 2 |
| Mobile App | On-the-go capture | Low | Very High | P3 | 3 |
| Compliance | Regulated industries | High | Medium | P2 | 2 |
| Analytics | Insights & trends | Low | High | P3 | 3 |
| Multilingual | Global market | Low | High | P3 | 3 |

---

## 4. Why Features Were Postponed: The Trade-Off Analysis

### 4.1 Audio Transcription (Phase 2)

**Question:** Why not include Whisper transcription in Phase 1?

**Trade-offs:**
| Aspect | Include MVP | Defer to Phase 2 |
|--------|---|---|
| **Launch Speed** | Slower (transcription adds complexity) | Faster (text input only) |
| **User Friction** | Lower (just speak) | Higher (must type) |
| **Cost per Meeting** | ~$0.02 (Whisper API) | $0 (Python stdlib) |
| **Operational Complexity** | Higher (API, audio processing) | Lower (no external deps) |
| **MVP Validation** | Conflates input method with extraction | Isolates extraction value |

**Decision Rationale:**
- MVP goal: Validate extraction value (not transcription)
- Text input isolates the core innovation (extraction)
- If transcription required for adoption, Phase 1.5 easy add
- Whisper is commodity; our IP is in extraction logic

---

### 4.2 LLM Enhancement (Phase 2)

**Question:** Why not use GPT-4 from the start?

**Trade-offs:**
| Aspect | Include MVP | Defer to Phase 2 |
|--------|---|---|
| **API Cost** | ~$0.10 per meeting | $0 (no API calls) |
| **Reliability** | Dependent on OpenAI uptime | Always available (offline) |
| **User Trust** | Risk: "Did it hallucinate?" | Transparent (rule-based) |
| **Speed to Launch** | Slower (prompt engineering) | Faster (simple rules) |
| **Operational Complexity** | Higher (API keys, rate limits) | Lower (local processing) |

**Decision Rationale:**
- Rule-based is good enough for MVP (70% accuracy acceptable)
- Hybrid approach: Validate rules first, add LLM refinement later
- Reduces operational risk (no third-party dependency)
- User trust: Rule-based output is explainable ("it found 'will review'")

---

### 4.3 Jira Integration (Phase 2)

**Question:** Why not integrate Jira in Phase 1?

**Trade-offs:**
| Aspect | Include MVP | Defer to Phase 2 |
|---|---|---|
| **Workflow Integration** | Direct (action → Jira) | Manual (export Markdown) |
| **Setup Friction** | High (Jira auth, config) | Low (export file) |
| **User Base** | Only Jira users | All teams |
| **Implementation Effort** | 3-4 days | Same (no change) |
| **Scope Bloat** | Risk: Over-engineering | Focus on core value |

**Decision Rationale:**
- Not all teams use Jira (Linear, GitHub Projects, Notion alternatives exist)
- Markdown export is tool-agnostic (solves integration problem generically)
- Markdown → Jira automation is simple (Zapier, custom scripts)
- Phase 1 focuses on extraction; Phase 2 adds connectors

---

## 5. Out-of-Scope Decisions

### 5.1 Why No Mobile App in MVP?

**Research Findings:**
- 95% of meetings are synchronous at desk (Zoom, Teams on laptop)
- Only 5% need mobile capture (walking meetings, 1-on-1s)
- Effort: 15-20 days for iOS + Android

**Outcome:** Web version in Phase 2; mobile in Phase 3 (if demand)

---

### 5.2 Why No Multilingual Support in MVP?

**Research Findings:**
- Bootcamp/internship context: English-only market
- Translation APIs exist (Phase 2 add-on)
- Effort: 3-5 days of work (but ongoing QA burden)

**Outcome:** English-only MVP; Phase 2 add translation support

---

### 5.3 Why No Custom Workflows?

**Research Findings:**
- Notion offers custom workflows; users find it overwhelming
- MVP principle: Do one thing really well
- No-code platforms (Zapier) provide extensibility if needed

**Outcome:** Clean API in Phase 2; users can build workflows via Zapier

---

## 6. Conclusion

MVP design prioritizes **core value** (structured extraction) over **convenience features** (integrations, transcription). This strategy:

1. **Launches faster** (core features in 2-3 weeks)
2. **Reduces risk** (no external dependencies)
3. **Validates demand** (proves users want extraction)
4. **Enables informed Phase 2** (add features based on feedback)

**Phase 1 (MVP):** Meeting management + Extraction + Export  
**Phase 1.5:** Search + Slack integration + In-meeting editing  
**Phase 2:** Transcription + LLM enhancement + Jira integration  
**Phase 3:** Analytics + Mobile + Compliance  

This roadmap balances speed (ship MVP fast) with quality (deliberate feature prioritization).

---

**Document Status:** MVP Design Complete  
**Date:** 2026-07-10  
**Version:** 1.0
