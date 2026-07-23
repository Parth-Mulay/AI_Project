"""Agent 3: Refinement & AI Synthesis Agent.

Responsible for deduplication, quality enhancement, owner assignment resolution,
executive summary generation, and confidence rating.
"""

from typing import Any, Dict, List, Set
from .base_agent import BaseAgent
from backend.ai.llm_service import AISummaryService


class RefinementSynthesisAgent(BaseAgent):
    """
    Agent 3 - Refinement & AI Synthesis Agent.

    Deduplicates action items, resolves default owners/dates, synthesizes an executive summary,
    and assigns quality/confidence metrics.
    """

    def __init__(self):
        super().__init__(
            name="Agent-3:RefinementSynthesis",
            role="Refines, deduplicates, synthesizes executive summaries, and scores quality confidence.",
        )
        self.ai_service = AISummaryService()

    def process(self, context: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
        raw_actions: List[Dict[str, Any]] = context.get("raw_action_items", [])
        raw_decisions: List[Dict[str, Any]] = context.get("raw_decisions", [])
        raw_notes: List[Dict[str, Any]] = context.get("raw_notes", [])
        sanitized_text: str = context.get("sanitized_text", "")
        speakers: List[str] = context.get("speakers", [])

        logs.append("Deduplicating and refining action items.")
        refined_actions = self._refine_action_items(raw_actions, speakers)

        logs.append("Deduplicating decisions and notes.")
        refined_decisions = self._deduplicate_by_key(raw_decisions, "description")
        refined_notes = self._deduplicate_by_key(raw_notes, "description")

        logs.append("Synthesizing Executive Summary.")
        summary_result = self.ai_service.generate_summary(sanitized_text)
        executive_summary = summary_result.get("summary", "No summary available.")
        summary_source = summary_result.get("source", "rule-based")

        logs.append(f"Generated summary using [{summary_source}] engine.")

        # Compute Confidence Metric based on extraction cleanliness & clarity
        confidence_score = self._compute_confidence(
            refined_actions, refined_decisions, refined_notes, speakers
        )

        return {
            "executive_summary": executive_summary,
            "summary_source": summary_source,
            "refined_action_items": refined_actions,
            "refined_decisions": refined_decisions,
            "refined_notes": refined_notes,
            "confidence_score": confidence_score,
            "quality_grade": "High" if confidence_score >= 0.85 else "Medium",
        }

    @staticmethod
    def _refine_action_items(raw_actions: List[Dict[str, Any]], speakers: List[str]) -> List[Dict[str, Any]]:
        """Deduplicates and standardizes action item attributes."""
        refined: List[Dict[str, Any]] = []
        seen_descriptions: Set[str] = set()

        default_owner = speakers[0] if speakers else "Unassigned"

        for item in raw_actions:
            desc = item.get("description", "").strip()
            desc_key = desc.lower()

            if desc_key in seen_descriptions:
                continue

            seen_descriptions.add(desc_key)

            owner = item.get("owner")
            if not owner or owner.lower() == "unknown":
                owner = default_owner

            refined.append({
                "description": desc.capitalize(),
                "owner": owner,
                "due_date": item.get("due_date", "TBD"),
                "status": "Pending",
            })

        return refined

    @staticmethod
    def _deduplicate_by_key(items: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        """Deduplicate dict items based on lowercased key content."""
        seen: Set[str] = set()
        deduped: List[Dict[str, Any]] = []

        for item in items:
            val = str(item.get(key, "")).strip().lower()
            if val and val not in seen:
                seen.add(val)
                deduped.append(item)

        return deduped

    @staticmethod
    def _compute_confidence(
        actions: List[Any], decisions: List[Any], notes: List[Any], speakers: List[str]
    ) -> float:
        """Calculates a baseline confidence score between 0.70 and 0.98."""
        score = 0.80
        if speakers and len(speakers) > 1:
            score += 0.08
        if actions:
            score += 0.05
        if decisions:
            score += 0.05
        return round(min(score, 0.98), 2)
