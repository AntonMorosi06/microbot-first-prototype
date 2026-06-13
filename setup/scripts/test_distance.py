#!/usr/bin/env python3
"""
MicroBot Round V0 distance sensor test.

This script tests the MicroBot distance / obstacle helper.

Supported sources:

- unavailable: default mode, no distance sensor installed
- mock: provide distance with --distance
- manual: provide manually measured distance with --distance
- env: read distance from MICROBOT_DISTANCE_CM
- file: read distance from a text file
- vl53l0x: try to read a real VL53L0X distance sensor

Examples:

    python setup/scripts/test_distance.py

    python setup/scripts/test_distance.py --source mock --distance 42

    python setup/scripts/test_distance.py --source mock --distance 10

    MICROBOT_DISTANCE_CM=18 python setup/scripts/test_distance.py --source env

    echo 31.5 > /tmp/microbot_distance.txt
    python setup/scripts/test_distance.py --source file --file /tmp/microbot_distance.txt

    python setup/scripts/test_distance.py --source vl53l0x

JSON output:

    python setup/scripts/test_distance.py --source mock --distance 42 --json

Safety:
This script does not move the robot.
It only evaluates whether the measured distance would allow forward movement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import distance  # noqa: E402


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


def format_distance(value: Any) -> str:
    """
    Format distance value.
    """

    if value is None:
        return "unavailable"

    try:
        return f"{float(value):.1f} cm"
    except (TypeError, ValueError):
        return str(value)


def print_distance_report(result: dict[str, Any]) -> None:
    """
    Print a readable distance report.
    """

    status = normalize_status(result.get("status"))
    distance_cm = result.get("distance_cm")
    obstacle_detected = result.get("obstacle_detected")
    forward_allowed = result.get("forward_movement_allowed")
    source = result.get("source")
    message = result.get("message")

    print("MicroBot Round V0 distance test")
    print("===============================")
    print()
    print(f"Status: {status}")
    print(f"Distance: {format_distance(distance_cm)}")
    print(f"Obstacle detected: {obstacle_detected}")
    print(f"Forward movement allowed: {forward_allowed}")
    print(f"Source: {source}")
    print(f"Message: {message}")
    print()

    print("Safety interpretation")
    print("---------------------")

    if status == "OK" and forward_allowed:
        print("Path distance is acceptable for the configured thresholds.")
    elif status == "WARNING" and forward_allowed:
        print("Object is close. Only careful supervised movement should be considered.")
    elif status in {"OBSTACLE", "CRITICAL"}:
        print("Forward movement must be blocked.")
    elif status == "UNAVAILABLE":
        print("Distance sensor is unavailable. Forward movement should stay blocked unless explicitly allowed for a controlled test.")
    elif status == "FAILED":
        print("Distance reading failed. Do not use this reading to allow movement.")
    else:
        print("Distance status is unknown. Stay conservative and do not move forward.")

    print()

    print("Notes")
    print("-----")
    print("- A distance sensor is optional in the first MicroBot Round V0 build.")
    print("- If no sensor is installed, UNAVAILABLE is expected.")
    print("- For real obstacle detection, use a VL53L0X/VL53L1X or similar ToF sensor.")
    print("- Forward movement should be blocked when an obstacle is below the stop threshold.")
    print()


def run_threshold_demo() -> list[dict[str, Any]]:
    """
    Run an offline obstacle threshold demo.

    This does not read real hardware. It only shows how the distance module
    classifies common distances.
    """

    demo_distances = [
        100.0,
        50.0,
        30.0,
        25.0,
        20.0,
        15.0,
        10.0,
        8.0,
        5.0,
    ]

    results: list[dict[str, Any]] = []

    for distance_cm in demo_distances:
        config = distance.DistanceConfig(
            source="mock",
            mock_distance_cm=distance_cm,
        )
        status = distance.read_distance_status(config)
        results.append(distance.status_to_dict(status))

    return results


def print_threshold_demo(results: list[dict[str, Any]]) -> None:
    """
    Print distance threshold demo table.
    """

    print("Distance threshold demo")
    print("=======================")
    print("This is an offline classification demo, not a real sensor reading.")
    print()

    print(f"{'Distance':<12} {'Status':<12} {'Obstacle':<10} {'Forward':<10} Message")
    print("-" * 95)

    for item in results:
        distance_text = format_distance(item.get("distance_cm"))
        status = str(item.get("status"))
        obstacle = str(item.get("obstacle_detected"))
        forward = str(item.get("forward_movement_allowed"))
        message = str(item.get("message"))

        print(f"{distance_text:<12} {status:<12} {obstacle:<10} {forward:<10} {message}")

    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 distance / obstacle test."
    )

    parser.add_argument(
        "--source",
        choices=["unavailable", "mock", "manual", "env", "file", "vl53l0x"],
        default="unavailable",
        help="Distance source.",
    )

    parser.add_argument(
        "--distance",
        type=float,
        default=None,
        help="Mock or manual distance in centimeters.",
    )

    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a text file containing one distance value in centimeters.",
    )

    parser.add_argument(
        "--warning-cm",
        type=float,
        default=25.0,
        help="Warning threshold in centimeters.",
    )

    parser.add_argument(
        "--stop-cm",
        type=float,
        default=15.0,
        help="Stop threshold in centimeters.",
    )

    parser.add_argument(
        "--critical-cm",
        type=float,
        default=8.0,
        help="Critical threshold in centimeters.",
    )

    parser.add_argument(
        "--max-valid-cm",
        type=float,
        default=400.0,
        help="Maximum valid distance in centimeters.",
    )

    parser.add_argument(
        "--allow-forward-if-unavailable",
        action="store_true",
        help="Allow forward movement if distance sensor is unavailable. Not recommended for real movement.",
    )

    parser.add_argument(
        "--threshold-demo",
        action="store_true",
        help="Print an offline distance threshold demo.",
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

    config = distance.DistanceConfig(
        source=args.source,
        mock_distance_cm=args.distance,
        distance_file=args.file,
        warning_distance_cm=args.warning_cm,
        stop_distance_cm=args.stop_cm,
        critical_distance_cm=args.critical_cm,
        max_valid_distance_cm=args.max_valid_cm,
        block_forward_if_unavailable=not args.allow_forward_if_unavailable,
    )

    status = distance.read_distance_status(config)
    status_dict = distance.status_to_dict(status)

    if args.json:
        print(json.dumps(status_dict, indent=2, sort_keys=True, default=str))
    else:
        print_distance_report(status_dict)

    status_name = normalize_status(status_dict.get("status"))

    if status_name in {"FAILED", "CRITICAL"}:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())