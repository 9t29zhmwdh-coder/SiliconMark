"""powermetrics parsing and runtime availability, without sudo or a model."""

from siliconmark.core import registry
from siliconmark.metrics.apple import _parse_averaged, worst_thermal_pressure

# Trimmed real output of `powermetrics --samplers cpu_power,gpu_power,thermal`
# on an M4 Pro: power lines plus a thermal pressure level, no die temperature.
SAMPLE = """
*** Sampled system activity ***
**** Processor usage ****
CPU Power: 5000 mW
GPU Power: 2500 mW
ANE Power: 0 mW
Combined Power (CPU + GPU + ANE): 7500 mW
**** Thermal pressure ****
Current pressure level: Nominal
*** Sampled system activity ***
CPU Power: 7000 mW
GPU Power: 3500 mW
ANE Power: 0 mW
Combined Power (CPU + GPU + ANE): 10500 mW
**** Thermal pressure ****
Current pressure level: Moderate
"""


def test_parser_averages_power_and_keeps_the_worst_thermal_level():
    snap = _parse_averaged(SAMPLE)
    assert snap.cpu_power_mw == 6000
    assert snap.gpu_power_mw == 3000
    assert snap.package_power_mw == 9000
    assert snap.thermal_pressure == "Moderate"


def test_worst_thermal_pressure_orders_levels_and_ignores_unknown():
    assert worst_thermal_pressure(["Nominal", "Heavy", "Moderate"]) == "Heavy"
    assert worst_thermal_pressure(["Nominal"]) == "Nominal"
    assert worst_thermal_pressure(["Warm"]) is None
    assert worst_thermal_pressure([]) is None


def test_unknown_runtime_is_not_available():
    assert registry.runtime_available("nope") is False


def test_every_listed_runtime_has_an_availability_check():
    assert {name for name, _ in registry.list_runtimes()} == set(registry._CHECKS)
