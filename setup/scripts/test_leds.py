#!/usr/bin/env python3
"""
MicroBot Round V0 LED test.

This script tests the MicroBot WS2812B / NeoPixel LED ring.

Reference hardware pattern:

- Raspberry Pi Zero 2 W
- WS2812B / NeoPixel LED ring
- 7 pixels
- data line on GPIO12 / physical pin 32
- 5 V power rail
- common ground

Important Raspberry Pi note:
The rpi_ws281x library often requires root permissions because it uses PWM/DMA
timing. If the test fails with a permissions error, run:

    sudo -E python setup/scripts/test_leds.py

Examples:

    sudo -E python setup/scripts/test_leds.py

    sudo -E python setup/scripts/test_leds.py --color blue

    sudo -E python setup/scripts/test_leds.py --color green --brightness 30

    sudo -E python setup/scripts/test_leds.py --spin purple

    sudo -E python setup/scripts/test_leds.py --pulse cyan

    sudo -E python setup/scripts/test_leds.py --off

JSON output:

    sudo -E python setup/scripts/test_leds.py --json

Safety:
This script does not move the robot.
It only controls the LED ring.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SETUP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SETUP_DIR))


from microbot import leds  # noqa: E402
from microbot import pins  # noqa: E402


def normalize_status(value: Any) -> str:
    """
    Normalize status text.
    """

    if value is None:
        return "UNKNOWN"

    return str(value).strip().upper()


def to_dict_safe(value: Any) -> dict[str, Any]:
    """
    Convert result object or dictionary into a plain dictionary.
    """

    if isinstance(value, dict):
        return value

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return {
        "status": "UNKNOWN",
        "message": str(value),
    }


def build_config(args: argparse.Namespace) -> leds.LedConfig:
    """
    Build LED configuration from command-line arguments.
    """

    return leds.LedConfig(
        count=args.count,
        pin=args.pin,
        brightness=leds.clamp(args.brightness),
    )


def print_header(args: argparse.Namespace) -> None:
    """
    Print test header.
    """

    print("MicroBot Round V0 LED test")
    print("==========================")
    print(f"LED count: {args.count}")
    print(f"GPIO pin: {args.pin}")
    print(f"Brightness: {args.brightness}")
    print()


def print_result(result: dict[str, Any]) -> None:
    """
    Print readable LED result.
    """

    print("Result")
    print("------")
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    print()

    print("Notes")
    print("-----")
    print("- If initialization fails, try running with sudo -E.")
    print("- Check WS2812 data line on GPIO12 / physical pin 32.")
    print("- Check 5 V power and common ground.")
    print("- Keep brightness low during first power tests.")
    print("- LED failure should not block non-LED robot tests.")
    print()


def run_led_test(args: argparse.Namespace) -> dict[str, Any]:
    """
    Run the selected LED test.
    """

    config = build_config(args)

    try:
        ring = leds.LedRing(config)

        if args.off:
            ring.off()
            return {
                "status": "OK",
                "message": "LED ring turned off.",
                "operation": "off",
                "pin": args.pin,
                "count": args.count,
                "brightness": args.brightness,
            }

        if args.color:
            rgb = leds.color_from_name(args.color)
            ring.fill(rgb)
            return {
                "status": "OK",
                "message": f"LED ring set to color: {args.color}.",
                "operation": "color",
                "color": args.color,
                "rgb": rgb,
                "pin": args.pin,
                "count": args.count,
                "brightness": args.brightness,
            }

        if args.spin:
            rgb = leds.color_from_name(args.spin)
            ring.spin(
                rgb,
                rounds=args.rounds,
                delay=args.delay,
                clear_after=not args.keep_on,
            )
            return {
                "status": "OK",
                "message": f"LED spin animation completed with color: {args.spin}.",
                "operation": "spin",
                "color": args.spin,
                "rgb": rgb,
                "rounds": args.rounds,
                "delay": args.delay,
                "pin": args.pin,
                "count": args.count,
                "brightness": args.brightness,
            }

        if args.pulse:
            rgb = leds.color_from_name(args.pulse)
            ring.pulse(
                rgb,
                pulses=args.pulses,
                steps=args.steps,
                delay=args.delay,
                clear_after=not args.keep_on,
            )
            return {
                "status": "OK",
                "message": f"LED pulse animation completed with color: {args.pulse}.",
                "operation": "pulse",
                "color": args.pulse,
                "rgb": rgb,
                "pulses": args.pulses,
                "steps": args.steps,
                "delay": args.delay,
                "pin": args.pin,
                "count": args.count,
                "brightness": args.brightness,
            }

        if args.boot:
            ring.boot_animation()
            if not args.keep_on:
                ring.off()
            return {
                "status": "OK",
                "message": "LED boot animation completed.",
                "operation": "boot",
                "pin": args.pin,
                "count": args.count,
                "brightness": args.brightness,
            }

        result = ring.self_check()
        return {
            **to_dict_safe(result),
            "operation": "self_check",
            "pin": args.pin,
            "count": args.count,
            "brightness": args.brightness,
        }

    except Exception as exc:
        return {
            "status": "FAILED",
            "message": f"LED test failed: {type(exc).__name__}: {exc}",
            "operation": "unknown",
            "pin": args.pin,
            "count": args.count,
            "brightness": args.brightness,
            "hint": "On Raspberry Pi, try: sudo -E python setup/scripts/test_leds.py",
        }


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 WS2812B / NeoPixel LED ring test."
    )

    parser.add_argument(
        "--color",
        default=None,
        help="Set the full LED ring to a named color.",
    )

    parser.add_argument(
        "--spin",
        default=None,
        help="Run spin animation with a named color.",
    )

    parser.add_argument(
        "--pulse",
        default=None,
        help="Run pulse animation with a named color.",
    )

    parser.add_argument(
        "--boot",
        action="store_true",
        help="Run MicroBot boot animation.",
    )

    parser.add_argument(
        "--off",
        action="store_true",
        help="Turn the LED ring off.",
    )

    parser.add_argument(
        "--brightness",
        type=int,
        default=pins.LED_BRIGHTNESS,
        help=f"LED brightness from 0 to 255. Default: {pins.LED_BRIGHTNESS}",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=pins.LED_COUNT,
        help=f"Number of LEDs in the ring. Default: {pins.LED_COUNT}",
    )

    parser.add_argument(
        "--pin",
        type=int,
        default=pins.LED_PIN,
        help=f"BCM GPIO pin for WS2812 data. Default: GPIO{pins.LED_PIN}",
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=2,
        help="Number of spin animation rounds.",
    )

    parser.add_argument(
        "--pulses",
        type=int,
        default=2,
        help="Number of pulse animation cycles.",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=12,
        help="Number of pulse brightness steps.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.05,
        help="Animation delay in seconds.",
    )

    parser.add_argument(
        "--keep-on",
        action="store_true",
        help="Do not clear LEDs after animation.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output.",
    )

    return parser


def main() -> int:
    """
    Main CLI entry point.
    """

    args = build_arg_parser().parse_args()

    if not args.json:
        print_header(args)

    result = run_led_test(args)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
    else:
        print_result(result)

    return 0 if normalize_status(result.get("status")) == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())