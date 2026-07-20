"""
Unit tests for the dynamic document analysis and processing pipeline.

Verifies file validation, standard-library text extraction, keyword analysis, and dynamic summary generation.
"""

import os
import sys
import tempfile
import zipfile
import pytest

# Add both root and src directory to path to support static analysis and runtime relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.models.meeting_model import Meeting
from src.services.detection_service import DetectionService
from src.app import MeetingNotesApp


def create_mock_docx(file_path: str, text: str) -> None:
    """Helper to create a minimal valid docx programmatically."""
    xml_data = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body>
        <w:p>
          <w:r>
            <w:t>{text}</w:t>
          </w:r>
        </w:p>
      </w:body>
    </w:document>"""
    with zipfile.ZipFile(file_path, "w") as z:
        z.writestr("word/document.xml", xml_data)


def test_dynamic_docx_extraction_and_different_summaries():
    """Verify that analyzing different docx files produces different summaries and action items."""
    service = DetectionService()

    # Document 1: Database migration sync
    text1 = (
        "Meeting Minutes: Database Migration.\n"
        "Participants: Amit, Rahul, Priya\n"
        "Amit: We need to complete the Postgres migration by Monday.\n"
        "Rahul: I decided to approve the database schema update.\n"
        "Priya: I will write the migration scripts before launch."
    )
    
    # Document 2: Design system alignment
    text2 = (
        "Meeting Minutes: Design System Review.\n"
        "Participants: Brian, Priya\n"
        "Brian: We must finish the color contrast compliance audit by tomorrow.\n"
        "Priya: I agreed to adopt the new Inter fonts guidelines.\n"
        "Brian: I will check the focus outline styles next week."
    )

    m1 = Meeting("Migration Sync", ["Unknown"])
    m2 = Meeting("Design Review", ["Unknown"])

    # Run analysis
    service.analyze_document(m1, text1)
    service.analyze_document(m2, text2)

    # Verify summaries are completely different and match file contents
    assert "Database Migration" in m1.summary
    assert "Design System Review" in m2.summary
    assert m1.summary != m2.summary

    # Verify action items are extracted dynamically and differ
    assert len(m1.action_items) == 2
    assert len(m2.action_items) == 2

    # Assert correct owners are mapped
    owners_m1 = [a.assigned_to for a in m1.action_items]
    assert "Amit" in owners_m1 or "Priya" in owners_m1

    owners_m2 = [a.assigned_to for a in m2.action_items]
    assert "Brian" in owners_m2

    # Verify deadlines are extracted dynamically
    deadlines_m1 = [a.due_date for a in m1.action_items if a.due_date and a.due_date != "Pending"]
    assert len(deadlines_m1) > 0

    deadlines_m2 = [a.due_date for a in m2.action_items if a.due_date and a.due_date != "Pending"]
    assert len(deadlines_m2) > 0


def test_no_hardcoded_text_remains():
    """Ensure no hardcoded demo responses appear in output from custom document uploads."""
    service = DetectionService()
    m = Meeting("Test Upload", ["Unknown"])
    
    custom_text = "Alice: We will implement redis caching for session persistence by Friday."
    service.analyze_document(m, custom_text)

    # Assert no hardcoded Priya or Uploader text appears
    assert "Priya will deploy the code by Friday." not in m.summary
    assert "Approve the release notes." not in m.summary
    assert "We uploaded the file for documentation." not in m.summary

    # Assert actual text contents are reflected
    assert "redis caching" in m.summary or "redis" in m.summary.lower()
    assert len(m.action_items) >= 1
    assert "redis caching" in m.action_items[0].description.lower()


def test_file_validation_error_conditions():
    """Verify that file validation error conditions trigger appropriate exceptions."""
    app = MeetingNotesApp()

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Empty TXT file
        empty_txt = os.path.join(tmpdir, "empty.txt")
        with open(empty_txt, "w") as f:
            f.write("")
        
        with pytest.raises(ValueError, match="The document is empty"):
            app._extract_text_from_txt(empty_txt)

        # 2. Corrupted docx (not a zip)
        corrupt_docx = os.path.join(tmpdir, "corrupt.docx")
        with open(corrupt_docx, "w") as f:
            f.write("Definitely not a zip file content.")

        with pytest.raises(ValueError, match="The document is corrupted or unreadable"):
            app._extract_text_from_docx(corrupt_docx)

        # 3. Non-existent file
        missing_file = os.path.join(tmpdir, "missing.txt")
        with pytest.raises(ValueError):
            app._extract_text_from_txt(missing_file)


def test_empty_docx_validation():
    """Verify that programmatically creating an empty docx raises an error."""
    app = MeetingNotesApp()

    tmpdir = tempfile.mkdtemp()
    try:
        empty_docx = os.path.join(tmpdir, "empty.docx")
        create_mock_docx(empty_docx, "")
        
        with pytest.raises(ValueError):
            app._extract_text_from_docx(empty_docx)
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)
