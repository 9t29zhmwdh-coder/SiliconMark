<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>

  <h1>SiliconMark</h1>
</div>

**Apple Silicon LLM Benchmark Suite**

Measure real-world inference performance of local LLM runtimes on Apple Silicon: Token/s, RAM usage, power draw, ANE activity and temperature, all from one CLI.

[![CI](https://github.com/9t29zhmwdh-coder/SiliconMark/actions/workflows/ci.yml/badge.svg)](https://github.com/9t29zhmwdh-coder/SiliconMark/actions) ![Apple Silicon](https://img.shields.io/badge/Apple-Silicon-000000?logo=apple&logoColor=white) ![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?logo=apple&logoColor=black) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![AI | Claude Code](https://img.shields.io/badge/AI-Claude_Code-black?logo=anthropic&logoColor=white) ![AI | Copilot](https://img.shields.io/badge/AI-Copilot-black?logo=github&logoColor=white) ![AI | Ollama](https://img.shields.io/badge/AI-Ollama-black?logo=ollama&logoColor=white)
[![CI](https://github.com/9t29zhmwdh-coder/SiliconMark/actions/workflows/ci.yml/badge.svg)](https://github.com/9t29zhmwdh-coder/SiliconMark/actions/workflows/ci.yml)


---

## Features

| | |
|---|---|
| **Runtimes** | Ollama · llama.cpp server · MLC-LLM · Direct GGUF (llama-cpp-python) |
| **Metrics** | Token/s · Time-to-first-token · RAM (mean & peak) · CPU usage |
| **Apple-specific** | Package / CPU / GPU / ANE power (mW) · CPU die temperature |
| **Export** | Structured JSON: one file per run |
| **Dashboard** | Web UI with Chart.js charts: `siliconmark dashboard` |
| **Extensible** | Add a new runtime in ~40 lines by subclassing `BaseRuntime` |

> **Power metrics** require `sudo powermetrics` without a password prompt.  
> See [Enabling Power Metrics](#enabling-power-metrics).

---

## Requirements

- macOS 13+ on Apple Silicon (M1 / M2 / M3 / M4)
- Python 3.11+

---

## Installation

```bash
# Clone and install in editable mode
git clone https://github.com/9t29zhmwdh-coder/siliconmark.git
cd siliconmark
pip install -e .

# Optional: GGUF support (llama-cpp-python with Metal)
pip install -e ".[gguf]"
```

---

## Quick Start

```bash
# Benchmark Ollama
siliconmark run --runtime ollama --model llama3.2:3b

# Benchmark llama.cpp server
siliconmark run --runtime llamacpp --model llama3.2 --tokens 300

# Benchmark a GGUF file directly
siliconmark run --runtime gguf --model llama3.2 --model-path ~/models/llama3.2-3b.Q4_K_M.gguf

# Open the visual dashboard
siliconmark dashboard --results ./results
```

---

## CLI Reference

```
Usage: siliconmark [OPTIONS] COMMAND [ARGS]...

Commands:
  run             Run a benchmark (runtime + model)
  dashboard       Launch the web dashboard
  list-runtimes   Show all available runtimes
  device          Print the detected Apple Silicon chip
```

### `siliconmark run`

| Option | Default | Description |
|--------|---------|-------------|
| `--runtime` / `-r` | *(required)* | `ollama` · `llamacpp` · `mlc` · `gguf` |
| `--model` / `-m` | *(required)* | Model name (e.g. `llama3.2:3b`) |
| `--model-path` / `-p` |; | Path to `.gguf` file (gguf runtime only) |
| `--tokens` / `-t` | `200` | Number of tokens to generate |
| `--prompt` | *(default)* | Custom benchmark prompt |
| `--output` / `-o` | `./results` | Directory to save JSON results |
| `--no-warmup` | `false` | Skip the warmup inference call |

### `siliconmark dashboard`

| Option | Default | Description |
|--------|---------|-------------|
| `--results` / `-r` | `./results` | Results directory to load |
| `--host` | `127.0.0.1` | Bind address |
| `--port` / `-p` | `8080` | Port |

---

## JSON Result Schema

Every run saves a file to `./results/`:

```json
{
  "id": "a3f2c1b0",
  "timestamp": "2026-06-10T18:32:11",
  "device": "Apple M4 Pro (24 GB)",
  "config": {
    "runtime": "ollama",
    "model": { "name": "llama3.2:3b" },
    "max_tokens": 200,
    "warmup": true
  },
  "performance": {
    "tokens_per_second": 87.4,
    "time_to_first_token_ms": 312,
    "total_tokens": 200,
    "total_duration_s": 2.29,
    "prompt_tokens": 42
  },
  "system": {
    "ram_used_gb_mean": 8.21,
    "ram_used_gb_peak": 9.04,
    "ram_percent_mean": 34.2,
    "cpu_percent_mean": 18.7,
    "apple": {
      "cpu_power_mw": 3240,
      "gpu_power_mw": 1820,
      "ane_power_mw": 540,
      "package_power_mw": 5600,
      "cpu_die_temp_celsius": 48.3
    }
  }
}
```

---

## Runtime Setup

### Ollama

```bash
brew install ollama
ollama serve          # runs on localhost:11434
ollama pull llama3.2:3b
```

### llama.cpp server

```bash
brew install llama.cpp
llama-server -m ~/models/llama3.2-3b.Q4_K_M.gguf --port 8080
```

### GGUF (direct)

```bash
pip install "siliconmark[gguf]"
siliconmark run --runtime gguf --model my-model \
  --model-path ~/models/llama3.2-3b.Q4_K_M.gguf
```

### MLC-LLM

```bash
pip install mlc-llm
# See https://llm.mlc.ai for model downloads
```

---

## Enabling Power Metrics

Power and temperature metrics require passwordless `sudo` for `powermetrics`.

```bash
sudo visudo
# Add this line (replace YOUR_USERNAME):
YOUR_USERNAME ALL=(ALL) NOPASSWD: /usr/bin/powermetrics
```

If not configured, SiliconMark runs normally but Apple-specific fields will be `null`.

---

## Adding a Custom Runtime

1. Create `siliconmark/runtimes/myruntime.py`
2. Subclass `BaseRuntime` and implement `infer()`
3. Register it in `siliconmark/core/registry.py`

```python
# siliconmark/runtimes/myruntime.py
from siliconmark.runtimes.base import BaseRuntime, InferenceResult

class MyRuntime(BaseRuntime):
    name = "myruntime"

    def infer(self, prompt: str, max_tokens: int) -> InferenceResult:
        # ... call your runtime ...
        return InferenceResult(
            tokens_generated=n,
            total_duration_s=elapsed,
            time_to_first_token_ms=ttft,
            prompt_tokens=None,
            raw_response=text,
        )
```

```python
# siliconmark/core/registry.py  — add one line:
"myruntime": "siliconmark.runtimes.myruntime:MyRuntime",
```

---

## Project Structure

```
siliconmark/
├── cli.py                   # Typer CLI entry point
├── core/
│   ├── models.py            # Pydantic result models
│   ├── runner.py            # Benchmark orchestration + device detection
│   └── registry.py         # Runtime registry
├── runtimes/
│   ├── base.py              # Abstract BaseRuntime
│   ├── ollama.py            # Ollama REST adapter
│   ├── llamacpp.py          # llama.cpp server adapter
│   ├── mlc.py               # MLC-LLM adapter
│   └── gguf.py              # llama-cpp-python adapter
├── metrics/
│   ├── collector.py         # Background RAM/CPU sampler (threading)
│   └── apple.py             # powermetrics wrapper
├── exporters/
│   └── json_exporter.py     # JSON save/load
└── dashboard/
    ├── app.py               # FastAPI server
    └── static/index.html    # Chart.js dashboard UI
```

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

---

---

**Author:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Active · v0.1.0 · **License:** MIT
