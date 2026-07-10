<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>
  <h1>SiliconMark</h1>
</div>

[![CI](https://github.com/9t29zhmwdh-coder/SiliconMark/actions/workflows/ci.yml/badge.svg)](https://github.com/9t29zhmwdh-coder/SiliconMark/actions) ![Apple Silicon](https://img.shields.io/badge/Apple-Silicon-000000?logo=apple&logoColor=white) ![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?logo=apple&logoColor=black) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![AI | Claude Code](https://img.shields.io/badge/AI-Claude_Code-black?logo=anthropic&logoColor=white) ![AI | Copilot](https://img.shields.io/badge/AI-Copilot-black?logo=github&logoColor=white) ![AI | Ollama](https://img.shields.io/badge/AI-Ollama-black?logo=ollama&logoColor=white)

[🇬🇧 English Version](README.md)

**Apple Silicon LLM Benchmark Suite: Token/s, RAM, Leistung, ANE · Ollama · llama.cpp · MLC · GGUF**

SiliconMark misst die Inferenz-Performance lokaler LLM-Runtimes auf Apple Silicon:brauch, Energiebedarf, ANE-Aktivität und Temperatur, alles über ein einziges CLI.

---

> 🌱 Neu hier? → [Schritt-für-Schritt-Anleitung für Einsteiger](GETTING_STARTED.md)

---

## Funktionen

| Funktion | Beschreibung |
|---|---|
| **Runtimes** | Ollama · llama.cpp Server · MLC-LLM · Direktes GGUF (llama-cpp-python) |
| **Metriken** | Token/s · Zeit bis zum ersten Token · RAM (Mittelwert & Peak) · CPU-Auslastung |
| **Apple-spezifisch** | Package / CPU / GPU / ANE-Leistung (mW) · CPU-Die-Temperatur |
| **Export** | Strukturiertes JSON: eine Datei pro Benchmark-Lauf |
| **Dashboard** | Web-UI mit Chart.js · `siliconmark dashboard` |
| **Erweiterbar** | Neue Runtime in ~40 Zeilen via `BaseRuntime`-Subklasse |

> **Leistungsmetriken** benötigen `sudo powermetrics` ohne Passwort-Prompt.

---

## Voraussetzungen

- macOS mit Apple Silicon (M1/M2/M3/M4)
- Python 3.11+
- Mindestens eine unterstützte Runtime (Ollama empfohlen)

---

## Schnellstart

```bash
git clone https://github.com/9t29zhmwdh-coder/SiliconMark
cd SiliconMark
pip install -e .

# Ollama benchmarken
siliconmark benchmark --runtime ollama --model llama3

# llama.cpp Server benchmarken
siliconmark benchmark --runtime llamacpp --model /path/to/model.gguf

# Alle Runtimes
siliconmark benchmark --all

# Dashboard starten
siliconmark dashboard
```

---

## Energiemetriken aktivieren

```bash
sudo visudo
# Zeile hinzufügen:
# username ALL=(ALL) NOPASSWD: /usr/bin/powermetrics
```

---

**Autor:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Active · ![version](https://img.shields.io/github/v/release/9t29zhmwdh-coder/SiliconMark?color=6b7280&style=flat-square) · **Lizenz:** MIT
