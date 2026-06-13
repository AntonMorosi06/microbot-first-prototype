"""
MicroBot Round V0 LED module.

This module provides safe, minimal LED ring helpers for the first MicroBot Round V0
hardware bring-up.

Expected V0 hardware reference:

- WS2812B / NeoPixel LED ring
- 7 pixels
- data line on Raspberry Pi GPIO12
- 5 V power rail
- common ground with Raspberry Pi and the rest of the robot

Important Raspberry Pi note:
The rpi_ws281x library uses PWM/DMA timing and often requires root permissions.
If LED initialization fails, try running the script with:

    sudo -E python setup/microbot/leds.py

LEDs are not safety-critical, but they are useful for robot status:

- blue: boot / idle
- green: OK
- yellow: warning
- red: error / safe mode
- purple: decision / autonomy
- orange: obstacle
- white: self-check
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import time


try:
    from rpi_ws281x import Color, PixelStrip
except ImportError:  # pragma: no cover
    Color = None
    PixelStrip = None


try:
    from . import pins
except ImportError:  # Allows running this file directly during early testing.
    pins = None


DEFAULT_LED_PIN = getattr(pins, "LED_PIN", 12)
DEFAULT_LED_COUNT = getattr(pins, "LED_COUNT", 7)
DEFAULT_LED_BRIGHTNESS = getattr(pins, "LED_BRIGHTNESS", 40)
DEFAULT_LED_FREQ_HZ = getattr(pins, "LED_FREQ_HZ", 800_000)
DEFAULT_LED_DMA = getattr(pins, "LED_DMA", 10)
DEFAULT_LED_CHANNEL = getattr(pins, "LED_CHANNEL", 0)
DEFAULT_LED_INVERT = False


COLOR_MAP: dict[str, tuple[int, int, int]] = {
    "off": (0, 0, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 80, 255),
    "yellow": (255, 180, 0),
    "orange": (255, 80, 0),
    "purple": (150, 0, 255),
    "cyan": (0, 255, 255),
    "pink": (255, 40, 120),
}


@dataclass(frozen=True)
class LedConfig:
    """
    LED ring configuration.

    count:
        Number of LEDs in the ring.

    pin:
        Raspberry Pi GPIO number, BCM numbering.

    brightness:
        Global brightness from 0 to 255.

    freq_hz:
        WS2812 signal frequency.

    dma:
        DMA channel used by rpi_ws281x.

    channel:
        PWM channel. GPIO12 usually uses channel 0.

    invert:
        Usually False for normal WS2812 rings.
    """

    count: int = DEFAULT_LED_COUNT
    pin: int = DEFAULT_LED_PIN
    brightness: int = DEFAULT_LED_BRIGHTNESS
    freq_hz: int = DEFAULT_LED_FREQ_HZ
    dma: int = DEFAULT_LED_DMA
    channel: int = DEFAULT_LED_CHANNEL
    invert: bool = DEFAULT_LED_INVERT


@dataclass(frozen=True)
class LedResult:
    """
    Structured result returned by LED operations.

    status:
        OK, WARNING, FAILED, or UNAVAILABLE.

    message:
        Human-readable explanation.
    """

    status: str
    message: str
    timestamp: float


def clamp(value: int | float, minimum: int = 0, maximum: int = 255) -> int:
    """
    Clamp a numeric value to an integer range.
    """

    return int(max(minimum, min(maximum, int(value))))


def normalize_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Clamp an RGB tuple to valid 0-255 values.
    """

    r, g, b = rgb
    return clamp(r), clamp(g), clamp(b)


def color_from_name(name: str) -> tuple[int, int, int]:
    """
    Convert a color name into an RGB tuple.

    Unknown color names return white.
    """

    return COLOR_MAP.get(name.strip().lower(), COLOR_MAP["white"])


def scale_rgb(rgb: tuple[int, int, int], scale: float) -> tuple[int, int, int]:
    """
    Scale an RGB tuple by a float factor.
    """

    r, g, b = rgb
    return normalize_rgb((int(r * scale), int(g * scale), int(b * scale)))


