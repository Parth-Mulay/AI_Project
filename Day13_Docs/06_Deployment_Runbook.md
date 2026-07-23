# Deployment Runbook

## Overview

This runbook covers the complete deployment lifecycle for the **AI Meeting Notes Manager**, including environment setup, deployment steps, rollback procedures, monitoring, and troubleshooting. Designed for operators with basic DevOps knowledge.

---

## 1. Architecture Overview

```
Users ──> Vercel CDN (Frontend) ──> Render (Backend API) ──> SQLite (Database)
              │                            │
              │                      UptimeRobot (Monitoring)
              │                            │
         GitHub Actions (CI/CD)       Render Logs (Observability)
```

| Component | Provider | URL |
| :--- | :--- | :--- |
| Frontend (React SPA) | Vercel Free | `https://ai-meeting-notes-manager.vercel.app` |
| Backend (FastAPI) | Render Free | `https://ai-meeting-notes-backend.onrender.com` |
| Database | SQLite | Embedded in Render instance |
| CI/CD | GitHub Actions | `.github/workflows/ci.yml` |
| Monitoring | UptimeRobot | `https://ai-meeting-notes-backend.onrender.com/health` |

---

## 2. Prerequisites

### Required Accounts

- [GitHub](https://github.com) account with repository access
- [Vercel](https://vercel.com) account (free tier)
- [Render](https://render.com) account (free tier)
- [UptimeRobot](https://uptimerobot.com) account (free tier, optional)

### Required Tools (Local)

- Git
- Python 3.12+
- Node.js 20+
- npm or yarn

---

## 3. Initial Environment Setup

### 3.1 Repository Setup

```bash
git clone https://github.com/Parth-Mulay/AI_Project.git
cd AI-Meeting-Notes-Manager
```

### 3.2 Backend Local Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env if needed
```

### 3.3 Frontend Local Setup

```bash
cd frontend
npm install
cp .env.example .env
cd ..
```

---

## 4. Deployment Steps

### 4.1 Deploy Backend to Render

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Configure:
   - **Name**: `ai-meeting-notes-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.server:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Add environment variables:
   - `ENVIRONMENT`: `production`
   - `LOG_LEVEL`: `INFO`
   - `CORS_ORIGINS`: `https://ai-meeting-notes-manager.vercel.app,http://localhost:5173`
   - `DATABASE_URL`: `sqlite:///./meeting_notes.db`
6. Click **Create Web Service**.
7. Wait for build and deploy to complete.
8. Verify: Visit `https://ai-meeting-notes-backend.onrender.com/health`

### 4.2 Deploy Backend via render.yaml (Blueprint)

If using Render Blueprint:

1. Push `render.yaml` to the repository root.
2. In Render Dashboard, click **New +** > **Blueprint**.
3. Connect the repository.
4. Render automatically reads `render.yaml` and provisions the service.
5. Verify deployment completes.

### 4.3 Deploy Frontend to Vercel

1. Log in to [Vercel Dashboard](https://vercel.com).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add environment variable:
   - `VITE_API_BASE_URL`: `https://ai-meeting-notes-backend.onrender.com`
6. Click **Deploy**.
7. Wait for deployment.
8. Verify: Visit the generated Vercel URL.

### 4.4 Configure UptimeRobot Monitoring

1. Log in to [UptimeRobot](https://uptimerobot.com).
2. Click **Add New Monitor**.
3. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: `AI Meeting Notes Backend`
   - **URL**: `https://ai-meeting-notes-backend.onrender.com/health`
   - **Interval**: 5 minutes
4. Set alert contacts (email).
5. Click **Create Monitor**.

---

## 5. Environment Variables Reference

| Variable | Required | Description |
| :--- | :--- | :--- |
| `PORT` | No | Server port (Render sets automatically) |
| `HOST` | No | Bind address (default: `0.0.0.0`) |
| `ENVIRONMENT` | No | `development`, `staging`, or `production` |
| `LOG_LEVEL` | No | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `CORS_ORIGINS` | Yes | Comma-separated allowed origins |
| `DATABASE_URL` | No | Database connection string |
| `VITE_API_BASE_URL` | Yes | Backend API URL for frontend |

---

## 6. CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/ci.yml` runs on every push and pull request:

1. **Checkout** repository
2. **Setup Python 3.12** with pip cache
3. **Install backend dependencies** from `requirements.txt`
4. **Run unit tests** (`pytest tests/unit/ -v`)
5. **Setup Node.js 20** with npm cache
6. **Install frontend dependencies**
7. **Verify production build** (`npm run build`)

The pipeline fails immediately if any step fails.

---

## 7. Rollback Procedures

### Git Rollback

```bash
git fetch origin main
git log -n 5 --oneline
git revert <bad_commit_hash>
git push origin main
```

### Render Rollback

1. Go to Render Dashboard > ai-meeting-notes-backend > Events.
2. Find the last successful deploy.
3. Click **...** > **Redeploy this build**.

### Vercel Rollback

1. Go to Vercel Dashboard > ai-meeting-notes-manager > Deployments.
2. Find the last successful production deployment.
3. Click **...** > **Promote to Production**.

---

## 8. Deployment Verification Checklist

After any deployment:

- [ ] Backend health endpoint returns `{"status": "ok"}`
- [ ] Frontend loads without errors
- [ ] API endpoints respond correctly
- [ ] File upload works for .txt, .docx, .pdf
- [ ] Meeting summary generates properly
- [ ] Action items are extracted
- [ ] Export to Markdown works
- [ ] UptimeRobot monitor shows green

---

## 9. Monitoring & Troubleshooting

### Logs

- **Render**: Dashboard > ai-meeting-notes-backend > Logs
- **Local**: `logs/backend.log`

### Common Issues

| Issue | Symptom | Solution |
| :--- | :--- | :--- |
| Cold Start | Slow first request | UptimeRobot keep-alive ping every 5 min |
| CORS Error | Frontend can't reach backend | Verify `CORS_ORIGINS` includes frontend URL |
| 500 Error | Internal server error | Check Render logs for traceback |
| Database Reset | Data lost after redeploy | SQLite is ephemeral on Render free tier |
| Build Failure | CI pipeline fails | Check GitHub Actions logs |

### Health Check Endpoint

```bash
curl https://ai-meeting-notes-backend.onrender.com/health
# Response: {"status": "ok"}
```

---

## 10. Maintenance Tasks

### Weekly

- Review Render logs for errors
- Check UptimeRobot monthly SLA report
- Verify CI pipeline status

### Monthly

- Review cost report (should remain $0)
- Clean up old meeting exports
- Verify environment variables are current

### Per-Release

- Run full test suite locally before pushing
- Verify staging deployment before production
- Update documentation for any configuration changes
