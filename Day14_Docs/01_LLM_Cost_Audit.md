# LLM Cost Audit

## 1. Current AI Architecture

The **AI Meeting Notes Manager** currently uses a **rule-based NLP pipeline** that operates entirely locally with zero external API calls. This means the current monthly AI cost is **$0.00**.

### Current Pipeline Components

| Component | Implementation | Cost |
| :--- | :--- | :--- |
| Text Extraction | python-docx, pdfplumber, built-in audio transcriber | $0 |
| Keyword Detection | Regex-based (keyword_detector.py) | $0 |
| NLP Pipeline | spaCy, NLTK, dateparser (offline) | $0 |
| Summarization | Rule-based sentence extraction | $0 |
| Action Item Extraction | Pattern matching + spaCy NER | $0 |
| Decision Detection | Keyword matching | $0 |
| Risk Detection | Keyword matching | $0 |
| RAG Pipeline | Local bag-of-words embedding (rag.py) | $0 |
| LLM Service | AISummaryService with fallback to rule-based | $0 |

### Cost Summary

| Metric | Value |
| :--- | :--- |
| Current monthly AI cost | **$0.00** |
| AI provider calls per month | 0 |
| Local computation cost | Negligible (CPU cycles) |
| External API dependency | None |

---

## 2. Future LLM Support Architecture

The codebase includes a provider abstraction layer (`backend/ai/providers.py`) that supports:

- **Anthropic Claude** (via `AnthropicProvider`)
- **OpenAI GPT** (configurable, prompt templates ready)
- **Google Gemini** (API key placeholder in env)

The `AISummaryService` already implements a fallback pattern:
1. Try external LLM provider
2. If unavailable, fall back to rule-based local summarizer

### Prompt Templates (Pre-built)

Located in `backend/ai/prompts/`:
- `summary_prompt.txt` - Meeting summarization prompt
- Additional prompt templates for action extraction and decision detection

---

## 3. Cost Projections with External LLM

### Assumptions

- 500 meetings/month
- Average transcript: 2,000 tokens input
- Average summary: 500 tokens output
- 50% cache hit rate after optimization

### Provider Pricing (as of 2026)

| Provider | Model | Input Price | Output Price | Monthly Cost (500 meetings) |
| :--- | :--- | :--- | :--- | :--- |
| OpenAI | GPT-4o-mini | $0.15/1M tokens | $0.60/1M tokens | **~$0.75** |
| Anthropic | Claude 3 Haiku | $0.25/1M tokens | $1.25/1M tokens | **~$1.50** |
| Google | Gemini 1.5 Flash | Free tier | Free tier | **$0.00** |
| Current | Rule-based | $0 | $0 | **$0.00** |

### Detailed Cost Calculation (OpenAI GPT-4o-mini)

```
Input tokens per meeting: 2,000
Output tokens per meeting: 500
Total input tokens: 500 × 2,000 = 1,000,000 tokens
Total output tokens: 500 × 500 = 250,000 tokens

Input cost: 1,000,000 / 1,000,000 × $0.15 = $0.15
Output cost: 250,000 / 1,000,000 × $0.60 = $0.15
Total: $0.30/month (without caching)
With 50% cache hit rate: ~$0.15/month
```

---

## 4. Context Window Considerations

| Model | Context Window | Strategy |
| :--- | :--- | :--- |
| GPT-4o-mini | 128K tokens | Truncate to first 8K tokens for summaries |
| Claude 3 Haiku | 48K tokens | Chunk transcripts > 40K tokens |
| Gemini 1.5 Flash | 1M tokens | No truncation needed for typical meetings |
| Rule-based (current) | Unlimited | No context limits |

### Recommendation

For transcripts under 10K tokens, use direct processing. For longer transcripts, implement:
1. **Chunking**: Split into segments of 4K tokens
2. **Hierarchical summarization**: Summarize chunks, then summarize summaries
3. **Sliding window**: Process overlapping windows for coherence

---

## 5. Cache Strategy

### Implementation Options

| Strategy | Description | Expected Savings |
| :--- | :--- | :--- |
| **Content hash cache** | Cache summaries by document hash | 40-60% |
| **Session cache** | Cache within same meeting session | 10-20% |
| **Similar document cache** | Match similar documents via embedding | 15-25% |

### Current Local Cache

The `DetectionService._is_duplicate_action`, `_is_duplicate_decision`, and `_is_duplicate_note` methods already prevent duplicate processing within a single meeting.

---

## 6. Prompt Optimization Opportunities

| Optimization | Current | Improved | Savings |
| :--- | :--- | :--- | :--- |
| System prompt length | ~200 tokens | ~100 tokens | 50% |
| Include only relevant context | Full transcript | Key sentences only | 60-80% |
| Few-shot examples | 3 examples | 1 example | 66% |
| Output format | Full paragraphs | Bullet points | 40% |

---

## 7. Batching Strategy

Instead of one API call per meeting, batch multiple meetings:

```
Current: 500 calls × 2,500 tokens = 1,250,000 tokens
Batched (10 per call): 50 calls × 25,000 tokens = 1,250,000 tokens
```

Batching does not reduce token usage but may reduce latency overhead. However, for the current rule-based system, batching is unnecessary.

---

## 8. Model Selection Recommendations

| Use Case | Recommended Model | Rationale |
| :--- | :--- | :--- |
| Summarization | Rule-based (current) | Free, fast, deterministic |
| Action extraction | Rule-based (current) | More reliable than LLMs for structured extraction |
| Complex reasoning | GPT-4o-mini (future) | Best cost/quality ratio |
| Long documents | Gemini 1.5 Flash (future) | 1M context window, free tier |
| Real-time processing | Rule-based (current) | Sub-millisecond latency |

---

## 9. Conclusion

**Current AI cost: $0.00/month** - The rule-based NLP pipeline delivers reliable meeting analysis with zero API expenditure. If external LLMs are enabled in the future, the estimated cost ranges from **$0.15 to $1.50 per month** for 500 meetings, well within a free-tier or low-budget operation.
