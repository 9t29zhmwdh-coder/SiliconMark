"""Background system metrics collector — samples RAM and CPU at a fixed interval."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

import psutil


@dataclass
class MetricsSample:
    timestamp: float
    ram_used_gb: float
    ram_percent: float
    cpu_percent: float


@dataclass
class CollectorResult:
    samples: list[MetricsSample] = field(default_factory=list)

    @property
    def ram_used_gb_mean(self) -> float:
        return _mean([s.ram_used_gb for s in self.samples])

    @property
    def ram_used_gb_peak(self) -> float:
        return max((s.ram_used_gb for s in self.samples), default=0.0)

    @property
    def ram_percent_mean(self) -> float:
        return _mean([s.ram_percent for s in self.samples])

    @property
    def cpu_percent_mean(self) -> float:
        return _mean([s.cpu_percent for s in self.samples])


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


class MetricsCollector:
    """Daemon thread that polls psutil every `interval_s` seconds."""

    def __init__(self, interval_s: float = 0.5) -> None:
        self._interval = interval_s
        self._result = CollectorResult()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        self._stop_event.clear()
        self._result = CollectorResult()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> CollectorResult:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
        return self._result

    def _run(self) -> None:
        while not self._stop_event.is_set():
            vm = psutil.virtual_memory()
            self._result.samples.append(MetricsSample(
                timestamp=time.time(),
                ram_used_gb=round(vm.used / 1024 ** 3, 3),
                ram_percent=vm.percent,
                cpu_percent=psutil.cpu_percent(interval=None),
            ))
            time.sleep(self._interval)
