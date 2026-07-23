# src/server.py
"""FastAPI backend for AI Meeting Notes Manager.

Serves REST API endpoints for uploading documents, retrieving meetings,
and exporting markdown. Also serves static files from src/web/.
"""

from contextlib import asynccontextmanager
import os
import sys
import time
from typing import List

# Add the project root to PYTHONPATH so absolute imports work when running this file directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Use absolute imports now that the root is on the path
from src.database import initialize_database
from src.models.meeting_model import Attachment, Meeting
from src.persistence import load_meetings, save_meetings
from src.services.detection_service import DetectionService
from src.services.export_service import ExportService
from src.agents import MultiAgentOrchestrator
from backend.core.logging import app_logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize database tables when the FastAPI app starts."""
    initialize_database()
    yield


app = FastAPI(title="AI Meeting Notes Manager API", lifespan=lifespan)

# HTTP Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    app_logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - {duration_ms:.2f}ms"
    )
    return response

# CORS - allow configured origins or default to all origins
cors_origins_str = os.getenv("CORS_ORIGINS", "*")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency instances - singletons for the app lifetime
_detection_service = DetectionService()
_export_service = ExportService()

# Serve the static dashboard (src/web/index.html and assets)
static_path = os.path.join(os.path.dirname(__file__), "web")
app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

# Serve root index for the web UI when requested directly.
@app.get("/")
def root() -> FileResponse:
    return FileResponse(os.path.join(static_path, "index.html"))


# Helper to get current meetings list (database-backed persistence)
def get_meetings() -> List[Meeting]:
    return load_meetings()


def persist(meetings: List[Meeting]) -> None:
    save_meetings(meetings)


# -------------------- API ENDPOINTS --------------------

@app.get("/api/v1/meetings", response_model=List[dict])
def list_meetings():
    meetings = get_meetings()
    # Return a lightweight summary for each meeting
    return [
        {
            "id": m.id,
            "title": m.title,
            "created_at": m.created_at.isoformat(),
            "participants": m.participants,
            "message_count": len(m.messages),
        }
        for m in meetings
    ]


@app.get("/api/v1/meetings/{meeting_id}", response_model=dict)
def get_meeting(meeting_id: str):
    meetings = get_meetings()
    for m in meetings:
        if m.id == meeting_id:
            return m.to_dict()
    raise HTTPException(status_code=404, detail="Meeting not found")


@app.delete("/api/v1/meetings/{meeting_id}")
def delete_meeting(meeting_id: str):
    meetings = get_meetings()
    filtered = [m for m in meetings if m.id != meeting_id]
    if len(filtered) == len(meetings):
        raise HTTPException(status_code=404, detail="Meeting not found")
    persist(filtered)
    return {"detail": "Meeting deleted"}


@app.post("/api/v1/upload")
async def upload_document(file: UploadFile = File(...)):
    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".docx", ".pdf", ".txt", ".mp3", ".wav"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Save to a temporary location
    temp_dir = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as out:
        content = await file.read()
        out.write(content)

    # Extract raw text using the same helpers from src/app.py
    from src.app import (
        MeetingNotesApp,
    )

    app_instance = MeetingNotesApp()

    try:
        if ext == ".docx":
            raw_text = app_instance._extract_text_from_docx(temp_path)
        elif ext == ".pdf":
            raw_text = app_instance._extract_text_from_pdf(temp_path)
        elif ext == ".txt":
            raw_text = app_instance._extract_text_from_txt(temp_path)
        else:  # audio
            raw_text = app_instance._extract_text_from_audio(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")

    # Create a meeting and run the NLP pipeline
    title = f"Uploaded Document - {os.path.basename(file.filename)}"
    meeting = Meeting(title, ["Unknown"])
    meeting.add_attachment(
        Attachment(
            file_name=file.filename,
            file_path=temp_path,
            content_type=file.content_type,
            file_size_bytes=len(content),
        )
    )
    _detection_service.analyze_document(meeting, raw_text)

    # Persist
    meetings = get_meetings()
    meetings.append(meeting)
    persist(meetings)

    # Return summary info
    return {
        "id": meeting.id,
        "title": meeting.title,
        "summary": meeting.summary,
        "participants": meeting.participants,
        "action_items": [a.to_dict() for a in meeting.action_items],
        "decisions": [d.to_dict() for d in meeting.decisions],
    }


@app.get("/api/v1/meetings/{meeting_id}/export")
def export_meeting(meeting_id: str):
    meetings = get_meetings()
    for m in meetings:
        if m.id == meeting_id:
            try:
                path = _export_service.export_to_markdown(m)
                return FileResponse(path, media_type="text/markdown", filename=os.path.basename(path))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail="Meeting not found")


# Optional health check
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})


# ------------------------------------------------------------------
# Note: Running the server directly with `python -m uvicorn src.server:app`
# or `python src/server.py` (the latter will invoke uvicorn automatically).
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
