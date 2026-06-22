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
from siliconmark.metrics.apple import PowermetricsSession
from siliconmark.metrics.collector import MetricsCollector

console = Console()


def get_device_name() -> str:
    try:
        out = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True,
            text=True,
            timeout=5,
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

        return round(psutil.virtual_memory().total / 1024**3)
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
        task = progress.add_task(f"Loading {config.runtime} / {config.model.name}…", total=None)

        if config.warmup:
            progress.update(task, description=f"Warming up {config.runtime}…")
        runtime.prepare()

        best_inference = None
        best_sys = None
        best_apple_snap = None

        for run_idx in range(config.num_runs):
            collector = MetricsCollector(interval_s=0.5)
            collector.start()

            progress.update(
                task,
                description=(
                    f"Run {run_idx + 1}/{config.num_runs} — "
                    f"{config.max_tokens} tokens via {config.runtime}…"
                ),
            )

            # Start power sampling before inference and stop after — captures the full
            # inference window regardless of duration, then averages all collected samples.
            apple_session = PowermetricsSession(sample_interval_ms=200)
            apple_session.start()
            inference = runtime.infer(config.prompt, config.max_tokens)
            apple_snap = apple_session.stop()

            sys_result = collector.stop()

            tps = inference.tokens_generated / max(inference.total_duration_s, 1e-9)
            best_tps = (
                best_inference.tokens_generated / max(best_inference.total_duration_s, 1e-9)
                if best_inference
                else -1.0
            )
            if tps > best_tps:
                best_inference = inference
                best_sys = sys_result
                best_apple_snap = apple_snap

        runtime.cleanup()

    return BenchmarkResult(
        device=device,
        config=config,
        performance=runtime.to_performance_metrics(best_inference),
        system=SystemMetrics(
            ram_used_gb_mean=best_sys.ram_used_gb_mean,
            ram_used_gb_peak=best_sys.ram_used_gb_peak,
            ram_percent_mean=best_sys.ram_percent_mean,
            cpu_percent_mean=best_sys.cpu_percent_mean,
            apple=AppleMetrics(
                cpu_power_mw=best_apple_snap.cpu_power_mw,
                gpu_power_mw=best_apple_snap.gpu_power_mw,
                ane_power_mw=best_apple_snap.ane_power_mw,
                package_power_mw=best_apple_snap.package_power_mw,
                cpu_die_temp_celsius=best_apple_snap.cpu_die_temp_celsius,
            ),
        ),
    )
