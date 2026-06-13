<div align="center">
  <img src="RayStudio.png" alt="RayStudio Logo" width="120"/>
  <h1>SiliconMark</h1>
</div>

[🇬🇧 English Version](README.md)

**Apple Silicon LLM Benchmark Suite — Token/s, RAM, Leistung, ANE · Ollama · llama.cpp · MLC · GGUF**

SiliconMark misst die Inferenz-Performance lokaler LLM-Runtimes auf Apple Silicon — Token/s, RAM-Verbrauch, Energiebedarf, ANE-Aktivität und Temperatur, alles über ein einziges CLI.

---

## Funktionen

| Funktion | Beschreibung |
|---|---|
| **Runtimes** | Ollama · llama.cpp Server · MLC-LLM · Direktes GGUF (llama-cpp-python) |
| **Metriken** | Token/s · Zeit bis zum ersten Token · RAM (Mittelwert & Peak) · CPU-Auslastung |
| **Apple-spezifisch** | Package / CPU / GPU / ANE-Leistung (mW) · CPU-Die-Temperatur |
| **Export** | Strukturiertes JSON — eine Datei pro Benchmark-Lauf |
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

**Author:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Active · **Last Updated:** Juni 2026
