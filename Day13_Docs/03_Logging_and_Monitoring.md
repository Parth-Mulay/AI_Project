# Logging & Monitoring Architecture

## Overview

Observability is critical for identifying runtime errors, tracking response latency, and verifying application availability. This document outlines the structured logging mechanism, request tracing, health endpoints, and free-tier automated uptime monitoring for the **AI Meeting Notes Manager**.

---

## 1. Logging Strategy

### Architecture
The backend employs a dual-handler logging architecture configured in `backend/core/logging.py` and integrated into FastAPI in `src/server.py`:
1. **Console Handler (`StreamHandler`)**: Emits structured log logs to standard stdout/stderr, which are automatically captured by Render's built-in log aggregation system.
2. **Rotating File Handler (`RotatingFileHandler`)**: Writes log records to `logs/backend.log` (5MB max size, 5 backup rotations) for local development and file-based inspection.

### Log Format
```
YYYY-MM-DD HH:MM:SS | ai_meeting_notes | <module> | <function> | <LEVEL> | <message>
```

Example output:
```
2026-07-21 09:45:12 | ai_meeting_notes | server | log_requests | INFO | GET /api/v1/meetings - Status: 200 - 4.12ms
2026-07-21 09:46:01 | ai_meeting_notes | detection_service | analyze_document | INFO | Document processed successfully: 12 action items extracted
```

### Request Tracing Middleware
FastAPI HTTP request middleware in `src/server.py` logs all inbound requests, returning status codes and timing metrics:
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    app_logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - {duration_ms:.2f}ms"
    )
    return response
```

---

## 2. Accessing Render Built-in Logs

Render captures standard output and standard error streams automatically from the uvicorn process.

### How to View Live Logs on Render:
1. Navigate to the [Render Dashboard](https://dashboard.render.com).
2. Click on the **`ai-meeting-notes-backend`** Web Service.
3. Select **Logs** from the left navigation panel.
4. Filter by keyword (e.g., `ERROR`, `/api/v1/upload`, `health`) or inspect live streaming logs.

---

## 3. Health Endpoint Specification

The backend exposes an unauthenticated health check endpoint designed for automated monitoring tools and load balancers:

- **Endpoint**: `GET /health`
- **Response Status**: `200 OK`
- **Content Type**: `application/json`
- **Payload**:
  ```json
  {
    "status": "ok"
  }
  ```

---

## 4. Uptime Monitoring with UptimeRobot (Free Tier)

Render Free instances automatically enter a sleep mode after 15 minutes of inactivity. **UptimeRobot Free Tier** is configured to ping the health endpoint every 5 minutes, keeping the instance warm and alerting maintainers if an outage occurs.

### Setup Instructions for UptimeRobot:
1. Create a free account at [UptimeRobot.com](https://uptimerobot.com).
2. Click **Add New Monitor**.
3. Configure settings:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: `AI Meeting Notes Backend`
   - **URL (or IP)**: `https://ai-meeting-notes-backend.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
4. Add alert contacts (Email / Slack).
5. Click **Create Monitor**.

### Benefits:
- Maintains backend warm status, reducing cold-start latency for web app users.
- Sends instant email alerts if the service is unreachable.
- Calculates 30-day availability SLAs (Target: >99.5%).
