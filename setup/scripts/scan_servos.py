#!/usr/bin/env python3
"""
MicroBot Round V0 read-only servo scan.

This script checks whether the SCS0009 / SC09 serial bus servos respond on the
configured UART port.

Default hardware reference:

- Raspberry Pi Zero 2 W
- servo bus on /dev/serial0
- baud rate 1,000,000
- expected IDs: 1 and 2
- half-duplex DATA line
- TX through 1 kOhm resistor
- RX directly connected to DATA

Safety:
This script does not command movement.
It only sends ping/read commands.

Run from the repository root:

    python setup/scripts/scan_servos.py

Common Raspberry Pi setup reminder:

    sudo raspi-config

Then:
Interface Options -> Serial Port
- login shell over serial: No
- serial port hardware: Yes

On Pi Zero 2 W, /dev/serial0 is usually the correct port.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import pins  # noqa: E402
from microbot import servos  # noqa: E402


def parse_ids(ids_text: str) -> tuple[int, ...]:
    """
    Parse comma-separated servo IDs.

    Example:

        "1,2,3" -> (1, 2, 3)
    """

    parsed: list[int] = []

    for item in ids_text.split(","):
        clean = item.strip()

        if not clean:
            continue

        parsed.append(int(clean))

    return tuple(parsed)


def print_scan_header(port: str, baud: int, ids: tuple[int, ...]) -> None:
    """
    Print a clear scan header.
    """

    print("MicroBot Round V0 servo scan")
    print("============================")
    print("Mode: read-only, no movement")
    print(f"Port: {port}")
    print(f"Baud: {baud}")
    print(f"IDs: {ids}")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build command-line argument parser.
    """

    default_ids = ",".join(str(item) for item in (*pins.SERVO_IDS, 3, 4, 5, 6))

    parser = argparse.ArgumentParser(
        description="Read-only scan for MicroBot Round V0 SCS0009 / SC09 servos."
    )

    parser.add_argument(
        "--port",
        default=pins.SERVO_PORT,
        help=f"Servo serial port. Default: {pins.SERVO_PORT}",
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=pins.SERVO_BAUD,
        help=f"Servo baud rate. Default: {pins.SERVO_BAUD}",
    )

    parser.add_argument(
        "--ids",
        default=default_ids,
        help=f"Comma-separated servo IDs to scan. Default: {default_ids}",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON result instead of formatted text.",
    )

    return parser


def result_to_dict(result: Any) -> dict[str, Any]:
    """
    Convert ServoScanResult to dictionary.
    """

    try:
        return servos.scan_result_to_dict(result)
    except Exception:
        return {
            "status": "FAILED",
            "message": "Could not convert scan result to dictionary.",
            "result": str(result),
        }


def main() -> int:
    """
    Main CLI entry point.
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        ids = parse_ids(args.ids)
    except ValueError as exc:
        print(f"Invalid --ids value: {args.ids}")
        print(f"Error: {exc}")
        return 1

    config = servos.ServoConfig(
        port=args.port,
        baud=args.baud,
    )

    if not args.json:
        print_scan_header(
            port=args.port,
            baud=args.baud,
            ids=ids,
        )

    result = servos.scan_servos(
        servo_ids=ids,
        config=config,
    )

    if args.json:
        print(json.dumps(result_to_dict(result), indent=2, sort_keys=True, default=str))
    else:
        print(servos.format_scan_result(result))

    if result.status == "OK":
        print()
        print("Scan completed successfully.")
        print("Next safe step:")
        print("  python setup/scripts/test_servos_safe.py")
        return 0

    print()
    print("No valid servo scan completed.")
    print("Check:")
    print("- servo power rail")
    print("- common ground")
    print("- TX through 1 kOhm resistor to DATA")
    print("- RX directly to DATA")
    print("- /dev/serial0 enabled")
    print("- serial console disabled")
    print("- servo IDs")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())