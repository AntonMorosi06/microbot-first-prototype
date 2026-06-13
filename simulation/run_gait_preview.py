#!/usr/bin/env python3
"""
MicroBot Round V0 - MuJoCo gait preview.

This script runs a very small alternating left/right movement pattern.

It is NOT a real walking controller yet.
It is a controlled simulation preview used to check whether repeated
safe nudges remain stable over multiple cycles.

Sequence:

    settle
    left nudge
    return
    right nudge
    return
    repeat

Outputs:

    evidence/reports/sim_gait_preview_<timestamp>.json
    evidence/reports/sim_gait_preview_<timestamp>.md
    evidence/reports/sim_gait_preview_<timestamp>.csv

Run:

    python simulation/run_gait_preview.py

More cycles:

    python simulation/run_gait_preview.py --cycles 5

Slightly stronger movement:

    python simulation/run_gait_preview.py --amplitude 0.10

This is simulation evidence only.
It does not validate real physical movement.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path
from typing import Any


try:
    import mujoco
except ImportError as exc:
    print("ERROR: mujoco is not installed in this Python environment.")
    print("Activate the MuJoCo environment first:")
    print("    source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh")
    print("    conda activate microbot312")
    print("    python simulation/run_gait_preview.py")
    raise SystemExit(1) from exc


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def timestamp_id(prefix: str) -> str:
    return time.strftime(f"{prefix}_%Y-%m-%d_%H-%M-%S")


def quat_to_euler_degrees(qw: float, qx: float, qy: float, qz: float) -> tuple[float, float, float]:
    sinr_cosp = 2.0 * (qw * qx + qy * qz)
    cosr_cosp = 1.0 - 2.0 * (qx * qx + qy * qy)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2.0 * (qw * qy - qz * qx)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


def name_to_id(model: mujoco.MjModel, object_type: Any, name: str) -> int:
    return mujoco.mj_name2id(model, object_type, name)


def load_keyframe(model: mujoco.MjModel, data: mujoco.MjData, key_name: str) -> bool:
    key_id = name_to_id(model, mujoco.mjtObj.mjOBJ_KEY, key_name)

    if key_id < 0:
        return False

    data.qpos[:] = model.key_qpos[key_id]
    data.qvel[:] = 0.0

    if model.nu > 0:
        data.ctrl[:] = model.key_ctrl[key_id]

    data.time = 0.0
    mujoco.mj_forward(model, data)
    return True


def actuator_id(model: mujoco.MjModel, name: str) -> int:
    return name_to_id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)


def joint_position(model: mujoco.MjModel, data: mujoco.MjData, joint_name: str) -> float | None:
    joint_id = name_to_id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)

    if joint_id < 0:
        return None

    qpos_address = model.jnt_qposadr[joint_id]
    return float(data.qpos[qpos_address])


def set_ctrl(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    left_id: int,
    right_id: int,
    left_value: float,
    right_value: float,
) -> None:
    if model.nu <= 0:
        return

    data.ctrl[:] = 0.0

    if left_id >= 0:
        data.ctrl[left_id] = left_value

    if right_id >= 0:
        data.ctrl[right_id] = right_value


def collect_state(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    phase: str,
    cycle: int,
) -> dict[str, Any]:
    x = float(data.qpos[0])
    y = float(data.qpos[1])
    z = float(data.qpos[2])

    qw = float(data.qpos[3])
    qx = float(data.qpos[4])
    qy = float(data.qpos[5])
    qz = float(data.qpos[6])

    roll, pitch, yaw = quat_to_euler_degrees(qw, qx, qy, qz)
    tilt = max(abs(roll), abs(pitch))
    xy = math.sqrt((x * x) + (y * y))

    return {
        "time": float(data.time),
        "phase": phase,
        "cycle": cycle,
        "x": x,
        "y": y,
        "z": z,
        "xy_distance": xy,
        "roll_degrees": roll,
        "pitch_degrees": pitch,
        "yaw_degrees": yaw,
        "tilt_degrees": tilt,
        "left_leg_hinge": joint_position(model, data, "left_leg_hinge"),
        "right_leg_hinge": joint_position(model, data, "right_leg_hinge"),
        "ctrl": [float(value) for value in data.ctrl],
    }


def check_unstable(
    state: dict[str, Any],
    min_height: float,
    max_tilt: float,
    max_xy: float,
) -> tuple[bool, str]:
    x = float(state["x"])
    y = float(state["y"])
    z = float(state["z"])
    tilt = float(state["tilt_degrees"])
    xy = float(state["xy_distance"])

    if not all(math.isfinite(value) for value in (x, y, z, tilt, xy)):
        return True, "non-finite simulation state"

    if z < min_height:
        return True, f"root height below limit: {z:.4f} < {min_height:.4f}"

    if tilt > max_tilt:
        return True, f"tilt above limit: {tilt:.2f} > {max_tilt:.2f}"

    if xy > max_xy:
        return True, f"XY drift above limit: {xy:.4f} > {max_xy:.4f}"

    return False, "stable"


def run_phase(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    phase: str,
    cycle: int,
    duration: float,
    left_ctrl: float,
    right_ctrl: float,
    left_id: int,
    right_id: int,
    min_height: float,
    max_tilt: float,
    max_xy: float,
    sample_stride: int,
    samples: list[dict[str, Any]],
) -> tuple[bool, str]:
    dt = float(model.opt.timestep)
    steps = max(1, int(duration / dt))

    for step in range(steps):
        set_ctrl(
            model=model,
            data=data,
            left_id=left_id,
            right_id=right_id,
            left_value=left_ctrl,
            right_value=right_ctrl,
        )

        mujoco.mj_step(model, data)

        if step % sample_stride == 0 or step == steps - 1:
            state = collect_state(model, data, phase=phase, cycle=cycle)
            samples.append(state)

            unstable, reason = check_unstable(
                state=state,
                min_height=min_height,
                max_tilt=max_tilt,
                max_xy=max_xy,
            )

            if unstable:
                return False, f"{phase} cycle {cycle}: {reason}"

    return True, f"{phase} cycle {cycle}: stable"


def summarize_samples(samples: list[dict[str, Any]]) -> dict[str, Any]:
    if not samples:
        return {
            "max_tilt_degrees": 0.0,
            "min_root_height": 0.0,
            "max_xy_distance": 0.0,
            "final_x": 0.0,
            "final_y": 0.0,
            "final_z": 0.0,
            "final_time": 0.0,
        }

    max_tilt = max(float(s["tilt_degrees"]) for s in samples)
    min_height = min(float(s["z"]) for s in samples)
    max_xy = max(float(s["xy_distance"]) for s in samples)
    final = samples[-1]

    return {
        "max_tilt_degrees": max_tilt,
        "min_root_height": min_height,
        "max_xy_distance": max_xy,
        "final_x": float(final["x"]),
        "final_y": float(final["y"]),
        "final_z": float(final["z"]),
        "final_time": float(final["time"]),
        "final_tilt_degrees": float(final["tilt_degrees"]),
    }


def build_markdown_report(result: dict[str, Any]) -> str:
    summary = result["summary"]

    lines = [
        "# MicroBot Round V0 - Gait Preview Simulation Report",
        "",
        f"Session ID: `{result['session_id']}`",
        f"XML model: `{result['xml_path']}`",
        "",
        "## Summary",
        "",
        f"- Status: `{summary['status']}`",
        f"- Message: {summary['message']}",
        f"- Cycles requested: `{result['parameters']['cycles']}`",
        f"- Cycles completed: `{summary['cycles_completed']}`",
        f"- Amplitude: `{result['parameters']['amplitude']}`",
        f"- Max tilt: `{summary['max_tilt_degrees']:.2f} deg`",
        f"- Min root height: `{summary['min_root_height']:.4f} m`",
        f"- Max XY drift: `{summary['max_xy_distance']:.4f} m`",
        f"- Final X: `{summary['final_x']:.4f} m`",
        f"- Final Y: `{summary['final_y']:.4f} m`",
        f"- Final Z: `{summary['final_z']:.4f} m`",
        f"- Final tilt: `{summary['final_tilt_degrees']:.2f} deg`",
        f"- Total simulation time: `{summary['final_time']:.3f} s`",
        "",
        "## Phase Results",
        "",
    ]

    for item in result["phase_results"]:
        lines.append(
            f"- Cycle `{item['cycle']}`, phase `{item['phase']}`: `{item['status']}` - {item['message']}"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )

    if summary["status"] == "OK":
        lines.append(
            "The simulated MicroBot remained stable during the repeated alternating left/right gait preview. This is a positive offline simulation result, but it is still not physical hardware validation."
        )
    else:
        lines.append(
            "The simulated MicroBot exceeded a stability threshold during the gait preview. Reduce amplitude, increase damping, adjust foot geometry, or improve mass distribution before testing stronger motion."
        )

    lines.extend(
        [
            "",
            "## Important Limitation",
            "",
            "This is simulation evidence only. It does not prove that the physical MicroBot can walk. The physical robot must still be tested with servo scan, safe power validation, small supervised nudge, and safety-layer gating.",
            "",
        ]
    )

    return "\n".join(lines)


def save_reports(root: Path, result: dict[str, Any]) -> dict[str, str]:
    reports_dir = root / "evidence" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    session_id = result["session_id"]

    json_path = reports_dir / f"{session_id}.json"
    md_path = reports_dir / f"{session_id}.md"
    csv_path = reports_dir / f"{session_id}.csv"

    json_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(build_markdown_report(result), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "time",
                "cycle",
                "phase",
                "x",
                "y",
                "z",
                "xy_distance",
                "roll_degrees",
                "pitch_degrees",
                "yaw_degrees",
                "tilt_degrees",
                "left_leg_hinge",
                "right_leg_hinge",
                "ctrl",
            ]
        )

        for s in result["samples"]:
            writer.writerow(
                [
                    s["time"],
                    s["cycle"],
                    s["phase"],
                    s["x"],
                    s["y"],
                    s["z"],
                    s["xy_distance"],
                    s["roll_degrees"],
                    s["pitch_degrees"],
                    s["yaw_degrees"],
                    s["tilt_degrees"],
                    s["left_leg_hinge"],
                    s["right_leg_hinge"],
                    json.dumps(s["ctrl"]),
                ]
            )

    result_with_reports = dict(result)
    result_with_reports["reports"] = {
        "json": str(json_path),
        "markdown": str(md_path),
        "csv": str(csv_path),
    }

    json_path.write_text(json.dumps(result_with_reports, indent=2, sort_keys=True), encoding="utf-8")

    return result_with_reports["reports"]


def print_summary(result: dict[str, Any]) -> None:
    summary = result["summary"]
    reports = result["reports"]

    print()
    print("MicroBot Round V0 gait preview")
    print("==============================")
    print(f"Status: {summary['status']}")
    print(f"Message: {summary['message']}")
    print(f"Cycles completed: {summary['cycles_completed']} / {result['parameters']['cycles']}")
    print(f"Amplitude: {result['parameters']['amplitude']}")
    print()
    print("Metrics")
    print("-------")
    print(f"Max tilt: {summary['max_tilt_degrees']:.2f} deg")
    print(f"Min root height: {summary['min_root_height']:.4f} m")
    print(f"Max XY drift: {summary['max_xy_distance']:.4f} m")
    print(f"Final X: {summary['final_x']:.4f} m")
    print(f"Final Y: {summary['final_y']:.4f} m")
    print(f"Final Z: {summary['final_z']:.4f} m")
    print(f"Final tilt: {summary['final_tilt_degrees']:.2f} deg")
    print(f"Total simulation time: {summary['final_time']:.3f} s")
    print()
    print("Reports")
    print("-------")
    print(f"JSON: {reports['json']}")
    print(f"MD:   {reports['markdown']}")
    print(f"CSV:  {reports['csv']}")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run MicroBot Round V0 MuJoCo gait preview."
    )

    parser.add_argument(
        "--xml",
        default="simulation/microbot_round_body.xml",
        help="Path to MuJoCo XML model.",
    )

    parser.add_argument(
        "--cycles",
        type=int,
        default=3,
        help="Number of alternating gait preview cycles.",
    )

    parser.add_argument(
        "--amplitude",
        type=float,
        default=0.08,
        help="Motor control amplitude.",
    )

    parser.add_argument(
        "--settle",
        type=float,
        default=1.0,
        help="Initial settle duration in seconds.",
    )

    parser.add_argument(
        "--pulse",
        type=float,
        default=0.45,
        help="Duration of each nudge pulse in seconds.",
    )

    parser.add_argument(
        "--return-time",
        type=float,
        default=0.45,
        help="Return-to-idle duration after each nudge.",
    )

    parser.add_argument(
        "--min-height",
        type=float,
        default=0.035,
        help="Minimum allowed root height.",
    )

    parser.add_argument(
        "--max-tilt",
        type=float,
        default=45.0,
        help="Maximum allowed tilt in degrees.",
    )

    parser.add_argument(
        "--max-xy",
        type=float,
        default=0.35,
        help="Maximum allowed XY drift.",
    )

    parser.add_argument(
        "--sample-stride",
        type=int,
        default=10,
        help="Sample every N simulation steps.",
    )

    return parser


def run(args: argparse.Namespace) -> int:
    root = project_root()
    xml_path = (root / args.xml).resolve()

    if not xml_path.exists():
        print(f"ERROR: XML file not found: {xml_path}")
        return 1

    session_id = timestamp_id("sim_gait_preview")

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    loaded_key = load_keyframe(model, data, "standing_idle")

    left_id = actuator_id(model, "left_leg_motor")
    right_id = actuator_id(model, "right_leg_motor")

    samples: list[dict[str, Any]] = []
    phase_results: list[dict[str, Any]] = []

    overall_ok = True
    message = "Gait preview completed successfully."
    cycles_completed = 0

    initial_ok, initial_message = run_phase(
        model=model,
        data=data,
        phase="initial_settle",
        cycle=0,
        duration=args.settle,
        left_ctrl=0.0,
        right_ctrl=0.0,
        left_id=left_id,
        right_id=right_id,
        min_height=args.min_height,
        max_tilt=args.max_tilt,
        max_xy=args.max_xy,
        sample_stride=args.sample_stride,
        samples=samples,
    )

    phase_results.append(
        {
            "cycle": 0,
            "phase": "initial_settle",
            "status": "OK" if initial_ok else "FAILED",
            "message": initial_message,
        }
    )

    if not initial_ok:
        overall_ok = False
        message = initial_message

    for cycle in range(1, max(1, args.cycles) + 1):
        if not overall_ok:
            break

        phases = [
            ("left_nudge", args.pulse, args.amplitude, 0.0),
            ("return_after_left", args.return_time, 0.0, 0.0),
            ("right_nudge", args.pulse, 0.0, -args.amplitude),
            ("return_after_right", args.return_time, 0.0, 0.0),
        ]

        cycle_ok = True

        for phase_name, duration, left_ctrl, right_ctrl in phases:
            ok, phase_message = run_phase(
                model=model,
                data=data,
                phase=phase_name,
                cycle=cycle,
                duration=duration,
                left_ctrl=left_ctrl,
                right_ctrl=right_ctrl,
                left_id=left_id,
                right_id=right_id,
                min_height=args.min_height,
                max_tilt=args.max_tilt,
                max_xy=args.max_xy,
                sample_stride=args.sample_stride,
                samples=samples,
            )

            phase_results.append(
                {
                    "cycle": cycle,
                    "phase": phase_name,
                    "status": "OK" if ok else "FAILED",
                    "message": phase_message,
                }
            )

            if not ok:
                overall_ok = False
                cycle_ok = False
                message = phase_message
                break

        if cycle_ok:
            cycles_completed += 1

    metrics = summarize_samples(samples)

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
            "left_leg_motor_id": int(left_id),
            "right_leg_motor_id": int(right_id),
        },
        "parameters": {
            "cycles": args.cycles,
            "amplitude": args.amplitude,
            "settle": args.settle,
            "pulse": args.pulse,
            "return_time": args.return_time,
            "min_height": args.min_height,
            "max_tilt": args.max_tilt,
            "max_xy": args.max_xy,
            "sample_stride": args.sample_stride,
        },
        "phase_results": phase_results,
        "samples": samples,
        "summary": {
            "status": "OK" if overall_ok else "FAILED",
            "message": message,
            "cycles_completed": cycles_completed,
            **metrics,
        },
    }

    reports = save_reports(root, result)
    result["reports"] = reports

    print_summary(result)

    return 0 if overall_ok else 1


def main() -> int:
    args = build_arg_parser().parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
