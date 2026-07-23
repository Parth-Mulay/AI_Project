"""Agent 1: Ingestion & Validation Agent.

Responsible for receiving, validating, sanitizing, and extracting metadata
from raw meeting inputs or uploaded files.
"""

import os
import zipfile
from datetime import datetime
from typing import Any, Dict, List
from xml.etree import ElementTree as ET
from .base_agent import BaseAgent


class FileIngestionAgent(BaseAgent):
    """
    Agent 1 - Ingestion & Validation Agent.

    Enforces input security, format validation, size checking, and text sanitization.
    """

    ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".docx", ".log"}
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit

    def __init__(self):
        super().__init__(
            name="Agent-1:IngestionValidation",
            role="Accepts, validates, sanitizes, and prepares raw meeting files and text.",
        )

    def process(self, context: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
        raw_text = context.get("raw_text")
        file_path = context.get("file_path")
        meeting_title = context.get("title", "Untitled Meeting")

        sanitized_content = ""
        metadata: Dict[str, Any] = {
            "title": meeting_title,
            "source_type": "text_input",
            "size_bytes": 0,
            "line_count": 0,
            "timestamp": datetime.now().isoformat(),
        }

        if file_path:
            # Secure file path sanitization
            safe_basename = os.path.basename(file_path)
            ext = os.path.splitext(safe_basename)[1].lower()

            logs.append(f"Processing uploaded file: {safe_basename}")

            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file extension '{ext}'. Allowed: {', '.join(sorted(self.ALLOWED_EXTENSIONS))}"
                )

            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Specified file path does not exist: {file_path}")

            file_size = os.path.getsize(file_path)
            if file_size > self.MAX_FILE_SIZE_BYTES:
                raise ValueError(f"File size ({file_size} bytes) exceeds maximum limit of 10MB.")

            metadata["size_bytes"] = file_size
            metadata["source_type"] = f"file ({ext})"
            metadata["filename"] = safe_basename

            sanitized_content = self._read_supported_file(file_path, ext)

        elif raw_text:
            logs.append("Processing raw text string input.")
            sanitized_content = raw_text
            metadata["size_bytes"] = len(raw_text.encode("utf-8"))
        else:
            raise ValueError("Context must provide either 'raw_text' or 'file_path'.")

        # Sanitize text content: replace null bytes, normalize newlines
        sanitized_content = sanitized_content.replace("\x00", "").replace("\r\n", "\n")
        lines = [line.strip() for line in sanitized_content.split("\n") if line.strip()]

        metadata["line_count"] = len(lines)
        logs.append(f"Ingested {len(lines)} non-empty lines cleanly ({metadata['size_bytes']} bytes).")

        return {
            "sanitized_text": sanitized_content,
            "sanitized_lines": lines,
            "metadata": metadata,
            "validation_passed": True,
        }

    @staticmethod
    def _read_supported_file(file_path: str, ext: str) -> str:
        """Read text-like meeting files and extract text from supported docx uploads."""
        if ext == ".docx":
            return FileIngestionAgent._extract_docx_text(file_path)

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    @staticmethod
    def _extract_docx_text(file_path: str) -> str:
        """Extract visible paragraph text from a .docx file without external dependencies."""
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        try:
            with zipfile.ZipFile(file_path) as archive:
                document_xml = archive.read("word/document.xml")
        except (FileNotFoundError, KeyError, zipfile.BadZipFile) as exc:
            raise ValueError(f"Unreadable DOCX file: {exc}") from exc

        try:
            root = ET.fromstring(document_xml)
        except ET.ParseError as exc:
            raise ValueError(f"Corrupted DOCX XML: {exc}") from exc

        paragraphs: List[str] = []
        for paragraph in root.findall(".//w:p", namespace):
            text_parts = [node.text for node in paragraph.findall(".//w:t", namespace) if node.text]
            paragraph_text = "".join(text_parts).strip()
            if paragraph_text:
                paragraphs.append(paragraph_text)

        return "\n".join(paragraphs)
