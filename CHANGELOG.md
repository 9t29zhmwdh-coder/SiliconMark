# Changelog: SiliconMark

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.4] - 2026-09-30

### Changed

Dependency and CI updates merged since v1.1.3, each with green checks:

- chore(ci): bump the actions group with 3 updates (#43)

---

## [1.1.3] - 2026-09-27

### Security

- The editable install in CI now runs with `--no-build-isolation`, so the build backend pinned in `requirements/ci.txt` builds it. Before, pip fetched a fresh, unpinned backend into an isolated environment for that one step, which undercut the hash-pinned installs from v1.1.2.
- `editables` joins the lock, since hatchling needs it for editable installs once build isolation is off.
- Workflows call `python -m pip` rather than `pip`, because `pip.exe` cannot replace itself on Windows when the lock pins a newer pip.

---

## [1.1.2] - 2026-09-27

### Security

- Every package the CI and the release build install now comes from `requirements/ci.txt` with its hash checked (`pip install --require-hashes`). Before, `pip install -e ".[dev]"`, `pip install pip-audit` and `pip install build` took whatever version the index served at that moment, which OpenSSF Scorecard scored 3 of 10 for pinned dependencies. The package itself is installed with `--no-deps`, and the wheel is built with `--no-isolation` so the build backend is the pinned `hatchling` rather than a fresh download.
- CI checks that `requirements/ci.txt` still matches `pyproject.toml`, starting from the committed pins, so a changed dependency cannot slip past the lock.

---

## [1.1.1] - 2026-09-27

### Security

- `SECURITY.md` links GitHub's private advisory form in full. The link was missing or relative, so OpenSSF Scorecard found no reporting channel and scored the policy 4 of 10.
- The supported-versions table named a version line that is no longer current; it now says that the latest release gets security fixes.

### Changed

Dependency updates merged since v1.1.0:

- chore(deps): bump ruff from 0.16.0 to 0.16.1 in the python group (#36)

---

## [1.1.0] - 2026-09-26

### Changed

- Thermal pressure replaces the CPU die temperature. `powermetrics` on Apple Silicon reports no die temperature at all, only macOS's thermal pressure level, so `cpu_die_temp_celsius` was `null` on every supported machine. Runs now record the worst level reached (Nominal, Moderate, Heavy, Trapping) as `thermal_pressure` in the JSON, the terminal summary and the dashboard. Result files from older versions still load.
- The RAM figures are labelled as what they are: system RAM in use during the run, not the model's own footprint.

### Fixed

- `list-runtimes` promised to show what is usable but listed every runtime alike. It now checks each one: Ollama and the llama.cpp server have to answer, MLC and llama-cpp-python have to be importable.
- `list-runtimes` dropped `[gguf]` from `pip install siliconmark[gguf]`, because the terminal renderer read it as a formatting tag.
- The version was out of step: `pyproject.toml` said 1.0.8 and `siliconmark.__version__` 0.1.5. Both now say 1.1.0.

### Security

- The README no longer recommends a permanent passwordless `sudo` rule for `powermetrics`. `powermetrics` can write its output to any file as root, so the rule is now set up for a benchmark session in `/etc/sudoers.d/` and removed afterwards.

Verified on an M4 Pro with Ollama and `qwen2.5:0.5b`: power values and a thermal pressure of "Nominal" recorded, `list-runtimes` marks Ollama usable and the others not, the dashboard shows the new column.

---

## [1.0.9] - 2026-08-04

### Fixed

- The release workflow no longer fails when the release for a tag already exists. It called `gh release create` unconditionally and aborted with `a release with the same tag name already exists` whenever the release had come about some other way. The build had succeeded by then; only the step after it went red. In repositories that attach binaries the release was left with nothing to download, which is the same failure wearing a friendlier face.

---

## [1.0.8] - 2026-07-31

### Fixed

- The supported-versions table in `SECURITY.md` still listed `0.1.x`, a release line that no longer exists. Somebody reporting a vulnerability reads that table first, and it told them the current release was out of scope. It lists `1.0.x`.

---

## [1.0.7] - 2026-07-31

### Changed

- Both READMEs now open with the question that sends someone here, which is whether a model will actually run on their Mac before they spend an hour downloading it, rather than naming the metric list. The four commands follow directly, and a short paragraph says that comparing Macs you do not own is what published benchmark tables are for.

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
