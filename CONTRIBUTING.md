<div align="center"><img src="RayStudio.png" alt="RayStudio Logo" width="120"/><h1>SiliconMark</h1></div>

> 🇬🇧 You are reading the English version. | 🇩🇪 [Deutsche Version](README.de.md)

# Contributing

## Prerequisites

- macOS on Apple Silicon (M1 or newer)
- Python 3.11+
- Passwordless `sudo powermetrics` for power metrics (optional but recommended)

## Dev Setup

```bash
git clone https://github.com/9t29zhmwdh-coder/SiliconMark.git
cd SiliconMark
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Linting & Formatting

```bash
ruff check .
ruff format .
```

Both must pass before opening a pull request.

## Commit Prefixes

| Prefix | Use |
|--------|-----|
| `feat:` | new feature |
| `fix:` | bug fix |
| `docs:` | documentation only |
| `chore:` | maintenance, deps |
| `refactor:` | code restructure, no behaviour change |

## Branch Strategy

- `main`: stable, tagged releases
- `dev`: integration branch
- Feature branches: `feat/<name>`

## Adding a Runtime

Subclass `BaseRuntime` in `siliconmark/runtimes/` and register it in `siliconmark/core/registry.py`. See existing adapters for reference.

---

**Author:** [Rafael Yilmaz](https://github.com/9t29zhmwdh-coder) · **Status:** Active · v0.1.0 · **License:** MIT
