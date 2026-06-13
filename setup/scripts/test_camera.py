#!/usr/bin/env python3
"""
MicroBot Round V0 camera test.

This script tests the MicroBot camera subsystem by capturing one still frame.

Reference hardware pattern:

- Raspberry Pi Zero 2 W
- Pi-compatible CSI camera
- Pi Zero narrow CSI ribbon
- Raspberry Pi OS camera stack
- picamera2 Python API or rpicam-still CLI fallback

Run from repository root:

    python setup/scripts/test_camera.py

Custom resolution:

    python setup/scripts/test_camera.py --width 1280 --height 720

Custom output path:

    python setup/scripts/test_camera.py --output evidence/photos/test_frame.jpg

JSON output:

    python setup/scripts/test_camera.py --json

Notes:
Camera capture usually needs to run on the Raspberry Pi with the camera connected
and enabled. On a normal laptop, this test will usually fail or return unavailable.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import camera  # noqa: E402
from microbot.config import get_config, make_session_id  # noqa: E402


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
    Normalize status text.
    """

    if value is None:
        return "UNKNOWN"

    return str(value).strip().upper()


def file_exists_and_size(path: str | None) -> tuple[bool, int]:
    """
    Return whether a file exists and its size in bytes.
    """

    if not path:
        return False, 0

    file_path = Path(path)

    if not file_path.exists():
        return False, 0

    try:
        return True, file_path.stat().st_size
    except OSError:
        return True, 0


def print_camera_report(result: dict[str, Any]) -> None:
    """
    Print a readable camera report.
    """

    status = normalize_status(result.get("status"))
    backend = result.get("backend")
    path = result.get("path")
    size_bytes = result.get("size_bytes")
    message = result.get("message")

    exists, real_size = file_exists_and_size(path)

    print("MicroBot Round V0 camera test")
    print("=============================")
    print()
    print(f"Status: {status}")
    print(f"Backend: {backend}")
    print(f"Path: {path}")
    print(f"Reported size bytes: {size_bytes}")
    print(f"File exists: {exists}")
    print(f"Actual file size bytes: {real_size}")
    print(f"Message: {message}")
    print()

    print("Notes")
    print("-----")

    if status == "OK":
        print("- Camera capture completed successfully.")
        print("- Open or copy the saved image to visually inspect it.")
        print("- This frame can be used as evidence for the hardware bring-up log.")
    else:
        print("- If picamera2 is unavailable, check Raspberry Pi camera packages.")
        print("- If rpicam-still is unavailable, check Raspberry Pi OS camera tools.")
        print("- Check the CSI ribbon orientation and camera connector.")
        print("- Make sure the camera is connected before boot when required.")
        print("- On a non-Raspberry Pi machine, this failure is expected.")

    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    config = get_config()

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 camera capture test."
    )

    parser.add_argument(
        "--width",
        type=int,
        default=config.camera.width,
        help="Capture width in pixels.",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=config.camera.height,
        help="Capture height in pixels.",
    )

    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=config.camera.timeout_ms,
        help="rpicam-still timeout in milliseconds.",
    )

    parser.add_argument(
        "--warmup",
        type=float,
        default=config.camera.warmup_seconds,
        help="picamera2 warmup delay in seconds.",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Optional explicit output JPG path.",
    )

    parser.add_argument(
        "--label",
        default="camera_test",
        help="Label used for generated filename when --output is not provided.",
    )

    parser.add_argument(
        "--session-id",
        default=None,
        help="Optional session ID used in generated filename.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output.",
    )

    return parser


def main() -> int:
    """
    Main entry point.
    """

    args = build_arg_parser().parse_args()

    config = get_config()
    config.ensure_runtime_directories()

    session_id = args.session_id or make_session_id("camera_test")

    camera_config = camera.CameraConfig(
        photo_dir=config.paths.photos_dir,
        width=args.width,
        height=args.height,
        timeout_ms=args.timeout_ms,
        warmup_seconds=args.warmup,
    )

    result = camera.capture_frame(
        output_path=args.output,
        label=args.label,
        session_id=session_id,
        config=camera_config,
    )

    result_dict = to_dict_safe(result)
    result_dict["session_id"] = session_id
    result_dict["requested_width"] = args.width
    result_dict["requested_height"] = args.height

    if args.json:
        print(json.dumps(result_dict, indent=2, sort_keys=True, default=str))
    else:
        print_camera_report(result_dict)

    return 0 if normalize_status(result_dict.get("status")) == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())