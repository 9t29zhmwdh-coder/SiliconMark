# Changelog: SiliconMark

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.6] - 2026-07-29

### Security

- The release workflow no longer grants `contents: write` for its whole run. The permission moves to the one job that publishes the release, and everything else runs with `contents: read`. OpenSSF Scorecard scores the Token-Permissions check 0 out of 10 whenever any workflow holds a top-level write permission, regardless of how little of the run needs it, so this single line was what held the check at zero.

---

## [1.0.5] - 2026-07-29

### Changed

Dependency and workflow updates merged since 1.0.4:

- chore(ci): bump the actions group across 1 directory with 4 updates

---

## [1.0.4] - 2026-07-28

### Changed

- CodeQL moved from GitHub's default setup to an advanced setup with a committed `.github/workflows/codeql.yml`. The default setup skips pull requests that touch no code of a given language, so a dependency pull request changing only a lock file reported `skipping` on the required `Analyze (...)` checks forever and could never be merged. The workflow runs on every pull request regardless of what changed and uses the `security-extended` query suite, which the default setup does not allow choosing. Required checks are unchanged.
- The CodeQL job requests only `security-events: write` beyond the workflow-level `contents: read`. Repeating read grants at job level is what OpenSSF Scorecard counts as excessive token permissions, and it costs the full `Token-Permissions` score.
- Dependabot now groups only minor and patch updates per ecosystem; majors arrive as individual pull requests. The previous grouping bundled breaking changes with urgently needed security patches into one unreviewable diff. Actions stay grouped wholesale. Follows `engineering-standards` v0.11.0.

## [1.0.3] - 2026-07-28

### Fixed

- CI went red without a single source change. `ruff` was declared as `>=0.4`, so the runner picked up 0.16.0, and that release **widened ruff's default rule set**. This repository configures no `select` at all, so it inherits whatever the default happens to be. 21 findings appeared from rules that were simply not part of the default before.
- Blind `except Exception` in `core/runner.py` and `exporters/json_exporter.py` replaced with the exceptions that can actually occur there (`ImportError`/`OSError` for the optional psutil import, `OSError`/`JSONDecodeError`/`ValidationError` for result file parsing). This also resolves the S112 finding about silently swallowing errors, at the cause rather than by adding a logger to a project that has none.
- `subprocess.run` calls now pass `check=False` explicitly. The default was already `False`, so behaviour is unchanged; the call now states its intent.
- 11 `Optional[X]` annotations converted to `X | None`, plus one unsorted import block and two files reformatted.

### Changed

- `ruff` is pinned to 0.16.0 instead of `>=0.4`, per `engineering-standards` v0.7.0. Without the pin the next default-set change repeats this.
- `B008` is configured away for `typer.Option`, `typer.Argument` and `Path.home` via `extend-immutable-calls`. Passing typer objects as argument defaults is the documented typer API, not an oversight, and "fixing" it would break the CLI.

## [1.0.2] - 2026-07-28

### Added

- `.github/dependabot.yml`, with grouped weekly updates. The file was missing, and without it there are no version updates at all: repository security alerts only fire for disclosed vulnerabilities, which is how action pins across this portfolio quietly went stale. Follows `engineering-standards` v0.10.0.

### Fixed

- `actions/checkout` pins now carry the full version in the comment instead of a bare major, and all workflows use the same SHA.

## [1.0.1] - 2026-07-20

### Changed

- OpenSSF Scorecard workflow and badge.
- `copilot-instructions.md` for consistent AI-assisted contributions.
- Split the README's security/CI badges onto their own line, separate from the platform/tech/AI badges (they were rendering as a single merged line).

## [1.0.0] - 2026-07-17

First stable release: a real, installable distribution (a real PyPI-style
wheel/sdist, attached to every GitHub Release) already exists for end
users, the prerequisite for a 1.0 release per this portfolio's own
SemVer discipline.

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
