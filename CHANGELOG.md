# Changelog: SiliconMark

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.9] - 2026-07-17

### Changed
- CI: added an explicit `permissions: contents: read` block to the workflow(s) that were missing one (CodeQL `actions/missing-workflow-permissions`), narrowing the default GITHUB_TOKEN scope.

## [0.1.8] - 2026-07-13

### Added

- README.de.md was missing 7 whole sections that README.md has (Installation, CLI Reference, JSON Result Schema, Runtime Setup, Adding a Custom Runtime, Project Structure, Development) and its remaining content was stale (referenced a removed `--all` flag and an old `benchmark` subcommand name). Fully rewritten to match README.md.

### Fixed

- Fixed a formatting bug in the "run" CLI reference table (`--model-path` showed a stray semicolon instead of a "no default" marker), in both languages.

## [0.1.7] - 2026-07-12

### Added

- Release workflow (`release.yml`) building a wheel and sdist via `python -m build` and attaching them to a GitHub Release on every `v*` tag push. Previously releases were tag-only with no installable artifact.
- `pip-audit` step in CI.

### Fixed

- README installation instructions replaced with `pip install git+https://github.com/9t29zhmwdh-coder/SiliconMark.git` (no clone required, always the latest commit); fixed an incorrect lowercase repo URL in the previous instructions. Editable clone install kept as the documented path for development.
- Pinned `actions/checkout` and `actions/setup-python` in `ci.yml` to a commit SHA instead of a mutable tag, per the portfolio's supply-chain integrity standard.

## [0.1.6] - 2026-07-11

### Fixed

- Removed an eszett and em-dashes across the repo (LICENSE, TEMPLATE_NOTES.md, ARCHITECTURE.md, SKELETON.md, GETTING_STARTED.md, CONTRIBUTING.md, and the dashboard's index.html). Swiss German orthography.

## [0.1.5] - 2026-07-11

### Added

- Documented Dual-Licensing assessment (Community-only) in ROADMAP.md.

### Fixed

- Removed em-dashes from ROADMAP.md and SECURITY.md.

## [0.1.4] - 2026-07-11

### Fixed

- Updated actions/checkout and actions/setup-python to their latest major versions in CI, since GitHub is deprecating the Node.js 20 runtime and older action versions were being forced onto Node 24 and crashing during post-run cleanup.

## [0.1.3] - 2026-07-11

### Added

- Added a real dashboard screenshot to README.md/README.de.md (docs/screenshot.png), captured from the actual FastAPI/Chart.js web dashboard

### Fixed

- Removed em-dashes from module docstrings and CLI help text across the codebase, replaced with colons or plain commas
- Fixed a broken sentence in README.de.md (missing "Token/s, RAM-Verbrauch" text)

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
