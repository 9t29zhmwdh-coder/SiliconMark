"""Abstract base class for LLM runtime adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from siliconmark.core.models import PerformanceMetrics


@dataclass
class InferenceResult:
    tokens_generated: int
    total_duration_s: float
    time_to_first_token_ms: float | None
    prompt_tokens: int | None
    raw_response: str


class BaseRuntime(ABC):
    name: str = "base"

    def __init__(self, model) -> None:
        self.model = model

    def prepare(self) -> None:
        """Load model, warm up, verify connectivity. Called once before the first infer()."""

    @abstractmethod
    def infer(self, prompt: str, max_tokens: int) -> InferenceResult:
        """Run inference synchronously and return timing + token counts."""

    def cleanup(self) -> None:
        """Release resources after all runs are done."""

    def to_performance_metrics(self, result: InferenceResult) -> PerformanceMetrics:
        tps = (
            result.tokens_generated / result.total_duration_s
            if result.total_duration_s > 0
            else 0.0
        )
        return PerformanceMetrics(
            tokens_per_second=round(tps, 2),
            time_to_first_token_ms=result.time_to_first_token_ms,
            total_tokens=result.tokens_generated,
            total_duration_s=round(result.total_duration_s, 3),
            prompt_tokens=result.prompt_tokens,
        )
