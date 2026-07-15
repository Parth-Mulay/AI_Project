"""Reusable document extraction helpers for uploads and tests."""

from __future__ import annotations


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a plain text document."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file_handle:
            text = file_handle.read()
        if not text.strip():
            raise ValueError("The document is empty.")
        return text
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"The document is corrupted or unreadable. Details: {exc}") from exc


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    import docx

    try:
        document = docx.Document(file_path)
        paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
        extracted = "\n".join(paragraphs).strip()
        if not extracted:
            raise ValueError("The document is empty.")
        return extracted
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"The document is corrupted or unreadable. Details: {exc}") from exc


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    import pdfplumber

    try:
        with pdfplumber.open(file_path) as pdf_document:
            pages = []
            for page in pdf_document.pages:
                text = page.extract_text()
                if text and text.strip():
                    pages.append(text.strip())
            extracted = "\n".join(pages).strip()
        if not extracted:
            raise ValueError("The document is empty.")
        return extracted
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"The document is corrupted or unreadable. Details: {exc}") from exc


def extract_text_from_audio(file_path: str) -> str:
    """Transcribe audio and return extracted text."""
    try:
        from .audio.transcriber import AudioTranscriber
    except ImportError:
        from audio.transcriber import AudioTranscriber

    try:
        transcriber = AudioTranscriber()
        text = transcriber.transcribe(file_path)
        if not text.strip():
            raise ValueError("The document is empty.")
        return text
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"The document is corrupted or unreadable. Details: {exc}") from exc
