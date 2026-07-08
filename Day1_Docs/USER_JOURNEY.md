# USER JOURNEY

Stages: Discover Product → Register → Login → Dashboard → Create Meeting → Upload Notes → Generate AI Summary → Review → Edit → Save → Search → Export → Logout

## Journey Table (Condensed)

| Stage | User Goal | User Actions | System Actions | Pain Points | Opportunities |
|---|---|---|---|---|---|
| Discover | Evaluate product fit | Visit site, watch demo | Landing, demo, feature list | Skepticism about AI | Emphasize fallback & compliance |
| Register | Create account | Signup (email/SSO) | Create account, onboarding | Friction for teams | Offer SSO/trial |
| Login | Secure access | Login, MFA | Authenticate, session | Password fatigue | SSO/MFA options |
| Dashboard | View recent meetings | Open dashboard | Show widgets | Info overload | Smart prioritization |
| Create Meeting | Add metadata | Create meeting, link calendar | Auto-fill metadata | Manual entry | Calendar sync |
| Upload Notes | Ingest content | Upload/paste/record | Store file, transcribe | File compatibility | Multi-format support |
| Generate Summary | Get AI summary | Click summarize | Call Anthropic; fallback if needed | AI latency | Show progress & explainability |
| Review/Edit | Validate content | Accept/edit items | Track edits, versioning | Incorrect extractions | Show provenance excerpts |
| Save/Search | Persist & find | Save meeting, search | Store, index, semantic search | False positives | Improve ranking |
| Export | Share summaries | Export/PDF/Push to tools | Generate export | Formatting mismatch | Provide templates |
| Logout | End session | Logout | Clear session | — | End-of-session survey |

## ASCII Flow Diagram

+-------+   +-------------+   +-----------+   +------------+   +-----------+
| User  |-->| Landing     |-->| Register  |-->| Dashboard  |-->| Create    |
+-------+   +-------------+   +-----------+   +------------+   +-----------+
                                                             |
                                                             v
                                                       +-----------+
                                                       | Upload    |
                                                       | Notes     |
                                                       +-----------+
                                                             |
                                                             v
                                                      +--------------+
                                                      | Processing   |
                                                      | (Anthropic)  |
                                                      |  or Fallback |
                                                      +--------------+
                                                             |
                                                             v
                                                  +----------------------+
                                                  | Summary + Extractors |
                                                  +----------------------+
                                                             |
                                                  +----------+----------+
                                                  | Review/Edit/Assign  |
                                                  +---------------------+
                                                             |
                                                             v
                                                       +-----------+
                                                       | Save/Export|
                                                       +-----------+

## Pain Points & Opportunities
- Pain: AI latency/accuracy, privacy concerns, integration friction.
- Opportunities: Explainability UI, fallback guarantee, admin controls, scheduling of follow-ups.

(End of User Journey)
