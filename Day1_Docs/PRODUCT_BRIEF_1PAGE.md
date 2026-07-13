# Product Brief (1-page) — AI Meeting Notes Manager (AI + Deterministic Fallback)

## 1) One-sentence problem statement
Teams waste time and miss accountability because meeting outcomes (decisions + action items) are scattered and inconsistently documented across tools.

## 2) Who it’s for + core value proposition
**For** product managers, engineering leads, and consultants who run frequent collaborative meetings, **who need** a reliable, fast way to turn discussions into decisions and next steps, **our product** generates structured action items (with owners + due dates), decision logs (with context/excerpts), and searchable summaries **unlike** existing note tools that either (a) don’t extract actions/decisions well, or (b) rely entirely on generative AI without predictable fallback.

## 3) Ideation snapshot (10 variations → 3 shortlist)
### 10 variations (high level)
1. Meeting-to-Jira automator (actions + owners → Jira tickets)
2. Decision log generator (who decided what, when, and why)
3. Executive recap mode (1-page summary for leaders)
4. Classroom mode (lecture meeting summaries + study actions)
5. Remote incident postmortem assistant (risks/blockers + follow-ups)
6. Compliance/audit meeting vault (provenance + retention controls)
7. “Owner-first” action board (actions created immediately during meeting)
8. Team meeting archive with semantic + keyword search
9. Multichannel recap (Teams/Slack/Docs ingest and unify)
10. Consultant packager (client-ready meeting deliverables)

### Shortlist (3) with reasons
- **#1 Meeting-to-Jira automator**: direct workflow impact; measurable reduction in follow-up churn.
- **#6 Compliance/audit meeting vault**: differentiates on trust—includes retention + audit trail, not just summaries.
- **#8 Team meeting archive with semantic + keyword search**: reduces “what did we decide last time?” time-to-retrieval.

Chosen direction for this brief: **Hybrid meeting assistant** (actions/decisions + searchable archive + auditability).

## 4) User personas (3)
### Persona A — Emma Park (Product Manager)
- **Goals:** Convert meeting outcomes into tasks and keep teams aligned.
- **Frustrations:** Action ownership is unclear; summaries require manual rework.
- **Context:** Uses Slack/Jira and runs weekly planning + cross-functional syncs.

### Persona B — Ajay Patel (Head of Engineering)
- **Goals:** Maintain a decision record and accountability across sprints.
- **Frustrations:** Decisions get lost; rework repeats exceptions.
- **Context:** Leads architecture reviews/sprint planning; cares about auditability.

### Persona C — Sofia Alvarez (Freelance UX Consultant)
- **Goals:** Produce polished client-ready recaps quickly.
- **Frustrations:** Context switching across clients; manual formatting wastes time.
- **Context:** Communicates via Slack/Drive; deliverables must be consistent.

## 5) Competitor scan (what we must beat)
Competitors reviewed: Otter.ai, Fireflies.ai, Fathom, Notion AI, Microsoft Copilot, Google Gemini.
- Many tools excel at **transcription/highlights** but are weaker on **structured action + decision provenance**.
- Platform-native copilots can have **licensing complexity/vendor lock-in** and may lack deterministic behavior when AI is unavailable.

(Verified facts from internal competitor matrix in Day1_Docs/COMPETITOR_ANALYSIS.md)
- **Fallback/non-AI reliability** is specifically present in our approach (hybrid AI + deterministic extraction).
- **Structured action/decision extraction** is a core differentiator in our requirements.

## 6) MVP scope vs later phases
### MVP (build first)
- **Dashboard**: recent meetings + pending actions
- **Meeting CRUD**: create meetings and store transcripts/notes
- **AI summary trigger + deterministic fallback** (hybrid summarization)
- **Action items + decisions extraction** (owners + due dates where possible)
- **Search**: full-text search across meetings (keyword + basic semantic where available)
- **Export**: Markdown/PDF/DOCX
- **Basic integration**: Slack posting + Jira/Asana push (as connectors)
- **Team settings & retention + audit trail** (core governance)

### OUT of scope (explicitly for this MVP)
- Native mobile apps
- On-prem deployments
- Advanced analytics/BI dashboards
- Video conferencing UI and deep playback features
- SOC2 certification at launch (but design for later)
- Real-time transcription streaming (focus is end-to-end after upload/text input)

## 7) Success metrics we will optimize
- **Processing time:** end-to-end summary ≤15s for typical docs
- **Search performance:** top-20 results ≤2s
- **Fallback success rate:** ≥95% when AI is unavailable
- **User satisfaction:** CSAT ≥85%; NPS ≥40
- **Business:** trial→paid 8–12%; paid retention ≥70% at 6 months

## 8) MVP product experience (what the user sees)
1. Upload meeting content / add transcript
2. Instant “meeting insights” panel: summary, decisions, action items
3. Review/edit structured outputs (explainable excerpts)
4. Export + push actions to tools (Jira/Slack)
5. Search the archive and track accountability over time

---
**Status:** ready for implementation as the MVP product brief.

