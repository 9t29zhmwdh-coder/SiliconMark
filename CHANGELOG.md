# Changelog — SiliconMark

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] — 2026-06-15

### Added
- OllamaRuntime: benchmark models via Ollama HTTP API
- GGUFRuntime: direct inference via llama-cpp-python (Metal-accelerated)
- MLCRuntime: MLC-LLM backend support
- MetricsCollector: psutil-based RAM and CPU sampling
- Apple powermetrics integration: tokens/s, RAM, power draw, ANE activity, temperature
- Structured JSON and CSV output
- CLI with argparse (runtime, model, prompt, iterations, output flags)
