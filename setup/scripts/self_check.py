#!/usr/bin/env python3
"""
MicroBot Round V0 self-check script.

This script runs the first integrated diagnostic check for MicroBot Round V0.

It checks:

- configuration
- logger
- safety module
- LED ring
- audio tools
- camera capture
- IMU
- read-only servo scan
- distance sensor status
- battery status

Safety:
This script does NOT command movement.
It does NOT run safe nudge.
It only checks availability, configuration and read-only subsystem status.

Run from the repository root:

    python setup/scripts/self_check.py

On Raspberry Pi, LED checks may require:

    sudo -E python setup/scripts/self_check.py

For a lighter software-only check:

    python setup/scripts/self_check.py --skip-leds --skip-camera --skip-imu --skip-servos
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


from microbot import audio  # noqa: E402
from microbot import battery  # noqa: E402
from microbot import camera  # noqa: E402
from microbot import distance  # noqa: E402
from microbot import imu  # noqa: E402
from microbot import leds  # noqa: E402
from microbot import safety  # noqa: E402
from microbot import servos  # noqa: E402
from microbot.config import get_config, make_session_id  # noqa: E402
from microbot.logger import MicroBotLogger  # noqa: E402


PASS_STATUSES = {"OK", "PASSED"}
WARNING_STATUSES = {"WARNING", "UNAVAILABLE", "SKIPPED"}
FAIL_STATUSES = {"FAILED", "ERROR", "CRITICAL"}


def normalize_status(status: Any) -> str:
    """
    Normalize a status value.
    """

    if status is None:
        return "UNKNOWN"

    return str(status).strip().upper()


def result_status(result: Any) -> str:
    """
    Extract a status value from a dictionary or object.
    """

    if isinstance(result, dict):
        return normalize_status(result.get("status"))

    if hasattr(result, "status"):
        return normalize_status(getattr(result, "status"))

    return "UNKNOWN"


def result_message(result: Any) -> str:
    """
    Extract a readable message from a dictionary or object.
    """

    if isinstance(result, dict):
        return str(result.get("message", ""))

    if hasattr(result, "message"):
        return str(getattr(result, "message"))

    return str(result)


def to_dict_safe(value: Any) -> dict[str, Any]:
    """
    Convert a result object to a dictionary when possible.
    """

    if isinstance(value, dict):
        return value

    if hasattr(value, "to_dict"):
        try:
            return value.to_dict()
        except Exception:
            pass

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return {
        "status": "UNKNOWN",
        "message": str(value),
    }


def skipped_result(message: str) -> dict[str, Any]:
    """
    Build a standard skipped result.
    """

    return {
        "status": "SKIPPED",
        "message": message,
        "timestamp": time.time(),
    }


def failed_result(message: str, exc: BaseException | None = None) -> dict[str, Any]:
    """
    Build a standard failed result.
    """

    payload: dict[str, Any] = {
        "status": "FAILED",
        "message": message,
        "timestamp": time.time(),
    }

    if exc is not None:
        payload["error_type"] = type(exc).__name__
        payload["error"] = str(exc)

    return payload


def run_config_check() -> dict[str, Any]:
    """
    Check configuration and runtime directories.
    """

    try:
        config = get_config()
        config.ensure_runtime_directories()

        return {
            "status": "OK",
            "message": "Configuration loaded and runtime directories are available.",
            "project_name": config.project_name,
            "project_slug": config.project_slug,
            "software_version": config.software_version,
            "hardware_version": config.hardware_version,
            "status_label": config.status,
            "project_root": str(config.paths.project_root),
            "logs_dir": str(config.paths.logs_dir),
            "photos_dir": str(config.paths.photos_dir),
            "reports_dir": str(config.paths.reports_dir),
            "movement_enabled": config.features.enable_movement,
            "timestamp": time.time(),
        }

    except Exception as exc:
        return failed_result("Configuration check failed.", exc)


def run_logger_check(logger: MicroBotLogger) -> dict[str, Any]:
    """
    Check that the main logger is active.
    """

    try:
        logger.info(
            "logger",
            "Logger check event written from self_check.py.",
            {
                "session_id": logger.session_id,
                "jsonl_path": str(logger.paths.jsonl_path),
                "report_path": str(logger.paths.markdown_report_path),
            },
        )

        return {
            "status": "OK",
            "message": "Logger is active and accepted a test event.",
            "session_id": logger.session_id,
            "jsonl_path": str(logger.paths.jsonl_path),
            "report_path": str(logger.paths.markdown_report_path),
            "timestamp": time.time(),
        }

    except Exception as exc:
        return failed_result("Logger check failed.", exc)


def run_safety_check() -> dict[str, Any]:
    """
    Run safety module self-check.
    """

    try:
        return safety.safety_self_check()
    except Exception as exc:
        return failed_result("Safety self-check failed.", exc)


def run_led_check(skip: bool) -> dict[str, Any]:
    """
    Run LED self-check.
    """

    if skip:
        return skipped_result("LED check skipped by command-line flag.")

    try:
        return leds.led_self_check()
    except Exception as exc:
        return failed_result("LED self-check failed.", exc)


def run_audio_check(skip: bool, include_microphone: bool) -> dict[str, Any]:
    """
    Run audio capability check and optional microphone test.
    """

    if skip:
        return skipped_result("Audio check skipped by command-line flag.")

    try:
        report = audio.audio_self_check()

        result: dict[str, Any] = {
            "status": "OK",
            "message": "Audio capability check completed.",
            "capabilities": report,
            "microphone_test": None,
            "timestamp": time.time(),
        }

        speech_engine = report.get("speech_engine") if isinstance(report, dict) else None
        if not speech_engine:
            result["status"] = "UNAVAILABLE"
            result["message"] = "No speech engine available. Install espeak-ng or flite."

        if include_microphone:
            mic_result = audio.microphone_level_test()
            result["microphone_test"] = to_dict_safe(mic_result)

            mic_status = result_status(mic_result)
            if mic_status in FAIL_STATUSES:
                result["status"] = "WARNING"
                result["message"] = "Audio check completed, but microphone test failed or is unavailable."

        return result

    except Exception as exc:
        return failed_result("Audio check failed.", exc)


def run_camera_check(skip: bool, session_id: str) -> dict[str, Any]:
    """
    Run camera self-check.
    """

    if skip:
        return skipped_result("Camera check skipped by command-line flag.")

    try:
        result = camera.capture_frame(
            label="self_check_camera",
            session_id=session_id,
        )
        return to_dict_safe(result)
    except Exception as exc:
        return failed_result("Camera check failed.", exc)


def run_imu_check(skip: bool) -> dict[str, Any]:
    """
    Run IMU self-check.
    """

    if skip:
        return skipped_result("IMU check skipped by command-line flag.")

    try:
        return imu.imu_self_check()
    except Exception as exc:
        return failed_result("IMU self-check failed.", exc)


def run_servo_check(skip: bool) -> dict[str, Any]:
    """
    Run read-only servo scan.

    This does not command movement.
    """

    if skip:
        return skipped_result("Servo scan skipped by command-line flag.")

    try:
        return servos.servo_self_check()
    except Exception as exc:
        return failed_result("Servo scan failed.", exc)


def run_distance_check(skip: bool) -> dict[str, Any]:
    """
    Run distance sensor status check.

    Default may be UNAVAILABLE if no sensor is installed.
    """

    if skip:
        return skipped_result("Distance check skipped by command-line flag.")

    try:
        return distance.distance_self_check()
    except Exception as exc:
        return failed_result("Distance check failed.", exc)


def run_battery_check(skip: bool) -> dict[str, Any]:
    """
    Run battery status check.

    Default may be UNAVAILABLE if no ADC/fuel gauge is installed.
    """

    if skip:
        return skipped_result("Battery check skipped by command-line flag.")

    try:
        return battery.battery_self_check()
    except Exception as exc:
        return failed_result("Battery check failed.", exc)


def summarize_results(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Build a global summary from subsystem results.
    """

    counts = {
        "OK": 0,
        "WARNING": 0,
        "UNAVAILABLE": 0,
        "SKIPPED": 0,
        "FAILED": 0,
        "UNKNOWN": 0,
    }

    failed_subsystems: list[str] = []
    warning_subsystems: list[str] = []
    unavailable_subsystems: list[str] = []
    skipped_subsystems: list[str] = []

    for subsystem, result in results.items():
        status = result_status(result)

        if status in PASS_STATUSES:
            counts["OK"] += 1
        elif status == "WARNING":
            counts["WARNING"] += 1
            warning_subsystems.append(subsystem)
        elif status == "UNAVAILABLE":
            counts["UNAVAILABLE"] += 1
            unavailable_subsystems.append(subsystem)
        elif status == "SKIPPED":
            counts["SKIPPED"] += 1
            skipped_subsystems.append(subsystem)
        elif status in FAIL_STATUSES:
            counts["FAILED"] += 1
            failed_subsystems.append(subsystem)
        else:
            counts["UNKNOWN"] += 1
            warning_subsystems.append(subsystem)

    if counts["FAILED"] > 0:
        global_status = "FAILED"
        message = "One or more required self-checks failed."
    elif counts["WARNING"] > 0 or counts["UNAVAILABLE"] > 0 or counts["UNKNOWN"] > 0:
        global_status = "WARNING"
        message = "Self-check completed with warnings or unavailable optional hardware."
    else:
        global_status = "OK"
        message = "Self-check completed successfully."

    return {
        "status": global_status,
        "message": message,
        "counts": counts,
        "failed_subsystems": failed_subsystems,
        "warning_subsystems": warning_subsystems,
        "unavailable_subsystems": unavailable_subsystems,
        "skipped_subsystems": skipped_subsystems,
        "timestamp": time.time(),
    }


