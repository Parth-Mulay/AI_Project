"""Base abstract class for specialized AI Agents."""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List
from backend.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class AgentResult:
    """Standardized execution output returned by an Agent."""

    agent_name: str
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    message: str = ""
    logs: List[str] = field(default_factory=list)


class BaseAgent(ABC):
    """Abstract Base Class for single-responsibility AI processing agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.logger = logger

    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Executes agent logic wrapped with performance tracking and error logging."""
        start_time = time.time()
        logs: List[str] = []

        logs.append(f"[{self.name}] Starting execution - Role: {self.role}")
        self.logger.info(f"[{self.name}] Agent execution started.")

        try:
            result_data = self.process(context, logs)
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            logs.append(f"[{self.name}] Completed successfully in {elapsed_ms}ms.")

            return AgentResult(
                agent_name=self.name,
                success=True,
                data=result_data,
                execution_time_ms=elapsed_ms,
                message=f"{self.name} completed successfully.",
                logs=logs,
            )
        except Exception as exc:
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            error_msg = f"[{self.name}] Failed with error: {str(exc)}"
            logs.append(error_msg)
            self.logger.exception(f"[{self.name}] Execution error")

            return AgentResult(
                agent_name=self.name,
                success=False,
                data={},
                execution_time_ms=elapsed_ms,
                message=error_msg,
                logs=logs,
            )

    @abstractmethod
    def process(self, context: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
        """Core agent logic to be implemented by child agent classes."""
        pass
