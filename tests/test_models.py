"""Smoke-tests for core data models and helpers."""

from datetime import datetime

import pytest

from siliconmark.core.models import (
    AppleMetrics,
    BenchmarkConfig,
    BenchmarkResult,
    ModelInfo,
    PerformanceMetrics,
    SystemMetrics,
)
from siliconmark.metrics.collector import CollectorResult, MetricsSample
from siliconmark.runtimes.base import BaseRuntime, InferenceResult


# ── models ────────────────────────────────────────────────────────────────────

def _make_result() -> BenchmarkResult:
    return BenchmarkResult(
        device="Apple M4 Pro (24 GB)",
        config=BenchmarkConfig(
            runtime="ollama",
            model=ModelInfo(name="llama3.2:3b"),
            prompt="Hello",
            max_tokens=50,
        ),
        performance=PerformanceMetrics(
            tokens_per_second=45.3,
            total_tokens=50,
            total_duration_s=1.1,
        ),
        system=SystemMetrics(
            ram_used_gb_mean=8.2,
            ram_used_gb_peak=9.1,
            ram_percent_mean=34.0,
            cpu_percent_mean=18.5,
        ),
    )


def test_result_roundtrip():
    r = _make_result()
    json_str = r.model_dump_json()
    r2 = BenchmarkResult.model_validate_json(json_str)
    assert r2.performance.tokens_per_second == r.performance.tokens_per_second
    assert r2.device == r.device


def test_result_id_unique():
    r1, r2 = _make_result(), _make_result()
    assert r1.id != r2.id


def test_apple_metrics_defaults():
    a = AppleMetrics()
    assert a.cpu_power_mw is None
    assert a.ane_power_mw is None


# ── collector ─────────────────────────────────────────────────────────────────

def test_collector_result_stats():
    cr = CollectorResult(samples=[
        MetricsSample(timestamp=0, ram_used_gb=8.0, ram_percent=33, cpu_percent=20),
        MetricsSample(timestamp=1, ram_used_gb=9.0, ram_percent=37, cpu_percent=40),
    ])
    assert cr.ram_used_gb_mean == pytest.approx(8.5)
    assert cr.ram_used_gb_peak == pytest.approx(9.0)
    assert cr.cpu_percent_mean == pytest.approx(30.0)


def test_collector_empty():
    cr = CollectorResult()
    assert cr.ram_used_gb_mean == 0.0
    assert cr.ram_used_gb_peak == 0.0


# ── runtime base ──────────────────────────────────────────────────────────────

def test_to_performance_metrics():
    class _DummyRuntime(BaseRuntime):
        name = "dummy"
        def infer(self, prompt, max_tokens):
            return InferenceResult(50, 1.0, 80.0, 10, "hi")

    rt = _DummyRuntime(ModelInfo(name="test"))
    inf = InferenceResult(100, 2.0, 120.0, 20, "response")
    pm = rt.to_performance_metrics(inf)
    assert pm.tokens_per_second == pytest.approx(50.0)
    assert pm.total_tokens == 100
