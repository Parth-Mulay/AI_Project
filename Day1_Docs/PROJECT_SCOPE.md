# PROJECT SCOPE

## Project Scope Statement
Deliver a cloud-native SaaS MVP with:
- User authentication and team management
- Meeting CRUD and attachments
- AI-powered summarization (Anthropic) and deterministic fallback
- Action & decision extraction and follow-up tracking
- Searchable meeting history with tagging and filtering
- Integrations: calendar (Google/Outlook), Zoom/Teams, Slack, Jira/Notion export
- Admin features: retention policies, role-based access, audit logs

## In Scope (MVP)
- Core auth (email/SSO), dashboard, meeting upload, AI summary + fallback, assign actions, search, PDF/DOCX export, calendar and Slack integrations, basic admin features, billing via Stripe.

## Out of Scope (Initial)
- Native mobile apps
- On-prem deployments
- Advanced analytics & BI dashboards
- Video conferencing UI
- SOC2 certification at launch (plan for later)

## Future Enhancements
- Mobile apps (iOS/Android)
- On-prem/VPC deployments
- Multi-language summarization
- Deeper PM tool integrations
- Video summarization & sentiment analysis

## Project Boundaries
- No indefinite storage of raw audio without retention policies.
- Generative AI usage depends on Anthropic; logs and provenance will be stored.

## Dependencies
- Anthropic API
- OAuth providers (Google, Microsoft)
- Third-party APIs (Zoom, Slack, Jira)
- Cloud provider (AWS/Azure/GCP) for storage and search

## Assumptions
- Anthropic SLA acceptable for production; fallback acceptable for continuity.

## Success Definition
- MVP with AI + fallback deployed; pilot with 50 users and validated time savings.

(End of Project Scope)
