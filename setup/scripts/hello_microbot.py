#!/usr/bin/env python3
"""
MicroBot Round V0 hello demo.

This script is the first integrated bring-up demo for MicroBot Round V0.

It tries to run the main subsystems together:

- logger session
- LED boot/status
- startup voice
- camera boot frame
- IMU self-check
- read-only servo scan
- optional safety-gated safe nudge

Default behavior:
The script does NOT move the robot by default.

To allow the safe nudge movement, run:

    python setup/scripts/hello_microbot.py --enable-movement --safe-nudge

On Raspberry Pi, LED control may require:

    sudo -E python setup/scripts/hello_microbot.py

Full hardware demo, after power and wiring validation:

    sudo -E python setup/scripts/hello_microbot.py --enable-movement --safe-nudge

The script is intentionally tolerant: if one subsystem is missing, it logs the
failure and continues where safe.
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
from microbot import camera  # noqa: E402
from microbot import imu  # noqa: E402
from microbot import leds  # noqa: E402
from microbot import servos  # noqa: E402
from microbot import safety  # noqa: E402
from microbot.config import get_config, make_session_id  # noqa: E402
from microbot.logger import MicroBotLogger  # noqa: E402


def print_header() -> None:
    """
    Print demo title.
    """

    print()
    print("MicroBot Round V0")
    print("=================")
    print("Integrated hello demo")
    print()


def result_status(result: Any) -> str:
    """
    Extract status from dict, dataclass-like object or fallback.
    """

    if isinstance(result, dict):
        return str(result.get("status", "UNKNOWN")).upper()

    if hasattr(result, "status"):
        return str(getattr(result, "status")).upper()

    return "UNKNOWN"


def result_message(result: Any) -> str:
    """
    Extract message from dict, dataclass-like object or fallback.
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

    return {"value": str(value)}


def run_led_boot(logger: MicroBotLogger, enabled: bool) -> bool:
    """
    Run LED boot animation if possible.
    """

    if not enabled:
        logger.info("leds", "LED boot skipped by configuration.")
        return False

    try:
        ring = leds.LedRing()
        ring.boot_animation()
        logger.info("leds", "LED boot animation completed.")
        return True
    except Exception as exc:
        logger.warning(
            "leds",
            "LED boot animation skipped.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
                "hint": "On Raspberry Pi, try sudo -E when using WS2812 LEDs.",
            },
        )
        return False


