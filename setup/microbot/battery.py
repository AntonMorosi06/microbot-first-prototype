"""
MicroBot Round V0 battery module.

This module provides safe, minimal battery and power-status helpers for the first
MicroBot Round V0 hardware bring-up.

Important V0 limitation:
Raspberry Pi boards do not have built-in analog inputs. This means battery
voltage cannot be read directly from a GPIO pin. Real battery monitoring requires
one of the following:

- external ADC module
- battery fuel gauge module
- safe voltage divider connected to an ADC
- USB power meter / manual measurement
- mocked value during software testing

This module is intentionally conservative. If battery monitoring is unavailable,
it returns UNAVAILABLE instead of pretending that the battery is safe.

Movement code should treat CRITICAL, FAILED, or UNAVAILABLE battery state
according to the safety configuration of the current test.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import os
import time


BATTERY_ENV_VAR = "MICROBOT_BATTERY_VOLTAGE"


@dataclass(frozen=True)
class BatteryConfig:
    """
    Battery configuration for MicroBot Round V0.

    The default values are conservative placeholders for a single-cell lithium
    battery. They must be validated with the real battery, regulator and power
    system before battery-based movement tests.

    For early bench testing, battery monitoring may remain unavailable.
    """

    chemistry: str = "liion_1s"

    empty_voltage: float = 3.20
    critical_voltage: float = 3.30
    low_voltage: float = 3.50
    warning_voltage: float = 3.65
    nominal_voltage: float = 3.70
    full_voltage: float = 4.20

    movement_block_voltage: float = 3.45

    source: str = "unavailable"
    voltage_file: str | None = None
    mock_voltage: float | None = None


@dataclass(frozen=True)
class BatteryStatus:
    """
    Structured battery status.

    status:
        OK, WARNING, LOW, CRITICAL, UNAVAILABLE, or FAILED.

    voltage:
        Measured or mocked battery voltage.

    percentage:
        Estimated battery percentage from voltage.

    movement_allowed:
        Whether movement may continue according to this battery status alone.

    source:
        unavailable, mock, env, file, manual, or future_adc.

    message:
        Human-readable explanation.
    """

    status: str
    voltage: float | None
    percentage: float | None
    movement_allowed: bool
    source: str
    message: str
    timestamp: float


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Clamp a numeric value between minimum and maximum.
    """

    return max(minimum, min(maximum, value))


def estimate_liion_1s_percentage(voltage: float, config: BatteryConfig | None = None) -> float:
    """
    Estimate 1S Li-ion/LiPo percentage from voltage.

    This is only a rough estimate. Lithium battery voltage is not a perfect state
    of charge indicator, especially under load. The value is useful for basic
    warnings, not for precision runtime prediction.
    """

    cfg = config or BatteryConfig()

    if voltage <= cfg.empty_voltage:
        return 0.0

    if voltage >= cfg.full_voltage:
        return 100.0

    points = [
        (cfg.empty_voltage, 0.0),
        (3.30, 5.0),
        (3.50, 15.0),
        (3.65, 35.0),
        (3.75, 55.0),
        (3.85, 70.0),
        (3.95, 82.0),
        (4.05, 92.0),
        (cfg.full_voltage, 100.0),
    ]

    for index in range(len(points) - 1):
        v0, p0 = points[index]
        v1, p1 = points[index + 1]

        if v0 <= voltage <= v1:
            ratio = (voltage - v0) / (v1 - v0)
            return clamp(p0 + ratio * (p1 - p0), 0.0, 100.0)

    return clamp((voltage - cfg.empty_voltage) / (cfg.full_voltage - cfg.empty_voltage) * 100.0, 0.0, 100.0)


