"""Provider abstraction for AI backends."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import os


class LLMProvider(Protocol):
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        ...


@dataclass
class AnthropicProvider:
    api_key: str | None = None
    model: str = "claude-3-haiku-20240307"

    def __init__(self, api_key: str | None = None, model: str = "claude-3-haiku-20240307") -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")

    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured")

        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("anthropic package is not installed") from exc

        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=400,
            system=system_prompt or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
