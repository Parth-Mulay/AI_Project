# Environment Management Strategy

## Overview

The **AI Meeting Notes Manager** operates across three distinct environment tiers: **Development**, **Staging**, and **Production**. This document defines the purpose, configuration, deployment workflow, and technical differences between each environment to ensure stable releases and zero-downtime operations.

---

## 1. Environment Specifications

### A. Development (`development`)
- **Purpose**: Active local feature development, rapid iteration, debugging, and unit testing.
- **Hosting**: Local developer machine.
- **Frontend**: Vite dev server (`http://localhost:5173`) with Hot Module Replacement (HMR).
- **Backend**: FastAPI running locally via `uvicorn src.server:app --reload` (`http://localhost:8000`).
- **Database**: Ephemeral local SQLite database (`meeting_notes.db` or memory).
- **Logging Level**: `DEBUG` (verbose console output and file handler).
- **CORS**: Unrestricted (`*` or `http://localhost:5173`).

### B. Staging (`staging`)
- **Purpose**: Pre-production integration testing, automated PR verification, and UAT validation.
- **Hosting**: GitHub Actions CI container & Render Staging Web Service (`ai-meeting-notes-staging.onrender.com`).
- **Frontend**: Vercel Preview Deployments automatically generated per Pull Request.
- **Backend**: Render Free Instance running production build against staging database.
- **Database**: Isolated SQLite storage instance or dedicated PostgreSQL staging instance.
- **Logging Level**: `INFO`.
- **CORS**: Restricted to Vercel preview domain pattern (`https://ai-meeting-notes-*.vercel.app`).

### C. Production (`production`)
- **Purpose**: Live environment serving end-users and capstone evaluators.
- **Hosting**: 
  - **Frontend**: Vercel Global CDN (`https://ai-meeting-notes-manager.vercel.app`).
  - **Backend**: Render Free Web Service (`https://ai-meeting-notes-backend.onrender.com`).
- **Database**: Persistent SQLite storage or free tier PostgreSQL.
- **Logging Level**: `INFO` / `WARNING` (structured JSON-style log format).
- **CORS**: Strict whitelist limited to Vercel production domain.
- **SSL/TLS**: Enforced HTTPS for all API and web requests via Vercel & Render automated Let's Encrypt certificates.

---

## 2. Environment Comparison Matrix

| Feature / Aspect | Development | Staging | Production |
| :--- | :--- | :--- | :--- |
| **API URL** | `http://localhost:8000` | `https://ai-meeting-notes-staging.onrender.com` | `https://ai-meeting-notes-backend.onrender.com` |
| **Frontend Host** | `localhost:5173` | Vercel PR Preview | Vercel Main Domain |
| **Trigger** | Local `npm run dev` / `uvicorn` | Pull Request / `develop` branch push | Push to `main` branch |
| **Database** | Local `meeting_notes.db` | Staging SQLite | Production SQLite |
| **Log Level** | `DEBUG` | `INFO` | `INFO` |
| **Auto-Deploy** | Manual | Automated via GitHub Actions & Vercel PR | Automated on `main` push |
| **Health Checks** | Manual endpoint check | Automated CI health test | UptimeRobot (5-min interval) |

---

## 3. Deployment Workflow across Environments

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Development   │ ────> │     Staging     │ ────> │   Production    │
│  (Local Branch) │       │ (PR / Preview)  │       │ (Main Branch)   │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
   Local Pytest &            GitHub Actions &          Render Web Service &
   Vite Dev Server          Vercel Preview Build        Vercel Production CDN
```

1. **Development Phase**: Developers build features on feature branches, running `python -m pytest` and `npm run dev` locally.
2. **Staging Phase**: Pull Requests trigger `.github/workflows/ci.yml`. Tests run automatically, and Vercel builds a preview link for visual QA.
3. **Production Release**: Merging to `main` triggers Render auto-deploy for FastAPI backend and Vercel production deployment for React frontend.
