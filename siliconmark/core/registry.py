"""Runtime registry: maps names to adapter classes."""

from __future__ import annotations

import importlib
import importlib.util
import urllib.request
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from siliconmark.runtimes.base import BaseRuntime

_REGISTRY: dict[str, str] = {
    "ollama": "siliconmark.runtimes.ollama:OllamaRuntime",
    "llamacpp": "siliconmark.runtimes.llamacpp:LlamaCppRuntime",
    "mlc": "siliconmark.runtimes.mlc:MLCRuntime",
    "gguf": "siliconmark.runtimes.gguf:GGUFRuntime",
}

_DESCRIPTIONS: dict[str, str] = {
    "ollama": "Ollama REST API, localhost:11434  (ollama serve)",
    "llamacpp": "llama.cpp server, localhost:8080   (llama-server -m model.gguf)",
    "mlc": "MLC-LLM Python SDK (pip install mlc-llm)",
    "gguf": "Direct GGUF via llama-cpp-python (pip install siliconmark[gguf])",
}


def get_runtime(name: str) -> type[BaseRuntime]:
    if name not in _REGISTRY:
        raise ValueError(f"Unknown runtime: {name!r}. Available: {list(_REGISTRY)}")
    module_path, class_name = _REGISTRY[name].split(":")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def list_runtimes() -> list[tuple[str, str]]:
    return [(k, _DESCRIPTIONS[k]) for k in _REGISTRY]


def _answers(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=1) as resp:
            return resp.status == 200
    except OSError:
        return False


# Servers must be running; SDKs must be importable.
_CHECKS = {
    "ollama": lambda: _answers("http://localhost:11434/api/version"),
    "llamacpp": lambda: _answers("http://localhost:8080/health"),
    "mlc": lambda: importlib.util.find_spec("mlc_llm") is not None,
    "gguf": lambda: importlib.util.find_spec("llama_cpp") is not None,
}


def runtime_available(name: str) -> bool:
    """Whether the runtime can be benchmarked right now."""
    check = _CHECKS.get(name)
    return bool(check and check())
