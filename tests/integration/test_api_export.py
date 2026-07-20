"""Integration tests for the export API endpoint."""

import pytest


class TestExportEndpoint:
    def test_export_existing_meeting(self, client):
        response = client.get("/api/v1/meetings")
        meetings = response.json()
        if not meetings:
            pytest.skip("No meetings available to export")
        meeting_id = meetings[0]["id"]
        response = client.get(f"/api/v1/meetings/{meeting_id}/export")
        assert response.status_code == 200
        assert "text/markdown" in response.headers["content-type"]

    def test_export_content_contains_title(self, client):
        response = client.get("/api/v1/meetings")
        meetings = response.json()
        if not meetings:
            pytest.skip("No meetings available")
        meeting_id = meetings[0]["id"]
        response = client.get(f"/api/v1/meetings/{meeting_id}/export")
        content = response.text
        assert "# " in content

    def test_export_nonexistent_meeting(self, client):
        response = client.get("/api/v1/meetings/nonexistent-id/export")
        assert response.status_code == 404
        assert "Meeting not found" in response.json()["detail"]

    def test_export_markdown_has_statistics(self, client):
        response = client.get("/api/v1/meetings")
        meetings = response.json()
        if not meetings:
            pytest.skip("No meetings available")
        meeting_id = meetings[0]["id"]
        response = client.get(f"/api/v1/meetings/{meeting_id}/export")
        content = response.text
        assert "Statistics" in content

    def test_export_meeting_after_new_upload(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("export_test.txt", b"Alice: We must review the code.", "text/plain")},
        )
        assert response.status_code == 200
        meeting_id = response.json()["id"]
        response = client.get(f"/api/v1/meetings/{meeting_id}/export")
        assert response.status_code == 200
        content = response.text
        assert "review" in content.lower()
