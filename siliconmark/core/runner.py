"""BenchmarkRunner — orchestrates a full run with metrics collection."""

from __future__ import annotations

import platform
import subprocess

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from siliconmark.core.models import (
    AppleMetrics,
    BenchmarkConfig,
    BenchmarkResult,
    SystemMetrics,
)
from siliconmark.core.registry import get_runtime
from siliconmark.metrics.apple import sample_powermetrics
from siliconmark.metrics.collector import MetricsCollector

console = Console()


def get_device_name() -> str:
    try:
        out = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if out:
            ram = _total_ram_gb()
            return f"{out} ({ram} GB)" if ram else out
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return platform.processor() or platform.machine()


def _total_ram_gb() -> int | None:
    try:
        import psutil
        return round(psutil.virtual_memory().total / 1024 ** 3)
    except Exception:
        return None


def run_benchmark(config: BenchmarkConfig) -> BenchmarkResult:
    device = get_device_name()
    runtime_cls = get_runtime(config.runtime)
    runtime = runtime_cls(config.model)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"Loading {config.runtime} / {config.model.name}…", total=None
        )

        if config.warmup:
            progress.update(task, description=f"Warming up {config.runtime}…")
            runtime.prepare()

        collector = MetricsCollector(interval_s=0.5)
        collector.start()

        progress.update(
            task,
            description=f"Generating {config.max_tokens} tokens via {config.runtime}…",
        )
        inference = runtime.infer(config.prompt, config.max_tokens)

        sys_result = collector.stop()
        runtime.cleanup()

    apple_snap = sample_powermetrics(duration_ms=500)

    return BenchmarkResult(
        device=device,
        config=config,
        performance=runtime.to_performance_metrics(inference),
        system=SystemMetrics(
            ram_used_gb_mean=sys_result.ram_used_gb_mean,
            ram_used_gb_peak=sys_result.ram_used_gb_peak,
            ram_percent_mean=sys_result.ram_percent_mean,
            cpu_percent_mean=sys_result.cpu_percent_mean,
            apple=AppleMetrics(
                cpu_power_mw=apple_snap.cpu_power_mw,
                gpu_power_mw=apple_snap.gpu_power_mw,
                ane_power_mw=apple_snap.ane_power_mw,
                package_power_mw=apple_snap.package_power_mw,
                cpu_die_temp_celsius=apple_snap.cpu_die_temp_celsius,
            ),
        ),
    )
