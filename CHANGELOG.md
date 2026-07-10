# Changelog: SiliconMark

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.2] - 2026-07-10

### Fixed

- Removed em-dashes from CHANGELOG.md, replaced with colons/plain hyphens

## [0.1.1] - 2026-07-10

### Fixed

- Removed a duplicate "New here? -> beginners guide" callout from README.md (was shown twice)

### Added

- Added the "New here?" beginner guide callout to README.de.md (was missing)

## [0.1.0] - 2026-06-15

### Added
- OllamaRuntime: benchmark models via Ollama HTTP API
- GGUFRuntime: direct inference via llama-cpp-python (Metal-accelerated)
- MLCRuntime: MLC-LLM backend support
- MetricsCollector: psutil-based RAM and CPU sampling
- Apple powermetrics integration: tokens/s, RAM, power draw, ANE activity, temperature
- Structured JSON and CSV output
- CLI with argparse (runtime, model, prompt, iterations, output flags)
