"""Integration tests for meetings CRUD API endpoints."""

import pytest


class TestListMeetings:
    def test_list_meetings_returns_list(self, client):
        response = client.get("/api/v1/meetings")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_meetings_contains_expected_keys(self, client):
        response = client.get("/api/v1/meetings")
        data = response.json()
        if data:
            meeting = data[0]
            assert "id" in meeting
            assert "title" in meeting
            assert "created_at" in meeting
            assert "participants" in meeting
            assert "message_count" in meeting

    def test_list_meetings_returns_lightweight(self, client):
        response = client.get("/api/v1/meetings")
        data = response.json()
        if data:
            meeting = data[0]
            assert "summary" not in meeting
            assert "action_items" not in meeting


class TestGetMeeting:
    def test_get_existing_meeting(self, client):
        response = client.get("/api/v1/meetings")
        meetings = response.json()
        if not meetings:
            pytest.skip("No meetings available to test")
        meeting_id = meetings[0]["id"]
        response = client.get(f"/api/v1/meetings/{meeting_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == meeting_id

    def test_get_meeting_returns_full_details(self, client):
        response = client.get("/api/v1/meetings")
        meetings = response.json()
        if not meetings:
            pytest.skip("No meetings available")
        meeting_id = meetings[0]["id"]
        response = client.get(f"/api/v1/meetings/{meeting_id}")
        data = response.json()
        assert "summary" in data
        assert "messages" in data
        assert "action_items" in data
        assert "decisions" in data
        assert "duration" in data

    def test_get_nonexistent_meeting_returns_404(self, client):
        response = client.get("/api/v1/meetings/nonexistent-id-12345")
        assert response.status_code == 404
        assert "Meeting not found" in response.json()["detail"]

    def test_get_meeting_with_invalid_id_format(self, client):
        response = client.get("/api/v1/meetings/   ")
        assert response.status_code == 404


class TestDeleteMeeting:
    def test_delete_nonexistent_meeting_returns_404(self, client):
        response = client.delete("/api/v1/meetings/nonexistent-id-12345")
        assert response.status_code == 404

    def test_delete_existing_meeting(self, client):
        response = client.get("/api/v1/meetings")
        meetings = response.json()
        if not meetings:
            pytest.skip("No meetings available to delete")
        meeting_id = meetings[0]["id"]
        response = client.delete(f"/api/v1/meetings/{meeting_id}")
        assert response.status_code == 200
        assert response.json()["detail"] == "Meeting deleted"
        response = client.get(f"/api/v1/meetings/{meeting_id}")
        assert response.status_code == 404

    def test_delete_same_meeting_twice(self, client):
        response = client.delete("/api/v1/meetings/nonexistent-double-delete")
        assert response.status_code == 404
        response = client.delete("/api/v1/meetings/nonexistent-double-delete")
        assert response.status_code == 404
