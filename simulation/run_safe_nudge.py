#!/usr/bin/env python3
"""
MicroBot Round V0 - MuJoCo safe nudge simulation.

This script loads the MicroBot MuJoCo XML model, applies a small controlled
motor command to the left leg and then to the right leg, and records whether
the robot remains stable.

It is the simulation equivalent of a physical safe servo nudge.

Run:

    python simulation/run_safe_nudge.py

Run with live viewer:

    python simulation/run_safe_nudge.py --viewer

Output:

    evidence/reports/sim_safe_nudge_<timestamp>.json
    evidence/reports/sim_safe_nudge_<timestamp>.md
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any


try:
    import mujoco
except ImportError as exc:
    print("ERROR: mujoco is not installed in this Python environment.")
    print("Activate the environment that opened the MuJoCo viewer, then run again.")
    print("Example:")
    print("    conda activate microbot312")
    print("    python simulation/run_safe_nudge.py")
    raise SystemExit(1) from exc


def quat_to_euler_degrees(qw: float, qx: float, qy: float, qz: float) -> tuple[float, float, float]:
    """
    Convert quaternion w, x, y, z to roll, pitch, yaw in degrees.
    """

    sinr_cosp = 2.0 * (qw * qx + qy * qz)
    cosr_cosp = 1.0 - 2.0 * (qx * qx + qy * qy)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2.0 * (qw * qy - qz * qx)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return (
        math.degrees(roll),
        math.degrees(pitch),
        math.degrees(yaw),
    )


def project_root() -> Path:
    """
    Return repository root.
    """

    return Path(__file__).resolve().parents[1]


def timestamp_id(prefix: str) -> str:
    """
    Return timestamp-based session ID.
    """

    return time.strftime(f"{prefix}_%Y-%m-%d_%H-%M-%S")


def name_to_id(model: mujoco.MjModel, object_type: Any, name: str) -> int:
    """
    Resolve a MuJoCo object name to ID.
    """

    return mujoco.mj_name2id(model, object_type, name)


def load_keyframe(model: mujoco.MjModel, data: mujoco.MjData, key_name: str) -> bool:
    """
    Load a named keyframe into qpos/qvel/ctrl if available.
    """

    key_id = name_to_id(model, mujoco.mjtObj.mjOBJ_KEY, key_name)

    if key_id < 0:
        return False

    data.qpos[:] = model.key_qpos[key_id]

    if model.nv > 0:
        data.qvel[:] = 0.0

    if model.nu > 0:
        data.ctrl[:] = model.key_ctrl[key_id]

    mujoco.mj_forward(model, data)
    return True


def get_joint_qpos(model: mujoco.MjModel, data: mujoco.MjData, joint_name: str) -> float | None:
    """
    Return joint position by name.
    """

    joint_id = name_to_id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)

    if joint_id < 0:
        return None

    qpos_address = model.jnt_qposadr[joint_id]
    return float(data.qpos[qpos_address])


def get_actuator_id(model: mujoco.MjModel, actuator_name: str) -> int:
    """
    Return actuator ID.
    """

    return name_to_id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name)


def set_controls(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    left_actuator_id: int,
    right_actuator_id: int,
    left_value: float,
    right_value: float,
) -> None:
    """
    Set left and right motor controls.
    """

    if model.nu <= 0:
        return

    data.ctrl[:] = 0.0

    if left_actuator_id >= 0:
        data.ctrl[left_actuator_id] = left_value

    if right_actuator_id >= 0:
        data.ctrl[right_actuator_id] = right_value


def collect_state(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    phase: str,
    sim_time: float,
) -> dict[str, Any]:
    """
    Collect current simulated robot state.
    """

    x = float(data.qpos[0])
    y = float(data.qpos[1])
    z = float(data.qpos[2])
    qw = float(data.qpos[3])
    qx = float(data.qpos[4])
    qy = float(data.qpos[5])
    qz = float(data.qpos[6])

    roll, pitch, yaw = quat_to_euler_degrees(qw, qx, qy, qz)

    tilt = max(abs(roll), abs(pitch))

    left_angle = get_joint_qpos(model, data, "left_leg_hinge")
    right_angle = get_joint_qpos(model, data, "right_leg_hinge")

    return {
        "phase": phase,
        "time": sim_time,
        "root_position": {
            "x": x,
            "y": y,
            "z": z,
        },
        "root_orientation_degrees": {
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
            "tilt": tilt,
        },
        "joint_position": {
            "left_leg_hinge": left_angle,
            "right_leg_hinge": right_angle,
        },
        "ctrl": [float(value) for value in data.ctrl],
    }


def is_unstable(
    state: dict[str, Any],
    min_height: float,
    max_tilt_degrees: float,
    max_xy_distance: float,
) -> tuple[bool, str]:
    """
    Decide whether the simulated robot became unstable.
    """

    position = state["root_position"]
    orientation = state["root_orientation_degrees"]

    x = float(position["x"])
    y = float(position["y"])
    z = float(position["z"])
    tilt = float(orientation["tilt"])

    xy_distance = math.sqrt((x * x) + (y * y))

    if not math.isfinite(x) or not math.isfinite(y) or not math.isfinite(z):
        return True, "non-finite root position"

    if z < min_height:
        return True, f"root height below limit: {z:.4f} < {min_height:.4f}"

    if tilt > max_tilt_degrees:
        return True, f"tilt above limit: {tilt:.2f} > {max_tilt_degrees:.2f}"

    if xy_distance > max_xy_distance:
        return True, f"root drift above limit: {xy_distance:.4f} > {max_xy_distance:.4f}"

    return False, "stable"


def simulate_phase(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    phase: str,
    duration: float,
    left_ctrl: float,
    right_ctrl: float,
    left_actuator_id: int,
    right_actuator_id: int,
    log: list[dict[str, Any]],
    min_height: float,
    max_tilt_degrees: float,
    max_xy_distance: float,
    viewer: Any | None = None,
    realtime: bool = False,
    log_every_steps: int = 10,
) -> tuple[bool, str]:
    """
    Simulate one control phase.
    """

    timestep = float(model.opt.timestep)
    steps = max(1, int(duration / timestep))

    for step in range(steps):
        set_controls(
            model=model,
            data=data,
            left_actuator_id=left_actuator_id,
            right_actuator_id=right_actuator_id,
            left_value=left_ctrl,
            right_value=right_ctrl,
        )

        mujoco.mj_step(model, data)

        sim_time = float(data.time)

        if step % log_every_steps == 0 or step == steps - 1:
            state = collect_state(model, data, phase=phase, sim_time=sim_time)
            log.append(state)

            unstable, reason = is_unstable(
                state=state,
                min_height=min_height,
                max_tilt_degrees=max_tilt_degrees,
                max_xy_distance=max_xy_distance,
            )

            if unstable:
                return False, f"{phase}: {reason}"

        if viewer is not None:
            viewer.sync()

        if realtime:
            time.sleep(timestep)

    return True, f"{phase}: stable"


def build_report_markdown(result: dict[str, Any]) -> str:
    """
    Build Markdown report.
    """

    summary = result["summary"]

    lines = [
        "# MicroBot Round V0 - Safe Nudge Simulation Report",
        "",
        f"Session ID: `{result['session_id']}`",
        "",
        "## Summary",
        "",
        f"- Status: `{summary['status']}`",
        f"- Message: {summary['message']}",
        f"- XML: `{result['xml_path']}`",
        f"- Total simulation time: `{summary['total_simulation_time']:.3f} s`",
        f"- Max tilt: `{summary['max_tilt_degrees']:.2f} deg`",
        f"- Min root height: `{summary['min_root_height']:.4f} m`",
        f"- Max XY drift: `{summary['max_xy_distance']:.4f} m`",
        "",
        "## Phase Results",
        "",
    ]

    for item in result["phase_results"]:
        lines.append(f"- `{item['phase']}`: `{item['status']}` - {item['message']}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )

    if summary["status"] == "OK":
        lines.append(
            "The simulated MicroBot remained stable during idle, left-leg safe nudge, return-to-idle, right-leg safe nudge and final return-to-idle."
        )
    else:
        lines.append(
            "The simulated MicroBot became unstable or exceeded at least one safety threshold. The XML model or motor command should be reduced before testing stronger motion."
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "This is simulation evidence only. It does not prove that the physical robot can move safely.",
            "The equivalent physical test remains `setup/scripts/test_servos_safe.py` and must be run only after wiring, power and servo scan validation.",
            "",
        ]
    )

    return "\n".join(lines)


def save_reports(root: Path, result: dict[str, Any]) -> tuple[Path, Path]:
    """
    Save JSON and Markdown reports.
    """

    reports_dir = root / "evidence" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    session_id = result["session_id"]

    json_path = reports_dir / f"{session_id}.json"
    md_path = reports_dir / f"{session_id}.md"

    json_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(build_report_markdown(result), encoding="utf-8")

    return json_path, md_path


def summarize_log(log: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Summarize simulation log.
    """

    if not log:
        return {
            "max_tilt_degrees": 0.0,
            "min_root_height": 0.0,
            "max_xy_distance": 0.0,
            "total_simulation_time": 0.0,
        }

    max_tilt = 0.0
    min_height = float("inf")
    max_xy = 0.0
    final_time = 0.0

    for item in log:
        position = item["root_position"]
        orientation = item["root_orientation_degrees"]

        x = float(position["x"])
        y = float(position["y"])
        z = float(position["z"])
        tilt = abs(float(orientation["tilt"]))

        max_tilt = max(max_tilt, tilt)
        min_height = min(min_height, z)
        max_xy = max(max_xy, math.sqrt((x * x) + (y * y)))
        final_time = max(final_time, float(item["time"]))

    return {
        "max_tilt_degrees": max_tilt,
        "min_root_height": min_height,
        "max_xy_distance": max_xy,
        "total_simulation_time": final_time,
    }