def make_color(rgb: tuple[int, int, int]):
    """
    Convert an RGB tuple into rpi_ws281x Color.

    This function exists so the rest of the module can handle missing hardware
    libraries gracefully.
    """

    if Color is None:
        raise RuntimeError("rpi_ws281x is not installed. Run: pip install rpi_ws281x")

    r, g, b = normalize_rgb(rgb)
    return Color(r, g, b)


class LedRing:
    """
    Minimal WS2812 LED ring driver.

    The class raises clear errors if rpi_ws281x is missing or if the Raspberry Pi
    process does not have the permissions needed for PWM/DMA access.
    """

    def __init__(self, config: LedConfig | None = None) -> None:
        if PixelStrip is None:
            raise RuntimeError("rpi_ws281x is not installed. Run: pip install rpi_ws281x")

        self.config = config or LedConfig()
        self.count = self.config.count

        self.strip = PixelStrip(
            self.config.count,
            self.config.pin,
            self.config.freq_hz,
            self.config.dma,
            self.config.invert,
            clamp(self.config.brightness),
            self.config.channel,
        )

        try:
            self.strip.begin()
        except Exception as exc:
            raise RuntimeError(
                "LED initialization failed. WS2812 on Raspberry Pi often needs root. "
                "Try: sudo -E python setup/microbot/leds.py. "
                f"Original error: {type(exc).__name__}: {exc}"
            ) from exc

    def set_pixel(self, index: int, rgb: tuple[int, int, int]) -> None:
        """
        Set one LED pixel.
        """

        if index < 0 or index >= self.count:
            raise IndexError(f"LED index out of range: {index}")

        self.strip.setPixelColor(index, make_color(rgb))

    def show(self) -> None:
        """
        Push pending color values to the LED ring.
        """

        self.strip.show()

    def fill(self, rgb: tuple[int, int, int], show: bool = True) -> None:
        """
        Fill the entire LED ring with one color.
        """

        color = make_color(rgb)

        for index in range(self.count):
            self.strip.setPixelColor(index, color)

        if show:
            self.strip.show()

    def fill_name(self, color_name: str, show: bool = True) -> None:
        """
        Fill the ring using a named color.
        """

        self.fill(color_from_name(color_name), show=show)

    def off(self) -> None:
        """
        Turn the LED ring off.
        """

        self.fill(COLOR_MAP["off"])

    def spin(
        self,
        rgb: tuple[int, int, int],
        rounds: int = 2,
        delay: float = 0.05,
        clear_after: bool = True,
    ) -> None:
        """
        Chase one lit pixel around the ring.
        """

        color = make_color(rgb)
        off_color = make_color(COLOR_MAP["off"])

        for _ in range(max(1, rounds)):
            for lit in range(self.count):
                for index in range(self.count):
                    self.strip.setPixelColor(index, color if index == lit else off_color)
                self.strip.show()
                time.sleep(max(0.0, delay))

        if clear_after:
            self.off()

    def pulse(
        self,
        rgb: tuple[int, int, int],
        pulses: int = 2,
        steps: int = 12,
        delay: float = 0.035,
        clear_after: bool = True,
    ) -> None:
        """
        Pulse the whole ring by increasing and decreasing brightness.
        """

        pulses = max(1, pulses)
        steps = max(2, steps)

        for _ in range(pulses):
            for step in range(steps):
                scale = step / (steps - 1)
                self.fill(scale_rgb(rgb, scale))
                time.sleep(max(0.0, delay))

            for step in range(steps - 1, -1, -1):
                scale = step / (steps - 1)
                self.fill(scale_rgb(rgb, scale))
                time.sleep(max(0.0, delay))

        if clear_after:
            self.off()

    def boot_animation(self) -> None:
        """
        MicroBot boot LED sequence.
        """

        self.fill_name("blue")
        time.sleep(0.25)
        self.spin(COLOR_MAP["cyan"], rounds=1, delay=0.04, clear_after=False)
        self.fill_name("white")
        time.sleep(0.15)
        self.fill_name("blue")

    def ok(self) -> None:
        """
        Show OK status.
        """

        self.fill_name("green")

    def warning(self) -> None:
        """
        Show warning status.
        """

        self.fill_name("yellow")

    def error(self) -> None:
        """
        Show error / safe mode status.
        """

        self.fill_name("red")

    def decision(self) -> None:
        """
        Show decision / autonomy status.
        """

        self.fill_name("purple")

    def obstacle(self) -> None:
        """
        Show obstacle status.
        """

        self.fill_name("orange")

    def self_check(self) -> LedResult:
        """
        Run a short LED self-check.

        The sequence is intentionally simple:
        red, green, blue, white, spin, off.
        """

        try:
            for color_name in ("red", "green", "blue", "white"):
                self.fill_name(color_name)
                time.sleep(0.25)

            self.spin(COLOR_MAP["cyan"], rounds=1, delay=0.04)
            self.off()

            return LedResult(
                status="OK",
                message="LED self-check completed successfully.",
                timestamp=time.time(),
            )
        except Exception as exc:
            return LedResult(
                status="FAILED",
                message=f"LED self-check failed: {type(exc).__name__}: {exc}",
                timestamp=time.time(),
            )


