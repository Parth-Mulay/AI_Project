# Monthly Operating Cost Estimation

## Overview

As an academic capstone project, the **AI Meeting Notes Manager** architecture is engineered strictly to operate within **$0.00/month (100% Free Tier)** cloud infrastructure while maintaining high availability, automated CI/CD pipelines, structured logging, and uptime monitoring.

---

## 1. Current Infrastructure Cost Breakdown

| Component | Provider & Plan | Allocated Free Usage Allowance | Estimated Monthly Usage | Total Monthly Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend Hosting** | Vercel Free Tier | 100 GB Bandwidth, Unlimited Builds | ~2.5 GB Bandwidth | **$0.00** |
| **Backend Hosting** | Render Free Tier | 750 free instance hours/month | 744 hours (1 Web Service) | **$0.00** |
| **Database Storage** | SQLite (Embedded File) / Render Free Postgres | 1 GB Free Disk Storage | ~50 MB DB Storage | **$0.00** |
| **CI/CD Automation** | GitHub Actions Free | 2,000 build minutes/month | ~120 build minutes | **$0.00** |
| **Uptime Monitoring** | UptimeRobot Free Tier | 50 Monitors, 5-minute intervals | 1 Monitor (Health Check) | **$0.00** |
| **Log Management** | Render Built-in Logs | Infinite stdout stream & dashboard | Daily streaming logs | **$0.00** |
| **LLM Inference Engine** | Local Rule-Based NLP Pipeline | Unlimited execution (Local CPU) | ~1,000 document extractions | **$0.00** |
| **TOTAL ESTIMATED MONTHLY OPERATING COST** | | | | **$0.00 / month** |

---

## 2. Platform Free Tier Limits & Resource Safeguards

### A. Vercel Free Tier
- **Limits**: 100 GB bandwidth / month, 6,000 build minutes / month.
- **Safeguard**: Production build artifact size is optimized to **~200 KB gzipped**, consuming negligible bandwidth even under continuous evaluation.

### B. Render Free Tier
- **Limits**: 512 MB RAM, 0.1 CPU core, 750 free instance hours per month, sleep after 15 minutes of inactivity.
- **Safeguard**: UptimeRobot 5-minute health check keep-alive prevents cold starts while keeping total runtime within the 750-hour monthly allowance for a single web service.

### C. GitHub Actions Free
- **Limits**: 2,000 free runner minutes per month for public/private repositories.
- **Safeguard**: Parallel jobs for `backend-test` (Python) and `frontend-build` (Node.js) complete in under **45 seconds** per workflow run.

---

## 3. Future Cost Projections & Optimization Strategies (If External AI Added)

If external commercial LLM APIs (e.g., OpenAI GPT-4o, Google Gemini API, Anthropic Claude) are enabled in future phases, the following cost management strategies apply:

| Service | Estimated Usage | Commercial Unit Price | Projected Monthly Cost | Optimization Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI GPT-4o-mini** | 500 meeting summaries (2k tokens/req) | $0.15 / 1M input tokens | **~$0.15 - $0.30** | Enable local rule-based NLP fallback as primary engine; use LLM only when requested. |
| **Google Gemini 1.5 Flash** | 500 meeting summaries | Free Tier (15 RPM / 1M TPM) | **$0.00 (Free Tier)** | Utilize Gemini 1.5 Flash free tier API keys for capstone demos. |
| **Render Paid Starter** | Always-on, no cold starts | $7.00 / month | **$7.00** | Optional upgrade if 512 MB RAM limit is exceeded under heavy concurrent traffic. |

### Cost Reduction Recommendations:
1. **Rule-Based Engine Priority**: Continue leveraging the optimized local standard-library NLP pipeline (`src/services/detection_service.py`) for zero API billings.
2. **Caching Summaries**: Cache generated summaries and extracted action items in SQLite so duplicate requests bypass LLM API calls.
3. **Chunking & Token Truncation**: Limit prompt context size to the first 4,000 tokens of meeting transcripts.
