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


def sample_powermetrics(duration_ms: int = 1000) -> ApplePowerSnapshot:
    """
    Spawn powermetrics for one sample and parse the result.
    Requires `sudo powermetrics` without a password prompt (NOPASSWD in sudoers).
    Returns an empty snapshot if unavailable — callers must treat None as "not measured".
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
        return _parse(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return ApplePowerSnapshot()


def _parse(raw: str) -> ApplePowerSnapshot:
    snap = ApplePowerSnapshot()

    m = re.search(r"^CPU Power:\s+([\d.]+)\s+mW", raw, re.MULTILINE)
    if m:
        snap.cpu_power_mw = float(m.group(1))

    m = re.search(r"^GPU Power:\s+([\d.]+)\s+mW", raw, re.MULTILINE)
    if m:
        snap.gpu_power_mw = float(m.group(1))

    m = re.search(r"^ANE Power:\s+([\d.]+)\s+mW", raw, re.MULTILINE)
    if m:
        snap.ane_power_mw = float(m.group(1))

    m = re.search(r"^Combined Power[^:]*:\s+([\d.]+)\s+mW", raw, re.MULTILINE)
    if m:
        snap.package_power_mw = float(m.group(1))
    else:
        parts = [snap.cpu_power_mw, snap.gpu_power_mw, snap.ane_power_mw]
        if any(p is not None for p in parts):
            snap.package_power_mw = sum(p for p in parts if p is not None)

    m = re.search(r"CPU die temperature:\s+([\d.]+)\s+C", raw, re.MULTILINE | re.IGNORECASE)
    if m:
        snap.cpu_die_temp_celsius = float(m.group(1))

    return snap
