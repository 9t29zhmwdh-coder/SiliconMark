# Skeleton — SiliconMark

This file documents the repository structure and CI expectations for contributors.

## Repository Layout

```
SiliconMark/
├── siliconmark/
│   ├── cli.py
│   ├── runtimes/
│   ├── metrics/
│   ├── benchmark.py
│   └── output.py
├── tests/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── pyproject.toml
├── ARCHITECTURE.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── PRIVACY.md
├── ROADMAP.md
├── SECURITY.md
└── SKELETON.md
```

## CI Expectations

- `ruff check .` — must pass
- `ruff format --check .` — must pass
- `pytest` — must pass
- Type hints maintained throughout

## Branch Strategy

- `main` — stable, tagged releases
- `dev` — integration branch
- Feature branches: `feat/<name>`
