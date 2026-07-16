"""Basic guardrails for AI usage."""

from __future__ import annotations

import re
from typing import Any


class Guardrails:
    def __init__(self, max_input_chars: int = 8000, max_output_chars: int = 2000) -> None:
        self.max_input_chars = max_input_chars
        self.max_output_chars = max_output_chars

    def validate_input(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Input text is empty")
        if len(text) > self.max_input_chars:
            raise ValueError("Input text exceeds the maximum length")
        if re.search(r"ignore previous instructions|system prompt|developer message", text, re.IGNORECASE):
            raise ValueError("Potential prompt injection detected")
        return text.strip()

    def validate_output(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Model returned empty output")
        if len(text) > self.max_output_chars:
            raise ValueError("Model output exceeds the maximum length")
        return text.strip()

    def validate_response_shape(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("Malformed AI response")
        return payload
