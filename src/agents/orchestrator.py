"""Multi-Agent Orchestrator.

Coordinates execution across Agent 1 -> Agent 2 -> Agent 3 -> Agent 4 pipeline,
managing state context, per-agent telemetry, and step logging.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .base_agent import AgentResult
from .ingestion_agent import FileIngestionAgent
from .processing_agent import ProcessingExtractionAgent
from .refinement_agent import RefinementSynthesisAgent
from .output_agent import OutputFormattingAgent
from backend.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PipelineResult:
    """Summary of the complete Multi-Agent pipeline execution."""

    success: bool
    total_execution_time_ms: float
    agent_results: List[AgentResult] = field(default_factory=list)
    final_meeting_entity: Any = None
    markdown_export: str = ""
    json_payload: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""


class MultiAgentOrchestrator:
    """
    Orchestrates the sequential 4-agent meeting note processing pipeline:

    1. Agent-1: Ingestion & Validation Agent
    2. Agent-2: Processing & Extraction Agent
    3. Agent-3: Refinement & AI Synthesis Agent
    4. Agent-4: Output & Formatting Agent
    """

    def __init__(self):
        self.agent_ingestion = FileIngestionAgent()
        self.agent_processing = ProcessingExtractionAgent()
        self.agent_refinement = RefinementSynthesisAgent()
        self.agent_output = OutputFormattingAgent()

    def process_meeting(self, raw_text: str = None, file_path: str = None, title: str = "AI Meeting Notes") -> PipelineResult:
        """Runs raw meeting input or file through the 4-agent pipeline sequentially."""
        start_time = time.time()
        agent_results: List[AgentResult] = []
        pipeline_context: Dict[str, Any] = {
            "raw_text": raw_text,
            "file_path": file_path,
            "title": title,
        }

        # Step 1: Ingestion & Validation Agent
        res1 = self.agent_ingestion.execute(pipeline_context)
        agent_results.append(res1)
        if not res1.success:
            return self._failed_pipeline(start_time, agent_results, res1.message)
        pipeline_context.update(res1.data)

        # Step 2: Processing & Extraction Agent
        res2 = self.agent_processing.execute(pipeline_context)
        agent_results.append(res2)
        if not res2.success:
            return self._failed_pipeline(start_time, agent_results, res2.message)
        pipeline_context.update(res2.data)

        # Step 3: Refinement & AI Synthesis Agent
        res3 = self.agent_refinement.execute(pipeline_context)
        agent_results.append(res3)
        if not res3.success:
            return self._failed_pipeline(start_time, agent_results, res3.message)
        pipeline_context.update(res3.data)

        # Step 4: Output & Formatting Agent
        res4 = self.agent_output.execute(pipeline_context)
        agent_results.append(res4)
        if not res4.success:
            return self._failed_pipeline(start_time, agent_results, res4.message)
        pipeline_context.update(res4.data)

        total_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"[MultiAgentOrchestrator] Completed 4-Agent pipeline in {total_ms}ms.")

        return PipelineResult(
            success=True,
            total_execution_time_ms=total_ms,
            agent_results=agent_results,
            final_meeting_entity=res4.data.get("meeting_entity"),
            markdown_export=res4.data.get("markdown_export", ""),
            json_payload=res4.data.get("json_payload", {}),
        )

    def _failed_pipeline(self, start_time: float, agent_results: List[AgentResult], error_message: str) -> PipelineResult:
        total_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(f"[MultiAgentOrchestrator] Pipeline failed: {error_message}")

        return PipelineResult(
            success=False,
            total_execution_time_ms=total_ms,
            agent_results=agent_results,
            error_message=error_message,
        )
