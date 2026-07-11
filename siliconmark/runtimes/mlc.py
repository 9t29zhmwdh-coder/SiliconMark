"""MLC-LLM runtime adapter: uses the MLC Python SDK (streaming chat completions)."""

from __future__ import annotations

import time

from siliconmark.core.models import ModelInfo
from siliconmark.runtimes.base import BaseRuntime, InferenceResult


class MLCRuntime(BaseRuntime):
    name = "mlc"

    def __init__(self, model: ModelInfo) -> None:
        super().__init__(model)
        self._engine = None

    def prepare(self) -> None:
        try:
            from mlc_llm import MLCEngine  # type: ignore[import-not-found]

            self._engine = MLCEngine(self.model.name)
        except ImportError as e:
            raise RuntimeError("MLC-LLM not installed. Install with: pip install mlc-llm") from e

    def infer(self, prompt: str, max_tokens: int) -> InferenceResult:
        if self._engine is None:
            raise RuntimeError("MLCRuntime.prepare() was not called.")

        first_token_time: float | None = None
        start = time.perf_counter()
        chunks: list[str] = []
        tokens_generated = 0

        for response in self._engine.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            stream=True,
        ):
            delta = response.choices[0].delta.content or ""
            if delta and first_token_time is None:
                first_token_time = (time.perf_counter() - start) * 1000
            chunks.append(delta)
            tokens_generated += 1

        return InferenceResult(
            tokens_generated=tokens_generated,
            total_duration_s=time.perf_counter() - start,
            time_to_first_token_ms=round(first_token_time, 1) if first_token_time else None,
            prompt_tokens=None,
            raw_response="".join(chunks),
        )

    def cleanup(self) -> None:
        if self._engine is not None:
            self._engine.terminate()
            self._engine = None
