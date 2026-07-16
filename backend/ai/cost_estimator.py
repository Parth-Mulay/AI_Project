"""Very small cost estimation helpers for AI calls."""

from __future__ import annotations


def estimate_cost(input_text: str, output_text: str, *, input_price_per_1k: float = 0.00025, output_price_per_1k: float = 0.00125) -> float:
    """Estimate a rough USD cost for an Anthropic-style prompt/response pair."""
    input_tokens = max(1, len(input_text.split()) * 1.3)
    output_tokens = max(1, len(output_text.split()) * 1.3)
    input_cost = (input_tokens / 1000.0) * input_price_per_1k
    output_cost = (output_tokens / 1000.0) * output_price_per_1k
    return input_cost + output_cost
