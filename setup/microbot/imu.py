"""
MicroBot Round V0 IMU module.

This module provides a minimal MPU-6050 IMU reader for the first MicroBot Round V0
hardware bring-up.

The IMU is used for:

- detecting whether the robot is flat or tilted
- blocking movement when orientation is unsafe
- logging acceleration and gyro readings
- supporting future movement analysis
- supporting the first autonomous safety demo

Recommended V0 IMU:

- MPU-6050 / GY-521 module
- I2C address usually 0x68
- connected to Raspberry Pi I2C bus

Important V0 rule:
If the IMU is unavailable or returns invalid data, physical movement should be
blocked by the safety layer.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import math
import time


try:
    import smbus2
except ImportError:  # pragma: no cover
    smbus2 = None


try:
    from . import pins
except ImportError:  # Allows running this file directly during early testing.
    pins = None


DEFAULT_IMU_I2C_ADDR = getattr(pins, "IMU_I2C_ADDR", 0x68)
DEFAULT_I2C_BUS = 1

REG_PWR_MGMT_1 = 0x6B
REG_WHO_AM_I = 0x75
REG_ACCEL_XOUT_H = 0x3B
REG_GYRO_XOUT_H = 0x43

ACCEL_SCALE = 16384.0
GYRO_SCALE = 131.0


@dataclass(frozen=True)
class ImuConfig:
    """
    IMU configuration.

    address:
        I2C address of the MPU-6050.

    bus_num:
        I2C bus number. Raspberry Pi usually uses bus 1.

    tilt_warning_degrees:
        Tilt threshold for warning status.

    tilt_critical_degrees:
        Tilt threshold for unsafe status.

    expected_who_am_i:
        Common WHO_AM_I values for MPU-6050 family modules.
    """

    address: int = DEFAULT_IMU_I2C_ADDR
    bus_num: int = DEFAULT_I2C_BUS
    tilt_warning_degrees: float = 20.0
    tilt_critical_degrees: float = 30.0
    expected_who_am_i: tuple[int, ...] = (0x68, 0x70, 0x71, 0x98)


@dataclass(frozen=True)
class ImuReading:
    """
    Structured IMU reading.

    ax, ay, az:
        Acceleration in g.

    gx, gy, gz:
        Angular velocity in degrees per second.

    roll_degrees:
        Estimated roll angle from accelerometer.

    pitch_degrees:
        Estimated pitch angle from accelerometer.

    tilt_degrees:
        Maximum absolute tilt between roll and pitch.

    stable:
        True if tilt is below the warning threshold.

    status:
        OK, WARNING, CRITICAL, or FAILED.

    message:
        Human-readable explanation.
    """

    ax: float
    ay: float
    az: float

    gx: float
    gy: float
    gz: float

    roll_degrees: float
    pitch_degrees: float
    tilt_degrees: float

    stable: bool
    status: str
    message: str
    timestamp: float


@dataclass(frozen=True)
class ImuSelfCheckResult:
    """
    Structured IMU self-check result.
    """

    status: str
    who_am_i: int | None
    reading: ImuReading | None
    message: str
    timestamp: float


def calculate_roll_pitch(ax: float, ay: float, az: float) -> tuple[float, float]:
    """
    Estimate roll and pitch from accelerometer values.

    This is a simple static estimate. It is useful for early tilt safety checks,
    but it is not a full orientation filter.
    """

    roll = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt((ay * ay) + (az * az))))

    return roll, pitch


def classify_tilt(
    roll_degrees: float,
    pitch_degrees: float,
    config: ImuConfig | None = None,
) -> tuple[str, bool, str, float]:
    """
    Classify tilt state using roll and pitch.

    Returns:
        status, stable, message, tilt_degrees
    """

    cfg = config or ImuConfig()
    tilt = max(abs(roll_degrees), abs(pitch_degrees))

    if tilt >= cfg.tilt_critical_degrees:
        return (
            "CRITICAL",
            False,
            "Tilt is above critical threshold. Movement must be blocked.",
            tilt,
        )

    if tilt >= cfg.tilt_warning_degrees:
        return (
            "WARNING",
            False,
            "Tilt is above warning threshold. Movement should be blocked or reduced.",
            tilt,
        )

    return (
        "OK",
        True,
        "Robot orientation is within configured stable range.",
        tilt,
    )


class Imu:
    """
    Minimal MPU-6050 reader.

    This class opens the I2C bus, wakes the MPU-6050 from sleep and exposes
    methods for reading WHO_AM_I, acceleration, gyro and tilt status.
    """

    def __init__(self, config: ImuConfig | None = None) -> None:
        if smbus2 is None:
            raise RuntimeError("smbus2 is not installed. Run: pip install smbus2")

        self.config = config or ImuConfig()
        self.address = self.config.address
        self.bus_num = self.config.bus_num
        self.bus = smbus2.SMBus(self.bus_num)

        self.bus.write_byte_data(self.address, REG_PWR_MGMT_1, 0x00)
        time.sleep(0.05)

    def close(self) -> None:
        """
        Close the I2C bus.
        """

        try:
            self.bus.close()
        except Exception:
            pass

    def __enter__(self) -> "Imu":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def _read_signed_word(self, register: int) -> int:
        """
        Read a signed 16-bit big-endian word from the IMU.
        """

        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) | low

        if value >= 0x8000:
            value -= 65536

        return value

    def who_am_i(self) -> int:
        """
        Read the WHO_AM_I register.
        """

        return self.bus.read_byte_data(self.address, REG_WHO_AM_I)

    def read_accel_gyro(self) -> dict[str, float]:
        """
        Read acceleration and gyroscope values.

        Returns:
            Dictionary with ax, ay, az in g and gx, gy, gz in deg/s.
        """

        return {
            "ax": self._read_signed_word(REG_ACCEL_XOUT_H) / ACCEL_SCALE,
            "ay": self._read_signed_word(REG_ACCEL_XOUT_H + 2) / ACCEL_SCALE,
            "az": self._read_signed_word(REG_ACCEL_XOUT_H + 4) / ACCEL_SCALE,
            "gx": self._read_signed_word(REG_GYRO_XOUT_H) / GYRO_SCALE,
            "gy": self._read_signed_word(REG_GYRO_XOUT_H + 2) / GYRO_SCALE,
            "gz": self._read_signed_word(REG_GYRO_XOUT_H + 4) / GYRO_SCALE,
        }

    def read(self) -> ImuReading:
        """
        Read full IMU state and classify stability.
        """

        values = self.read_accel_gyro()

        ax = values["ax"]
        ay = values["ay"]
        az = values["az"]
        gx = values["gx"]
        gy = values["gy"]
        gz = values["gz"]

        roll, pitch = calculate_roll_pitch(ax, ay, az)
        status, stable, message, tilt = classify_tilt(
            roll_degrees=roll,
            pitch_degrees=pitch,
            config=self.config,
        )

        return ImuReading(
            ax=ax,
            ay=ay,
            az=az,
            gx=gx,
            gy=gy,
            gz=gz,
            roll_degrees=roll,
            pitch_degrees=pitch,
            tilt_degrees=tilt,
            stable=stable,
            status=status,
            message=message,
            timestamp=time.time(),
        )

    def self_check(self) -> ImuSelfCheckResult:
        """
        Run a minimal IMU self-check.

        The check verifies:
        - I2C device responds
        - WHO_AM_I can be read
        - one accel/gyro sample can be read
        """

        try:
            who = self.who_am_i()
        except Exception as exc:
            return ImuSelfCheckResult(
                status="FAILED",
                who_am_i=None,
                reading=None,
                message=f"Could not read WHO_AM_I: {type(exc).__name__}: {exc}",
                timestamp=time.time(),
            )

        try:
            reading = self.read()
        except Exception as exc:
            return ImuSelfCheckResult(
                status="FAILED",
                who_am_i=who,
                reading=None,
                message=f"Could not read IMU sample: {type(exc).__name__}: {exc}",
                timestamp=time.time(),
            )

        if who not in self.config.expected_who_am_i:
            return ImuSelfCheckResult(
                status="WARNING",
                who_am_i=who,
                reading=reading,
                message=(
                    f"IMU responded, but WHO_AM_I=0x{who:02x} is not in expected "
                    f"values {tuple(hex(v) for v in self.config.expected_who_am_i)}."
                ),
                timestamp=time.time(),
            )

        return ImuSelfCheckResult(
            status="OK",
            who_am_i=who,
            reading=reading,
            message="IMU self-check completed successfully.",
            timestamp=time.time(),
        )


def reading_to_dict(reading: ImuReading) -> dict[str, float | bool | str]:
    """
    Convert ImuReading to a dictionary for JSON logs.
    """

    return {
        "ax": reading.ax,
        "ay": reading.ay,
        "az": reading.az,
        "gx": reading.gx,
        "gy": reading.gy,
        "gz": reading.gz,
        "roll_degrees": reading.roll_degrees,
        "pitch_degrees": reading.pitch_degrees,
        "tilt_degrees": reading.tilt_degrees,
        "stable": reading.stable,
        "status": reading.status,
        "message": reading.message,
        "timestamp": reading.timestamp,
    }


def self_check_to_dict(
    result: ImuSelfCheckResult,
) -> dict[str, str | int | float | bool | None | dict]:
    """
    Convert ImuSelfCheckResult to a dictionary for JSON logs.
    """

    return {
        "status": result.status,
        "who_am_i": result.who_am_i,
        "reading": reading_to_dict(result.reading) if result.reading else None,
        "message": result.message,
        "timestamp": result.timestamp,
    }


def imu_self_check(config: ImuConfig | None = None) -> dict[str, str | int | float | bool | None | dict]:
    """
    Run IMU self-check and return dictionary result.
    """

    try:
        with Imu(config) as imu:
            return self_check_to_dict(imu.self_check())
    except Exception as exc:
        return {
            "status": "FAILED",
            "who_am_i": None,
            "reading": None,
            "message": f"IMU unavailable: {type(exc).__name__}: {exc}",
            "timestamp": time.time(),
        }


def format_reading(reading: ImuReading) -> str:
    """
    Format one IMU reading for terminal output.
    """

    return (
        f"acc=({reading.ax:+.2f},{reading.ay:+.2f},{reading.az:+.2f})g  "
        f"gyro=({reading.gx:+.1f},{reading.gy:+.1f},{reading.gz:+.1f})deg/s  "
        f"roll={reading.roll_degrees:+.1f}deg  "
        f"pitch={reading.pitch_degrees:+.1f}deg  "
        f"tilt={reading.tilt_degrees:.1f}deg  "
        f"status={reading.status}"
    )


def print_imu_self_check(config: ImuConfig | None = None) -> ImuSelfCheckResult:
    """
    Print IMU self-check and return the result object.
    """

    try:
        with Imu(config) as imu:
            result = imu.self_check()
    except Exception as exc:
        result = ImuSelfCheckResult(
            status="FAILED",
            who_am_i=None,
            reading=None,
            message=f"IMU unavailable: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )

    print("IMU self-check")
    print("==============")
    print(f"Status: {result.status}")
    print(
        "WHO_AM_I: "
        + ("unavailable" if result.who_am_i is None else f"0x{result.who_am_i:02x}")
    )
    print(f"Message: {result.message}")

    if result.reading:
        print(format_reading(result.reading))

    return result


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI argument parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 MPU-6050 IMU test helper."
    )

    parser.add_argument(
        "--address",
        type=lambda value: int(value, 0),
        default=DEFAULT_IMU_I2C_ADDR,
        help="IMU I2C address, for example 0x68.",
    )

    parser.add_argument(
        "--bus",
        type=int,
        default=DEFAULT_I2C_BUS,
        help="I2C bus number.",
    )

    parser.add_argument(
        "--samples",
        type=int,
        default=6,
        help="Number of samples to print.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay between samples in seconds.",
    )

    parser.add_argument(
        "--tilt-warning",
        type=float,
        default=20.0,
        help="Tilt warning threshold in degrees.",
    )

    parser.add_argument(
        "--tilt-critical",
        type=float,
        default=30.0,
        help="Tilt critical threshold in degrees.",
    )

    return parser


def main() -> int:
    """
    CLI entry point.

    Run from repository root:

        python setup/microbot/imu.py

    On Raspberry Pi, make sure I2C is enabled and smbus2 is installed.
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    config = ImuConfig(
        address=args.address,
        bus_num=args.bus,
        tilt_warning_degrees=args.tilt_warning,
        tilt_critical_degrees=args.tilt_critical,
    )

    print("MicroBot Round V0 IMU test")
    print("==========================")

    try:
        with Imu(config) as imu:
            who = imu.who_am_i()
            print(
                f"WHO_AM_I=0x{who:02x} "
                "(MPU-6050 family often reports 0x68/0x70/0x71/0x98)"
            )
            print("Samples: tilt the robot to watch values change.")
            print()

            for _ in range(max(1, args.samples)):
                reading = imu.read()
                print(format_reading(reading))
                time.sleep(max(0.0, args.delay))

    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}")
        return 1

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())