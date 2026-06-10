"""llama.cpp server runtime adapter — uses the HTTP completion API."""

from __future__ import annotations

import json
import time

import httpx

from siliconmark.core.models import ModelInfo
from siliconmark.runtimes.base import BaseRuntime, InferenceResult

_BASE_URL = "http://localhost:8080"


class LlamaCppRuntime(BaseRuntime):
    name = "llamacpp"

    def __init__(self, model: ModelInfo, base_url: str = _BASE_URL) -> None:
        super().__init__(model)
        self._client = httpx.Client(base_url=base_url, timeout=300)

    def prepare(self) -> None:
        try:
            self._client.get("/health").raise_for_status()
        except (httpx.ConnectError, httpx.HTTPStatusError) as e:
            raise RuntimeError(
                "llama.cpp server not reachable. "
                "Start with: llama-server -m <model.gguf> --port 8080"
            ) from e

    def infer(self, prompt: str, max_tokens: int) -> InferenceResult:
        first_token_time: float | None = None
        start = time.perf_counter()
        chunks: list[str] = []
        tokens_generated = 0
        timings: dict = {}

        with self._client.stream(
            "POST", "/completion",
            json={"prompt": prompt, "n_predict": max_tokens, "stream": True},
        ) as resp:
            resp.raise_for_status()
            for raw_line in resp.iter_lines():
                line = raw_line.strip()
                if not line or not line.startswith("data:"):
                    continue
                data = json.loads(line[5:].strip())
                text = data.get("content", "")
                if text and first_token_time is None:
                    first_token_time = (time.perf_counter() - start) * 1000
                chunks.append(text)
                if data.get("stop"):
                    timings = data.get("timings", {})
                    tokens_generated = data.get("tokens_predicted", len(chunks))

        predicted_ms = timings.get("predicted_ms", 0)
        total_s = predicted_ms / 1000 if predicted_ms else (time.perf_counter() - start)

        return InferenceResult(
            tokens_generated=tokens_generated,
            total_duration_s=total_s,
            time_to_first_token_ms=round(first_token_time, 1) if first_token_time else None,
            prompt_tokens=timings.get("prompt_n"),
            raw_response="".join(chunks),
        )

    def cleanup(self) -> None:
        self._client.close()
