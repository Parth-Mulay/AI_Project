# Day 10 AI Architecture Notes

## What changed
- Added a provider abstraction for AI backends in backend/ai/providers.py.
- Added reusable prompt templates under backend/ai/prompts/.
- Added a lightweight local RAG pipeline in backend/ai/rag.py.
- Added basic guardrails in backend/ai/guardrails.py and a simple cost estimator in backend/ai/cost_estimator.py.
- Wired the existing summary flow to use the AI service when available, while preserving the rule-based summarizer as the fallback.

## Notes
- The application still relies on deterministic meeting analysis first.
- AI is optional and degrades gracefully when no provider key is configured.
- The current implementation is intentionally lightweight and production-safe, suitable for an MVP.
