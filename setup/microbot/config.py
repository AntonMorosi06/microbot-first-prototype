"""
MicroBot Round V0 central configuration.

This module contains project-level configuration for the first MicroBot Round V0
hardware bring-up.

The goal is to keep robot identity, paths, feature flags, demo settings, safety
thresholds and logging options in one place.

Pin numbers and hardware bus constants belong in pins.py.
Runtime hardware logic belongs in the specific modules: leds.py, imu.py,
camera.py, audio.py, battery.py, servos.py and safety.py.

Important V0 rule:
movement is disabled by default until servo scan, power validation, IMU reading
and safety checks are working on real hardware.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import os
import time


PROJECT_NAME = "MicroBot Round V0"
PROJECT_SLUG = "microbot-round-v0"
SOFTWARE_VERSION = "0.1.0"
HARDWARE_VERSION = "v0"
DEFAULT_STATUS = "prepared"


def env_bool(name: str, default: bool = False) -> bool:
    """
    Read a boolean value from an environment variable.

    Accepted true values:
        1, true, yes, y, on

    Accepted false values:
        0, false, no, n, off
    """

    value = os.environ.get(name)

    if value is None:
        return default

    normalized = value.strip().lower()

    if normalized in {"1", "true", "yes", "y", "on"}:
        return True

    if normalized in {"0", "false", "no", "n", "off"}:
        return False

    return default


def env_float(name: str, default: float) -> float:
    """
    Read a float from an environment variable.
    """

    value = os.environ.get(name)

    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


def env_int(name: str, default: int) -> int:
    """
    Read an integer from an environment variable.
    """

    value = os.environ.get(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def find_project_root(start: Path | None = None) -> Path:
    """
    Find the project root.

    This function assumes the file lives in:

        setup/microbot/config.py

    So parents[2] should be the repository root.

    If the structure changes, update this function.
    """

    current = start or Path(__file__).resolve()
    return current.parents[2]


def make_session_id(prefix: str = "session") -> str:
    """
    Create a timestamped session ID.
    """

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}"


@dataclass(frozen=True)
class PathConfig:
    """
    Project path configuration.
    """

    project_root: Path = field(default_factory=find_project_root)
    logs_dir_name: str = "logs"
    evidence_dir_name: str = "evidence"
    photos_dir_name: str = "photos"
    videos_dir_name: str = "videos"
    reports_dir_name: str = "reports"

    @property
    def logs_dir(self) -> Path:
        return self.project_root / self.logs_dir_name

    @property
    def evidence_dir(self) -> Path:
        return self.project_root / self.evidence_dir_name

    @property
    def photos_dir(self) -> Path:
        return self.evidence_dir / self.photos_dir_name

    @property
    def videos_dir(self) -> Path:
        return self.evidence_dir / self.videos_dir_name

    @property
    def reports_dir(self) -> Path:
        return self.evidence_dir / self.reports_dir_name

    def ensure_directories(self) -> None:
        """
        Create all runtime output directories.
        """

        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.photos_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class FeatureConfig:
    """
    Feature flags for MicroBot Round V0.

    Movement is disabled by default. Enable it only after:
    - power rail validation
    - servo scan
    - servo position read
    - safe nudge testing
    - IMU safety testing
    """

    enable_leds: bool = True
    enable_imu: bool = True
    enable_camera: bool = True
    enable_audio: bool = True
    enable_microphone: bool = True
    enable_distance_sensor: bool = False
    enable_battery_monitor: bool = False
    enable_servos: bool = True

    enable_movement: bool = False
    enable_autonomy: bool = False
    enable_dashboard: bool = False
    enable_simulation: bool = False

    graceful_hardware_skip: bool = True


@dataclass(frozen=True)
class LoggingConfig:
    """
    Logging configuration.
    """

    session_prefix: str = "microbot_session"
    write_json_log: bool = True
    write_markdown_report: bool = True
    print_to_terminal: bool = True
    include_timestamps: bool = True


@dataclass(frozen=True)
class CameraRuntimeConfig:
    """
    Camera runtime configuration.

    The actual camera driver is implemented in camera.py.
    """

    width: int = 640
    height: int = 480
    timeout_ms: int = 800
    warmup_seconds: float = 0.4
    save_boot_frame: bool = True
    save_post_movement_frame: bool = True
    save_obstacle_frame: bool = True


@dataclass(frozen=True)
class LedRuntimeConfig:
    """
    LED runtime configuration.

    Pin-level constants belong in pins.py.
    """

    brightness: int = 40
    boot_animation_enabled: bool = True
    idle_color_name: str = "blue"
    ok_color_name: str = "green"
    warning_color_name: str = "yellow"
    error_color_name: str = "red"
    decision_color_name: str = "purple"
    obstacle_color_name: str = "orange"


@dataclass(frozen=True)
class AudioRuntimeConfig:
    """
    Audio runtime configuration.
    """

    startup_phrase: str = "MicroBot Round V0 online. System check started."
    complete_phrase: str = "MicroBot Round V0. Autonomous safety demo completed."
    warning_phrase: str = "Warning. Safe mode active."
    audio_during_movement: bool = False
    microphone_test_seconds: float = 1.0


@dataclass(frozen=True)
class ServoRuntimeConfig:
    """
    Servo runtime configuration.

    Servo bus constants and register constants belong in pins.py.
    This section controls runtime behavior.
    """

    movement_enabled_by_default: bool = False
    safe_nudge_enabled: bool = True
    safe_nudge_repetitions: int = 1
    movement_timeout_seconds: float = 1.0
    movement_cooldown_seconds: float = 1.0
    release_torque_on_exit: bool = True
    require_position_read_before_move: bool = True
    require_imu_before_move: bool = True


@dataclass(frozen=True)
class SafetyConfig:
    """
    Safety thresholds and movement permissions.

    These values are placeholders and must be calibrated on real hardware.
    """

    safe_mode_on_unknown_state: bool = True
    block_movement_without_imu: bool = True
    block_movement_without_servo_position: bool = True
    block_movement_without_logging: bool = False

    tilt_warning_degrees: float = 20.0
    tilt_critical_degrees: float = 30.0

    obstacle_warning_cm: float = 25.0
    obstacle_stop_cm: float = 15.0

    battery_warning_voltage: float = 3.65
    battery_low_voltage: float = 3.50
    battery_movement_block_voltage: float = 3.45
    battery_critical_voltage: float = 3.30

    max_failed_movements_before_safe_mode: int = 3
    emergency_stop_initial_state: bool = False


@dataclass(frozen=True)
class AutonomyConfig:
    """
    Constrained autonomy configuration.

    The first autonomy layer may only select from safe high-level action names.
    It must never output raw servo target positions.
    """

    allowed_actions: tuple[str, ...] = (
        "STOP",
        "MOVE_FORWARD_SMALL",
        "TURN_LEFT_SMALL",
        "TURN_RIGHT_SMALL",
        "TAKE_PHOTO",
        "SPEAK_STATUS",
        "RUN_SELF_CHECK",
        "RETURN_TO_IDLE",
        "SAFE_MODE",
        "SHUTDOWN",
    )

    movement_actions: tuple[str, ...] = (
        "MOVE_FORWARD_SMALL",
        "TURN_LEFT_SMALL",
        "TURN_RIGHT_SMALL",
    )

    default_action: str = "STOP"
    decision_interval_seconds: float = 2.0
    max_actions_per_demo: int = 1


@dataclass(frozen=True)
class DemoConfig:
    """
    Demo configuration for hello_microbot.py.
    """

    demo_name: str = "MicroBot Round V0 First Autonomous Safety Demo"
    run_led_boot: bool = True
    run_audio_startup: bool = True
    run_self_check: bool = True
    run_camera_boot_capture: bool = True
    run_servo_scan: bool = True
    run_safe_nudge: bool = False
    run_autonomy_cycle: bool = False
    generate_final_report: bool = True


@dataclass(frozen=True)
class MicroBotConfig:
    """
    Complete MicroBot Round V0 configuration object.
    """

    project_name: str = PROJECT_NAME
    project_slug: str = PROJECT_SLUG
    software_version: str = SOFTWARE_VERSION
    hardware_version: str = HARDWARE_VERSION
    status: str = DEFAULT_STATUS

    paths: PathConfig = field(default_factory=PathConfig)
    features: FeatureConfig = field(default_factory=FeatureConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    camera: CameraRuntimeConfig = field(default_factory=CameraRuntimeConfig)
    leds: LedRuntimeConfig = field(default_factory=LedRuntimeConfig)
    audio: AudioRuntimeConfig = field(default_factory=AudioRuntimeConfig)
    servos: ServoRuntimeConfig = field(default_factory=ServoRuntimeConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    autonomy: AutonomyConfig = field(default_factory=AutonomyConfig)
    demo: DemoConfig = field(default_factory=DemoConfig)

    def ensure_runtime_directories(self) -> None:
        """
        Create logs and evidence directories.
        """

        self.paths.ensure_directories()

    def to_dict(self) -> dict:
        """
        Convert configuration to dictionary.

        Path objects are converted to strings for JSON compatibility.
        """

        data = asdict(self)

        def convert_paths(value):
            if isinstance(value, Path):
                return str(value)

            if isinstance(value, dict):
                return {key: convert_paths(item) for key, item in value.items()}

            if isinstance(value, list):
                return [convert_paths(item) for item in value]

            if isinstance(value, tuple):
                return tuple(convert_paths(item) for item in value)

            return value

        return convert_paths(data)


def load_config_from_env() -> MicroBotConfig:
    """
    Build a MicroBotConfig object with selected environment overrides.

    Example:

        MICROBOT_ENABLE_MOVEMENT=1 python setup/scripts/hello_microbot.py

    Movement should only be enabled after real hardware safety validation.
    """

    paths = PathConfig()

    features = FeatureConfig(
        enable_leds=env_bool("MICROBOT_ENABLE_LEDS", True),
        enable_imu=env_bool("MICROBOT_ENABLE_IMU", True),
        enable_camera=env_bool("MICROBOT_ENABLE_CAMERA", True),
        enable_audio=env_bool("MICROBOT_ENABLE_AUDIO", True),
        enable_microphone=env_bool("MICROBOT_ENABLE_MICROPHONE", True),
        enable_distance_sensor=env_bool("MICROBOT_ENABLE_DISTANCE_SENSOR", False),
        enable_battery_monitor=env_bool("MICROBOT_ENABLE_BATTERY_MONITOR", False),
        enable_servos=env_bool("MICROBOT_ENABLE_SERVOS", True),
        enable_movement=env_bool("MICROBOT_ENABLE_MOVEMENT", False),
        enable_autonomy=env_bool("MICROBOT_ENABLE_AUTONOMY", False),
        enable_dashboard=env_bool("MICROBOT_ENABLE_DASHBOARD", False),
        enable_simulation=env_bool("MICROBOT_ENABLE_SIMULATION", False),
        graceful_hardware_skip=env_bool("MICROBOT_GRACEFUL_HARDWARE_SKIP", True),
    )

    camera = CameraRuntimeConfig(
        width=env_int("MICROBOT_CAMERA_WIDTH", 640),
        height=env_int("MICROBOT_CAMERA_HEIGHT", 480),
        timeout_ms=env_int("MICROBOT_CAMERA_TIMEOUT_MS", 800),
        warmup_seconds=env_float("MICROBOT_CAMERA_WARMUP_SECONDS", 0.4),
        save_boot_frame=env_bool("MICROBOT_SAVE_BOOT_FRAME", True),
        save_post_movement_frame=env_bool("MICROBOT_SAVE_POST_MOVEMENT_FRAME", True),
        save_obstacle_frame=env_bool("MICROBOT_SAVE_OBSTACLE_FRAME", True),
    )

    leds = LedRuntimeConfig(
        brightness=env_int("MICROBOT_LED_BRIGHTNESS", 40),
        boot_animation_enabled=env_bool("MICROBOT_LED_BOOT_ANIMATION", True),
    )

    audio = AudioRuntimeConfig(
        startup_phrase=os.environ.get(
            "MICROBOT_STARTUP_PHRASE",
            "MicroBot Round V0 online. System check started.",
        ),
        complete_phrase=os.environ.get(
            "MICROBOT_COMPLETE_PHRASE",
            "MicroBot Round V0. Autonomous safety demo completed.",
        ),
        warning_phrase=os.environ.get(
            "MICROBOT_WARNING_PHRASE",
            "Warning. Safe mode active.",
        ),
        audio_during_movement=env_bool("MICROBOT_AUDIO_DURING_MOVEMENT", False),
        microphone_test_seconds=env_float("MICROBOT_MICROPHONE_TEST_SECONDS", 1.0),
    )

    servos = ServoRuntimeConfig(
        movement_enabled_by_default=env_bool("MICROBOT_ENABLE_MOVEMENT", False),
        safe_nudge_enabled=env_bool("MICROBOT_SAFE_NUDGE_ENABLED", True),
        safe_nudge_repetitions=env_int("MICROBOT_SAFE_NUDGE_REPETITIONS", 1),
        movement_timeout_seconds=env_float("MICROBOT_MOVEMENT_TIMEOUT_SECONDS", 1.0),
        movement_cooldown_seconds=env_float("MICROBOT_MOVEMENT_COOLDOWN_SECONDS", 1.0),
        release_torque_on_exit=env_bool("MICROBOT_RELEASE_TORQUE_ON_EXIT", True),
        require_position_read_before_move=env_bool(
            "MICROBOT_REQUIRE_POSITION_READ_BEFORE_MOVE",
            True,
        ),
        require_imu_before_move=env_bool("MICROBOT_REQUIRE_IMU_BEFORE_MOVE", True),
    )

    safety = SafetyConfig(
        safe_mode_on_unknown_state=env_bool("MICROBOT_SAFE_MODE_ON_UNKNOWN_STATE", True),
        block_movement_without_imu=env_bool("MICROBOT_BLOCK_MOVEMENT_WITHOUT_IMU", True),
        block_movement_without_servo_position=env_bool(
            "MICROBOT_BLOCK_MOVEMENT_WITHOUT_SERVO_POSITION",
            True,
        ),
        block_movement_without_logging=env_bool(
            "MICROBOT_BLOCK_MOVEMENT_WITHOUT_LOGGING",
            False,
        ),
        tilt_warning_degrees=env_float("MICROBOT_TILT_WARNING_DEGREES", 20.0),
        tilt_critical_degrees=env_float("MICROBOT_TILT_CRITICAL_DEGREES", 30.0),
        obstacle_warning_cm=env_float("MICROBOT_OBSTACLE_WARNING_CM", 25.0),
        obstacle_stop_cm=env_float("MICROBOT_OBSTACLE_STOP_CM", 15.0),
        battery_warning_voltage=env_float("MICROBOT_BATTERY_WARNING_VOLTAGE", 3.65),
        battery_low_voltage=env_float("MICROBOT_BATTERY_LOW_VOLTAGE", 3.50),
        battery_movement_block_voltage=env_float(
            "MICROBOT_BATTERY_MOVEMENT_BLOCK_VOLTAGE",
            3.45,
        ),
        battery_critical_voltage=env_float("MICROBOT_BATTERY_CRITICAL_VOLTAGE", 3.30),
        max_failed_movements_before_safe_mode=env_int(
            "MICROBOT_MAX_FAILED_MOVEMENTS_BEFORE_SAFE_MODE",
            3,
        ),
        emergency_stop_initial_state=env_bool("MICROBOT_EMERGENCY_STOP_INITIAL_STATE", False),
    )

    demo = DemoConfig(
        run_led_boot=env_bool("MICROBOT_DEMO_LED_BOOT", True),
        run_audio_startup=env_bool("MICROBOT_DEMO_AUDIO_STARTUP", True),
        run_self_check=env_bool("MICROBOT_DEMO_SELF_CHECK", True),
        run_camera_boot_capture=env_bool("MICROBOT_DEMO_CAMERA_BOOT_CAPTURE", True),
        run_servo_scan=env_bool("MICROBOT_DEMO_SERVO_SCAN", True),
        run_safe_nudge=env_bool("MICROBOT_DEMO_SAFE_NUDGE", False),
        run_autonomy_cycle=env_bool("MICROBOT_DEMO_AUTONOMY_CYCLE", False),
        generate_final_report=env_bool("MICROBOT_DEMO_FINAL_REPORT", True),
    )

    return MicroBotConfig(
        paths=paths,
        features=features,
        camera=camera,
        leds=leds,
        audio=audio,
        servos=servos,
        safety=safety,
        demo=demo,
    )


DEFAULT_CONFIG = load_config_from_env()


def get_config() -> MicroBotConfig:
    """
    Return the default runtime configuration.
    """

    return DEFAULT_CONFIG


def print_config_summary(config: MicroBotConfig | None = None) -> None:
    """
    Print a concise configuration summary.
    """

    cfg = config or get_config()

    print(cfg.project_name)
    print("=" * len(cfg.project_name))
    print(f"Project slug: {cfg.project_slug}")
    print(f"Software version: {cfg.software_version}")
    print(f"Hardware version: {cfg.hardware_version}")
    print(f"Status: {cfg.status}")
    print(f"Project root: {cfg.paths.project_root}")
    print()
    print("Feature flags")
    print("-------------")
    print(f"LEDs: {cfg.features.enable_leds}")
    print(f"IMU: {cfg.features.enable_imu}")
    print(f"Camera: {cfg.features.enable_camera}")
    print(f"Audio: {cfg.features.enable_audio}")
    print(f"Microphone: {cfg.features.enable_microphone}")
    print(f"Distance sensor: {cfg.features.enable_distance_sensor}")
    print(f"Battery monitor: {cfg.features.enable_battery_monitor}")
    print(f"Servos: {cfg.features.enable_servos}")
    print(f"Movement: {cfg.features.enable_movement}")
    print(f"Autonomy: {cfg.features.enable_autonomy}")
    print()
    print("Safety")
    print("------")
    print(f"Tilt warning degrees: {cfg.safety.tilt_warning_degrees}")
    print(f"Tilt critical degrees: {cfg.safety.tilt_critical_degrees}")
    print(f"Obstacle warning cm: {cfg.safety.obstacle_warning_cm}")
    print(f"Obstacle stop cm: {cfg.safety.obstacle_stop_cm}")
    print(f"Battery movement block voltage: {cfg.safety.battery_movement_block_voltage}")


if __name__ == "__main__":
    DEFAULT_CONFIG.ensure_runtime_directories()
    print_config_summary(DEFAULT_CONFIG)