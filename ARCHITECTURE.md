# Architecture — SiliconMark

## Overview

SiliconMark is a Python package that benchmarks local LLM runtimes on Apple Silicon.

```
SiliconMark/
├── siliconmark/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point (argparse)
│   ├── runtimes/
│   │   ├── __init__.py
│   │   ├── ollama.py       # OllamaRuntime — HTTP API
│   │   ├── gguf.py         # GGUFRuntime — llama-cpp-python
│   │   └── mlc.py          # MLCRuntime — MLC-LLM
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── collector.py    # MetricsCollector (psutil + threading)
│   │   └── powermetrics.py # Apple powermetrics integration (subprocess)
│   ├── benchmark.py        # Orchestrator: run prompt, collect metrics, aggregate
│   └── output.py           # JSON + CSV export
├── tests/
├── pyproject.toml
└── README.md
```

## Benchmark Flow

1. **CLI** parses arguments (runtime, model, prompt, iterations, output format)
2. **Runtime** loads the specified model and runs inference
3. **MetricsCollector** samples psutil (RAM, CPU%) in a background thread
4. **powermetrics** captures ANE activity, GPU power, and package power (requires sudo)
5. **Benchmark** aggregates: tokens/s, peak RAM, avg power, temperature
6. **Output** writes structured JSON and optional CSV

## Supported Runtimes

| Runtime | Backend | Notes |
|---------|---------|-------|
| OllamaRuntime | Ollama HTTP API | No sudo required |
| GGUFRuntime | llama-cpp-python | Requires Metal build |
| MLCRuntime | MLC-LLM | Requires MLC installation |

## Metrics

- Tokens per second (prompt + generation)
- Peak RAM (RSS, GB)
- Average power draw (W) — requires sudo for powermetrics
- ANE activity (%) — Apple Neural Engine
- Die temperature (°C)
