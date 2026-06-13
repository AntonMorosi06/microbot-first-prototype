#!/usr/bin/env python3
"""
MicroBot Round V0 safe servo movement test.

This script performs a conservative test of the SCS0009 / SC09 servo bus.

Safety flow:

1. Open the servo bus.
2. Run read-only servo scan.
3. Read current servo positions.
4. Build a safety state.
5. Ask safety.py whether SAFE_NUDGE is allowed.
6. Only if allowed, nudge each servo by a small encoder delta.
7. Release torque on exit.

Default behavior:
This script does NOT move servos unless --enable-movement is provided.

Read-only scan:

    python setup/scripts/test_servos_safe.py

Safe nudge after power and wiring validation:

    python setup/scripts/test_servos_safe.py --enable-movement

Custom IDs:

    python setup/scripts/test_servos_safe.py --ids 1,2 --enable-movement

Custom small nudge:

    python setup/scripts/test_servos_safe.py --enable-movement --delta 20

JSON output:

    python setup/scripts/test_servos_safe.py --enable-movement --json

Hardware reference:

- Raspberry Pi Zero 2 W
- servo bus on /dev/serial0
- SCS0009 / SC09 serial bus servos
- 1 Mbps UART
- TX through 1 kOhm resistor to DATA
- RX directly from DATA
- common ground
- 5 V servo power rail

Important:
Keep the robot on a stand or hold it securely.
Keep fingers clear of all joints.
Do not run this before validating the 5 V rail with a multimeter.
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


from microbot import pins  # noqa: E402
from microbot import safety  # noqa: E402
from microbot import servos  # noqa: E402


def normalize_status(value: Any) -> str:
    """
    Normalize status text.
    """

    if value is None:
        return "UNKNOWN"

    return str(value).strip().upper()


def parse_ids(ids_text: str) -> tuple[int, ...]:
    """
    Parse comma-separated servo IDs.
    """

    ids: list[int] = []

    for item in ids_text.split(","):
        clean = item.strip()

        if clean:
            ids.append(int(clean))

    return tuple(ids)


def scan_result_to_plain_dict(result: servos.ServoScanResult) -> dict[str, Any]:
    """
    Convert scan result to a plain dictionary.
    """

    return servos.scan_result_to_dict(result)


def move_results_to_plain_list(results: list[servos.ServoMoveResult]) -> list[dict[str, Any]]:
    """
    Convert movement results to plain dictionaries.
    """

    return [servos.move_result_to_dict(item) for item in results]


def extract_servo_positions(scan_result: dict[str, Any]) -> dict[int, int]:
    """
    Extract servo_id -> present_position from a scan result dictionary.
    """

    positions: dict[int, int] = {}

    for item in scan_result.get("servos", ()):
        if not isinstance(item, dict):
            continue

        servo_id = item.get("servo_id")
        position = item.get("position")
        present = item.get("present")

        if present is not True:
            continue

        if servo_id is None or position is None:
            continue

        try:
            positions[int(servo_id)] = int(position)
        except (TypeError, ValueError):
            continue

    return positions


def extract_found_ids(scan_result: dict[str, Any]) -> tuple[int, ...]:
    """
    Extract found servo IDs from a scan result dictionary.
    """

    raw_ids = scan_result.get("found_ids", ())

    if not isinstance(raw_ids, (list, tuple)):
        return ()

    parsed: list[int] = []

    for item in raw_ids:
        try:
            parsed.append(int(item))
        except (TypeError, ValueError):
            continue

    return tuple(parsed)


def build_robot_state_from_scan(
    scan_result: dict[str, Any],
    require_imu: bool,
) -> safety.RobotState:
    """
    Build a RobotState for safety evaluation.

    For this isolated servo test, IMU is optional by default. If --require-imu is
    used, this state intentionally leaves IMU unknown unless the caller extends
    the script to read the IMU first.
    """

    if require_imu:
        imu_status = None
        tilt_degrees = None
    else:
        imu_status = "OK"
        tilt_degrees = 0.0

    return safety.RobotState(
        emergency_stop=False,
        servo_scan_ok=normalize_status(scan_result.get("status")) == "OK",
        servo_ids_found=extract_found_ids(scan_result),
        servo_positions=extract_servo_positions(scan_result),
        imu_status=imu_status,
        tilt_degrees=tilt_degrees,
        distance_status=None,
        distance_cm=None,
        battery_status=None,
        battery_voltage=None,
        failed_movement_count=0,
        safe_mode_active=False,
    )


def evaluate_safe_nudge(
    delta: int,
    robot_state: safety.RobotState,
    enable_movement: bool,
    require_imu: bool,
) -> safety.SafetyDecision:
    """
    Ask the safety layer whether safe nudge may run.
    """

    request = safety.MovementRequest(
        action="SAFE_NUDGE",
        nudge_amount=delta,
        reason="test_servos_safe.py safe nudge",
    )

    config = safety.SafetyConfig(
        hardware_movement_enabled=enable_movement,
        require_servo_scan_before_move=True,
        require_servo_position_before_move=True,
        require_imu_before_move=require_imu,
        require_safe_power_before_move=False,
        require_distance_for_forward_move=False,
        block_movement_if_distance_unavailable=False,
        block_movement_if_battery_unavailable=False,
        max_safe_nudge=pins.SAFE_NUDGE,
    )

    return safety.evaluate_safety(
        request=request,
        state=robot_state,
        config=config,
    )


def print_scan_report(scan_result: dict[str, Any]) -> None:
    """
    Print scan report.
    """

    print("Servo scan")
    print("==========")
    print(f"Status: {scan_result.get('status')}")
    print(f"Port: {scan_result.get('port')}")
    print(f"Baud: {scan_result.get('baud')}")
    print(f"Requested IDs: {scan_result.get('requested_ids')}")
    print(f"Found IDs: {scan_result.get('found_ids')}")
    print(f"Message: {scan_result.get('message')}")
    print()

    servos_data = scan_result.get("servos", ())

    if not servos_data:
        print("No servo status records.")
        print()
        return

    for item in servos_data:
        print(
            f"ID {item.get('servo_id')}: "
            f"present={item.get('present')} "
            f"position={item.get('position')} "
            f"message={item.get('message')}"
        )

    print()


def print_safety_decision(decision: safety.SafetyDecision) -> None:
    """
    Print safety decision.
    """

    print("Safety decision")
    print("===============")
    print(f"Action: {decision.action}")
    print(f"Allowed: {decision.allowed}")
    print(f"Movement allowed: {decision.movement_allowed}")
    print(f"State: {decision.state}")
    print(f"Severity: {decision.severity}")

    print("Reasons:")
    for reason in decision.reasons:
        print(f"- {reason}")

    if decision.warnings:
        print("Warnings:")
        for warning in decision.warnings:
            print(f"- {warning}")

    print()


def print_move_report(move_results: list[dict[str, Any]]) -> None:
    """
    Print movement report.
    """

    print("Safe nudge results")
    print("==================")

    if not move_results:
        print("No movement results.")
        print()
        return

    for item in move_results:
        print(
            f"ID {item.get('servo_id')}: "
            f"status={item.get('status')} "
            f"start={item.get('start_position')} "
            f"target={item.get('target_position')} "
            f"final={item.get('final_position')} "
            f"message={item.get('message')}"
        )

    print()


def print_final_notes(enable_movement: bool, moved: bool) -> None:
    """
    Print final operator notes.
    """

    print("Notes")
    print("-----")

    if not enable_movement:
        print("- Movement was disabled because --enable-movement was not provided.")
        print("- This is expected for a conservative first run.")
        print("- After validating power and wiring, run again with --enable-movement.")
    elif moved:
        print("- Safe nudge completed.")
        print("- Verify visually that movement was small and controlled.")
        print("- Check that torque was released after the test.")
    else:
        print("- Movement was requested but did not complete.")
        print("- Review the scan and safety decision before trying again.")

    print("- Keep fingers clear of the servo joints.")
    print("- If a servo stalls, disconnect power and inspect the mechanism.")
    print("- Do not increase --delta until the small nudge is reliable.")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    default_ids = ",".join(str(item) for item in pins.SERVO_IDS)

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 safe servo nudge test."
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
        help=f"Comma-separated servo IDs. Default: {default_ids}",
    )

    parser.add_argument(
        "--delta",
        type=int,
        default=pins.SAFE_NUDGE,
        help=f"Safe nudge amount in encoder units. Default: {pins.SAFE_NUDGE}",
    )

    parser.add_argument(
        "--enable-movement",
        action="store_true",
        help="Allow safety-gated servo movement.",
    )

    parser.add_argument(
        "--require-imu",
        action="store_true",
        help="Require IMU state before movement. Usually false for isolated bench servo tests.",
    )

    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of safe nudge repetitions.",
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

    try:
        ids = parse_ids(args.ids)
    except ValueError as exc:
        print(f"Invalid --ids value: {args.ids}")
        print(f"Error: {exc}")
        return 1

    servo_config = servos.ServoConfig(
        port=args.port,
        baud=args.baud,
    )

    scan = servos.scan_servos(
        servo_ids=ids,
        config=servo_config,
    )

    scan_dict = scan_result_to_plain_dict(scan)

    robot_state = build_robot_state_from_scan(
        scan_result=scan_dict,
        require_imu=args.require_imu,
    )

    decision = evaluate_safe_nudge(
        delta=args.delta,
        robot_state=robot_state,
        enable_movement=args.enable_movement,
        require_imu=args.require_imu,
    )

    move_results: list[dict[str, Any]] = []
    moved = False

    if decision.movement_allowed:
        repetitions = max(1, args.repeat)

        for _ in range(repetitions):
            raw_results = servos.safe_nudge_all(
                servo_ids=extract_found_ids(scan_dict),
                delta=args.delta,
                config=servo_config,
            )
            batch = move_results_to_plain_list(raw_results)
            move_results.extend(batch)

            if not all(normalize_status(item.get("status")) == "OK" for item in batch):
                break

            time.sleep(0.3)

        moved = bool(move_results) and all(
            normalize_status(item.get("status")) == "OK"
            for item in move_results
        )

    output = {
        "scan": scan_dict,
        "safety_decision": decision.to_dict(),
        "movement_requested": True,
        "movement_enabled": args.enable_movement,
        "moved": moved,
        "move_results": move_results,
        "timestamp": time.time(),
    }

    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True, default=str))
    else:
        print()
        print("MicroBot Round V0 safe servo test")
        print("=================================")
        print(f"Mode: {'movement enabled' if args.enable_movement else 'read-only / movement disabled'}")
        print(f"Port: {args.port}")
        print(f"Baud: {args.baud}")
        print(f"IDs: {ids}")
        print(f"Delta: {args.delta}")
        print()

        print_scan_report(scan_dict)
        print_safety_decision(decision)

        if move_results:
            print_move_report(move_results)

        print_final_notes(
            enable_movement=args.enable_movement,
            moved=moved,
        )

    if normalize_status(scan_dict.get("status")) != "OK":
        return 1

    if args.enable_movement and not moved:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())