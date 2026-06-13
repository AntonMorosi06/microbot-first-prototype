"""
MicroBot Round V0 camera module.

This module provides safe, minimal camera helpers for the first MicroBot Round V0
hardware bring-up.

The camera is used for:

- first boot snapshot
- demo evidence
- visual documentation
- future perception experiments

The module tries two Raspberry Pi camera methods:

1. picamera2 Python API
2. rpicam-still command-line fallback

If neither method works, the module returns a structured failure instead of
crashing the whole robot.

Expected hardware reference:

- Raspberry Pi Zero 2 W
- Pi-compatible camera module
- Pi Zero narrow CSI ribbon cable

Camera is not treated as a safety-critical sensor in V0 unless explicitly
configured later. If camera capture fails, the robot may continue in reduced
mode, but the failure must be logged.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import subprocess
import time


os.environ.setdefault("LIBCAMERA_LOG_LEVELS", "*:ERROR")


DEFAULT_PHOTO_DIR = Path("evidence/photos")
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_TIMEOUT_MS = 800


@dataclass(frozen=True)
class CameraConfig:
    """
    Configuration for camera capture.

    photo_dir:
        Directory where camera frames are saved.

    width:
        Capture width in pixels.

    height:
        Capture height in pixels.

    timeout_ms:
        Timeout used by rpicam-still.

    warmup_seconds:
        Small warmup delay for picamera2 before capture.
    """

    photo_dir: Path = DEFAULT_PHOTO_DIR
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    timeout_ms: int = DEFAULT_TIMEOUT_MS
    warmup_seconds: float = 0.4


@dataclass(frozen=True)
class CameraResult:
    """
    Structured result returned by camera operations.

    status:
        OK, WARNING, FAILED, or UNAVAILABLE.

    backend:
        picamera2, rpicam-still, unavailable, or unknown.

    path:
        Saved image path, if any.

    size_bytes:
        Captured file size.

    message:
        Human-readable explanation.
    """

    status: str
    backend: str
    path: str | None
    size_bytes: int | None
    message: str
    timestamp: float


def ensure_photo_dir(photo_dir: str | Path = DEFAULT_PHOTO_DIR) -> Path:
    """
    Create the photo directory if it does not already exist.
    """

    path = Path(photo_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_photo_path(
    label: str = "frame",
    photo_dir: str | Path = DEFAULT_PHOTO_DIR,
    session_id: str | None = None,
) -> Path:
    """
    Build a timestamped photo path.

    Example output:

        evidence/photos/microbot_boot_frame_2026-06-13_10-30-00.jpg
    """

    directory = ensure_photo_dir(photo_dir)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    clean_label = label.strip().lower().replace(" ", "_") or "frame"

    if session_id:
        clean_session = session_id.strip().replace(" ", "_")
        filename = f"microbot_{clean_session}_{clean_label}_{timestamp}.jpg"
    else:
        filename = f"microbot_{clean_label}_{timestamp}.jpg"

    return directory / filename


def file_size(path: str | Path) -> int:
    """
    Return file size in bytes, or 0 if the file does not exist.
    """

    file_path = Path(path)

    if not file_path.exists():
        return 0

    try:
        return file_path.stat().st_size
    except OSError:
        return 0


def _capture_with_picamera2(
    path: Path,
    width: int,
    height: int,
    warmup_seconds: float,
) -> CameraResult:
    """
    Capture a frame using the picamera2 Python API.
    """

    try:
        from picamera2 import Picamera2
    except Exception as exc:
        return CameraResult(
            status="UNAVAILABLE",
            backend="picamera2",
            path=str(path),
            size_bytes=None,
            message=f"picamera2 unavailable: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    try:
        camera = Picamera2()
        camera.configure(
            camera.create_still_configuration(
                main={"size": (int(width), int(height))}
            )
        )
        camera.start()
        time.sleep(max(0.0, warmup_seconds))
        camera.capture_file(str(path))
        camera.stop()
        camera.close()
    except Exception as exc:
        return CameraResult(
            status="FAILED",
            backend="picamera2",
            path=str(path),
            size_bytes=file_size(path),
            message=f"picamera2 capture failed: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    size = file_size(path)

    if size <= 0:
        return CameraResult(
            status="FAILED",
            backend="picamera2",
            path=str(path),
            size_bytes=size,
            message="picamera2 capture completed but output file is missing or empty.",
            timestamp=time.time(),
        )

    return CameraResult(
        status="OK",
        backend="picamera2",
        path=str(path),
        size_bytes=size,
        message="Camera frame captured successfully with picamera2.",
        timestamp=time.time(),
    )


def _capture_with_rpicam_still(
    path: Path,
    width: int,
    height: int,
    timeout_ms: int,
) -> CameraResult:
    """
    Capture a frame using the rpicam-still command-line tool.
    """

    command = [
        "rpicam-still",
        "-n",
        "--width",
        str(int(width)),
        "--height",
        str(int(height)),
        "-o",
        str(path),
        "--timeout",
        str(int(timeout_ms)),
    ]

    try:
        completed = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        )
    except FileNotFoundError:
        return CameraResult(
            status="UNAVAILABLE",
            backend="rpicam-still",
            path=str(path),
            size_bytes=None,
            message="rpicam-still command not found.",
            timestamp=time.time(),
        )
    except subprocess.TimeoutExpired:
        return CameraResult(
            status="FAILED",
            backend="rpicam-still",
            path=str(path),
            size_bytes=file_size(path),
            message="rpicam-still timed out.",
            timestamp=time.time(),
        )
    except Exception as exc:
        return CameraResult(
            status="FAILED",
            backend="rpicam-still",
            path=str(path),
            size_bytes=file_size(path),
            message=f"rpicam-still failed unexpectedly: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    size = file_size(path)

    if completed.returncode != 0:
        error = completed.stderr.strip() or completed.stdout.strip() or "unknown error"
        return CameraResult(
            status="FAILED",
            backend="rpicam-still",
            path=str(path),
            size_bytes=size,
            message=f"rpicam-still returned exit code {completed.returncode}: {error}",
            timestamp=time.time(),
        )

    if size <= 0:
        return CameraResult(
            status="FAILED",
            backend="rpicam-still",
            path=str(path),
            size_bytes=size,
            message="rpicam-still completed but output file is missing or empty.",
            timestamp=time.time(),
        )

    return CameraResult(
        status="OK",
        backend="rpicam-still",
        path=str(path),
        size_bytes=size,
        message="Camera frame captured successfully with rpicam-still.",
        timestamp=time.time(),
    )


def capture_frame(
    output_path: str | Path | None = None,
    label: str = "frame",
    session_id: str | None = None,
    config: CameraConfig | None = None,
) -> CameraResult:
    """
    Capture a single still frame.

    The function tries picamera2 first and rpicam-still second.

    Parameters:
        output_path:
            Optional explicit output file path.

        label:
            Label used for generated filename if output_path is not provided.

        session_id:
            Optional session identifier used in generated filename.

        config:
            CameraConfig object.

    Returns:
        CameraResult.
    """

    cfg = config or CameraConfig()

    if output_path is None:
        path = build_photo_path(
            label=label,
            photo_dir=cfg.photo_dir,
            session_id=session_id,
        )
    else:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

    picamera_result = _capture_with_picamera2(
        path=path,
        width=cfg.width,
        height=cfg.height,
        warmup_seconds=cfg.warmup_seconds,
    )

    if picamera_result.status == "OK":
        return picamera_result

    rpicam_result = _capture_with_rpicam_still(
        path=path,
        width=cfg.width,
        height=cfg.height,
        timeout_ms=cfg.timeout_ms,
    )

    if rpicam_result.status == "OK":
        return rpicam_result

    return CameraResult(
        status="FAILED",
        backend="unavailable",
        path=str(path),
        size_bytes=file_size(path),
        message=(
            "Camera capture failed. "
            f"picamera2 result: {picamera_result.message} | "
            f"rpicam-still result: {rpicam_result.message}"
        ),
        timestamp=time.time(),
    )


def capture_boot_frame(
    session_id: str | None = None,
    config: CameraConfig | None = None,
) -> CameraResult:
    """
    Capture the first boot frame for demo evidence.
    """

    return capture_frame(
        label="boot_frame",
        session_id=session_id,
        config=config,
    )


def capture_obstacle_frame(
    session_id: str | None = None,
    config: CameraConfig | None = None,
) -> CameraResult:
    """
    Capture a frame when an obstacle event occurs.
    """

    return capture_frame(
        label="obstacle_frame",
        session_id=session_id,
        config=config,
    )


def capture_post_movement_frame(
    session_id: str | None = None,
    config: CameraConfig | None = None,
) -> CameraResult:
    """
    Capture a frame after a movement action.
    """

    return capture_frame(
        label="post_movement_frame",
        session_id=session_id,
        config=config,
    )


def camera_self_check(config: CameraConfig | None = None) -> dict[str, str | int | float | None]:
    """
    Run a camera self-check by capturing one frame.

    This is designed for self_check.py.
    """

    result = capture_frame(label="camera_self_check", config=config)

    return {
        "status": result.status,
        "backend": result.backend,
        "path": result.path,
        "size_bytes": result.size_bytes,
        "message": result.message,
        "timestamp": result.timestamp,
    }


def format_camera_result(result: CameraResult) -> str:
    """
    Format a camera result for terminal output.
    """

    return (
        "Camera result\n"
        "=============\n"
        f"Status: {result.status}\n"
        f"Backend: {result.backend}\n"
        f"Path: {result.path}\n"
        f"Size bytes: {result.size_bytes}\n"
        f"Message: {result.message}\n"
    )


def print_camera_self_check(config: CameraConfig | None = None) -> CameraResult:
    """
    Capture one frame, print result, and return the CameraResult.
    """

    result = capture_frame(label="camera_self_check", config=config)
    print(format_camera_result(result))
    return result


def main() -> int:
    """
    CLI entry point for quick camera testing.

    Run from repository root:

        python setup/microbot/camera.py

    On Raspberry Pi OS, depending on camera stack and permissions, this may need
    to run directly on the Pi with the camera enabled.
    """

    result = print_camera_self_check()

    if result.status == "OK":
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())