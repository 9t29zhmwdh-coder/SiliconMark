"""Apple Silicon power & thermal metrics via powermetrics (requires passwordless sudo)."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass


@dataclass
class ApplePowerSnapshot:
    cpu_power_mw: float | None = None
    gpu_power_mw: float | None = None
    ane_power_mw: float | None = None
    package_power_mw: float | None = None
    cpu_die_temp_celsius: float | None = None


class PowermetricsSession:
    """Continuous powermetrics process spanning the full inference duration.

    Start before inference, stop after. Averages all collected samples.
    Requires passwordless sudo. Returns empty snapshot if unavailable.
    """

    def __init__(self, sample_interval_ms: int = 200) -> None:
        self._interval = sample_interval_ms
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]

    def start(self) -> None:
        try:
            self._proc = subprocess.Popen(
                [
                    "sudo",
                    "-n",
                    "powermetrics",
                    "--samplers",
                    "cpu_power,gpu_power,thermal",
                    "-i",
                    str(self._interval),
                    "-n",
                    "9999",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        except (FileNotFoundError, PermissionError):
            self._proc = None

    def stop(self) -> ApplePowerSnapshot:
        if self._proc is None:
            return ApplePowerSnapshot()
        self._proc.terminate()
        try:
            out, _ = self._proc.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            out, _ = self._proc.communicate()
        return _parse_averaged(out)


def sample_powermetrics(duration_ms: int = 1000) -> ApplePowerSnapshot:
    """Spawn powermetrics for one sample and parse the result.

    Requires passwordless sudo. Returns empty snapshot if unavailable.
    """
    try:
        result = subprocess.run(
            [
                "sudo",
                "-n",
                "powermetrics",
                "--samplers",
                "cpu_power,gpu_power,thermal",
                "-i",
                str(duration_ms),
                "-n",
                "1",
            ],
            capture_output=True,
            text=True,
            timeout=duration_ms / 1000 + 5,
        )
        if result.returncode != 0:
            return ApplePowerSnapshot()
        return _parse_averaged(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return ApplePowerSnapshot()


def _parse_averaged(raw: str) -> ApplePowerSnapshot:
    """Parse one or more powermetrics sample blocks and return averaged values."""

    def _avg(vals: list[float]) -> float | None:
        return sum(vals) / len(vals) if vals else None

    cpu_vals = [float(m) for m in re.findall(r"^CPU Power:\s+([\d.]+)\s+mW", raw, re.MULTILINE)]
    gpu_vals = [float(m) for m in re.findall(r"^GPU Power:\s+([\d.]+)\s+mW", raw, re.MULTILINE)]
    ane_vals = [float(m) for m in re.findall(r"^ANE Power:\s+([\d.]+)\s+mW", raw, re.MULTILINE)]
    pkg_vals = [
        float(m) for m in re.findall(r"^Combined Power[^:]*:\s+([\d.]+)\s+mW", raw, re.MULTILINE)
    ]
    temp_vals = [
        float(m)
        for m in re.findall(
            r"CPU die temperature:\s+([\d.]+)\s+C", raw, re.MULTILINE | re.IGNORECASE
        )
    ]

    cpu_avg = _avg(cpu_vals)
    gpu_avg = _avg(gpu_vals)
    ane_avg = _avg(ane_vals)
    pkg_avg = _avg(pkg_vals)

    if pkg_avg is None and any(v is not None for v in [cpu_avg, gpu_avg, ane_avg]):
        pkg_avg = sum(v for v in [cpu_avg, gpu_avg, ane_avg] if v is not None)

    return ApplePowerSnapshot(
        cpu_power_mw=cpu_avg,
        gpu_power_mw=gpu_avg,
        ane_power_mw=ane_avg,
        package_power_mw=pkg_avg,
        cpu_die_temp_celsius=_avg(temp_vals),
    )