def led_self_check(config: LedConfig | None = None) -> dict[str, str | float]:
    """
    Run LED self-check and return a dictionary for JSON logs.
    """

    try:
        ring = LedRing(config)
        result = ring.self_check()
    except Exception as exc:
        result = LedResult(
            status="FAILED",
            message=f"LED unavailable: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    return {
        "status": result.status,
        "message": result.message,
        "timestamp": result.timestamp,
    }


def print_led_self_check(config: LedConfig | None = None) -> LedResult:
    """
    Run LED self-check, print result and return LedResult.
    """

    try:
        ring = LedRing(config)
        result = ring.self_check()
    except Exception as exc:
        result = LedResult(
            status="FAILED",
            message=f"LED unavailable: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    print("LED self-check")
    print("==============")
    print(f"Status: {result.status}")
    print(f"Message: {result.message}")

    return result


def safe_set_status(color_name: str, config: LedConfig | None = None) -> LedResult:
    """
    Best-effort helper to set a status color without crashing the caller.

    This is useful inside self_check.py or hello_microbot.py.
    """

    try:
        ring = LedRing(config)
        ring.fill_name(color_name)
        return LedResult(
            status="OK",
            message=f"LED status set to {color_name}.",
            timestamp=time.time(),
        )
    except Exception as exc:
        return LedResult(
            status="FAILED",
            message=f"Could not set LED status: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI argument parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 WS2812 LED ring test."
    )

    parser.add_argument(
        "--color",
        default=None,
        help="Set a named color instead of running the full self-check.",
    )

    parser.add_argument(
        "--brightness",
        type=int,
        default=DEFAULT_LED_BRIGHTNESS,
        help="LED brightness from 0 to 255.",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_LED_COUNT,
        help="Number of LEDs in the ring.",
    )

    parser.add_argument(
        "--pin",
        type=int,
        default=DEFAULT_LED_PIN,
        help="BCM GPIO pin for WS2812 data.",
    )

    parser.add_argument(
        "--off",
        action="store_true",
        help="Turn the LED ring off.",
    )

    return parser


def main() -> int:
    """
    CLI entry point.

    Examples:

        sudo -E python setup/microbot/leds.py
        sudo -E python setup/microbot/leds.py --color blue
        sudo -E python setup/microbot/leds.py --color green --brightness 30
        sudo -E python setup/microbot/leds.py --off
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    config = LedConfig(
        count=args.count,
        pin=args.pin,
        brightness=clamp(args.brightness),
    )

    try:
        ring = LedRing(config)

        if args.off:
            ring.off()
            print("LED ring turned off.")
            return 0

        if args.color:
            ring.fill_name(args.color)
            print(f"LED ring set to {args.color}.")
            return 0

        result = ring.self_check()
        print("LED self-check")
        print("==============")
        print(f"Status: {result.status}")
        print(f"Message: {result.message}")

        return 0 if result.status == "OK" else 1

    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