def classify_voltage(voltage: float, config: BatteryConfig | None = None) -> tuple[str, bool, str]:
    """
    Classify battery voltage into a safety status.

    Returns:
        status, movement_allowed, message
    """

    cfg = config or BatteryConfig()

    if voltage <= 0:
        return (
            "FAILED",
            False,
            "Invalid battery voltage. Voltage must be greater than zero.",
        )

    if voltage <= cfg.critical_voltage:
        return (
            "CRITICAL",
            False,
            "Battery voltage is critical. Movement must be blocked.",
        )

    if voltage <= cfg.movement_block_voltage:
        return (
            "LOW",
            False,
            "Battery voltage is below movement threshold. Movement blocked.",
        )

    if voltage <= cfg.low_voltage:
        return (
            "LOW",
            False,
            "Battery voltage is low. Movement should remain disabled.",
        )

    if voltage <= cfg.warning_voltage:
        return (
            "WARNING",
            True,
            "Battery voltage is in warning range. Only short supervised tests are recommended.",
        )

    if voltage > cfg.full_voltage + 0.20:
        return (
            "FAILED",
            False,
            "Battery voltage is above expected range. Check wiring and measurement source.",
        )

    return (
        "OK",
        True,
        "Battery voltage is acceptable for the current configured thresholds.",
    )


def parse_voltage(value: str | float | int | None) -> float | None:
    """
    Convert a value to float voltage safely.
    """

    if value is None:
        return None

    try:
        voltage = float(value)
    except (TypeError, ValueError):
        return None

    return voltage


def read_voltage_from_env(env_var: str = BATTERY_ENV_VAR) -> float | None:
    """
    Read battery voltage from an environment variable.

    Example:

        export MICROBOT_BATTERY_VOLTAGE=3.91
        python setup/microbot/battery.py --source env
    """

    return parse_voltage(os.environ.get(env_var))


def read_voltage_from_file(path: str | Path) -> float | None:
    """
    Read battery voltage from a text file.

    The file should contain a single number, for example:

        3.87

    This can be used during testing or with a future external measurement script.
    """

    file_path = Path(path)

    if not file_path.exists():
        return None

    try:
        content = file_path.read_text(encoding="utf-8").strip()
    except OSError:
        return None

    return parse_voltage(content)


def unavailable_status(message: str = "Battery monitoring is unavailable.") -> BatteryStatus:
    """
    Return a structured unavailable status.
    """

    return BatteryStatus(
        status="UNAVAILABLE",
        voltage=None,
        percentage=None,
        movement_allowed=False,
        source="unavailable",
        message=message,
        timestamp=time.time(),
    )


def build_status(
    voltage: float,
    source: str,
    config: BatteryConfig | None = None,
) -> BatteryStatus:
    """
    Build a BatteryStatus object from a voltage reading.
    """

    cfg = config or BatteryConfig()

    status, movement_allowed, message = classify_voltage(voltage, cfg)
    percentage = estimate_liion_1s_percentage(voltage, cfg)

    return BatteryStatus(
        status=status,
        voltage=voltage,
        percentage=percentage,
        movement_allowed=movement_allowed,
        source=source,
        message=message,
        timestamp=time.time(),
    )


