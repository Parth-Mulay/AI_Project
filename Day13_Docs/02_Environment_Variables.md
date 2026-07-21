# Environment Variables & Security Management

## Overview

All configurable settings, host bindings, feature flags, and API endpoint origins are decoupled from the codebase and externalized into environment variables. This ensures security compliance, multi-environment portability, and zero hardcoded credentials in version control.

---

## 1. Required Environment Variables

### Backend Configuration (Render / Server)

| Variable | Type | Default / Recommended | Description | Secret? |
| :--- | :--- | :--- | :--- | :--- |
| `PORT` | Integer | `8000` | Port assigned by Render runtime | No |
| `HOST` | String | `0.0.0.0` | Bind host address for uvicorn server | No |
| `ENVIRONMENT` | String | `production` | Active runtime environment (`development`, `staging`, `production`) | No |
| `LOG_LEVEL` | String | `INFO` | Logging verbosity level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | No |
| `CORS_ORIGINS` | String | `https://ai-meeting-notes-manager.vercel.app` | Comma-separated list of allowed web frontend origins | No |
| `DATABASE_URL` | String | `sqlite:///./meeting_notes.db` | Connection string for database persistence | No |
| `OPENAI_API_KEY` | String | *(Optional)* | Key for optional external LLM summarization fallback | **YES** |
| `GEMINI_API_KEY` | String | *(Optional)* | Key for optional Google Gemini API fallback | **YES** |

### Frontend Configuration (Vercel / Vite)

| Variable | Type | Default / Recommended | Description | Secret? |
| :--- | :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | String | `https://ai-meeting-notes-backend.onrender.com` | Base URL pointing React frontend to FastAPI backend | No |

---

## 2. Configuration Templates

### Backend Root Template (`.env.example`)

```ini
# Server Settings
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO

# Security & CORS Whitelist
CORS_ORIGINS=https://ai-meeting-notes-manager.vercel.app,http://localhost:5173

# Persistence
DATABASE_URL=sqlite:///./meeting_notes.db

# Optional AI Provider Secrets
# OPENAI_API_KEY=sk-proj-placeholder
# GEMINI_API_KEY=AIzaSyPlaceholder
```

### Frontend Template (`frontend/.env.example`)

```ini
# Backend API Base URL
VITE_API_BASE_URL=https://ai-meeting-notes-backend.onrender.com
```

---

## 3. Platform Dashboard Configuration

### Setting Environment Variables on Render
1. Open the [Render Dashboard](https://dashboard.render.com).
2. Select the **`ai-meeting-notes-backend`** Web Service.
3. Click **Environment** in the left sidebar menu.
4. Add key-value pairs for `ENVIRONMENT`, `LOG_LEVEL`, `CORS_ORIGINS`, and `DATABASE_URL`.
5. Click **Save Changes**. Render will automatically initiate a new zero-downtime deployment.

### Setting Environment Variables on Vercel
1. Open the [Vercel Dashboard](https://vercel.com).
2. Select the **`ai-meeting-notes-manager`** project.
3. Go to **Settings** > **Environment Variables**.
4. Add `VITE_API_BASE_URL` with value `https://ai-meeting-notes-backend.onrender.com`.
5. Select environments (**Production**, **Preview**, **Development**).
6. Click **Save** and trigger a redeployment.

---

## 4. Security Verification & Secret Audit

A static analysis audit was performed across the codebase to ensure no credentials or tokens are committed:
- **`.gitignore`** excludes `.env`, `*.db`, `venv/`, `node_modules/`, `logs/`, and temporary uploaded files.
- All service modules read settings dynamically from `os.getenv()` or `src.config`.
- Rule-based NLP operates strictly locally without requiring external API keys.
- **Audit Status**: ✅ **100% Verified Clean - Zero Secrets Committed**.
