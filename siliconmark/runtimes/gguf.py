"""Direct GGUF runtime via llama-cpp-python with full Metal GPU offload."""

from __future__ import annotations

import time

from siliconmark.core.models import ModelInfo
from siliconmark.runtimes.base import BaseRuntime, InferenceResult


class GGUFRuntime(BaseRuntime):
    name = "gguf"

    def __init__(self, model: ModelInfo) -> None:
        super().__init__(model)
        if not model.path:
            raise ValueError("GGUFRuntime requires model.path to point to a .gguf file.")
        self._llm = None

    def prepare(self) -> None:
        try:
            from llama_cpp import Llama  # type: ignore[import-not-found]
            self._llm = Llama(
                model_path=self.model.path,
                n_ctx=self.model.context_length or 2048,
                n_gpu_layers=-1,  # offload all layers to Metal on Apple Silicon
                verbose=False,
            )
        except ImportError as e:
            raise RuntimeError(
                "llama-cpp-python not installed. "
                "Install with: pip install 'siliconmark[gguf]'"
            ) from e

    def infer(self, prompt: str, max_tokens: int) -> InferenceResult:
        if self._llm is None:
            raise RuntimeError("GGUFRuntime.prepare() was not called.")

        first_token_time: float | None = None
        start = time.perf_counter()
        chunks: list[str] = []
        tokens_generated = 0

        for chunk in self._llm(prompt, max_tokens=max_tokens, stream=True):
            text = chunk["choices"][0]["text"]
            if text and first_token_time is None:
                first_token_time = (time.perf_counter() - start) * 1000
            chunks.append(text)
            tokens_generated += 1

        return InferenceResult(
            tokens_generated=tokens_generated,
            total_duration_s=time.perf_counter() - start,
            time_to_first_token_ms=round(first_token_time, 1) if first_token_time else None,
            prompt_tokens=None,
            raw_response="".join(chunks),
        )

    def cleanup(self) -> None:
        if self._llm is not None:
            del self._llm
            self._llm = None
