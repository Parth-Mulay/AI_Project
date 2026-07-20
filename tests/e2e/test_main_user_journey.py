"""End-to-end test covering the main user journey.

Flow:
1. Health check
2. List existing meetings
3. Upload a meeting transcript
4. Verify processing (summary, action items, decisions)
5. Retrieve the meeting by ID
6. Export the meeting as Markdown
7. Verify the meeting appears in the list
8. Delete the meeting
"""

import pytest
from fastapi.testclient import TestClient

from src.server import app


@pytest.fixture(scope="module")
def e2e_client():
    return TestClient(app)


class TestMainUserJourney:
    """Complete end-to-end user journey test."""

    def test_full_journey(self, e2e_client):
        # Step 1: Health check
        response = e2e_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

        # Step 2: List existing meetings
        response = e2e_client.get("/api/v1/meetings")
        assert response.status_code == 200
        initial_meetings = response.json()
        assert isinstance(initial_meetings, list)

        # Step 3: Upload a meeting transcript
        transcript_content = (
            "Meeting Minutes: Sprint Planning.\n"
            "Participants: Alice, Bob, Charlie\n"
            "Alice: We must complete the authentication module by Friday.\n"
            "Bob: I agreed to adopt the new design system for the frontend.\n"
            "Charlie: Risk identified - the deployment server has limited resources.\n"
            "Alice: I will write the migration scripts before the launch.\n"
            "Bob: We decided to use JWT for token management.\n"
            "Charlie: We must finish the API documentation by Monday."
        )
        response = e2e_client.post(
            "/api/v1/upload",
            files={"file": ("sprint_planning.txt", transcript_content.encode("utf-8"), "text/plain")},
        )
        assert response.status_code == 200, f"Upload failed: {response.text}"
        upload_data = response.json()

        # Step 4: Verify processing
        assert "id" in upload_data, "No meeting ID returned"
        assert "title" in upload_data, "No title returned"
        assert "summary" in upload_data, "No summary returned"
        assert "action_items" in upload_data, "No action items returned"
        assert "decisions" in upload_data, "No decisions returned"
        meeting_id = upload_data["id"]
        assert "sprint_planning" in upload_data["title"]

        # Verify action items are extracted
        action_items = upload_data["action_items"]
        assert len(action_items) > 0, "No action items extracted"
        action_descriptions = [a["description"] for a in action_items]
        has_auth_action = any("authentication" in d.lower() for d in action_descriptions)
        has_api_action = any("API documentation" in d for d in action_descriptions)
        assert has_auth_action or has_api_action, "Expected action items not found"

        # Verify decisions are extracted
        decisions = upload_data["decisions"]
        assert len(decisions) > 0, "No decisions extracted"

        # Step 5: Retrieve the meeting by ID
        response = e2e_client.get(f"/api/v1/meetings/{meeting_id}")
        assert response.status_code == 200
        meeting_detail = response.json()
        assert meeting_detail["id"] == meeting_id
        assert meeting_detail["title"] == upload_data["title"]
        assert "messages" in meeting_detail
        assert len(meeting_detail["messages"]) > 0

        # Step 6: Export the meeting as Markdown
        response = e2e_client.get(f"/api/v1/meetings/{meeting_id}/export")
        assert response.status_code == 200
        assert "text/markdown" in response.headers["content-type"]
        markdown_content = response.text
        assert "# " in markdown_content
        assert "Summary" in markdown_content
        assert "Action Items" in markdown_content
        assert "Decisions" in markdown_content
        assert "Statistics" in markdown_content

        # Step 7: Verify meeting appears in list
        response = e2e_client.get("/api/v1/meetings")
        meetings = response.json()
        meeting_ids = [m["id"] for m in meetings]
        assert meeting_id in meeting_ids, "Meeting not found in list"

        # Step 8: Delete the meeting
        response = e2e_client.delete(f"/api/v1/meetings/{meeting_id}")
        assert response.status_code == 200
        assert response.json()["detail"] == "Meeting deleted"

        # Verify deletion
        response = e2e_client.get(f"/api/v1/meetings/{meeting_id}")
        assert response.status_code == 404

        # Verify it's removed from the list
        response = e2e_client.get("/api/v1/meetings")
        meetings = response.json()
        meeting_ids = [m["id"] for m in meetings]
        assert meeting_id not in meeting_ids, "Meeting still in list after deletion"
