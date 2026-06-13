"""
MicroBot Round V0 distance sensor module.

This module provides safe, minimal distance / obstacle helpers for the first
MicroBot Round V0 hardware bring-up.

The distance sensor is used for:

- basic obstacle detection
- forward movement blocking
- safety events
- demo evidence
- future perception experiments

Recommended V0 sensor:

- VL53L0X or VL53L1X time-of-flight distance sensor

Important V0 limitation:
The distance sensor may not be installed in the first build. If unavailable,
this module returns UNAVAILABLE instead of pretending that the path is clear.

Movement code should treat UNAVAILABLE carefully. If forward movement depends
on obstacle awareness, movement should be blocked or the robot should run in
reduced mode.

Optional future Python dependency for real VL53L0X hardware:

    pip install adafruit-circuitpython-vl53l0x

The module also supports mock, manual, environment-variable and file-based
distance readings for offline testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import os
import time


DISTANCE_ENV_VAR = "MICROBOT_DISTANCE_CM"


@dataclass(frozen=True)
class DistanceConfig:
    """
    Distance sensor configuration.

    source:
        unavailable, mock, manual, env, file, or vl53l0x.

    mock_distance_cm:
        Used by mock/manual source.

    distance_file:
        Used by file source. The file should contain one number in centimeters.

    warning_distance_cm:
        Distance below which the robot should warn.

    stop_distance_cm:
        Distance below which forward movement must be blocked.

    critical_distance_cm:
        Distance below which the obstacle is extremely close.

    max_valid_distance_cm:
        Readings above this value are considered invalid or out of useful range
        for the V0 safety demo.
    """

    source: str = "unavailable"

    mock_distance_cm: float | None = None
    distance_file: str | None = None

    i2c_address: int = 0x29

    warning_distance_cm: float = 25.0
    stop_distance_cm: float = 15.0
    critical_distance_cm: float = 8.0

    min_valid_distance_cm: float = 0.0
    max_valid_distance_cm: float = 400.0

    block_forward_if_unavailable: bool = True


@dataclass(frozen=True)
class DistanceStatus:
    """
    Structured distance status.

    status:
        OK, WARNING, OBSTACLE, CRITICAL, UNAVAILABLE, or FAILED.

    distance_cm:
        Measured or mocked distance in centimeters.

    obstacle_detected:
        True when an obstacle is below the stop threshold.

    forward_movement_allowed:
        Whether forward movement is allowed according to this distance status.

    source:
        unavailable, mock, manual, env, file, or vl53l0x.

    message:
        Human-readable explanation.
    """

    status: str
    distance_cm: float | None
    obstacle_detected: bool
    forward_movement_allowed: bool
    source: str
    message: str
    timestamp: float


def parse_distance(value: str | float | int | None) -> float | None:
    """
    Convert a value to float distance in centimeters.
    """

    if value is None:
        return None

    try:
        distance = float(value)
    except (TypeError, ValueError):
        return None

    return distance


def read_distance_from_env(env_var: str = DISTANCE_ENV_VAR) -> float | None:
    """
    Read distance from an environment variable.

    Example:

        export MICROBOT_DISTANCE_CM=42.5
        python setup/microbot/distance.py --source env
    """

    return parse_distance(os.environ.get(env_var))


def read_distance_from_file(path: str | Path) -> float | None:
    """
    Read distance from a text file.

    The file should contain one number in centimeters, for example:

        42.5
    """

    file_path = Path(path)

    if not file_path.exists():
        return None

    try:
        content = file_path.read_text(encoding="utf-8").strip()
    except OSError:
        return None

    return parse_distance(content)


def unavailable_status(
    config: DistanceConfig | None = None,
    message: str = "Distance sensor is unavailable.",
) -> DistanceStatus:
    """
    Return a structured unavailable status.

    By default, forward movement is blocked if the distance sensor is unavailable.
    """

    cfg = config or DistanceConfig()

    return DistanceStatus(
        status="UNAVAILABLE",
        distance_cm=None,
        obstacle_detected=False,
        forward_movement_allowed=not cfg.block_forward_if_unavailable,
        source="unavailable",
        message=message,
        timestamp=time.time(),
    )


def classify_distance(
    distance_cm: float,
    config: DistanceConfig | None = None,
    source: str = "unknown",
) -> DistanceStatus:
    """
    Classify a distance reading according to obstacle thresholds.
    """

    cfg = config or DistanceConfig()

    if distance_cm < cfg.min_valid_distance_cm:
        return DistanceStatus(
            status="FAILED",
            distance_cm=distance_cm,
            obstacle_detected=False,
            forward_movement_allowed=False,
            source=source,
            message="Distance reading is below the valid range.",
            timestamp=time.time(),
        )

    if distance_cm > cfg.max_valid_distance_cm:
        return DistanceStatus(
            status="FAILED",
            distance_cm=distance_cm,
            obstacle_detected=False,
            forward_movement_allowed=False,
            source=source,
            message="Distance reading is above the configured valid range.",
            timestamp=time.time(),
        )

    if distance_cm <= cfg.critical_distance_cm:
        return DistanceStatus(
            status="CRITICAL",
            distance_cm=distance_cm,
            obstacle_detected=True,
            forward_movement_allowed=False,
            source=source,
            message="Obstacle is critically close. Forward movement must be blocked.",
            timestamp=time.time(),
        )

    if distance_cm <= cfg.stop_distance_cm:
        return DistanceStatus(
            status="OBSTACLE",
            distance_cm=distance_cm,
            obstacle_detected=True,
            forward_movement_allowed=False,
            source=source,
            message="Obstacle detected below stop threshold. Forward movement blocked.",
            timestamp=time.time(),
        )

    if distance_cm <= cfg.warning_distance_cm:
        return DistanceStatus(
            status="WARNING",
            distance_cm=distance_cm,
            obstacle_detected=False,
            forward_movement_allowed=True,
            source=source,
            message="Object is within warning distance. Only careful movement is recommended.",
            timestamp=time.time(),
        )

    return DistanceStatus(
        status="OK",
        distance_cm=distance_cm,
        obstacle_detected=False,
        forward_movement_allowed=True,
        source=source,
        message="Path distance is acceptable for the configured thresholds.",
        timestamp=time.time(),
    )


def read_vl53l0x_distance_cm(config: DistanceConfig | None = None) -> DistanceStatus:
    """
    Read distance from a VL53L0X sensor using the Adafruit CircuitPython library.

    This function is optional because the dependency may not be installed during
    early development.

    Required optional package:

        pip install adafruit-circuitpython-vl53l0x

    On Raspberry Pi, I2C must be enabled.
    """

    cfg = config or DistanceConfig()

    try:
        import board
        import busio
        import adafruit_vl53l0x
    except Exception as exc:
        return DistanceStatus(
            status="UNAVAILABLE",
            distance_cm=None,
            obstacle_detected=False,
            forward_movement_allowed=not cfg.block_forward_if_unavailable,
            source="vl53l0x",
            message=(
                "VL53L0X library or Raspberry Pi I2C support is unavailable: "
                f"{type(exc).__name__}: {exc}"
            ),
            timestamp=time.time(),
        )

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_vl53l0x.VL53L0X(i2c, address=cfg.i2c_address)
        distance_mm = float(sensor.range)
        distance_cm = distance_mm / 10.0
    except Exception as exc:
        return DistanceStatus(
            status="FAILED",
            distance_cm=None,
            obstacle_detected=False,
            forward_movement_allowed=False,
            source="vl53l0x",
            message=f"VL53L0X read failed: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    return classify_distance(distance_cm, cfg, source="vl53l0x")


def read_distance_status(config: DistanceConfig | None = None) -> DistanceStatus:
    """
    Read distance status using the configured source.

    Supported V0 sources:

    - unavailable:
        No real distance sensor is installed.

    - mock:
        Uses config.mock_distance_cm.

    - manual:
        Same behavior as mock, intended for manually entered measurement.

    - env:
        Reads distance from MICROBOT_DISTANCE_CM.

    - file:
        Reads distance from config.distance_file.

    - vl53l0x:
        Reads a real VL53L0X sensor if optional dependencies are installed.
    """

    cfg = config or DistanceConfig()
    source = cfg.source.lower().strip()

    if source == "unavailable":
        return unavailable_status(
            cfg,
            "Distance sensor is not implemented. Forward movement should be blocked or reduced.",
        )

    if source == "mock":
        distance = parse_distance(cfg.mock_distance_cm)

        if distance is None:
            return DistanceStatus(
                status="FAILED",
                distance_cm=None,
                obstacle_detected=False,
                forward_movement_allowed=False,
                source="mock",
                message="Mock distance source selected, but mock_distance_cm is missing or invalid.",
                timestamp=time.time(),
            )

        return classify_distance(distance, cfg, source="mock")

    if source == "manual":
        distance = parse_distance(cfg.mock_distance_cm)

        if distance is None:
            return DistanceStatus(
                status="FAILED",
                distance_cm=None,
                obstacle_detected=False,
                forward_movement_allowed=False,
                source="manual",
                message="Manual distance source selected, but no manual distance was provided.",
                timestamp=time.time(),
            )

        return classify_distance(distance, cfg, source="manual")

    if source == "env":
        distance = read_distance_from_env()

        if distance is None:
            return DistanceStatus(
                status="UNAVAILABLE",
                distance_cm=None,
                obstacle_detected=False,
                forward_movement_allowed=not cfg.block_forward_if_unavailable,
                source="env",
                message=f"Environment variable {DISTANCE_ENV_VAR} is missing or invalid.",
                timestamp=time.time(),
            )

        return classify_distance(distance, cfg, source="env")

    if source == "file":
        if not cfg.distance_file:
            return DistanceStatus(
                status="FAILED",
                distance_cm=None,
                obstacle_detected=False,
                forward_movement_allowed=False,
                source="file",
                message="File distance source selected, but distance_file is not configured.",
                timestamp=time.time(),
            )

        distance = read_distance_from_file(cfg.distance_file)

        if distance is None:
            return DistanceStatus(
                status="UNAVAILABLE",
                distance_cm=None,
                obstacle_detected=False,
                forward_movement_allowed=not cfg.block_forward_if_unavailable,
                source="file",
                message=f"Could not read valid distance from file: {cfg.distance_file}",
                timestamp=time.time(),
            )

        return classify_distance(distance, cfg, source="file")

    if source == "vl53l0x":
        return read_vl53l0x_distance_cm(cfg)

    return DistanceStatus(
        status="FAILED",
        distance_cm=None,
        obstacle_detected=False,
        forward_movement_allowed=False,
        source=source,
        message=f"Unsupported distance source: {source}",
        timestamp=time.time(),
    )


def status_to_dict(status: DistanceStatus) -> dict[str, str | float | bool | None]:
    """
    Convert DistanceStatus to a dictionary for JSON logs.
    """

    return {
        "status": status.status,
        "distance_cm": status.distance_cm,
        "obstacle_detected": status.obstacle_detected,
        "forward_movement_allowed": status.forward_movement_allowed,
        "source": status.source,
        "message": status.message,
        "timestamp": status.timestamp,
    }


def format_distance_status(status: DistanceStatus) -> str:
    """
    Format distance status for terminal output.
    """

    distance_text = (
        "unavailable"
        if status.distance_cm is None
        else f"{status.distance_cm:.1f} cm"
    )

    return (
        "Distance status\n"
        "===============\n"
        f"Status: {status.status}\n"
        f"Distance: {distance_text}\n"
        f"Obstacle detected: {status.obstacle_detected}\n"
        f"Forward movement allowed: {status.forward_movement_allowed}\n"
        f"Source: {status.source}\n"
        f"Message: {status.message}\n"
    )


def distance_self_check(
    config: DistanceConfig | None = None,
) -> dict[str, str | float | bool | None]:
    """
    Return distance self-check information as a dictionary.
    """

    status = read_distance_status(config)
    return status_to_dict(status)


def print_distance_self_check(config: DistanceConfig | None = None) -> DistanceStatus:
    """
    Print distance status and return the DistanceStatus object.
    """

    status = read_distance_status(config)
    print(format_distance_status(status))
    return status


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build command-line parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 distance / obstacle helper."
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
        help="Path to a text file containing distance in centimeters.",
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
        "--allow-forward-if-unavailable",
        action="store_true",
        help="Allow forward movement if distance sensor is unavailable. Not recommended for real movement.",
    )

    return parser


def main() -> int:
    """
    CLI entry point for quick distance testing.

    Examples:

        python setup/microbot/distance.py --source mock --distance 42
        python setup/microbot/distance.py --source mock --distance 10
        MICROBOT_DISTANCE_CM=18 python setup/microbot/distance.py --source env
        python setup/microbot/distance.py --source vl53l0x
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    config = DistanceConfig(
        source=args.source,
        mock_distance_cm=args.distance,
        distance_file=args.file,
        warning_distance_cm=args.warning_cm,
        stop_distance_cm=args.stop_cm,
        critical_distance_cm=args.critical_cm,
        block_forward_if_unavailable=not args.allow_forward_if_unavailable,
    )

    status = print_distance_self_check(config)

    if status.status in {"OK", "WARNING", "OBSTACLE", "CRITICAL", "UNAVAILABLE"}:
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())