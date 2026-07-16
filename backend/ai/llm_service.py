"""LLM service with provider abstraction and rule-based fallback."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .providers import AnthropicProvider
from .guardrails import Guardrails


class AISummaryService:
    def __init__(self, provider: Any | None = None, guardrails: Guardrails | None = None) -> None:
        self.provider = provider or (AnthropicProvider() if os.getenv("ANTHROPIC_API_KEY") else None)
        self.guardrails = guardrails or Guardrails()

    def generate_summary(self, text: str) -> dict[str, Any]:
        try:
            cleaned_text = self.guardrails.validate_input(text)
            prompt_path = Path(__file__).resolve().parent / "prompts" / "summary_prompt.txt"
            system_prompt = prompt_path.read_text(encoding="utf-8")
            if self.provider is None:
                raise RuntimeError("No AI provider configured")
            response_text = self.provider.generate(cleaned_text, system_prompt=system_prompt)
            response_text = self.guardrails.validate_output(response_text)
            return {"summary": response_text, "source": "llm"}
        except Exception as exc:
            fallback_summary = self._fallback_summary(cleaned_text if "cleaned_text" in locals() else text)
            return {"summary": fallback_summary, "source": "fallback", "error": str(exc)}

    def _fallback_summary(self, text: str) -> str:
        if not text or not text.strip():
            return "No meeting content available."
        sentences = [segment.strip() for segment in text.split(".") if segment.strip()]
        if not sentences:
            return "Meeting content processed with the fallback rule-based summarizer."
        return " | ".join(sentences[:3])
