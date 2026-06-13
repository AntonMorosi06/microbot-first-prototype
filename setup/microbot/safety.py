"""
MicroBot Round V0 safety module.

This module evaluates whether a requested robot action is allowed before any
physical movement reaches the servos.

Core rule:
No movement command should be sent to physical servos unless the safety layer
has explicitly allowed it.

This module does not move hardware directly. It only evaluates state and returns
a structured decision.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
import argparse
import json
import time


try:
    from . import pins
except ImportError:
    pins = None


ENCODER_MIN = getattr(pins, "ENCODER_MIN", 255)
ENCODER_MAX = getattr(pins, "ENCODER_MAX", 1023)
SAFE_NUDGE = getattr(pins, "SAFE_NUDGE", 30)
SERVO_IDS = getattr(pins, "SERVO_IDS", (1, 2))

TILT_WARNING_DEGREES = getattr(pins, "TILT_WARNING_DEGREES", 20.0)
TILT_CRITICAL_DEGREES = getattr(pins, "TILT_CRITICAL_DEGREES", 30.0)

DISTANCE_WARNING_CM = getattr(pins, "DISTANCE_WARNING_CM", 25.0)
DISTANCE_STOP_CM = getattr(pins, "DISTANCE_STOP_CM", 15.0)
DISTANCE_CRITICAL_CM = getattr(pins, "DISTANCE_CRITICAL_CM", 8.0)

BATTERY_WARNING_VOLTAGE = getattr(pins, "BATTERY_WARNING_VOLTAGE", 3.65)
BATTERY_LOW_VOLTAGE = getattr(pins, "BATTERY_LOW_VOLTAGE", 3.50)
BATTERY_MOVEMENT_BLOCK_VOLTAGE = getattr(pins, "BATTERY_MOVEMENT_BLOCK_VOLTAGE", 3.45)
BATTERY_CRITICAL_VOLTAGE = getattr(pins, "BATTERY_CRITICAL_VOLTAGE", 3.30)

MAX_FAILED_MOVEMENTS_BEFORE_SAFE_MODE = getattr(
    pins,
    "MAX_FAILED_MOVEMENTS_BEFORE_SAFE_MODE",
    3,
)


ALLOWED_ACTIONS = (
    "STOP",
    "IDLE",
    "RUN_SELF_CHECK",
    "TAKE_PHOTO",
    "SPEAK_STATUS",
    "LED_STATUS",
    "SCAN_SERVOS",
    "SAFE_NUDGE",
    "MOVE_FORWARD_SMALL",
    "TURN_LEFT_SMALL",
    "TURN_RIGHT_SMALL",
    "RETURN_TO_IDLE",
    "SAFE_MODE",
    "SHUTDOWN",
)

MOVEMENT_ACTIONS = (
    "SAFE_NUDGE",
    "MOVE_FORWARD_SMALL",
    "TURN_LEFT_SMALL",
    "TURN_RIGHT_SMALL",
)

FORWARD_CLEARANCE_ACTIONS = (
    "MOVE_FORWARD_SMALL",
)

NON_MOVEMENT_ACTIONS = tuple(
    action for action in ALLOWED_ACTIONS if action not in MOVEMENT_ACTIONS
)


@dataclass(frozen=True)
class SafetyConfig:
    """
    Safety configuration for MicroBot Round V0.
    """

    hardware_movement_enabled: bool = False

    require_servo_scan_before_move: bool = True
    require_servo_position_before_move: bool = True
    require_imu_before_move: bool = True
    require_safe_power_before_move: bool = True
    require_distance_for_forward_move: bool = False

    block_movement_on_unknown_state: bool = True
    block_movement_if_distance_unavailable: bool = True
    block_movement_if_battery_unavailable: bool = False

    encoder_min: int = ENCODER_MIN
    encoder_max: int = ENCODER_MAX
    max_safe_nudge: int = SAFE_NUDGE

    tilt_warning_degrees: float = TILT_WARNING_DEGREES
    tilt_critical_degrees: float = TILT_CRITICAL_DEGREES

    distance_warning_cm: float = DISTANCE_WARNING_CM
    distance_stop_cm: float = DISTANCE_STOP_CM
    distance_critical_cm: float = DISTANCE_CRITICAL_CM

    battery_warning_voltage: float = BATTERY_WARNING_VOLTAGE
    battery_low_voltage: float = BATTERY_LOW_VOLTAGE
    battery_movement_block_voltage: float = BATTERY_MOVEMENT_BLOCK_VOLTAGE
    battery_critical_voltage: float = BATTERY_CRITICAL_VOLTAGE

    max_failed_movements_before_safe_mode: int = MAX_FAILED_MOVEMENTS_BEFORE_SAFE_MODE


@dataclass(frozen=True)
class MovementRequest:
    """
    A requested robot action.

    action:
        One of ALLOWED_ACTIONS.

    servo_targets:
        Optional mapping of servo_id -> encoder position.

    nudge_amount:
        Optional small encoder delta for safe nudge tests.
    """

    action: str
    servo_targets: dict[int, int] = field(default_factory=dict)
    nudge_amount: int | None = None
    reason: str = "unspecified"


@dataclass(frozen=True)
class RobotState:
    """
    Current safety-relevant robot state.

    All fields are deliberately optional because early hardware bring-up often
    starts with incomplete sensor availability.
    """

    emergency_stop: bool = False

    servo_scan_ok: bool | None = None
    servo_ids_found: tuple[int, ...] = field(default_factory=tuple)
    servo_positions: dict[int, int] = field(default_factory=dict)

    imu_status: str | None = None
    tilt_degrees: float | None = None

    distance_status: str | None = None
    distance_cm: float | None = None

    battery_status: str | None = None
    battery_voltage: float | None = None

    failed_movement_count: int = 0
    safe_mode_active: bool = False

    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class SafetyDecision:
    """
    Result returned by the safety layer.
    """

    allowed: bool
    movement_allowed: bool
    action: str
    state: str
    severity: str
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_action(action: str) -> str:
    """
    Normalize action names.
    """

    return action.strip().upper().replace(" ", "_")


def is_movement_action(action: str) -> bool:
    """
    Return True if an action may move physical servos.
    """

    return normalize_action(action) in MOVEMENT_ACTIONS


def is_forward_clearance_action(action: str) -> bool:
    """
    Return True if the action requires forward obstacle clearance.
    """

    return normalize_action(action) in FORWARD_CLEARANCE_ACTIONS


def _decision(
    allowed: bool,
    movement_allowed: bool,
    action: str,
    state: str,
    severity: str,
    reasons: list[str] | tuple[str, ...],
    warnings: list[str] | tuple[str, ...] | None = None,
) -> SafetyDecision:
    """
    Build a SafetyDecision object.
    """

    return SafetyDecision(
        allowed=allowed,
        movement_allowed=movement_allowed,
        action=normalize_action(action),
        state=state,
        severity=severity,
        reasons=tuple(reasons),
        warnings=tuple(warnings or ()),
    )


def validate_action(action: str) -> tuple[bool, str]:
    """
    Validate an action name.
    """

    normalized = normalize_action(action)

    if normalized not in ALLOWED_ACTIONS:
        return False, f"Unsupported action: {normalized}"

    return True, "Action is supported."


def validate_servo_targets(
    servo_targets: dict[int, int],
    config: SafetyConfig | None = None,
) -> tuple[bool, list[str]]:
    """
    Validate requested servo encoder targets.
    """

    cfg = config or SafetyConfig()
    reasons: list[str] = []

    for servo_id, target in servo_targets.items():
        if servo_id not in SERVO_IDS:
            reasons.append(f"Servo ID {servo_id} is not in expected SERVO_IDS {SERVO_IDS}.")

        if not isinstance(target, int):
            reasons.append(f"Servo target for ID {servo_id} is not an integer.")

        if isinstance(target, int) and target < cfg.encoder_min:
            reasons.append(
                f"Servo target for ID {servo_id} is below encoder_min "
                f"({target} < {cfg.encoder_min})."
            )

        if isinstance(target, int) and target > cfg.encoder_max:
            reasons.append(
                f"Servo target for ID {servo_id} is above encoder_max "
                f"({target} > {cfg.encoder_max})."
            )

    return len(reasons) == 0, reasons


def validate_safe_nudge(
    request: MovementRequest,
    config: SafetyConfig | None = None,
) -> tuple[bool, list[str]]:
    """
    Validate a safe nudge request.
    """

    cfg = config or SafetyConfig()
    reasons: list[str] = []

    if request.action != "SAFE_NUDGE":
        return True, reasons

    if request.nudge_amount is None:
        return True, reasons

    if abs(request.nudge_amount) > cfg.max_safe_nudge:
        reasons.append(
            f"Requested nudge amount {request.nudge_amount} exceeds max_safe_nudge "
            f"{cfg.max_safe_nudge}."
        )

    return len(reasons) == 0, reasons


def evaluate_emergency_stop(state: RobotState) -> tuple[bool, list[str]]:
    """
    Evaluate emergency stop status.
    """

    if state.emergency_stop:
        return False, ["Emergency stop is active."]

    return True, []


def evaluate_safe_mode(state: RobotState) -> tuple[bool, list[str]]:
    """
    Evaluate safe mode status.
    """

    reasons: list[str] = []

    if state.safe_mode_active:
        reasons.append("Safe mode is already active.")

    if state.failed_movement_count >= MAX_FAILED_MOVEMENTS_BEFORE_SAFE_MODE:
        reasons.append(
            "Failed movement count reached or exceeded the safe-mode threshold."
        )

    return len(reasons) == 0, reasons


def evaluate_servo_state(
    state: RobotState,
    request: MovementRequest,
    config: SafetyConfig | None = None,
) -> tuple[bool, list[str], list[str]]:
    """
    Evaluate servo-related movement requirements.
    """

    cfg = config or SafetyConfig()
    reasons: list[str] = []
    warnings: list[str] = []

    if not is_movement_action(request.action):
        return True, reasons, warnings

    if cfg.require_servo_scan_before_move:
        if state.servo_scan_ok is not True:
            reasons.append("Servo scan has not passed.")

        if not state.servo_ids_found:
            reasons.append("No servo IDs have been confirmed.")

    if cfg.require_servo_position_before_move:
        if not state.servo_positions:
            reasons.append("No servo positions are available.")

        for servo_id in state.servo_ids_found:
            if servo_id not in state.servo_positions:
                reasons.append(f"Servo position missing for ID {servo_id}.")

    if not state.servo_ids_found and state.servo_scan_ok is None:
        warnings.append("Servo scan state is unknown.")

    targets_ok, target_reasons = validate_servo_targets(request.servo_targets, cfg)
    if not targets_ok:
        reasons.extend(target_reasons)

    nudge_ok, nudge_reasons = validate_safe_nudge(request, cfg)
    if not nudge_ok:
        reasons.extend(nudge_reasons)

    return len(reasons) == 0, reasons, warnings


def evaluate_imu_state(
    state: RobotState,
    request: MovementRequest,
    config: SafetyConfig | None = None,
) -> tuple[bool, list[str], list[str]]:
    """
    Evaluate IMU and tilt safety.
    """

    cfg = config or SafetyConfig()
    reasons: list[str] = []
    warnings: list[str] = []

    if not is_movement_action(request.action):
        return True, reasons, warnings

    imu_status = (state.imu_status or "UNKNOWN").upper()

    if cfg.require_imu_before_move and state.imu_status is None:
        reasons.append("IMU status is unknown.")

    if imu_status in {"FAILED", "ERROR", "CRITICAL"}:
        reasons.append(f"IMU status blocks movement: {imu_status}.")

    if state.tilt_degrees is None:
        if cfg.require_imu_before_move:
            reasons.append("Tilt angle is unavailable.")
        else:
            warnings.append("Tilt angle is unavailable.")
    else:
        if state.tilt_degrees >= cfg.tilt_critical_degrees:
            reasons.append(
                f"Tilt is critical: {state.tilt_degrees:.1f} degrees "
                f">= {cfg.tilt_critical_degrees:.1f} degrees."
            )
        elif state.tilt_degrees >= cfg.tilt_warning_degrees:
            reasons.append(
                f"Tilt is above warning threshold: {state.tilt_degrees:.1f} degrees "
                f">= {cfg.tilt_warning_degrees:.1f} degrees."
            )

    return len(reasons) == 0, reasons, warnings


def evaluate_distance_state(
    state: RobotState,
    request: MovementRequest,
    config: SafetyConfig | None = None,
) -> tuple[bool, list[str], list[str]]:
    """
    Evaluate distance / obstacle safety.
    """

    cfg = config or SafetyConfig()
    reasons: list[str] = []
    warnings: list[str] = []

    if not is_movement_action(request.action):
        return True, reasons, warnings

    if not is_forward_clearance_action(request.action):
        return True, reasons, warnings

    distance_status = (state.distance_status or "UNKNOWN").upper()

    if state.distance_status is None:
        if cfg.require_distance_for_forward_move or cfg.block_movement_if_distance_unavailable:
            reasons.append("Distance sensor status is unavailable for forward movement.")
        else:
            warnings.append("Distance sensor status is unavailable.")
        return len(reasons) == 0, reasons, warnings

    if distance_status in {"FAILED", "ERROR", "CRITICAL"}:
        reasons.append(f"Distance sensor status blocks movement: {distance_status}.")

    if state.distance_cm is None:
        if cfg.require_distance_for_forward_move or cfg.block_movement_if_distance_unavailable:
            reasons.append("Distance reading is unavailable for forward movement.")
        else:
            warnings.append("Distance reading is unavailable.")
        return len(reasons) == 0, reasons, warnings

    if state.distance_cm <= cfg.distance_critical_cm:
        reasons.append(
            f"Obstacle is critically close: {state.distance_cm:.1f} cm "
            f"<= {cfg.distance_critical_cm:.1f} cm."
        )
    elif state.distance_cm <= cfg.distance_stop_cm:
        reasons.append(
            f"Obstacle is within stop threshold: {state.distance_cm:.1f} cm "
            f"<= {cfg.distance_stop_cm:.1f} cm."
        )
    elif state.distance_cm <= cfg.distance_warning_cm:
        warnings.append(
            f"Object is within warning distance: {state.distance_cm:.1f} cm "
            f"<= {cfg.distance_warning_cm:.1f} cm."
        )

    return len(reasons) == 0, reasons, warnings


def evaluate_battery_state(
    state: RobotState,
    request: MovementRequest,
    config: SafetyConfig | None = None,
) -> tuple[bool, list[str], list[str]]:
    """
    Evaluate battery and power safety.
    """

    cfg = config or SafetyConfig()
    reasons: list[str] = []
    warnings: list[str] = []

    if not is_movement_action(request.action):
        return True, reasons, warnings

    battery_status = (state.battery_status or "UNKNOWN").upper()

    if state.battery_status is None:
        if cfg.block_movement_if_battery_unavailable:
            reasons.append("Battery status is unavailable.")
        else:
            warnings.append("Battery status is unavailable.")
        return len(reasons) == 0, reasons, warnings

    if battery_status in {"FAILED", "ERROR", "CRITICAL"}:
        reasons.append(f"Battery status blocks movement: {battery_status}.")

    if state.battery_voltage is None:
        if cfg.block_movement_if_battery_unavailable:
            reasons.append("Battery voltage is unavailable.")
        else:
            warnings.append("Battery voltage is unavailable.")
        return len(reasons) == 0, reasons, warnings

    if state.battery_voltage <= cfg.battery_critical_voltage:
        reasons.append(
            f"Battery voltage is critical: {state.battery_voltage:.2f} V "
            f"<= {cfg.battery_critical_voltage:.2f} V."
        )
    elif state.battery_voltage <= cfg.battery_movement_block_voltage:
        reasons.append(
            f"Battery voltage blocks movement: {state.battery_voltage:.2f} V "
            f"<= {cfg.battery_movement_block_voltage:.2f} V."
        )
    elif state.battery_voltage <= cfg.battery_low_voltage:
        reasons.append(
            f"Battery voltage is low: {state.battery_voltage:.2f} V "
            f"<= {cfg.battery_low_voltage:.2f} V."
        )
    elif state.battery_voltage <= cfg.battery_warning_voltage:
        warnings.append(
            f"Battery voltage is in warning range: {state.battery_voltage:.2f} V "
            f"<= {cfg.battery_warning_voltage:.2f} V."
        )

    return len(reasons) == 0, reasons, warnings


def evaluate_safety(
    request: MovementRequest,
    state: RobotState,
    config: SafetyConfig | None = None,
) -> SafetyDecision:
    """
    Evaluate whether a requested action is allowed.

    This is the main function other modules should call.
    """

    cfg = config or SafetyConfig()
    action = normalize_action(request.action)
    normalized_request = MovementRequest(
        action=action,
        servo_targets=request.servo_targets,
        nudge_amount=request.nudge_amount,
        reason=request.reason,
    )

    reasons: list[str] = []
    warnings: list[str] = []

    valid_action, action_message = validate_action(action)
    if not valid_action:
        return _decision(
            allowed=False,
            movement_allowed=False,
            action=action,
            state="CRITICAL_ERROR",
            severity="ERROR",
            reasons=[action_message],
            warnings=[],
        )

    emergency_ok, emergency_reasons = evaluate_emergency_stop(state)
    if not emergency_ok:
        reasons.extend(emergency_reasons)

    safe_mode_ok, safe_mode_reasons = evaluate_safe_mode(state)
    if not safe_mode_ok:
        reasons.extend(safe_mode_reasons)

    if action in {"STOP", "SAFE_MODE", "SHUTDOWN"}:
        if state.emergency_stop and action == "STOP":
            return _decision(
                allowed=True,
                movement_allowed=False,
                action=action,
                state="MOVEMENT_BLOCKED",
                severity="WARNING",
                reasons=["STOP is allowed even when emergency stop is active."],
                warnings=warnings,
            )

        return _decision(
            allowed=True,
            movement_allowed=False,
            action=action,
            state="SAFE_IDLE" if action == "STOP" else action,
            severity="INFO",
            reasons=[f"{action} is a safe non-movement action."],
            warnings=warnings,
        )

    if not is_movement_action(action):
        if reasons:
            return _decision(
                allowed=False,
                movement_allowed=False,
                action=action,
                state="SAFE_MODE",
                severity="ERROR",
                reasons=reasons,
                warnings=warnings,
            )

        return _decision(
            allowed=True,
            movement_allowed=False,
            action=action,
            state="SAFE_IDLE",
            severity="INFO",
            reasons=[f"{action} is allowed as a non-movement action."],
            warnings=warnings,
        )

    if not cfg.hardware_movement_enabled:
        reasons.append(
            "Hardware movement is disabled by configuration. "
            "Set hardware_movement_enabled=True only after real safety validation."
        )

    servo_ok, servo_reasons, servo_warnings = evaluate_servo_state(
        state,
        normalized_request,
        cfg,
    )
    if not servo_ok:
        reasons.extend(servo_reasons)
    warnings.extend(servo_warnings)

    imu_ok, imu_reasons, imu_warnings = evaluate_imu_state(
        state,
        normalized_request,
        cfg,
    )
    if not imu_ok:
        reasons.extend(imu_reasons)
    warnings.extend(imu_warnings)

    distance_ok, distance_reasons, distance_warnings = evaluate_distance_state(
        state,
        normalized_request,
        cfg,
    )
    if not distance_ok:
        reasons.extend(distance_reasons)
    warnings.extend(distance_warnings)

    battery_ok, battery_reasons, battery_warnings = evaluate_battery_state(
        state,
        normalized_request,
        cfg,
    )
    if not battery_ok:
        reasons.extend(battery_reasons)
    warnings.extend(battery_warnings)

    if cfg.block_movement_on_unknown_state:
        unknown_fields = []

        if state.servo_scan_ok is None and cfg.require_servo_scan_before_move:
            unknown_fields.append("servo_scan_ok")

        if state.imu_status is None and cfg.require_imu_before_move:
            unknown_fields.append("imu_status")

        if unknown_fields:
            reasons.append(
                "Unknown safety-critical state fields: " + ", ".join(unknown_fields)
            )

    if reasons:
        return _decision(
            allowed=False,
            movement_allowed=False,
            action=action,
            state="MOVEMENT_BLOCKED",
            severity="ERROR",
            reasons=reasons,
            warnings=warnings,
        )

    if warnings:
        return _decision(
            allowed=True,
            movement_allowed=True,
            action=action,
            state="MOVEMENT_ALLOWED",
            severity="WARNING",
            reasons=["Movement allowed with warnings."],
            warnings=warnings,
        )

    return _decision(
        allowed=True,
        movement_allowed=True,
        action=action,
        state="MOVEMENT_ALLOWED",
        severity="INFO",
        reasons=["All configured safety checks passed."],
        warnings=[],
    )


def require_movement_allowed(decision: SafetyDecision) -> None:
    """
    Raise SafetyError if a movement decision is not allowed.

    Servo modules or movement scripts can call this before sending commands.
    """

    if not decision.movement_allowed:
        joined = "; ".join(decision.reasons)
        raise SafetyError(f"Movement blocked by safety layer: {joined}")


def build_safe_mock_state() -> RobotState:
    """
    Build a safe-looking mock state for offline testing only.

    This is not hardware validation.
    """

    return RobotState(
        emergency_stop=False,
        servo_scan_ok=True,
        servo_ids_found=tuple(SERVO_IDS),
        servo_positions={servo_id: 512 for servo_id in SERVO_IDS},
        imu_status="OK",
        tilt_degrees=2.0,
        distance_status="OK",
        distance_cm=50.0,
        battery_status="OK",
        battery_voltage=3.90,
        failed_movement_count=0,
        safe_mode_active=False,
    )


def build_unsafe_mock_state() -> RobotState:
    """
    Build an unsafe mock state for offline testing.
    """

    return RobotState(
        emergency_stop=False,
        servo_scan_ok=True,
        servo_ids_found=tuple(SERVO_IDS),
        servo_positions={servo_id: 512 for servo_id in SERVO_IDS},
        imu_status="CRITICAL",
        tilt_degrees=45.0,
        distance_status="CRITICAL",
        distance_cm=5.0,
        battery_status="LOW",
        battery_voltage=3.30,
        failed_movement_count=0,
        safe_mode_active=False,
    )


def decision_to_json(decision: SafetyDecision) -> str:
    """
    Convert a SafetyDecision to pretty JSON.
    """

    return json.dumps(decision.to_dict(), indent=2, sort_keys=True, default=str)


def safety_self_check() -> dict[str, Any]:
    """
    Run a small internal safety self-check.

    This validates that:
    - safe mock state allows movement only when movement is enabled
    - unsafe mock state blocks movement
    - non-movement actions are allowed
    """

    safe_request = MovementRequest(action="SAFE_NUDGE", nudge_amount=SAFE_NUDGE)

    movement_enabled_config = SafetyConfig(hardware_movement_enabled=True)
    movement_disabled_config = SafetyConfig(hardware_movement_enabled=False)

    safe_state = build_safe_mock_state()
    unsafe_state = build_unsafe_mock_state()

    allowed_decision = evaluate_safety(
        request=safe_request,
        state=safe_state,
        config=movement_enabled_config,
    )

    disabled_decision = evaluate_safety(
        request=safe_request,
        state=safe_state,
        config=movement_disabled_config,
    )

    blocked_decision = evaluate_safety(
        request=safe_request,
        state=unsafe_state,
        config=movement_enabled_config,
    )

    photo_decision = evaluate_safety(
        request=MovementRequest(action="TAKE_PHOTO"),
        state=RobotState(),
        config=movement_disabled_config,
    )

    passed = (
        allowed_decision.movement_allowed is True
        and disabled_decision.movement_allowed is False
        and blocked_decision.movement_allowed is False
        and photo_decision.allowed is True
    )

    return {
        "status": "OK" if passed else "FAILED",
        "message": "Safety self-check completed." if passed else "Safety self-check failed.",
        "allowed_decision": allowed_decision.to_dict(),
        "disabled_decision": disabled_decision.to_dict(),
        "blocked_decision": blocked_decision.to_dict(),
        "photo_decision": photo_decision.to_dict(),
        "timestamp": time.time(),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 safety evaluator."
    )

    parser.add_argument(
        "--action",
        default="SAFE_NUDGE",
        help="Action to evaluate.",
    )

    parser.add_argument(
        "--enable-movement",
        action="store_true",
        help="Enable hardware movement in safety config for this evaluation.",
    )

    parser.add_argument(
        "--safe-mock",
        action="store_true",
        help="Use safe mock robot state.",
    )

    parser.add_argument(
        "--unsafe-mock",
        action="store_true",
        help="Use unsafe mock robot state.",
    )

    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Run safety self-check.",
    )

    return parser


def main() -> int:
    """
    CLI entry point.

    Examples:

        python setup/microbot/safety.py --self-check
        python setup/microbot/safety.py --action SAFE_NUDGE --safe-mock
        python setup/microbot/safety.py --action SAFE_NUDGE --safe-mock --enable-movement
        python setup/microbot/safety.py --action MOVE_FORWARD_SMALL --unsafe-mock --enable-movement
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    if args.self_check:
        result = safety_self_check()
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
        return 0 if result["status"] == "OK" else 1

    if args.unsafe_mock:
        state = build_unsafe_mock_state()
    elif args.safe_mock:
        state = build_safe_mock_state()
    else:
        state = RobotState()

    config = SafetyConfig(
        hardware_movement_enabled=args.enable_movement,
    )

    request = MovementRequest(
        action=args.action,
        nudge_amount=SAFE_NUDGE if normalize_action(args.action) == "SAFE_NUDGE" else None,
        reason="CLI evaluation",
    )

    decision = evaluate_safety(
        request=request,
        state=state,
        config=config,
    )

    print(decision_to_json(decision))

    return 0 if decision.allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())