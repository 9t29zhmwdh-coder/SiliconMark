"""JSON export and import for benchmark results."""

from __future__ import annotations

import json
from pathlib import Path

from siliconmark.core.models import BenchmarkResult, BenchmarkSuite


def export_result(result: BenchmarkResult, output_dir: Path) -> Path:
    """Save a single BenchmarkResult as JSON. Returns the written path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = result.timestamp.strftime("%Y%m%d_%H%M%S")
    model_slug = result.config.model.name.replace(":", "_").replace("/", "_")
    fname = f"{result.config.runtime}_{model_slug}_{ts}.json"
    path = output_dir / fname
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return path


def export_suite(suite: BenchmarkSuite, output_dir: Path) -> Path:
    """Save a BenchmarkSuite (multiple results) as a single JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = suite.timestamp.strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"suite_{suite.id}_{ts}.json"
    path.write_text(suite.model_dump_json(indent=2), encoding="utf-8")
    return path


def load_results(results_dir: Path) -> list[BenchmarkResult]:
    """Load all result JSON files from a directory (single results and suites)."""
    results: list[BenchmarkResult] = []
    for p in sorted(results_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if "results" in data:
                results.extend(BenchmarkSuite.model_validate(data).results)
            else:
                results.append(BenchmarkResult.model_validate(data))
        except Exception:
            continue
    return results
