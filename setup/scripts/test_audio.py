#!/usr/bin/env python3
"""
MicroBot Round V0 audio test.

This script tests the MicroBot audio subsystem:

- checks available audio tools
- speaks a test phrase through the configured TTS path
- optionally records a short microphone sample
- reports a rough microphone RMS level

Reference hardware pattern:

- MAX98357A I2S amplifier
- small speaker
- INMP441 I2S microphone
- Raspberry Pi OS audio tools:
  - espeak-ng or flite for text-to-speech
  - aplay for playback
  - arecord for microphone capture

Install useful system packages on Raspberry Pi OS:

    sudo apt update
    sudo apt install -y espeak-ng flite alsa-utils

Run from repository root:

    python setup/scripts/test_audio.py

Microphone test:

    python setup/scripts/test_audio.py --mic-test

Custom phrase:

    python setup/scripts/test_audio.py --phrase "Hello, I am MicroBot."

JSON output:

    python setup/scripts/test_audio.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import audio  # noqa: E402
from microbot.config import get_config  # noqa: E402


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


def result_status(result: Any) -> str:
    """
    Extract status from a result object or dictionary.
    """

    if isinstance(result, dict):
        return normalize_status(result.get("status"))

    if hasattr(result, "status"):
        return normalize_status(getattr(result, "status"))

    return "UNKNOWN"


def print_capability_report(report: dict[str, Any]) -> None:
    """
    Print audio capability report.
    """

    print("Audio capability report")
    print("=======================")

    for key, value in report.items():
        print(f"{key}: {value}")

    print()


def print_result(title: str, result: Any) -> None:
    """
    Print a structured result in readable form.
    """

    data = to_dict_safe(result)

    print(title)
    print("=" * len(title))

    for key, value in data.items():
        print(f"{key}: {value}")

    print()


def run_speech_test(phrase: str, skip: bool) -> dict[str, Any]:
    """
    Run TTS/speaker test.
    """

    if skip:
        return {
            "status": "SKIPPED",
            "message": "Speech test skipped by command-line flag.",
        }

    try:
        result = audio.speak(phrase)
        return to_dict_safe(result)
    except Exception as exc:
        return {
            "status": "FAILED",
            "message": f"Speech test failed: {type(exc).__name__}: {exc}",
        }


def run_microphone_test(
    enabled: bool,
    output_path: str,
    duration_seconds: float,
    sample_rate: int,
    channels: int,
    device: str | None,
) -> dict[str, Any]:
    """
    Run microphone RMS test.
    """

    if not enabled:
        return {
            "status": "SKIPPED",
            "message": "Microphone test skipped. Use --mic-test to enable it.",
        }

    try:
        result = audio.microphone_level_test(
            output_path=output_path,
            duration_seconds=duration_seconds,
            sample_rate=sample_rate,
            channels=channels,
            device=device,
        )
        return to_dict_safe(result)
    except Exception as exc:
        return {
            "status": "FAILED",
            "message": f"Microphone test failed: {type(exc).__name__}: {exc}",
            "path": output_path,
        }


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    config = get_config()

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 speaker and microphone test."
    )

    parser.add_argument(
        "--phrase",
        default=config.audio.startup_phrase,
        help="Phrase to speak during the audio test.",
    )

    parser.add_argument(
        "--skip-speech",
        action="store_true",
        help="Skip text-to-speech / speaker test.",
    )

    parser.add_argument(
        "--mic-test",
        action="store_true",
        help="Run microphone recording and RMS level test.",
    )

    parser.add_argument(
        "--mic-output",
        default="/tmp/microbot_microphone_test.wav",
        help="Output WAV path for microphone test.",
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=config.audio.microphone_test_seconds,
        help="Microphone recording duration in seconds.",
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Microphone sample rate.",
    )

    parser.add_argument(
        "--channels",
        type=int,
        default=1,
        help="Microphone channel count.",
    )

    parser.add_argument(
        "--device",
        default=None,
        help="Optional ALSA device, for example hw:1,0 or plughw:CARD=sndrpigooglevoi.",
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

    capability_report = audio.audio_self_check()

    speech_result = run_speech_test(
        phrase=args.phrase,
        skip=args.skip_speech,
    )

    microphone_result = run_microphone_test(
        enabled=args.mic_test,
        output_path=args.mic_output,
        duration_seconds=args.duration,
        sample_rate=args.sample_rate,
        channels=args.channels,
        device=args.device,
    )

    output = {
        "capabilities": capability_report,
        "speech": speech_result,
        "microphone": microphone_result,
    }

    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True, default=str))
    else:
        print("MicroBot Round V0 audio test")
        print("============================")
        print()

        print_capability_report(capability_report)
        print_result("Speech test", speech_result)
        print_result("Microphone test", microphone_result)

        print("Notes")
        print("-----")
        print("- If speech is unavailable, install espeak-ng or flite.")
        print("- If playback fails, check speaker wiring, ALSA device and amplifier power.")
        print("- If microphone RMS is very low, check mic wiring, ALSA input and gain.")
        print("- Audio failure should not block non-audio robot tests.")
        print()

    speech_status = result_status(speech_result)
    microphone_status = result_status(microphone_result)

    hard_failure = speech_status == "FAILED"

    if args.mic_test and microphone_status == "FAILED":
        hard_failure = True

    return 1 if hard_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())