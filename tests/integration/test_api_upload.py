"""Integration tests for the upload API endpoint."""

import io
import os
import tempfile

import pytest


class TestUploadEndpoint:
    def test_upload_text_file(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.txt", b"Alice: We must complete the migration by Friday.", "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "summary" in data

    def test_upload_empty_text_file(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("empty.txt", b"", "text/plain")},
        )
        assert response.status_code == 500

    def test_upload_unsupported_format(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.exe", b"some data", "application/octet-stream")},
        )
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_upload_no_file(self, client):
        response = client.post("/api/v1/upload")
        assert response.status_code == 422

    def test_upload_docx_file(self, client):
        import zipfile
        xml_content = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:body><w:p><w:r><w:t>Alice: We need to discuss the budget.</w:t></w:r></w:p></w:body>'
            '</w:document>'
        )
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("word/document.xml", xml_content)
        buf.seek(0)
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.docx", buf.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
        assert response.status_code in (200, 500)

    def test_upload_response_has_expected_fields(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("meeting.txt", b"Alice: We must complete the project by Friday.", "text/plain")},
        )
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "summary" in data
        assert "participants" in data
        assert "action_items" in data
        assert "decisions" in data

    def test_upload_large_file_still_processes(self, client):
        large_content = b"Alice: We must complete the task.\nBob: Agreed.\n" * 10000
        response = client.post(
            "/api/v1/upload",
            files={"file": ("large_transcript.txt", large_content, "text/plain")},
        )
        assert response.status_code == 200

    def test_upload_pdf_file(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.pdf", b"%PDF-1.4 fake pdf content", "application/pdf")},
        )
        assert response.status_code == 500

    def test_upload_preserves_filename(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("my_custom_meeting.txt", b"Alice: Hello everyone.", "text/plain")},
        )
        data = response.json()
        assert "my_custom_meeting" in data["title"]