def print_summary(result: dict[str, Any], json_path: Path, md_path: Path) -> None:
    """
    Print terminal summary.
    """

    summary = result["summary"]

    print()
    print("MicroBot Round V0 safe nudge simulation")
    print("======================================")
    print(f"Status: {summary['status']}")
    print(f"Message: {summary['message']}")
    print(f"Session ID: {result['session_id']}")
    print()
    print("Metrics")
    print("-------")
    print(f"Max tilt: {summary['max_tilt_degrees']:.2f} deg")
    print(f"Min root height: {summary['min_root_height']:.4f} m")
    print(f"Max XY drift: {summary['max_xy_distance']:.4f} m")
    print(f"Total simulation time: {summary['total_simulation_time']:.3f} s")
    print()
    print("Reports")
    print("-------")
    print(f"JSON: {json_path}")
    print(f"MD:   {md_path}")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="Run MicroBot Round V0 MuJoCo safe nudge simulation."
    )

    parser.add_argument(
        "--xml",
        default="simulation/microbot_round_body.xml",
        help="Path to MuJoCo XML model.",
    )

    parser.add_argument(
        "--left-ctrl",
        type=float,
        default=0.08,
        help="Small control value for left leg nudge.",
    )

    parser.add_argument(
        "--right-ctrl",
        type=float,
        default=-0.08,
        help="Small control value for right leg nudge.",
    )

    parser.add_argument(
        "--settle",
        type=float,
        default=1.0,
        help="Initial settling duration in seconds.",
    )

    parser.add_argument(
        "--pulse",
        type=float,
        default=0.7,
        help="Nudge pulse duration in seconds.",
    )

    parser.add_argument(
        "--return-time",
        type=float,
        default=0.7,
        help="Return-to-idle duration in seconds.",
    )

    parser.add_argument(
        "--min-height",
        type=float,
        default=0.035,
        help="Minimum allowed root height before declaring instability.",
    )

    parser.add_argument(
        "--max-tilt",
        type=float,
        default=45.0,
        help="Maximum allowed roll/pitch tilt in degrees.",
    )

    parser.add_argument(
        "--max-xy",
        type=float,
        default=0.25,
        help="Maximum allowed XY drift in meters.",
    )

    parser.add_argument(
        "--viewer",
        action="store_true",
        help="Run with live MuJoCo viewer.",
    )

    parser.add_argument(
        "--realtime",
        action="store_true",
        help="Sleep between simulation steps to approximate real time.",
    )

    return parser


