"""Pydantic data models for benchmark results."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AppleMetrics(BaseModel):
    cpu_power_mw: float | None = None
    gpu_power_mw: float | None = None
    ane_power_mw: float | None = None
    package_power_mw: float | None = None
    cpu_die_temp_celsius: float | None = None


class SystemMetrics(BaseModel):
    ram_used_gb_mean: float
    ram_used_gb_peak: float
    ram_percent_mean: float
    cpu_percent_mean: float
    apple: AppleMetrics = Field(default_factory=AppleMetrics)


class PerformanceMetrics(BaseModel):
    tokens_per_second: float
    time_to_first_token_ms: float | None = None
    total_tokens: int
    total_duration_s: float
    prompt_tokens: int | None = None


class ModelInfo(BaseModel):
    name: str
    path: str | None = None
    size_gb: float | None = None
    quantization: str | None = None
    context_length: int | None = None


class BenchmarkConfig(BaseModel):
    runtime: str
    model: ModelInfo
    prompt: str
    max_tokens: int
    num_runs: int = 1
    warmup: bool = True


class BenchmarkResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: datetime = Field(default_factory=datetime.now)
    device: str
    config: BenchmarkConfig
    performance: PerformanceMetrics
    system: SystemMetrics


class BenchmarkSuite(BaseModel):
    """Collection of results from a multi-runtime or multi-model run."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    device: str
    results: list[BenchmarkResult] = Field(default_factory=list)
