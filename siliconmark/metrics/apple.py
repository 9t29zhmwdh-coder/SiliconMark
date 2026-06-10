"""Apple Silicon power & thermal metrics via powermetrics (requires passwordless sudo)."""

from __future__ import annotations

import json
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
                "sudo", "-n", "powermetrics",
                "--samplers", "cpu_power,gpu_power,thermal",
                "--format", "json",
                "-i", str(duration_ms),
                "-n", "1",
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
    decoder = json.JSONDecoder()
    pos, last_obj = 0, None
    while pos < len(raw):
        try:
            obj, end = decoder.raw_decode(raw, pos)
            last_obj = obj
            pos = end
            while pos < len(raw) and raw[pos] in " \t\n\r":
                pos += 1
        except json.JSONDecodeError:
            pos += 1

    if last_obj is None:
        return ApplePowerSnapshot()

    snap = ApplePowerSnapshot()
    proc = last_obj.get("processor", {})
    snap.cpu_power_mw = _f(proc, "cpu_mw")
    snap.gpu_power_mw = _f(proc, "gpu_mw")
    snap.ane_power_mw = _f(proc, "ane_mw")
    snap.package_power_mw = _f(proc, "package_mw")

    # Fallback: sum individual components if package not reported
    if snap.package_power_mw is None:
        parts = [snap.cpu_power_mw, snap.gpu_power_mw, snap.ane_power_mw]
        if any(p is not None for p in parts):
            snap.package_power_mw = sum(p for p in parts if p is not None)

    thermal = last_obj.get("thermal", {})
    if isinstance(thermal, dict):
        snap.cpu_die_temp_celsius = _f(thermal, "cpu_die_temperature")

    return snap


def _f(d: dict, key: str) -> float | None:
    val = d.get(key)
    try:
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None