def set_led_status(logger: MicroBotLogger, color_name: str) -> None:
    """
    Best-effort LED status update.
    """

    try:
        result = leds.safe_set_status(color_name)
        logger.log_subsystem_result("leds", result, event_type="status")
    except Exception as exc:
        logger.warning(
            "leds",
            f"Could not set LED status to {color_name}.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )


def run_audio_startup(logger: MicroBotLogger, enabled: bool, phrase: str) -> bool:
    """
    Speak startup phrase if possible.
    """

    if not enabled:
        logger.info("audio", "Audio startup skipped by configuration.")
        return False

    try:
        result = audio.speak(phrase)
        logger.log_subsystem_result("audio", result, event_type="startup_voice")
        return result_status(result) == "OK"
    except Exception as exc:
        logger.warning(
            "audio",
            "Audio startup failed or unavailable.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
        return False


def run_camera_boot_capture(
    logger: MicroBotLogger,
    enabled: bool,
    session_id: str,
) -> bool:
    """
    Capture boot frame if possible.
    """

    if not enabled:
        logger.info("camera", "Camera boot capture skipped by configuration.")
        return False

    try:
        result = camera.capture_boot_frame(session_id=session_id)
        logger.log_subsystem_result("camera", result, event_type="boot_capture")
        return result_status(result) == "OK"
    except Exception as exc:
        logger.warning(
            "camera",
            "Camera boot capture failed or unavailable.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
        return False


def run_imu_self_check(logger: MicroBotLogger, enabled: bool) -> dict[str, Any]:
    """
    Run IMU self-check.
    """

    if not enabled:
        result = {
            "status": "UNAVAILABLE",
            "message": "IMU self-check skipped by configuration.",
        }
        logger.log_subsystem_result("imu", result, event_type="self_check")
        return result

    try:
        result = imu.imu_self_check()
        logger.log_subsystem_result("imu", result, event_type="self_check")
        return result
    except Exception as exc:
        result = {
            "status": "FAILED",
            "message": f"IMU self-check failed: {type(exc).__name__}: {exc}",
        }
        logger.log_subsystem_result("imu", result, event_type="self_check")
        return result


def run_servo_scan(logger: MicroBotLogger, enabled: bool) -> dict[str, Any]:
    """
    Run read-only servo scan.
    """

    if not enabled:
        result = {
            "status": "UNAVAILABLE",
            "message": "Servo scan skipped by configuration.",
            "found_ids": (),
        }
        logger.log_subsystem_result("servos", result, event_type="scan")
        return result

    try:
        result = servos.scan_servos()
        result_dict = servos.scan_result_to_dict(result)
        logger.log_subsystem_result("servos", result_dict, event_type="scan")
        return result_dict
    except Exception as exc:
        result = {
            "status": "FAILED",
            "message": f"Servo scan failed: {type(exc).__name__}: {exc}",
            "found_ids": (),
        }
        logger.log_subsystem_result("servos", result, event_type="scan")
        return result


def extract_tilt_from_imu_result(imu_result: dict[str, Any]) -> float | None:
    """
    Extract tilt_degrees from IMU self-check result if available.
    """

    reading = imu_result.get("reading")

    if not isinstance(reading, dict):
        return None

    tilt = reading.get("tilt_degrees")

    if tilt is None:
        return None

    try:
        return float(tilt)
    except (TypeError, ValueError):
        return None


def extract_servo_positions(scan_result: dict[str, Any]) -> dict[int, int]:
    """
    Extract servo positions from scan result.
    """

    positions: dict[int, int] = {}

    servos_data = scan_result.get("servos", ())

    if not isinstance(servos_data, (list, tuple)):
        return positions

    for item in servos_data:
        if not isinstance(item, dict):
            continue

        servo_id = item.get("servo_id")
        position = item.get("position")

        if servo_id is None or position is None:
            continue

        try:
            positions[int(servo_id)] = int(position)
        except (TypeError, ValueError):
            continue

    return positions


def build_robot_state_from_results(
    imu_result: dict[str, Any],
    servo_scan_result: dict[str, Any],
) -> safety.RobotState:
    """
    Build RobotState for safety evaluation.
    """

    found_ids_raw = servo_scan_result.get("found_ids", ())
    found_ids: tuple[int, ...]

    if isinstance(found_ids_raw, (list, tuple)):
        found_ids = tuple(int(item) for item in found_ids_raw)
    else:
        found_ids = ()

    return safety.RobotState(
        emergency_stop=False,
        servo_scan_ok=result_status(servo_scan_result) == "OK",
        servo_ids_found=found_ids,
        servo_positions=extract_servo_positions(servo_scan_result),
        imu_status=result_status(imu_result),
        tilt_degrees=extract_tilt_from_imu_result(imu_result),
        distance_status=None,
        distance_cm=None,
        battery_status=None,
        battery_voltage=None,
        failed_movement_count=0,
        safe_mode_active=False,
    )


def evaluate_safe_nudge_permission(
    logger: MicroBotLogger,
    robot_state: safety.RobotState,
    enable_movement: bool,
) -> safety.SafetyDecision:
    """
    Evaluate safety permission for safe nudge.
    """

    request = safety.MovementRequest(
        action="SAFE_NUDGE",
        nudge_amount=safety.SAFE_NUDGE,
        reason="hello_microbot integrated demo",
    )

    config = safety.SafetyConfig(
        hardware_movement_enabled=enable_movement,
        require_distance_for_forward_move=False,
        block_movement_if_distance_unavailable=False,
        block_movement_if_battery_unavailable=False,
    )

    decision = safety.evaluate_safety(
        request=request,
        state=robot_state,
        config=config,
    )

    logger.log_event(
        level="INFO" if decision.allowed else "WARNING",
        event_type="safety_decision",
        subsystem="safety",
        message="Safety decision evaluated for SAFE_NUDGE.",
        data=decision.to_dict(),
    )

    return decision


def run_safe_nudge_if_allowed(
    logger: MicroBotLogger,
    enable_movement: bool,
    requested: bool,
    robot_state: safety.RobotState,
) -> bool:
    """
    Run safe nudge only if requested and allowed by safety layer.
    """

    if not requested:
        logger.info(
            "servos",
            "Safe nudge not requested. No movement will be performed.",
        )
        return False

    decision = evaluate_safe_nudge_permission(
        logger=logger,
        robot_state=robot_state,
        enable_movement=enable_movement,
    )

    if not decision.movement_allowed:
        logger.warning(
            "safety",
            "Safe nudge blocked by safety layer.",
            {
                "reasons": decision.reasons,
                "warnings": decision.warnings,
            },
        )
        set_led_status(logger, "red")
        return False

    try:
        results = servos.safe_nudge_all(delta=safety.SAFE_NUDGE)
        formatted_results = [servos.move_result_to_dict(item) for item in results]

        logger.log_event(
            level="INFO" if all(item.get("status") == "OK" for item in formatted_results) else "WARNING",
            event_type="safe_nudge",
            subsystem="servos",
            message="Safe nudge sequence completed.",
            data={"results": formatted_results},
        )

        return all(item.get("status") == "OK" for item in formatted_results)

    except Exception as exc:
        logger.error(
            "servos",
            "Safe nudge failed unexpectedly.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
        return False


def run_optional_microphone_test(logger: MicroBotLogger, enabled: bool) -> bool:
    """
    Run optional microphone level test.
    """

    if not enabled:
        logger.info("audio", "Microphone test skipped.")
        return False

    try:
        result = audio.microphone_level_test()
        logger.log_subsystem_result("audio", result, event_type="microphone_test")
        return result_status(result) == "OK"
    except Exception as exc:
        logger.warning(
            "audio",
            "Microphone test failed or unavailable.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
        return False


def final_voice(logger: MicroBotLogger, enabled: bool, phrase: str) -> bool:
    """
    Speak final phrase.
    """

    if not enabled:
        return False

    try:
        result = audio.speak(phrase)
        logger.log_subsystem_result("audio", result, event_type="final_voice")
        return result_status(result) == "OK"
    except Exception as exc:
        logger.warning(
            "audio",
            "Final voice failed or unavailable.",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
        return False


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build command-line parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 integrated hello demo."
    )

    parser.add_argument(
        "--enable-movement",
        action="store_true",
        help="Allow safety-gated movement. Movement is disabled by default.",
    )

    parser.add_argument(
        "--safe-nudge",
        action="store_true",
        help="Request safe nudge movement after self-check and servo scan.",
    )

    parser.add_argument(
        "--skip-leds",
        action="store_true",
        help="Skip LED boot/status operations.",
    )

    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Skip startup and final voice.",
    )

    parser.add_argument(
        "--skip-camera",
        action="store_true",
        help="Skip camera boot capture.",
    )

    parser.add_argument(
        "--skip-imu",
        action="store_true",
        help="Skip IMU self-check.",
    )

    parser.add_argument(
        "--skip-servos",
        action="store_true",
        help="Skip servo scan and movement.",
    )

    parser.add_argument(
        "--mic-test",
        action="store_true",
        help="Run optional microphone level test.",
    )

    parser.add_argument(
        "--json-summary",
        action="store_true",
        help="Print final JSON summary.",
    )

    return parser


def main() -> int:
    """
    Main entry point.
    """

    args = build_arg_parser().parse_args()
    config = get_config()
    config.ensure_runtime_directories()

    session_id = make_session_id("hello_microbot")

    print_header()

    with MicroBotLogger(
        session_id=session_id,
        session_name="MicroBot Round V0 Hello Demo",
        print_to_terminal=True,
    ) as logger:
        logger.info(
            "system",
            "Hello demo started.",
            {
                "session_id": session_id,
                "enable_movement": args.enable_movement,
                "safe_nudge_requested": args.safe_nudge,
            },
        )

        if args.enable_movement:
            logger.warning(
                "safety",
                "Movement flag enabled. Physical movement is still safety-gated.",
            )
        else:
            logger.info(
                "safety",
                "Movement is disabled. Servo scan may run, but no movement will be performed.",
            )

        led_ok = run_led_boot(
            logger=logger,
            enabled=not args.skip_leds,
        )

        audio_ok = run_audio_startup(
            logger=logger,
            enabled=not args.skip_audio,
            phrase=config.audio.startup_phrase,
        )

        camera_ok = run_camera_boot_capture(
            logger=logger,
            enabled=not args.skip_camera,
            session_id=session_id,
        )

        imu_result = run_imu_self_check(
            logger=logger,
            enabled=not args.skip_imu,
        )

        servo_scan_result = run_servo_scan(
            logger=logger,
            enabled=not args.skip_servos,
        )

        mic_ok = run_optional_microphone_test(
            logger=logger,
            enabled=args.mic_test and not args.skip_audio,
        )

        robot_state = build_robot_state_from_results(
            imu_result=imu_result,
            servo_scan_result=servo_scan_result,
        )

        movement_ok = run_safe_nudge_if_allowed(
            logger=logger,
            enable_movement=args.enable_movement,
            requested=args.safe_nudge and not args.skip_servos,
            robot_state=robot_state,
        )

        if movement_ok:
            set_led_status(logger, "green")
        elif args.safe_nudge:
            set_led_status(logger, "red")
        else:
            set_led_status(logger, "blue")

        final_audio_ok = final_voice(
            logger=logger,
            enabled=not args.skip_audio,
            phrase=config.audio.complete_phrase,
        )

        summary = {
            "session_id": session_id,
            "led_ok": led_ok,
            "audio_startup_ok": audio_ok,
            "camera_ok": camera_ok,
            "imu_status": result_status(imu_result),
            "servo_scan_status": result_status(servo_scan_result),
            "microphone_ok": mic_ok,
            "movement_requested": args.safe_nudge,
            "movement_enabled": args.enable_movement,
            "movement_ok": movement_ok,
            "final_audio_ok": final_audio_ok,
            "status": "OK",
        }

        logger.info(
            "system",
            "Hello demo completed.",
            summary,
        )

        print()
        print("Demo summary")
        print("============")
        print(f"Session ID: {session_id}")
        print(f"LED boot: {led_ok}")
        print(f"Audio startup: {audio_ok}")
        print(f"Camera: {camera_ok}")
        print(f"IMU: {result_status(imu_result)}")
        print(f"Servo scan: {result_status(servo_scan_result)}")
        print(f"Movement requested: {args.safe_nudge}")
        print(f"Movement enabled: {args.enable_movement}")
        print(f"Movement OK: {movement_ok}")
        print()

        if args.json_summary:
            print(json.dumps(summary, indent=2, sort_keys=True, default=str))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())