def run(args: argparse.Namespace) -> int:
    """
    Main simulation runner.
    """

    root = project_root()
    xml_path = (root / args.xml).resolve()

    if not xml_path.exists():
        print(f"ERROR: XML file not found: {xml_path}")
        return 1

    session_id = timestamp_id("sim_safe_nudge")

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    loaded_key = load_keyframe(model, data, "standing_idle")

    left_actuator_id = get_actuator_id(model, "left_leg_motor")
    right_actuator_id = get_actuator_id(model, "right_leg_motor")

    log: list[dict[str, Any]] = []
    phase_results: list[dict[str, Any]] = []

    phases = [
        ("settle_idle", args.settle, 0.0, 0.0),
        ("left_safe_nudge", args.pulse, args.left_ctrl, 0.0),
        ("return_after_left", args.return_time, 0.0, 0.0),
        ("right_safe_nudge", args.pulse, 0.0, args.right_ctrl),
        ("return_after_right", args.return_time, 0.0, 0.0),
    ]

    viewer_context = None
    viewer = None

    try:
        if args.viewer:
            from mujoco import viewer as mujoco_viewer
            viewer_context = mujoco_viewer.launch_passive(model, data)
            viewer = viewer_context.__enter__()

        overall_ok = True
        failure_message = "Safe nudge simulation completed successfully."

        for phase_name, duration, left_ctrl, right_ctrl in phases:
            ok, message = simulate_phase(
                model=model,
                data=data,
                phase=phase_name,
                duration=duration,
                left_ctrl=left_ctrl,
                right_ctrl=right_ctrl,
                left_actuator_id=left_actuator_id,
                right_actuator_id=right_actuator_id,
                log=log,
                min_height=args.min_height,
                max_tilt_degrees=args.max_tilt,
                max_xy_distance=args.max_xy,
                viewer=viewer,
                realtime=args.realtime or args.viewer,
            )

            phase_results.append(
                {
                    "phase": phase_name,
                    "status": "OK" if ok else "FAILED",
                    "message": message,
                    "duration": duration,
                    "left_ctrl": left_ctrl,
                    "right_ctrl": right_ctrl,
                }
            )

            if not ok:
                overall_ok = False
                failure_message = message
                break

    finally:
        if viewer_context is not None:
            viewer_context.__exit__(None, None, None)

    metrics = summarize_log(log)

    result = {
        "session_id": session_id,
        "xml_path": str(xml_path),
        "loaded_standing_idle_keyframe": loaded_key,
        "model": {
            "nq": int(model.nq),
            "nv": int(model.nv),
            "nu": int(model.nu),
            "nbody": int(model.nbody),
            "ngeom": int(model.ngeom),
            "njnt": int(model.njnt),
        },
        "actuators": {
            "left_leg_motor_id": int(left_actuator_id),
            "right_leg_motor_id": int(right_actuator_id),
        },
        "parameters": {
            "left_ctrl": args.left_ctrl,
            "right_ctrl": args.right_ctrl,
            "settle": args.settle,
            "pulse": args.pulse,
            "return_time": args.return_time,
            "min_height": args.min_height,
            "max_tilt": args.max_tilt,
            "max_xy": args.max_xy,
        },
        "phase_results": phase_results,
        "log": log,
        "summary": {
            "status": "OK" if overall_ok else "FAILED",
            "message": failure_message,
            **metrics,
        },
    }

    json_path, md_path = save_reports(root, result)
    print_summary(result, json_path, md_path)

    return 0 if overall_ok else 1


def main() -> int:
    """
    CLI entry point.
    """

    args = build_arg_parser().parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
