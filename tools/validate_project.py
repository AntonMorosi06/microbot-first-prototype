#!/usr/bin/env python3
"""
MicroBot First Prototype - repository validation tool.

This script performs a local quality check before committing or pushing.

It verifies:

- required folders exist
- required documentation files exist
- required Python scripts exist
- Python files compile
- current status uses realistic claims
- hardware validation is not claimed before physical evidence exists
- simulation validation files are present

Run:

    python tools/validate_project.py

This is not a hardware test.
It does not move motors.
It does not access GPIO.
It is safe to run on macOS or Raspberry Pi.
"""

from __future__ import annotations

import argparse
import py_compile
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CheckResult:
    name: str
    status: str
    message: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ok(name: str, message: str) -> CheckResult:
    return CheckResult(name=name, status="OK", message=message)


def fail(name: str, message: str) -> CheckResult:
    return CheckResult(name=name, status="FAILED", message=message)


def warn(name: str, message: str) -> CheckResult:
    return CheckResult(name=name, status="WARNING", message=message)


def check_required_paths(root: Path) -> list[CheckResult]:
    required = [
        "README.md",
        "docs/current_status.md",
        "docs/architecture.md",
        "docs/safety.md",
        "hardware/BOM.md",
        "hardware/pinout.md",
        "hardware/wiring.md",
        "setup/microbot/config.py",
        "setup/microbot/safety.py",
        "setup/microbot/logger.py",
        "setup/microbot/servos.py",
        "setup/scripts/self_check.py",
        "setup/scripts/hello_microbot.py",
        "setup/scripts/scan_servos.py",
        "simulation/README.md",
        "simulation/microbot_round_body.xml",
        "simulation/run_safe_nudge.py",
        "simulation/run_stability_sweep.py",
        "simulation/run_gait_preview.py",
        "evidence",
        "logs",
    ]

    results: list[CheckResult] = []

    for rel in required:
        path = root / rel
        if path.exists():
            results.append(ok(f"path:{rel}", "present"))
        else:
            results.append(fail(f"path:{rel}", "missing"))

    return results


def check_python_compilation(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []

    ignored_parts = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
    }

    python_files = [
        path for path in root.rglob("*.py")
        if not any(part in ignored_parts for part in path.parts)
    ]

    if not python_files:
        return [fail("python:files", "no Python files found")]

    for path in python_files:
        rel = path.relative_to(root)
        try:
            py_compile.compile(str(path), doraise=True)
            results.append(ok(f"compile:{rel}", "compiled"))
        except py_compile.PyCompileError as exc:
            results.append(fail(f"compile:{rel}", str(exc)))

    return results


def read_text_safe(path: Path) -> str:
    if not path.exists():
        return ""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def check_status_claims(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []

    files = [
        root / "README.md",
        root / "docs" / "current_status.md",
    ]

    combined = "\n".join(read_text_safe(path) for path in files).lower()

    if "validated-offline" in combined or "simulation-validated" in combined:
        results.append(ok("claim:simulation_status", "validated-offline claim found"))
    else:
        results.append(warn("claim:simulation_status", "validated-offline claim not found"))

    forbidden_strong_claims = [
        "hardware validated",
        "hardware-validated",
        "real robot walks",
        "physical robot walks",
        "autonomous robot",
        "finished robot",
        "production ready",
    ]

    found_forbidden = [
        claim for claim in forbidden_strong_claims
        if claim in combined
    ]

    if found_forbidden:
        results.append(
            fail(
                "claim:forbidden_public_claims",
                "forbidden unsupported claims found: " + ", ".join(found_forbidden),
            )
        )
    else:
        results.append(ok("claim:forbidden_public_claims", "no unsupported hardware claims found"))

    safety_words = [
        "not hardware-validated",
        "physical movement",
        "disabled",
        "servo scan",
        "safety",
    ]

    missing_safety_words = [
        word for word in safety_words
        if word not in combined
    ]

    if missing_safety_words:
        results.append(
            warn(
                "claim:safety_boundary",
                "some safety boundary words are missing: " + ", ".join(missing_safety_words),
            )
        )
    else:
        results.append(ok("claim:safety_boundary", "safety boundary is documented"))

    return results


def check_simulation_evidence(root: Path) -> list[CheckResult]:
    reports_dir = root / "evidence" / "reports"
    results: list[CheckResult] = []

    if not reports_dir.exists():
        return [warn("evidence:reports", "evidence/reports directory does not exist")]

    patterns = [
        "sim_safe_nudge_*.md",
        "sim_stability_sweep_*.md",
        "sim_gait_preview_*.md",
    ]

    for pattern in patterns:
        matches = sorted(reports_dir.glob(pattern))
        if matches:
            latest = matches[-1].relative_to(root)
            results.append(ok(f"evidence:{pattern}", f"found latest report: {latest}"))
        else:
            results.append(warn(f"evidence:{pattern}", "no matching report found"))

    return results


def check_no_accidental_large_files(root: Path, max_mb: float) -> list[CheckResult]:
    results: list[CheckResult] = []
    max_bytes = int(max_mb * 1024 * 1024)

    ignored_parts = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
    }

    large_files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in ignored_parts for part in path.parts):
            continue

        try:
            size = path.stat().st_size
        except OSError:
            continue

        if size > max_bytes:
            large_files.append((path.relative_to(root), size))

    if not large_files:
        results.append(ok("files:large_files", f"no files above {max_mb:.1f} MB"))
        return results

    for rel, size in large_files:
        mb = size / (1024 * 1024)
        results.append(warn(f"files:large:{rel}", f"{mb:.2f} MB"))

    return results


def print_results(results: list[CheckResult]) -> int:
    failed = [item for item in results if item.status == "FAILED"]
    warnings = [item for item in results if item.status == "WARNING"]
    oks = [item for item in results if item.status == "OK"]

    print()
    print("MicroBot First Prototype validation")
    print("===================================")
    print(f"OK:       {len(oks)}")
    print(f"WARNING:  {len(warnings)}")
    print(f"FAILED:   {len(failed)}")
    print()

    for item in results:
        print(f"[{item.status:<7}] {item.name} - {item.message}")

    print()

    if failed:
        print("RESULT: FAILED")
        return 1

    if warnings:
        print("RESULT: OK WITH WARNINGS")
        return 0

    print("RESULT: OK")
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate MicroBot First Prototype repository."
    )
    parser.add_argument(
        "--max-file-mb",
        type=float,
        default=25.0,
        help="Warn if a committed file is larger than this size.",
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    root = project_root()

    results: list[CheckResult] = []
    results.extend(check_required_paths(root))
    results.extend(check_python_compilation(root))
    results.extend(check_status_claims(root))
    results.extend(check_simulation_evidence(root))
    results.extend(check_no_accidental_large_files(root, max_mb=args.max_file_mb))

    return print_results(results)


if __name__ == "__main__":
    raise SystemExit(main())
