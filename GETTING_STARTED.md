# Getting Started with SiliconMark

This guide is for people with **no coding experience**. It walks you through every step needed to run SiliconMark, from opening a terminal to seeing your first benchmark result.

> **Important:** SiliconMark only runs on **macOS with Apple Silicon** (M1/M2/M3/M4), because it reads Apple-specific hardware sensors (power draw, Neural Engine activity, CPU temperature). If you're on Windows or Linux, you cannot run SiliconMark directly on that machine: see the note at the end of this guide.

---

## Windows

SiliconMark cannot run natively on Windows: it depends on macOS-only tools (`powermetrics`) and Apple Silicon hardware counters. There is no workaround, this is a hard platform requirement, not a missing dependency.

If you want to try SiliconMark, you'll need access to a Mac with Apple Silicon. Skip ahead to the **macOS** section below and run the steps there.

---

## Linux

Same limitation as Windows: SiliconMark requires macOS on Apple Silicon and cannot run on Linux. Skip ahead to the **macOS** section below if you have access to a Mac.

---

## macOS

### 1. Open a terminal

Press `Cmd+Space` to open Spotlight, type `Terminal`, and press Enter.

### 2. Check your Python version

SiliconMark needs Python 3.11 or newer. Check what you have:

```bash
python3 --version
```

- If it prints `Python 3.11.x` or higher, you're set, continue to step 3.
- If it prints an older version, or `command not found: python3`, install a current Python:
  - Easiest: download the macOS installer from [python.org/downloads](https://www.python.org/downloads/) and run it.
  - Alternative, if you use [Homebrew](https://brew.sh): `brew install python@3.12`
- After installing, close and reopen Terminal, then re-run `python3 --version` to confirm.

### 3. Download SiliconMark

No-Git route:

1. Go to [github.com/9t29zhmwdh-coder/SiliconMark](https://github.com/9t29zhmwdh-coder/SiliconMark).
2. Click the green **Code** button → **Download ZIP**.
3. Extract it (double-click the ZIP in Finder), e.g. into your `Documents` folder.
4. In Terminal, move into the extracted folder:

```bash
cd ~/Documents/SiliconMark-main
```

(Adjust the folder name to whatever it was extracted as: GitHub ZIP downloads are usually named `<repo>-main`.)

Or, with Git:

```bash
git clone https://github.com/9t29zhmwdh-coder/siliconmark.git
cd siliconmark
```

### 4. Install SiliconMark

```bash
pip install -e .
```

This installs SiliconMark and its dependencies (uses your `python3`'s `pip`; if `pip install` isn't recognized, try `pip3 install -e .` or `python3 -m pip install -e .`).

If you also want to benchmark local `.gguf` model files directly (not just via Ollama), additionally run:

```bash
pip install -e ".[gguf]"
```

### 5. Install a runtime to benchmark

SiliconMark measures performance of an LLM runtime you already have installed: it doesn't include one itself. The simplest option is [Ollama](https://ollama.com):

```bash
brew install ollama
ollama serve
```

Leave that command running in this Terminal window, then open a **new** Terminal window (`Cmd+T` or `Cmd+N`) for the next steps, and pull a small model to test with:

```bash
ollama pull llama3.2:3b
```

### 6. Run your first benchmark

```bash
siliconmark run --runtime ollama --model llama3.2:3b
```

### 7. (Optional) View results in the dashboard

```bash
siliconmark dashboard --results ./results
```

Then open the URL it prints (typically `http://127.0.0.1:8080`) in your browser.

<!-- TODO: Screenshot of a completed benchmark run in the terminal -->

---

## What you should see

Running `siliconmark run --runtime ollama --model llama3.2:3b` prints live progress in the terminal, then a summary with tokens/second, time-to-first-token, and RAM usage. A JSON file with the full results is saved into `./results/`.

Apple-specific fields (power draw, CPU temperature) will show as `null` unless you've enabled passwordless `sudo` for `powermetrics`: see the "Enabling Power Metrics" section in the main [README.md](README.md) if you want those numbers too. This step is optional; SiliconMark works fine without it.

---

## A note for Windows and Linux users

If you don't have access to a Mac but want to explore what SiliconMark produces, ask the repository owner for a sample JSON result, or read the "JSON Result Schema" and "Features" sections in the main [README.md](README.md): they show exactly what a benchmark run captures.

---

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `command not found: python3` | Python isn't installed, or Terminal was opened before installing it | Install Python from [python.org](https://www.python.org/downloads/) or via `brew install python@3.12`, then open a **new** Terminal window |
| `command not found: siliconmark` after `pip install -e .` | The install succeeded but the command isn't on your `PATH`, common with certain Python installs | Try `python3 -m siliconmark.cli` instead, or re-check the `pip install -e .` output for a PATH warning near the end |
| `siliconmark run` fails with a connection error to Ollama | `ollama serve` isn't running, or finished/crashed | Open a Terminal window, run `ollama serve`, and leave it running while you use SiliconMark in another window |
| All Apple-specific fields (power, temperature) are `null` | Passwordless `sudo` for `powermetrics` isn't configured | This is optional and expected by default; follow "Enabling Power Metrics" in the main [README.md](README.md) if you want these values |
| `zsh: permission denied: ./scripts/...` or similar for any shell script | Script lacks the executable bit | Run `chmod +x path/to/script.sh` once, then try again |