def print_table(results: dict[str, dict[str, Any]], summary: dict[str, Any]) -> None:
    """
    Print a compact terminal summary table.
    """

    print()
    print("MicroBot Round V0 self-check")
    print("============================")
    print()

    width = max(len(name) for name in results.keys()) if results else 10

    for subsystem, result in results.items():
        status = result_status(result)
        message = result_message(result)
        print(f"{subsystem:<{width}}  {status:<12}  {message}")

    print()
    print("Summary")
    print("-------")
    print(f"Status: {summary['status']}")
    print(f"Message: {summary['message']}")
    print(f"Counts: {summary['counts']}")
    print()


def log_results(
    logger: MicroBotLogger,
    results: dict[str, dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    """
    Log all subsystem results.
    """

    for subsystem, result in results.items():
        logger.log_subsystem_result(
            subsystem=subsystem,
            result=result,
            event_type="self_check",
        )

    logger.log_event(
        level="INFO" if summary["status"] == "OK" else "WARNING",
        event_type="self_check_summary",
        subsystem="system",
        message=summary["message"],
        data=summary,
    )


def write_summary_json(
    output_path: Path,
    session_id: str,
    results: dict[str, dict[str, Any]],
    summary: dict[str, Any],
) -> Path:
    """
    Write final self-check summary JSON.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "session_id": session_id,
        "summary": summary,
        "results": results,
        "timestamp": time.time(),
    }

    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )

    return output_path


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build command-line parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 integrated self-check."
    )

    parser.add_argument(
        "--skip-leds",
        action="store_true",
        help="Skip LED self-check.",
    )

    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Skip audio capability check.",
    )

    parser.add_argument(
        "--skip-mic",
        action="store_true",
        help="Skip optional microphone level check.",
    )

    parser.add_argument(
        "--skip-camera",
        action="store_true",
        help="Skip camera capture check.",
    )

    parser.add_argument(
        "--skip-imu",
        action="store_true",
        help="Skip IMU self-check.",
    )

    parser.add_argument(
        "--skip-servos",
        action="store_true",
        help="Skip read-only servo scan.",
    )

    parser.add_argument(
        "--skip-distance",
        action="store_true",
        help="Skip distance sensor check.",
    )

    parser.add_argument(
        "--skip-battery",
        action="store_true",
        help="Skip battery status check.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON output.",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Optional path for final JSON summary.",
    )

    return parser


def main() -> int:
    """
    Main entry point.
    """

    args = build_arg_parser().parse_args()

    config = get_config()
    config.ensure_runtime_directories()

    session_id = make_session_id("self_check")

    with MicroBotLogger(
        session_id=session_id,
        session_name="MicroBot Round V0 Self-Check",
        print_to_terminal=False,
    ) as logger:
        results: dict[str, dict[str, Any]] = {}

        results["config"] = run_config_check()
        results["logger"] = run_logger_check(logger)
        results["safety"] = run_safety_check()
        results["leds"] = run_led_check(skip=args.skip_leds)
        results["audio"] = run_audio_check(
            skip=args.skip_audio,
            include_microphone=not args.skip_mic,
        )
        results["camera"] = run_camera_check(
            skip=args.skip_camera,
            session_id=session_id,
        )
        results["imu"] = run_imu_check(skip=args.skip_imu)
        results["servos"] = run_servo_check(skip=args.skip_servos)
        results["distance"] = run_distance_check(skip=args.skip_distance)
        results["battery"] = run_battery_check(skip=args.skip_battery)

        summary = summarize_results(results)
        log_results(logger, results, summary)

        if args.output:
            output_path = Path(args.output)
        else:
            output_path = config.paths.reports_dir / f"{session_id}_summary.json"

        written_summary = write_summary_json(
            output_path=output_path,
            session_id=session_id,
            results=results,
            summary=summary,
        )

        summary["summary_json_path"] = str(written_summary)

    if args.json:
        print(
            json.dumps(
                {
                    "session_id": session_id,
                    "summary": summary,
                    "results": results,
                },
                indent=2,
                sort_keys=True,
                default=str,
            )
        )
    else:
        print_table(results, summary)
        print(f"Session ID: {session_id}")
        print(f"Summary JSON: {summary['summary_json_path']}")
        print()

    if summary["status"] == "FAILED":
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())