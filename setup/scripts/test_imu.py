#!/usr/bin/env python3
"""
MicroBot Round V0 IMU test.

This script tests the MicroBot MPU-6050 / GY-521 IMU subsystem.

It checks:

- I2C communication
- WHO_AM_I register
- acceleration readings
- gyroscope readings
- estimated roll and pitch
- estimated tilt safety state

Reference hardware pattern:

- Raspberry Pi Zero 2 W
- MPU-6050 / GY-521 IMU
- I2C address 0x68
- SDA on GPIO2 / physical pin 3
- SCL on GPIO3 / physical pin 5
- 3.3 V power
- common ground

Install Python dependency:

    python -m pip install smbus2

Enable I2C on Raspberry Pi:

    sudo raspi-config

Then:
Interface Options -> I2C -> Enable

Run from repository root:

    python setup/scripts/test_imu.py

Custom sample count:

    python setup/scripts/test_imu.py --samples 20 --delay 0.1

Custom address:

    python setup/scripts/test_imu.py --address 0x68

JSON output:

    python setup/scripts/test_imu.py --json

Safety:
This script does not move the robot.
It only reads the IMU and reports whether the robot appears stable.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import imu  # noqa: E402
from microbot import pins  # noqa: E402


def normalize_status(value: Any) -> str:
    """
    Normalize a status value.
    """

    if value is None:
        return "UNKNOWN"

    return str(value).strip().upper()


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


def print_header(address: int, bus: int, samples: int, delay: float) -> None:
    """
    Print test header.
    """

    print("MicroBot Round V0 IMU test")
    print("==========================")
    print(f"I2C bus: {bus}")
    print(f"I2C address: 0x{address:02x}")
    print(f"Samples: {samples}")
    print(f"Delay: {delay:.2f} s")
    print()


def print_self_check(result: dict[str, Any]) -> None:
    """
    Print IMU self-check result.
    """

    print("Self-check")
    print("----------")
    print(f"Status: {result.get('status')}")
    print(f"WHO_AM_I: {format_who_am_i(result.get('who_am_i'))}")
    print(f"Message: {result.get('message')}")
    print()


def format_who_am_i(value: Any) -> str:
    """
    Format WHO_AM_I register value.
    """

    if value is None:
        return "unavailable"

    try:
        return f"0x{int(value):02x}"
    except (TypeError, ValueError):
        return str(value)


def print_reading_table_header() -> None:
    """
    Print live sample table header.
    """

    print("Live samples")
    print("------------")
    print(
        f"{'#':<4} "
        f"{'ax':>8} {'ay':>8} {'az':>8} "
        f"{'gx':>9} {'gy':>9} {'gz':>9} "
        f"{'roll':>9} {'pitch':>9} {'tilt':>9} "
        f"{'status':<10}"
    )
    print("-" * 104)


def print_reading(index: int, reading: imu.ImuReading) -> None:
    """
    Print one IMU reading row.
    """

    print(
        f"{index:<4} "
        f"{reading.ax:>+8.2f} {reading.ay:>+8.2f} {reading.az:>+8.2f} "
        f"{reading.gx:>+9.1f} {reading.gy:>+9.1f} {reading.gz:>+9.1f} "
        f"{reading.roll_degrees:>+9.1f} "
        f"{reading.pitch_degrees:>+9.1f} "
        f"{reading.tilt_degrees:>9.1f} "
        f"{reading.status:<10}"
    )


def print_interpretation(readings: list[dict[str, Any]]) -> None:
    """
    Print final safety interpretation.
    """

    if not readings:
        print()
        print("Interpretation")
        print("--------------")
        print("No readings collected.")
        return

    statuses = [normalize_status(item.get("status")) for item in readings]
    max_tilt = max(float(item.get("tilt_degrees", 0.0)) for item in readings)

    print()
    print("Interpretation")
    print("--------------")
    print(f"Maximum tilt observed: {max_tilt:.1f} degrees")

    if "CRITICAL" in statuses:
        print("Result: CRITICAL. Movement must be blocked.")
    elif "WARNING" in statuses:
        print("Result: WARNING. Robot is tilted beyond warning threshold.")
    elif all(status == "OK" for status in statuses):
        print("Result: OK. Robot orientation stayed within configured stable range.")
    else:
        print("Result: UNKNOWN. Review readings before allowing movement.")

    print()
    print("Notes")
    print("-----")
    print("- Tilt estimates are accelerometer-based and simple.")
    print("- This is enough for early safety checks, not full orientation filtering.")
    print("- If values do not change when tilting the robot, check I2C wiring.")
    print("- If WHO_AM_I fails, check power, ground, SDA, SCL and I2C enablement.")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 MPU-6050 IMU test."
    )

    parser.add_argument(
        "--address",
        type=lambda value: int(value, 0),
        default=pins.IMU_I2C_ADDR,
        help=f"IMU I2C address. Default: 0x{pins.IMU_I2C_ADDR:02x}",
    )

    parser.add_argument(
        "--bus",
        type=int,
        default=pins.I2C_BUS,
        help=f"I2C bus number. Default: {pins.I2C_BUS}",
    )

    parser.add_argument(
        "--samples",
        type=int,
        default=6,
        help="Number of live samples to print.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay between samples in seconds.",
    )

    parser.add_argument(
        "--tilt-warning",
        type=float,
        default=pins.TILT_WARNING_DEGREES,
        help="Tilt warning threshold in degrees.",
    )

    parser.add_argument(
        "--tilt-critical",
        type=float,
        default=pins.TILT_CRITICAL_DEGREES,
        help="Tilt critical threshold in degrees.",
    )

    parser.add_argument(
        "--self-check-only",
        action="store_true",
        help="Run only WHO_AM_I and one-sample self-check.",
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

    config = imu.ImuConfig(
        address=args.address,
        bus_num=args.bus,
        tilt_warning_degrees=args.tilt_warning,
        tilt_critical_degrees=args.tilt_critical,
    )

    output: dict[str, Any] = {
        "config": {
            "address": args.address,
            "address_hex": f"0x{args.address:02x}",
            "bus": args.bus,
            "samples": args.samples,
            "delay": args.delay,
            "tilt_warning_degrees": args.tilt_warning,
            "tilt_critical_degrees": args.tilt_critical,
        },
        "self_check": None,
        "readings": [],
    }

    if not args.json:
        print_header(
            address=args.address,
            bus=args.bus,
            samples=args.samples,
            delay=args.delay,
        )

    try:
        with imu.Imu(config) as imu_device:
            self_check_result = imu_device.self_check()
            self_check_dict = imu.self_check_to_dict(self_check_result)
            output["self_check"] = self_check_dict

            if not args.json:
                print_self_check(self_check_dict)

            if args.self_check_only:
                if args.json:
                    print(json.dumps(output, indent=2, sort_keys=True, default=str))
                return 0 if normalize_status(self_check_dict.get("status")) in {"OK", "WARNING"} else 1

            if not args.json:
                print_reading_table_header()

            sample_count = max(1, args.samples)

            for index in range(1, sample_count + 1):
                reading = imu_device.read()
                reading_dict = imu.reading_to_dict(reading)
                output["readings"].append(reading_dict)

                if not args.json:
                    print_reading(index, reading)

                time.sleep(max(0.0, args.delay))

    except Exception as exc:
        output["self_check"] = {
            "status": "FAILED",
            "who_am_i": None,
            "reading": None,
            "message": f"IMU test failed: {type(exc).__name__}: {exc}",
            "timestamp": time.time(),
        }

        if args.json:
            print(json.dumps(output, indent=2, sort_keys=True, default=str))
        else:
            print("FAILED")
            print("------")
            print(output["self_check"]["message"])
            print()
            print("Check:")
            print("- I2C enabled in raspi-config")
            print("- smbus2 installed")
            print("- IMU powered at 3.3 V")
            print("- common ground")
            print("- SDA on GPIO2 / physical pin 3")
            print("- SCL on GPIO3 / physical pin 5")
            print("- address 0x68 or 0x69")
            print()

        return 1

    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True, default=str))
    else:
        print_interpretation(output["readings"])

    self_check_status = normalize_status(output["self_check"].get("status"))
    reading_statuses = [normalize_status(item.get("status")) for item in output["readings"]]

    if self_check_status == "FAILED":
        return 1

    if "CRITICAL" in reading_statuses:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())