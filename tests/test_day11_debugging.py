import os
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.app import MeetingNotesApp
from src.server import app as fastapi_app


def test_meeting_app_imports_and_initializes() -> None:
    app = MeetingNotesApp()
    assert app is not None
    assert app.detection_service is not None
    assert app.export_service is not None


def test_upload_endpoint_accepts_text_upload() -> None:
    client = TestClient(fastapi_app)

    with tempfile.NamedTemporaryFile("wb", suffix=".txt", delete=False) as handle:
        handle.write(b"Priya will review the migration plan by Friday.")
        temp_path = handle.name

    try:
        with open(temp_path, "rb") as handle:
            response = client.post(
                "/api/v1/upload",
                files={"file": ("sample.txt", handle, "text/plain")},
            )
        assert response.status_code == 200, response.text
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
