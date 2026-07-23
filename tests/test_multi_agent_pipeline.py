"""Unit tests for the 4-Agent Multi-Agent Processing Pipeline."""

import os
import sys
import unittest
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agents import MultiAgentOrchestrator


class TestMultiAgentPipeline(unittest.TestCase):
    """Test suite verifying end-to-end functionality of all 4 AI agents."""

    def setUp(self):
        self.orchestrator = MultiAgentOrchestrator()
        self.sample_text = (
            "Alice: Rahul will update the frontend dashboard by Friday.\n"
            "Bob: We decided to deploy the backend microservice to production.\n"
            "Charlie: There is a blocker in the QA environment."
        )

    def test_pipeline_execution_with_raw_text(self):
        """Verify sequential 4-Agent pipeline run on raw transcript text."""
        result = self.orchestrator.process_meeting(raw_text=self.sample_text, title="Sprint Sync")

        self.assertTrue(result.success, f"Pipeline failed: {result.error_message}")
        self.assertEqual(len(result.agent_results), 4, "Expected 4 agent execution results")

        agent1_res = result.agent_results[0]
        self.assertEqual(agent1_res.agent_name, "Agent-1:IngestionValidation")
        self.assertTrue(agent1_res.success)

        agent2_res = result.agent_results[1]
        self.assertEqual(agent2_res.agent_name, "Agent-2:ProcessingExtraction")
        self.assertTrue(agent2_res.success)
        self.assertGreaterEqual(len(agent2_res.data["raw_action_items"]), 1)
        self.assertGreaterEqual(len(agent2_res.data["raw_notes"]), 1)

        agent3_res = result.agent_results[2]
        self.assertEqual(agent3_res.agent_name, "Agent-3:RefinementSynthesis")
        self.assertTrue(agent3_res.success)
        self.assertIn("executive_summary", agent3_res.data)

        agent4_res = result.agent_results[3]
        self.assertEqual(agent4_res.agent_name, "Agent-4:OutputFormatting")
        self.assertTrue(agent4_res.success)
        self.assertIn("Sprint Sync", result.markdown_export)
        self.assertEqual(len(result.final_meeting_entity.important_notes), 1)
        self.assertEqual(result.json_payload["message_count"], 3)

    def test_pipeline_assigns_first_person_actions_to_speaker_and_deduplicates(self):
        """Verify owner resolution uses the speaker and duplicate action lines collapse cleanly."""
        transcript = (
            "Bob: I will update the dashboard by Friday.\n"
            "Bob: I will update the dashboard by Friday.\n"
            "Alice: We decided to keep the launch date."
        )

        result = self.orchestrator.process_meeting(raw_text=transcript, title="Owner Resolution")

        self.assertTrue(result.success, f"Pipeline failed: {result.error_message}")
        self.assertEqual(len(result.json_payload["action_items"]), 1)
        self.assertEqual(result.json_payload["action_items"][0]["owner"], "Bob")
        self.assertEqual(result.json_payload["action_items"][0]["due_date"], "Friday")
        self.assertEqual(len(result.json_payload["decisions"]), 1)

    def test_pipeline_accepts_docx_file_input(self):
        """Verify Agent 1 extracts text from a real DOCX container for downstream agents."""
        docx_path = PROJECT_ROOT / "test_pipeline_input.docx"
        self._cleanup_path(docx_path)

        try:
            self._write_minimal_docx(
                docx_path,
                [
                    "Alice: We decided to launch on Monday.",
                    "Bob: Rahul will publish the release notes by Friday.",
                ],
            )
            result = self.orchestrator.process_meeting(file_path=str(docx_path), title="DOCX Intake")
        finally:
            self._cleanup_path(docx_path)

        self.assertTrue(result.success, f"Pipeline failed: {result.error_message}")
        self.assertEqual(result.json_payload["message_count"], 2)
        self.assertEqual(len(result.json_payload["action_items"]), 1)
        self.assertEqual(len(result.json_payload["decisions"]), 1)
        self.assertIn("DOCX Intake", result.markdown_export)

    def test_pipeline_invalid_extension(self):
        """Verify Agent 1 fails gracefully when given invalid file extension."""
        result = self.orchestrator.process_meeting(file_path="malicious_script.exe")
        self.assertFalse(result.success)
        self.assertIn("Unsupported file extension", result.error_message)

    def test_pipeline_missing_input(self):
        """Verify the pipeline rejects requests that do not include text or file input."""
        result = self.orchestrator.process_meeting()
        self.assertFalse(result.success)
        self.assertIn("Context must provide either 'raw_text' or 'file_path'", result.error_message)

    @staticmethod
    def _cleanup_path(path: Path) -> None:
        if path.exists():
            path.unlink()

    @staticmethod
    def _write_minimal_docx(path: Path, paragraphs: list[str]) -> None:
        """Build a minimal .docx file that WordprocessingML readers can parse."""
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
        paragraph_xml = "".join(
            f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>" for text in paragraphs
        )
        document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>{paragraph_xml}</w:body>
</w:document>"""

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("[Content_Types].xml", content_types)
            archive.writestr("_rels/.rels", rels)
            archive.writestr("word/document.xml", document)


if __name__ == "__main__":
    unittest.main()
