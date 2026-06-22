"""Ollama runtime adapter — uses the Ollama streaming REST API."""

from __future__ import annotations

import json
import time

import httpx

from siliconmark.core.models import ModelInfo
from siliconmark.runtimes.base import BaseRuntime, InferenceResult

_BASE_URL = "http://localhost:11434"


class OllamaRuntime(BaseRuntime):
    name = "ollama"

    def __init__(self, model: ModelInfo) -> None:
        super().__init__(model)
        self._client = httpx.Client(base_url=_BASE_URL, timeout=300)

    def prepare(self) -> None:
        try:
            self._client.post(
                "/api/generate",
                json={
                    "model": self.model.name,
                    "prompt": "hi",
                    "stream": False,
                    "options": {"num_predict": 1},
                },
            )
        except httpx.ConnectError as e:
            raise RuntimeError("Ollama is not running. Start it with: ollama serve") from e

    def infer(self, prompt: str, max_tokens: int) -> InferenceResult:
        first_token_time: float | None = None
        start = time.perf_counter()
        tokens_generated = 0
        prompt_tokens: int | None = None
        eval_duration_s = 0.0
        chunks: list[str] = []

        with self._client.stream(
            "POST",
            "/api/generate",
            json={
                "model": self.model.name,
                "prompt": prompt,
                "stream": True,
                "options": {"num_predict": max_tokens},
            },
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                text = chunk.get("response", "")
                if text and first_token_time is None:
                    first_token_time = (time.perf_counter() - start) * 1000
                chunks.append(text)
                if chunk.get("done"):
                    tokens_generated = chunk.get("eval_count", 0)
                    prompt_tokens = chunk.get("prompt_eval_count")
                    ns = chunk.get("eval_duration", 0)
                    eval_duration_s = ns / 1e9 if ns else 0.0

        total_s = eval_duration_s or (time.perf_counter() - start)
        return InferenceResult(
            tokens_generated=tokens_generated,
            total_duration_s=total_s,
            time_to_first_token_ms=round(first_token_time, 1) if first_token_time else None,
            prompt_tokens=prompt_tokens,
            raw_response="".join(chunks),
        )

    def cleanup(self) -> None:
        self._client.close()
