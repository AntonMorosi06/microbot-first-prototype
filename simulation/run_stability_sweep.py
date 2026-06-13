#!/usr/bin/env python3
"""
MicroBot Round V0 - MuJoCo stability sweep.

This script tests multiple safe-nudge control amplitudes and records whether
the simulated robot remains stable.

It answers one practical question:

    "How strong can the simulated leg nudge be before the robot becomes unstable?"

Run:

    python simulation/run_stability_sweep.py

Custom control range:

    python simulation/run_stability_sweep.py --controls 0.02,0.04,0.06,0.08,0.10,0.12,0.14

Output:

    evidence/reports/sim_stability_sweep_<timestamp>.json
    evidence/reports/sim_stability_sweep_<timestamp>.md
    evidence/reports/sim_stability_sweep_<timestamp>.csv

This is simulation evidence only. It does not prove that the physical robot can
move safely. Physical movement must still use setup/scripts/test_servos_safe.py.
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
    print("Activate the MuJoCo environment first.")
    print("Example:")
    print("    conda activate microbot312")
    print("    python simulation/run_stability_sweep.py")
    raise SystemExit(1) from exc


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def timestamp_id(prefix: str) -> str:
    return time.strftime(f"{prefix}_%Y-%m-%d_%H-%M-%S")


def parse_controls(text: str) -> list[float]:
    values: list[float] = []

    for raw in text.split(","):
        cleaned = raw.strip()
        if not cleaned:
            continue
        values.append(float(cleaned))

    if not values:
        raise ValueError("No control values were provided.")

    return values


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


def collect_state(data: mujoco.MjData) -> dict[str, float]:
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
        "x": x,
        "y": y,
        "z": z,
        "xy_distance": xy,
        "roll_degrees": roll,
        "pitch_degrees": pitch,
        "yaw_degrees": yaw,
        "tilt_degrees": tilt,
    }


def check_unstable(
    state: dict[str, float],
    min_height: float,
    max_tilt: float,
    max_xy: float,
) -> tuple[bool, str]:
    x = state["x"]
    y = state["y"]
    z = state["z"]
    tilt = state["tilt_degrees"]
    xy = state["xy_distance"]

    if not all(math.isfinite(v) for v in (x, y, z, tilt, xy)):
        return True, "non-finite state"

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
    duration: float,
    left_ctrl: float,
    right_ctrl: float,
    left_id: int,
    right_id: int,
    min_height: float,
    max_tilt: float,
    max_xy: float,
    sample_stride: int,
) -> tuple[bool, str, list[dict[str, float]]]:
    dt = float(model.opt.timestep)
    steps = max(1, int(duration / dt))

    samples: list[dict[str, float]] = []

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
            state = collect_state(data)
            state["phase"] = phase
            samples.append(state)

            unstable, reason = check_unstable(
                state=state,
                min_height=min_height,
                max_tilt=max_tilt,
                max_xy=max_xy,
            )

            if unstable:
                return False, f"{phase}: {reason}", samples

    return True, f"{phase}: stable", samples


def run_single_amplitude(
    model: mujoco.MjModel,
    amplitude: float,
    args: argparse.Namespace,
) -> dict[str, Any]:
    data = mujoco.MjData(model)

    loaded_key = load_keyframe(model, data, "standing_idle")

    left_id = actuator_id(model, "left_leg_motor")
    right_id = actuator_id(model, "right_leg_motor")

    phases = [
        {
            "name": "settle_idle",
            "duration": args.settle,
            "left_ctrl": 0.0,
            "right_ctrl": 0.0,
        },
        {
            "name": "left_nudge",
            "duration": args.pulse,
            "left_ctrl": amplitude,
            "right_ctrl": 0.0,
        },
        {
            "name": "return_after_left",
            "duration": args.return_time,
            "left_ctrl": 0.0,
            "right_ctrl": 0.0,
        },
        {
            "name": "right_nudge",
            "duration": args.pulse,
            "left_ctrl": 0.0,
            "right_ctrl": -amplitude,
        },
        {
            "name": "return_after_right",
            "duration": args.return_time,
            "left_ctrl": 0.0,
            "right_ctrl": 0.0,
        },
    ]

    all_samples: list[dict[str, float]] = []
    phase_results: list[dict[str, Any]] = []
    ok = True
    message = "Stable."

    for phase in phases:
        phase_ok, phase_message, samples = run_phase(
            model=model,
            data=data,
            phase=phase["name"],
            duration=phase["duration"],
            left_ctrl=phase["left_ctrl"],
            right_ctrl=phase["right_ctrl"],
            left_id=left_id,
            right_id=right_id,
            min_height=args.min_height,
            max_tilt=args.max_tilt,
            max_xy=args.max_xy,
            sample_stride=args.sample_stride,
        )

        all_samples.extend(samples)

        phase_results.append(
            {
                "phase": phase["name"],
                "status": "OK" if phase_ok else "FAILED",
                "message": phase_message,
                "duration": phase["duration"],
                "left_ctrl": phase["left_ctrl"],
                "right_ctrl": phase["right_ctrl"],
            }
        )

        if not phase_ok:
            ok = False
            message = phase_message
            break

    metrics = summarize_samples(all_samples)

    return {
        "amplitude": amplitude,
        "status": "OK" if ok else "FAILED",
        "message": message,
        "loaded_standing_idle_keyframe": loaded_key,
        "left_actuator_id": left_id,
        "right_actuator_id": right_id,
        "metrics": metrics,
        "phase_results": phase_results,
        "sample_count": len(all_samples),
    }


def summarize_samples(samples: list[dict[str, float]]) -> dict[str, float]:
    if not samples:
        return {
            "max_tilt_degrees": 0.0,
            "min_root_height": 0.0,
            "max_xy_distance": 0.0,
            "final_time": 0.0,
        }

    max_tilt = max(float(s["tilt_degrees"]) for s in samples)
    min_height = min(float(s["z"]) for s in samples)
    max_xy = max(float(s["xy_distance"]) for s in samples)
    final_time = max(float(s["time"]) for s in samples)

    return {
        "max_tilt_degrees": max_tilt,
        "min_root_height": min_height,
        "max_xy_distance": max_xy,
        "final_time": final_time,
    }


def find_recommended_safe_control(results: list[dict[str, Any]]) -> float | None:
    ok_values = [float(r["amplitude"]) for r in results if r["status"] == "OK"]

    if not ok_values:
        return None

    max_ok = max(ok_values)

    return round(max_ok * 0.75, 4)


def build_markdown_report(result: dict[str, Any]) -> str:
    summary = result["summary"]

    lines = [
        "# MicroBot Round V0 - Stability Sweep Report",
        "",
        f"Session ID: `{result['session_id']}`",
        f"XML model: `{result['xml_path']}`",
        "",
        "## Summary",
        "",
        f"- Overall status: `{summary['status']}`",
        f"- Tested amplitudes: `{summary['tested_count']}`",
        f"- Stable amplitudes: `{summary['stable_count']}`",
        f"- Failed amplitudes: `{summary['failed_count']}`",
        f"- Maximum stable amplitude: `{summary['max_stable_amplitude']}`",
        f"- Recommended conservative control: `{summary['recommended_conservative_control']}`",
        "",
        "## Results Table",
        "",
        "| Amplitude | Status | Max tilt | Min height | Max XY drift | Message |",
        "|---:|---|---:|---:|---:|---|",
    ]

    for item in result["results"]:
        metrics = item["metrics"]
        lines.append(
            "| "
            f"{item['amplitude']:.4f} | "
            f"{item['status']} | "
            f"{metrics['max_tilt_degrees']:.2f} deg | "
            f"{metrics['min_root_height']:.4f} m | "
            f"{metrics['max_xy_distance']:.4f} m | "
            f"{item['message']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )

    if summary["stable_count"] > 0:
        lines.append(
            "The model remained stable for at least one tested control amplitude. The recommended conservative control is intentionally lower than the maximum stable value."
        )
    else:
        lines.append(
            "No tested control amplitude remained stable. The model should be adjusted before attempting stronger simulated movement."
        )

    lines.extend(
        [
            "",
            "## Important Limitation",
            "",
            "This is simulation evidence only. It does not validate the real physical robot. The physical safe nudge must still be performed with hardware movement disabled by default, servo scan validation, supervised power testing, and the safety layer.",
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
                "amplitude",
                "status",
                "max_tilt_degrees",
                "min_root_height",
                "max_xy_distance",
                "message",
            ]
        )

        for item in result["results"]:
            metrics = item["metrics"]
            writer.writerow(
                [
                    item["amplitude"],
                    item["status"],
                    metrics["max_tilt_degrees"],
                    metrics["min_root_height"],
                    metrics["max_xy_distance"],
                    item["message"],
                ]
            )

    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "csv": str(csv_path),
    }


def print_summary(result: dict[str, Any]) -> None:
    summary = result["summary"]
    reports = result["reports"]

    print()
    print("MicroBot Round V0 stability sweep")
    print("=================================")
    print(f"Status: {summary['status']}")
    print(f"Tested amplitudes: {summary['tested_count']}")
    print(f"Stable: {summary['stable_count']}")
    print(f"Failed: {summary['failed_count']}")
    print(f"Max stable amplitude: {summary['max_stable_amplitude']}")
    print(f"Recommended conservative control: {summary['recommended_conservative_control']}")
    print()

    print("Results")
    print("-------")
    for item in result["results"]:
        metrics = item["metrics"]
        print(
            f"{item['amplitude']:.4f}  "
            f"{item['status']:<7}  "
            f"tilt={metrics['max_tilt_degrees']:.2f}deg  "
            f"height={metrics['min_root_height']:.4f}m  "
            f"xy={metrics['max_xy_distance']:.4f}m"
        )

    print()
    print("Reports")
    print("-------")
    print(f"JSON: {reports['json']}")
    print(f"MD:   {reports['markdown']}")
    print(f"CSV:  {reports['csv']}")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run MicroBot Round V0 MuJoCo stability sweep."
    )

    parser.add_argument(
        "--xml",
        default="simulation/microbot_round_body.xml",
        help="Path to MuJoCo XML model.",
    )

    parser.add_argument(
        "--controls",
        default="0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16,0.18,0.20",
        help="Comma-separated motor control amplitudes to test.",
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
        default=0.25,
        help="Maximum allowed XY drift.",
    )

    parser.add_argument(
        "--sample-stride",
        type=int,
        default=10,
        help="Sample every N simulation steps.",
    )

    return parser


def main() -> int:
    args = build_arg_parser().parse_args()

    root = project_root()
    xml_path = (root / args.xml).resolve()

    if not xml_path.exists():
        print(f"ERROR: XML file not found: {xml_path}")
        return 1

    controls = parse_controls(args.controls)

    model = mujoco.MjModel.from_xml_path(str(xml_path))

    results = []

    for amplitude in controls:
        item = run_single_amplitude(
            model=model,
            amplitude=amplitude,
            args=args,
        )
        results.append(item)

    stable = [item for item in results if item["status"] == "OK"]
    failed = [item for item in results if item["status"] != "OK"]

    max_stable = max((item["amplitude"] for item in stable), default=None)
    recommended = find_recommended_safe_control(results)

    session_id = timestamp_id("sim_stability_sweep")

    result = {
        "session_id": session_id,
        "xml_path": str(xml_path),
        "parameters": {
            "controls": controls,
            "settle": args.settle,
            "pulse": args.pulse,
            "return_time": args.return_time,
            "min_height": args.min_height,
            "max_tilt": args.max_tilt,
            "max_xy": args.max_xy,
            "sample_stride": args.sample_stride,
        },
        "model": {
            "nq": int(model.nq),
            "nv": int(model.nv),
            "nu": int(model.nu),
            "nbody": int(model.nbody),
            "ngeom": int(model.ngeom),
            "njnt": int(model.njnt),
        },
        "results": results,
        "summary": {
            "status": "OK" if stable else "FAILED",
            "tested_count": len(results),
            "stable_count": len(stable),
            "failed_count": len(failed),
            "max_stable_amplitude": max_stable,
            "recommended_conservative_control": recommended,
        },
    }

    reports = save_reports(root, result)
    result["reports"] = reports

    for path in reports.values():
        Path(path).write_text(
            Path(path).read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    if reports:
        json_path = Path(reports["json"])
        json_data = json.loads(json_path.read_text(encoding="utf-8"))
        json_data["reports"] = reports
        json_path.write_text(json.dumps(json_data, indent=2, sort_keys=True), encoding="utf-8")

    result["reports"] = reports
    print_summary(result)

    return 0 if stable else 1


if __name__ == "__main__":
    raise SystemExit(main())
