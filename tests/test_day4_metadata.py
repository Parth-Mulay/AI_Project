import os
import json
import pytest

METADATA_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "requirements")

def load_json(filename):
    filepath = os.path.join(METADATA_DIR, filename)
    assert os.path.exists(filepath), f"{filename} does not exist"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def test_metadata_files_exist():
    """Verify that all Day 4 metadata JSON files are present in the expected directory."""
    files = [
        "requirements_index.json",
        "user_stories.json",
        "acceptance_criteria.json",
        "feature_priority.json",
        "traceability.json"
    ]
    for filename in files:
        filepath = os.path.join(METADATA_DIR, filename)
        assert os.path.exists(filepath), f"Missing metadata file: {filename}"

def test_requirements_integrity():
    """Verify that the requirements are consistent across all metadata documents."""
    index_data = load_json("requirements_index.json")
    stories_data = load_json("user_stories.json")
    priority_data = load_json("feature_priority.json")
    traceability_data = load_json("traceability.json")
    criteria_data = load_json("acceptance_criteria.json")

    # Extract all requirement IDs from the index
    req_ids = {req["id"] for req in index_data["requirements"]}
    assert len(req_ids) == 27, f"Expected 27 requirements in the index, found {len(req_ids)}"

    # Check User Stories
    story_req_ids = {story["requirement_id"] for story in stories_data["user_stories"]}
    story_ids = {story["id"] for story in stories_data["user_stories"]}
    
    # Assert each requirement has at least one story mapping
    for req_id in req_ids:
        assert req_id in story_req_ids, f"Requirement {req_id} does not have a mapped user story"

    # Check priorities
    prioritized_ids = set()
    for cat in ["must_have", "should_have", "could_have", "wont_have"]:
        assert cat in priority_data, f"Priority category {cat} is missing from feature_priority.json"
        prioritized_ids.update(priority_data[cat])

    # Every requirement must have a defined priority
    for req_id in req_ids:
        # Note: Won't have requirements (like FR-REC-001) might not be in functional requirements index
        # but all indexed requirements must be categorized.
        assert req_id in prioritized_ids, f"Requirement {req_id} is not prioritized in feature_priority.json"

    # Check Traceability Matrix
    trace_req_ids = {trace["requirement_id"] for trace in traceability_data["traceability"]}
    for req_id in req_ids:
        assert req_id in trace_req_ids, f"Requirement {req_id} is missing from the traceability matrix"

    # Check Acceptance Criteria mappings
    for story_id in story_ids:
        assert story_id in criteria_data["acceptance_criteria"], f"User story {story_id} does not have acceptance criteria defined"
        ac_list = criteria_data["acceptance_criteria"][story_id]
        assert len(ac_list) > 0, f"User story {story_id} has an empty acceptance criteria list"
        for ac in ac_list:
            assert "scenario" in ac, f"Acceptance criteria scenario missing in story {story_id}"
            assert "steps" in ac, f"Acceptance criteria steps missing in story {story_id}"
            assert isinstance(ac["steps"], list), f"Acceptance criteria steps should be a list in story {story_id}"
            assert len(ac["steps"]) > 0, f"Acceptance criteria steps list is empty in story {story_id}"
