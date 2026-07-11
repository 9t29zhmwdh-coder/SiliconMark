# Roadmap: SiliconMark

## v0.1.0, Initial Release (2026-06-15)
- [x] OllamaRuntime (HTTP API)
- [x] GGUFRuntime (llama-cpp-python + Metal)
- [x] MLCRuntime (MLC-LLM)
- [x] MetricsCollector (psutil)
- [x] Apple powermetrics integration (tokens/s, RAM, power, ANE, temperature)
- [x] JSON + CSV output
- [x] CLI

## v0.2.0, Planned
- [ ] Comparison mode: benchmark multiple models side-by-side
- [ ] HTML report with charts
- [ ] Warm-up runs configurable
- [ ] Batch prompt support

## v0.3.0, Planned
- [ ] LM Studio runtime support
- [ ] GPU memory tracking (Metal Performance Shaders)
- [ ] Model registry (auto-fetch popular GGUF models)

## v1.0.0, Target
- [ ] CI benchmark mode (non-interactive, exit code on regression)
- [ ] Full test coverage
- [ ] PyPI release

## Dual-Licensing Readiness

Assessed 2026-07-11: Community-only, not a Dual-Licensing candidate. SiliconMark is a developer/researcher benchmarking CLI, the same category as tools like hyperfine, which conventionally stay fully open source. No team, multi-tenant or enterprise dimension exists anywhere on the roadmap; the planned monetization path (PyPI release, v1.0.0) is a standard distribution channel, not an open-core split. Revisit only if a genuine team/CI-fleet benchmarking use case emerges.