def read_battery_status(config: BatteryConfig | None = None) -> BatteryStatus:
    """
    Read battery status using the configured source.

    Supported V0 sources:

    - unavailable:
        No real battery monitoring exists.

    - mock:
        Uses config.mock_voltage.

    - env:
        Reads voltage from MICROBOT_BATTERY_VOLTAGE.

    - file:
        Reads voltage from config.voltage_file.

    - manual:
        Same behavior as mock, but intended for manually entered measurement.

    Future sources such as ADC or fuel gauge modules should be added only after
    the selected hardware is known.
    """

    cfg = config or BatteryConfig()
    source = cfg.source.lower().strip()

    if source == "unavailable":
        return unavailable_status(
            "Battery monitoring is not implemented. Use bench power or manual measurement."
        )

    if source == "mock":
        voltage = parse_voltage(cfg.mock_voltage)

        if voltage is None:
            return BatteryStatus(
                status="FAILED",
                voltage=None,
                percentage=None,
                movement_allowed=False,
                source="mock",
                message="Mock battery source selected, but mock_voltage is missing or invalid.",
                timestamp=time.time(),
            )

        return build_status(voltage, "mock", cfg)

    if source == "manual":
        voltage = parse_voltage(cfg.mock_voltage)

        if voltage is None:
            return BatteryStatus(
                status="FAILED",
                voltage=None,
                percentage=None,
                movement_allowed=False,
                source="manual",
                message="Manual battery source selected, but no manual voltage was provided.",
                timestamp=time.time(),
            )

        return build_status(voltage, "manual", cfg)

    if source == "env":
        voltage = read_voltage_from_env()

        if voltage is None:
            return BatteryStatus(
                status="UNAVAILABLE",
                voltage=None,
                percentage=None,
                movement_allowed=False,
                source="env",
                message=f"Environment variable {BATTERY_ENV_VAR} is missing or invalid.",
                timestamp=time.time(),
            )

        return build_status(voltage, "env", cfg)

    if source == "file":
        if not cfg.voltage_file:
            return BatteryStatus(
                status="FAILED",
                voltage=None,
                percentage=None,
                movement_allowed=False,
                source="file",
                message="File battery source selected, but voltage_file is not configured.",
                timestamp=time.time(),
            )

        voltage = read_voltage_from_file(cfg.voltage_file)

        if voltage is None:
            return BatteryStatus(
                status="UNAVAILABLE",
                voltage=None,
                percentage=None,
                movement_allowed=False,
                source="file",
                message=f"Could not read valid battery voltage from file: {cfg.voltage_file}",
                timestamp=time.time(),
            )

        return build_status(voltage, "file", cfg)

    return BatteryStatus(
        status="FAILED",
        voltage=None,
        percentage=None,
        movement_allowed=False,
        source=source,
        message=f"Unsupported battery source: {source}",
        timestamp=time.time(),
    )


def status_to_dict(status: BatteryStatus) -> dict[str, str | float | bool | None]:
    """
    Convert BatteryStatus to a dictionary for JSON logs.
    """

    return {
        "status": status.status,
        "voltage": status.voltage,
        "percentage": status.percentage,
        "movement_allowed": status.movement_allowed,
        "source": status.source,
        "message": status.message,
        "timestamp": status.timestamp,
    }


def format_battery_status(status: BatteryStatus) -> str:
    """
    Format battery status for terminal output.
    """

    voltage_text = "unavailable" if status.voltage is None else f"{status.voltage:.2f} V"
    percentage_text = (
        "unavailable" if status.percentage is None else f"{status.percentage:.1f}%"
    )

    return (
        "Battery status\n"
        "==============\n"
        f"Status: {status.status}\n"
        f"Voltage: {voltage_text}\n"
        f"Estimated percentage: {percentage_text}\n"
        f"Movement allowed: {status.movement_allowed}\n"
        f"Source: {status.source}\n"
        f"Message: {status.message}\n"
    )


def battery_self_check(config: BatteryConfig | None = None) -> dict[str, str | float | bool | None]:
    """
    Return battery self-check information as a dictionary.
    """

    status = read_battery_status(config)
    return status_to_dict(status)


def print_battery_self_check(config: BatteryConfig | None = None) -> BatteryStatus:
    """
    Print battery status and return the BatteryStatus object.
    """

    status = read_battery_status(config)
    print(format_battery_status(status))
    return status


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build command-line argument parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 battery status helper."
    )

    parser.add_argument(
        "--source",
        choices=["unavailable", "mock", "manual", "env", "file"],
        default="unavailable",
        help="Battery voltage source.",
    )

    parser.add_argument(
        "--voltage",
        type=float,
        default=None,
        help="Mock or manual battery voltage.",
    )

    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a text file containing battery voltage.",
    )

    parser.add_argument(
        "--movement-block-voltage",
        type=float,
        default=3.45,
        help="Voltage below which movement should be blocked.",
    )

    return parser


def main() -> None:
    """
    CLI entry point for quick battery testing.
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    config = BatteryConfig(
        source=args.source,
        mock_voltage=args.voltage,
        voltage_file=args.file,
        movement_block_voltage=args.movement_block_voltage,
    )

    print_battery_self_check(config)


if __name__ == "__main__":
    main()