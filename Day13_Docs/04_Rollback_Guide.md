# Incident Response & Rollback Strategy

## Overview

In the event of a deployment failure, broken release, database schema incompatibility, or critical regression, a rapid rollback procedure minimizes downtime and service disruption. This document details the step-by-step rollback procedures for both Git source control and cloud platform deployments (Render & Vercel).

---

## 1. Rollback Scenarios & Matrix

| Scenario | Severity | Recommended Rollback Mechanism | Recovery Time Objective (RTO) |
| :--- | :--- | :--- | :--- |
| **Failed Production Deployment** | High | Instant Render / Vercel Dashboard Rollback | < 2 minutes |
| **Faulty Code / Logic Bug** | Medium | Git Revert commit & Push to `main` | < 5 minutes |
| **Environment Variable Corruption** | Low | Restore previous env vars in Dashboard | < 1 minute |

---

## 2. Git-Based Rollback Procedures

### Strategy A: Safe Revert (`git revert`) - Recommended
`git revert` creates a new commit that explicitly undoes changes from a problematic commit without rewriting repository history.

```bash
# 1. Fetch latest commits from remote
git fetch origin main

# 2. Identify the commit hash to undo
git log -n 5 --oneline

# 3. Create revert commit (e.g. reverting commit 327d244)
git revert 327d244bc -m "revert: rollback broken deployment feature"

# 4. Push revert commit to main branch
git push origin main
```
*Result*: GitHub Actions CI will build and verify the revert commit, and Render/Vercel auto-deploy will deploy the restored state automatically.

### Strategy B: Hard Reset (`git reset`) - Use with Caution
If a broken commit was pushed to `main` and needs to be completely removed from remote history:

```bash
# 1. Reset local main branch to known good commit
git reset --hard <good_commit_hash>

# 2. Force push to remote (Requires repository admin privileges)
git push origin main --force
```

---

## 3. Render Dashboard Instant Rollback (Backend)

Render stores previous successful builds and enables instant redeployment of prior build artifacts without waiting for Git CI re-runs.

### Steps to Roll Back on Render:
1. Log into the [Render Dashboard](https://dashboard.render.com).
2. Click on the **`ai-meeting-notes-backend`** Web Service.
3. Navigate to **Events** in the sidebar menu.
4. Locate the last **"Deploy succeeded"** event prior to the broken release.
5. Click the three dots (`...`) menu next to that build event.
6. Select **Redeploy this build**.
7. Confirm the action. Render will immediately swap active traffic to the previous healthy container image.

---

## 4. Vercel Dashboard Instant Rollback (Frontend)

Vercel maintains immutable deployment previews for every git commit.

### Steps to Roll Back on Vercel:
1. Log into the [Vercel Dashboard](https://vercel.com).
2. Open the **`ai-meeting-notes-manager`** project.
3. Select the **Deployments** tab.
4. Locate the last successful production deployment.
5. Click the three dots (`...`) icon next to the healthy deployment.
6. Select **Promote to Production**.
7. Vercel will route global CDN traffic to the selected build instantly (0 seconds downtime).

---

## 5. Post-Rollback Recovery Verification Checklist

After initiating a rollback, perform the following verification steps:

- [ ] **Health Endpoint Check**: Verify `GET https://ai-meeting-notes-backend.onrender.com/health` returns status `200 OK`.
- [ ] **API Functional Check**: Verify `GET /api/v1/meetings` returns JSON list without HTTP 500 errors.
- [ ] **Frontend Inspection**: Open the Vercel live URL and verify dashboard components render correctly.
- [ ] **UptimeRobot Alert Status**: Confirm UptimeRobot monitor reports status `Up (200)`.
- [ ] **Post-Mortem**: Document root cause, error logs, and corrective action items in `Day13_Docs/`.
