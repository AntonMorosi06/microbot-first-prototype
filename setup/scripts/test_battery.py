#!/usr/bin/env python3
"""
MicroBot Round V0 battery test.

This script tests the MicroBot battery/power status helper.

Important V0 limitation:
Raspberry Pi boards do not have built-in analog input. Real battery voltage
cannot be measured directly from a GPIO pin. For real voltage monitoring, the
robot needs an external ADC, a fuel gauge module, or a separate measurement
system.

This script supports safe software-side test modes:

- unavailable: default mode, no battery monitor installed
- mock: provide voltage with --voltage
- manual: provide manually measured voltage with --voltage
- env: read voltage from MICROBOT_BATTERY_VOLTAGE
- file: read voltage from a text file

Examples:

    python setup/scripts/test_battery.py

    python setup/scripts/test_battery.py --source mock --voltage 3.92

    python setup/scripts/test_battery.py --source manual --voltage 3.48

    MICROBOT_BATTERY_VOLTAGE=3.86 python setup/scripts/test_battery.py --source env

    echo 3.77 > /tmp/microbot_battery_voltage.txt
    python setup/scripts/test_battery.py --source file --file /tmp/microbot_battery_voltage.txt

JSON output:

    python setup/scripts/test_battery.py --source mock --voltage 3.92 --json

Safety:
This script does not move the robot.
It only evaluates whether the battery status would allow movement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import battery  # noqa: E402


def to_dict_safe(value: Any) -> dict[str, Any]:
    """
    Convert a result object or dictionary into a plain dictionary.
    """

    if isinstance(value, dict):
        return value

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return {
        "status": "UNKNOWN",
        "message": str(value),
    }


def normalize_status(value: Any) -> str:
    """
    Normalize a status value.
    """

    if value is None:
        return "UNKNOWN"

    return str(value).strip().upper()


def print_battery_report(result: Any) -> None:
    """
    Print a readable battery report.
    """

    data = to_dict_safe(result)

    print("MicroBot Round V0 battery test")
    print("==============================")
    print()

    print(f"Status: {data.get('status')}")
    print(f"Voltage: {format_voltage(data.get('voltage'))}")
    print(f"Estimated percentage: {format_percentage(data.get('percentage'))}")
    print(f"Movement allowed: {data.get('movement_allowed')}")
    print(f"Source: {data.get('source')}")
    print(f"Message: {data.get('message')}")
    print()

    print("Safety interpretation")
    print("---------------------")

    status = normalize_status(data.get("status"))
    movement_allowed = bool(data.get("movement_allowed"))

    if status == "OK" and movement_allowed:
        print("Battery status is acceptable for the configured thresholds.")
    elif status == "WARNING" and movement_allowed:
        print("Battery is usable only for short, supervised tests.")
    elif status in {"LOW", "CRITICAL", "FAILED"}:
        print("Movement should be blocked.")
    elif status == "UNAVAILABLE":
        print("Battery monitoring is unavailable. Use manual measurement or bench power validation.")
    else:
        print("Battery status is unknown. Stay conservative and do not move the robot.")

    print()

    print("Notes")
    print("-----")
    print("- Raspberry Pi has no built-in analog input.")
    print("- Real voltage monitoring requires an ADC or fuel gauge.")
    print("- For V0, verify the 5 V rail with a multimeter before servo tests.")
    print("- If voltage is below the movement threshold, do not run movement scripts.")
    print()


def format_voltage(value: Any) -> str:
    """
    Format voltage value.
    """

    if value is None:
        return "unavailable"

    try:
        return f"{float(value):.2f} V"
    except (TypeError, ValueError):
        return str(value)


def format_percentage(value: Any) -> str:
    """
    Format percentage value.
    """

    if value is None:
        return "unavailable"

    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return str(value)


def run_threshold_demo() -> list[dict[str, Any]]:
    """
    Run a small offline threshold demo.

    This does not read real hardware. It only shows how the battery module
    classifies common 1S Li-ion/LiPo voltages.
    """

    demo_voltages = [
        4.20,
        3.95,
        3.75,
        3.65,
        3.50,
        3.45,
        3.30,
        3.20,
    ]

    results: list[dict[str, Any]] = []

    for voltage in demo_voltages:
        config = battery.BatteryConfig(
            source="mock",
            mock_voltage=voltage,
        )
        status = battery.read_battery_status(config)
        results.append(battery.status_to_dict(status))

    return results


def print_threshold_demo(results: list[dict[str, Any]]) -> None:
    """
    Print threshold demo table.
    """

    print("Battery threshold demo")
    print("======================")
    print("This is an offline classification demo, not a real measurement.")
    print()

    print(f"{'Voltage':<10} {'Status':<12} {'Move':<8} {'Estimated %':<12} Message")
    print("-" * 80)

    for item in results:
        voltage = format_voltage(item.get("voltage"))
        status = str(item.get("status"))
        movement = str(item.get("movement_allowed"))
        percentage = format_percentage(item.get("percentage"))
        message = str(item.get("message"))

        print(f"{voltage:<10} {status:<12} {movement:<8} {percentage:<12} {message}")

    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 battery status test."
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
        help="Path to a text file containing one voltage value.",
    )

    parser.add_argument(
        "--movement-block-voltage",
        type=float,
        default=3.45,
        help="Voltage below which movement should be blocked.",
    )

    parser.add_argument(
        "--warning-voltage",
        type=float,
        default=3.65,
        help="Voltage at or below which warning status begins.",
    )

    parser.add_argument(
        "--low-voltage",
        type=float,
        default=3.50,
        help="Voltage at or below which low status begins.",
    )

    parser.add_argument(
        "--critical-voltage",
        type=float,
        default=3.30,
        help="Voltage at or below which critical status begins.",
    )

    parser.add_argument(
        "--threshold-demo",
        action="store_true",
        help="Print an offline voltage threshold demo.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output.",
    )

    return parser


def main() -> int:
    """
    Main CLI entry point.
    """

    args = build_arg_parser().parse_args()

    if args.threshold_demo:
        demo_results = run_threshold_demo()

        if args.json:
            print(json.dumps({"threshold_demo": demo_results}, indent=2, sort_keys=True, default=str))
        else:
            print_threshold_demo(demo_results)

        return 0

    config = battery.BatteryConfig(
        source=args.source,
        mock_voltage=args.voltage,
        voltage_file=args.file,
        warning_voltage=args.warning_voltage,
        low_voltage=args.low_voltage,
        movement_block_voltage=args.movement_block_voltage,
        critical_voltage=args.critical_voltage,
    )

    status = battery.read_battery_status(config)
    status_dict = battery.status_to_dict(status)

    if args.json:
        print(json.dumps(status_dict, indent=2, sort_keys=True, default=str))
    else:
        print_battery_report(status_dict)

    status_name = normalize_status(status_dict.get("status"))

    if status_name in {"FAILED", "CRITICAL"}:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())