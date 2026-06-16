# Privacy Policy — SiliconMark

SiliconMark runs **fully locally** on your Apple Silicon machine.

## What data is processed

- LLM inference prompts and responses — used only for benchmark measurements, not stored permanently
- System metrics: CPU/GPU/ANE usage, RAM, power draw, temperature — read via psutil and Apple powermetrics

## What data leaves your machine

**Nothing.** All benchmarks run against local runtimes (Ollama, llama.cpp/GGUF, MLC-LLM).
No metrics, prompts, or results are transmitted to external servers.

## Storage

- Benchmark results are saved to local JSON/CSV files in the working directory
- No database or background service is installed

## Third-party services

None. SiliconMark does not use cloud services, analytics, or telemetry.

## Changes

This policy may be updated with new releases. Check the CHANGELOG for details.
