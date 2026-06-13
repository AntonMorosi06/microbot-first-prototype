"""
MicroBot Round V0 servo module.

This module provides a minimal, safety-aware driver for Feetech SCS0009 / SC09
serial bus servos.

Reference hardware pattern:

- Raspberry Pi Zero 2 W
- /dev/serial0
- 1 Mbps UART
- half-duplex DATA bus
- GPIO14 TX through 1 kOhm resistor to DATA
- GPIO15 RX directly from DATA
- two leg servos with IDs 1 and 2

Important SCS0009 rule:
Two-byte values are BIG-ENDIAN for reads and writes.

This module is intentionally conservative. It provides:

- read-only servo scan
- ping
- present position read
- torque enable / disable
- clamped movement
- sync movement
- safe nudge around current position
- torque release on exit

Movement scripts should still call safety.py before sending movement commands.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import argparse
import time
import json


try:
    import serial
except ImportError:  # pragma: no cover
    serial = None


try:
    from . import pins
except ImportError:
    pins = None


SERVO_PORT = getattr(pins, "SERVO_PORT", "/dev/serial0")
SERVO_BAUD = getattr(pins, "SERVO_BAUD", 1_000_000)
SERVO_TIMEOUT_SECONDS = getattr(pins, "SERVO_TIMEOUT_SECONDS", 0.05)

SERVO_IDS = getattr(pins, "SERVO_IDS", (1, 2))

ENCODER_MIN = getattr(pins, "ENCODER_MIN", 255)
ENCODER_MAX = getattr(pins, "ENCODER_MAX", 1023)
ENCODER_CENTER = getattr(pins, "ENCODER_CENTER", 512)

SAFE_NUDGE = getattr(pins, "SAFE_NUDGE", 30)
SAFE_NUDGE_STEP = getattr(pins, "SAFE_NUDGE_STEP", 5)
SAFE_NUDGE_DWELL_SECONDS = getattr(pins, "SAFE_NUDGE_DWELL_SECONDS", 0.02)
SERVO_SETTLE_SECONDS = getattr(pins, "SERVO_SETTLE_SECONDS", 0.20)

REG_ID = getattr(pins, "REG_ID", 0x03)
REG_TORQUE_ENABLE = getattr(pins, "REG_TORQUE_ENABLE", 0x28)
REG_GOAL_POS = getattr(pins, "REG_GOAL_POS", 0x2A)
REG_EEPROM_LOCK = getattr(pins, "REG_EEPROM_LOCK", 0x30)
REG_PRESENT_POS = getattr(pins, "REG_PRESENT_POS", 0x38)

INST_PING = getattr(pins, "INST_PING", 0x01)
INST_READ = getattr(pins, "INST_READ", 0x02)
INST_WRITE = getattr(pins, "INST_WRITE", 0x03)
INST_SYNC_WRITE = getattr(pins, "INST_SYNC_WRITE", 0x83)
BROADCAST_ID = getattr(pins, "BROADCAST_ID", 0xFE)

TORQUE_OFF = getattr(pins, "TORQUE_OFF", 0)
TORQUE_ON = getattr(pins, "TORQUE_ON", 1)


@dataclass(frozen=True)
class ServoConfig:
    """
    Servo bus configuration.
    """

    port: str = SERVO_PORT
    baud: int = SERVO_BAUD
    timeout: float = SERVO_TIMEOUT_SECONDS
    encoder_min: int = ENCODER_MIN
    encoder_max: int = ENCODER_MAX
    safe_nudge: int = SAFE_NUDGE
    safe_nudge_step: int = SAFE_NUDGE_STEP
    safe_nudge_dwell: float = SAFE_NUDGE_DWELL_SECONDS
    settle_seconds: float = SERVO_SETTLE_SECONDS


@dataclass(frozen=True)
class ServoStatus:
    """
    One servo status record.
    """

    servo_id: int
    present: bool
    position: int | None
    message: str
    timestamp: float


@dataclass(frozen=True)
class ServoScanResult:
    """
    Servo scan result.
    """

    status: str
    port: str
    baud: int
    requested_ids: tuple[int, ...]
    found_ids: tuple[int, ...]
    servos: tuple[ServoStatus, ...]
    message: str
    timestamp: float


@dataclass(frozen=True)
class ServoMoveResult:
    """
    Result returned by movement helpers.
    """

    status: str
    servo_id: int | None
    start_position: int | None
    target_position: int | None
    final_position: int | None
    message: str
    timestamp: float


def clamp_encoder(
    position: int,
    encoder_min: int = ENCODER_MIN,
    encoder_max: int = ENCODER_MAX,
) -> int:
    """
    Clamp a servo encoder position to the configured safe range.
    """

    return max(encoder_min, min(encoder_max, int(position)))


def checksum(servo_id: int, length: int, instruction: int, params: list[int]) -> int:
    """
    Compute SCS0009 packet checksum.
    """

    return (~(servo_id + length + instruction + sum(params))) & 0xFF


def build_packet(servo_id: int, instruction: int, params: list[int]) -> bytes:
    """
    Build an SCS0009 packet.

    Packet format:

        FF FF <id> <length> <instruction> <params...> <checksum>
    """

    length = len(params) + 2
    return bytes(
        [0xFF, 0xFF, servo_id, length, instruction]
        + list(params)
        + [checksum(servo_id, length, instruction, params)]
    )


def validate_response_packet(packet: bytes, expected_id: int | None = None) -> bool:
    """
    Return True if a packet appears well-formed and checksum-valid.
    """

    if len(packet) < 6:
        return False

    if packet[0] != 0xFF or packet[1] != 0xFF:
        return False

    servo_id = packet[2]

    if expected_id is not None and servo_id != expected_id:
        return False

    length = packet[3]
    expected_total_length = length + 4

    if len(packet) != expected_total_length:
        return False

    body = packet[2:]
    expected_checksum = (~sum(body[:-1])) & 0xFF

    return body[-1] == expected_checksum


def find_response(buffer: bytes, servo_id: int) -> bytes | None:
    """
    Find a checksum-valid response packet inside a serial buffer.

    The half-duplex bus may echo the transmitted packet before the servo reply.
    This function scans for a valid response frame instead of trusting fixed byte
    offsets.
    """

    index = 0

    while index < len(buffer) - 5:
        if (
            buffer[index] == 0xFF
            and buffer[index + 1] == 0xFF
            and buffer[index + 2] == servo_id
        ):
            length = buffer[index + 3]
            end = index + 4 + length

            if end <= len(buffer):
                candidate = buffer[index:end]

                if validate_response_packet(candidate, expected_id=servo_id):
                    return candidate

        index += 1

    return None


class ServoBus:
    """
    Thin interface to the SCS0009 / SC09 servo bus.
    """

    def __init__(
        self,
        port: str = SERVO_PORT,
        baud: int = SERVO_BAUD,
        timeout: float = SERVO_TIMEOUT_SECONDS,
        config: ServoConfig | None = None,
    ) -> None:
        if serial is None:
            raise RuntimeError("pyserial is not installed. Run: pip install pyserial")

        self.config = config or ServoConfig(port=port, baud=baud, timeout=timeout)
        self.port = port
        self.baud = baud
        self.timeout = timeout

        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baud,
            timeout=self.timeout,
        )

    def close(self) -> None:
        """
        Close the serial port.
        """

        try:
            self.serial.close()
        except Exception:
            pass

    def __enter__(self) -> "ServoBus":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def txrx(
        self,
        servo_id: int,
        instruction: int,
        params: list[int],
        read_extra: int = 16,
    ) -> bytes | None:
        """
        Send one packet and return a checksum-valid response if present.
        """

        packet = build_packet(servo_id, instruction, params)

        self.serial.reset_input_buffer()
        self.serial.write(packet)
        self.serial.flush()

        time.sleep(0.004)

        buffer = self.serial.read(len(packet) + read_extra)

        echo_index = buffer.find(packet)
        if echo_index >= 0:
            search_buffer = buffer[echo_index + len(packet) :]
        else:
            search_buffer = buffer

        return find_response(search_buffer, servo_id)

    def ping(self, servo_id: int) -> bool:
        """
        Return True if a servo responds to ping.
        """

        return self.txrx(servo_id, INST_PING, [], read_extra=8) is not None

    def read_bytes(self, servo_id: int, register: int, size: int) -> list[int] | None:
        """
        Read raw bytes from a servo register.
        """

        response = self.txrx(
            servo_id,
            INST_READ,
            [register, size],
            read_extra=size + 8,
        )

        if response is None:
            return None

        if len(response) < 5 + size:
            return None

        return list(response[5 : 5 + size])

    def read_byte(self, servo_id: int, register: int) -> int | None:
        """
        Read one byte from a servo register.
        """

        data = self.read_bytes(servo_id, register, 1)

        if not data:
            return None

        return data[0]

    def read_word(self, servo_id: int, register: int) -> int | None:
        """
        Read a two-byte BIG-ENDIAN word from a servo register.
        """

        data = self.read_bytes(servo_id, register, 2)

        if not data or len(data) != 2:
            return None

        return (data[0] << 8) | data[1]

    def write_bytes(self, servo_id: int, register: int, data: list[int]) -> None:
        """
        Write raw bytes to a servo register.
        """

        self.txrx(
            servo_id,
            INST_WRITE,
            [register] + list(data),
            read_extra=8,
        )

    def write_byte(self, servo_id: int, register: int, value: int) -> None:
        """
        Write one byte to a servo register.
        """

        self.write_bytes(servo_id, register, [int(value) & 0xFF])

    def write_word(self, servo_id: int, register: int, value: int) -> None:
        """
        Write a two-byte BIG-ENDIAN word to a servo register.
        """

        value = int(value) & 0xFFFF
        high = (value >> 8) & 0xFF
        low = value & 0xFF

        self.write_bytes(servo_id, register, [high, low])

    def present_position(self, servo_id: int) -> int | None:
        """
        Read the current servo encoder position.
        """

        return self.read_word(servo_id, REG_PRESENT_POS)

    def set_torque(self, servo_id: int, enabled: bool) -> None:
        """
        Enable or disable servo torque.
        """

        self.write_byte(servo_id, REG_TORQUE_ENABLE, TORQUE_ON if enabled else TORQUE_OFF)

    def release_torque(self, servo_ids: tuple[int, ...] | list[int] | None = None) -> None:
        """
        Release torque for multiple servos.

        This is best-effort and should be called in finally blocks.
        """

        ids = tuple(servo_ids) if servo_ids is not None else tuple(SERVO_IDS)

        for servo_id in ids:
            try:
                self.set_torque(servo_id, False)
            except Exception:
                pass

    def move(self, servo_id: int, position: int) -> int:
        """
        Command one servo to a clamped encoder position.

        Returns the clamped target actually sent.
        """

        target = clamp_encoder(
            position,
            self.config.encoder_min,
            self.config.encoder_max,
        )

        self.write_word(servo_id, REG_GOAL_POS, target)

        return target

    def move_sync(self, targets: dict[int, int]) -> None:
        """
        Command multiple servos using sync-write.

        This sends one broadcast packet so the servos start moving together.
        """

        params: list[int] = [REG_GOAL_POS, 2]

        for servo_id, position in targets.items():
            target = clamp_encoder(
                position,
                self.config.encoder_min,
                self.config.encoder_max,
            )
            params += [int(servo_id), (target >> 8) & 0xFF, target & 0xFF]

        length = len(params) + 2
        packet_checksum = (~(BROADCAST_ID + length + INST_SYNC_WRITE + sum(params))) & 0xFF

        packet = bytes(
            [0xFF, 0xFF, BROADCAST_ID, length, INST_SYNC_WRITE]
            + params
            + [packet_checksum]
        )

        self.serial.write(packet)
        self.serial.flush()
        self.serial.reset_input_buffer()

    def scan(self, servo_ids: tuple[int, ...] | list[int]) -> ServoScanResult:
        """
        Read-only scan for servos.

        This sends ping/read commands only. It does not command motion.
        """

        statuses: list[ServoStatus] = []
        found_ids: list[int] = []

        for servo_id in servo_ids:
            try:
                present = self.ping(int(servo_id))
                position = self.present_position(int(servo_id)) if present else None

                if present:
                    found_ids.append(int(servo_id))
                    message = "Servo responded."
                else:
                    message = "No response."

                statuses.append(
                    ServoStatus(
                        servo_id=int(servo_id),
                        present=present,
                        position=position,
                        message=message,
                        timestamp=time.time(),
                    )
                )
            except Exception as exc:
                statuses.append(
                    ServoStatus(
                        servo_id=int(servo_id),
                        present=False,
                        position=None,
                        message=f"Servo scan error: {type(exc).__name__}: {exc}",
                        timestamp=time.time(),
                    )
                )

        if found_ids:
            status = "OK"
            message = f"Found {len(found_ids)} servo(s): {found_ids}"
        else:
            status = "FAILED"
            message = "No servos found."

        return ServoScanResult(
            status=status,
            port=self.port,
            baud=self.baud,
            requested_ids=tuple(int(item) for item in servo_ids),
            found_ids=tuple(found_ids),
            servos=tuple(statuses),
            message=message,
            timestamp=time.time(),
        )

    def safe_nudge(
        self,
        servo_id: int,
        delta: int = SAFE_NUDGE,
        step: int = SAFE_NUDGE_STEP,
        dwell: float = SAFE_NUDGE_DWELL_SECONDS,
        release_after: bool = True,
    ) -> ServoMoveResult:
        """
        Move one servo a small amount around its current position.

        Flow:
        - read current position
        - clamp target
        - enable torque
        - move gradually to target
        - return gradually to start
        - optionally release torque

        This is the first safe movement test after read-only scan.
        """

        start = self.present_position(servo_id)

        if start is None:
            return ServoMoveResult(
                status="FAILED",
                servo_id=servo_id,
                start_position=None,
                target_position=None,
                final_position=None,
                message="Could not read servo position before nudge.",
                timestamp=time.time(),
            )

        safe_delta = max(-abs(self.config.safe_nudge), min(abs(self.config.safe_nudge), int(delta)))
        target = clamp_encoder(
            start + safe_delta,
            self.config.encoder_min,
            self.config.encoder_max,
        )

        try:
            self.set_torque(servo_id, True)

            direction = 1 if target >= start else -1
            step_size = max(1, abs(int(step))) * direction

            position = start

            while abs(target - position) > abs(step_size):
                position += step_size
                self.move(servo_id, position)
                time.sleep(max(0.0, dwell))

            self.move(servo_id, target)
            time.sleep(self.config.settle_seconds)

            return_direction = -direction
            return_step_size = abs(int(step)) * return_direction

            position = target

            while abs(start - position) > abs(return_step_size):
                position += return_step_size
                self.move(servo_id, position)
                time.sleep(max(0.0, dwell))

            self.move(servo_id, start)
            time.sleep(self.config.settle_seconds)

            final_position = self.present_position(servo_id)

            return ServoMoveResult(
                status="OK",
                servo_id=servo_id,
                start_position=start,
                target_position=target,
                final_position=final_position,
                message="Safe nudge completed and servo returned near start position.",
                timestamp=time.time(),
            )

        except Exception as exc:
            return ServoMoveResult(
                status="FAILED",
                servo_id=servo_id,
                start_position=start,
                target_position=target,
                final_position=None,
                message=f"Safe nudge failed: {type(exc).__name__}: {exc}",
                timestamp=time.time(),
            )

        finally:
            if release_after:
                try:
                    self.set_torque(servo_id, False)
                except Exception:
                    pass


def scan_servos(
    servo_ids: tuple[int, ...] | list[int] | None = None,
    config: ServoConfig | None = None,
) -> ServoScanResult:
    """
    Convenience function for read-only servo scan.
    """

    cfg = config or ServoConfig()
    ids = tuple(servo_ids) if servo_ids is not None else tuple(SERVO_IDS)

    try:
        with ServoBus(
            port=cfg.port,
            baud=cfg.baud,
            timeout=cfg.timeout,
            config=cfg,
        ) as bus:
            return bus.scan(ids)
    except Exception as exc:
        return ServoScanResult(
            status="FAILED",
            port=cfg.port,
            baud=cfg.baud,
            requested_ids=ids,
            found_ids=(),
            servos=(),
            message=f"Could not open servo bus: {type(exc).__name__}: {exc}",
            timestamp=time.time(),
        )


def safe_nudge_all(
    servo_ids: tuple[int, ...] | list[int] | None = None,
    delta: int = SAFE_NUDGE,
    config: ServoConfig | None = None,
) -> list[ServoMoveResult]:
    """
    Safely nudge all detected/requested servos.

    This function should only be used after the safety layer has allowed movement.
    """

    cfg = config or ServoConfig()
    ids = tuple(servo_ids) if servo_ids is not None else tuple(SERVO_IDS)
    results: list[ServoMoveResult] = []

    try:
        with ServoBus(
            port=cfg.port,
            baud=cfg.baud,
            timeout=cfg.timeout,
            config=cfg,
        ) as bus:
            try:
                for servo_id in ids:
                    if not bus.ping(servo_id):
                        results.append(
                            ServoMoveResult(
                                status="FAILED",
                                servo_id=servo_id,
                                start_position=None,
                                target_position=None,
                                final_position=None,
                                message="Servo did not respond to ping. Nudge skipped.",
                                timestamp=time.time(),
                            )
                        )
                        continue

                    results.append(bus.safe_nudge(servo_id, delta=delta, release_after=False))

            except KeyboardInterrupt:
                results.append(
                    ServoMoveResult(
                        status="FAILED",
                        servo_id=None,
                        start_position=None,
                        target_position=None,
                        final_position=None,
                        message="Safe nudge interrupted by user.",
                        timestamp=time.time(),
                    )
                )

            finally:
                bus.release_torque(ids)

    except Exception as exc:
        results.append(
            ServoMoveResult(
                status="FAILED",
                servo_id=None,
                start_position=None,
                target_position=None,
                final_position=None,
                message=f"Could not open servo bus: {type(exc).__name__}: {exc}",
                timestamp=time.time(),
            )
        )

    return results


def scan_result_to_dict(result: ServoScanResult) -> dict[str, Any]:
    """
    Convert ServoScanResult to a dictionary for JSON logs.
    """

    return asdict(result)


def move_result_to_dict(result: ServoMoveResult) -> dict[str, Any]:
    """
    Convert ServoMoveResult to a dictionary for JSON logs.
    """

    return asdict(result)


def servo_self_check(
    servo_ids: tuple[int, ...] | list[int] | None = None,
    config: ServoConfig | None = None,
) -> dict[str, Any]:
    """
    Run read-only servo self-check.

    This is safe: no movement is commanded.
    """

    result = scan_servos(servo_ids=servo_ids, config=config)

    return {
        "status": result.status,
        "port": result.port,
        "baud": result.baud,
        "requested_ids": result.requested_ids,
        "found_ids": result.found_ids,
        "servos": [asdict(item) for item in result.servos],
        "message": result.message,
        "timestamp": result.timestamp,
    }


def format_scan_result(result: ServoScanResult) -> str:
    """
    Format servo scan result for terminal output.
    """

    lines: list[str] = []

    lines.append("Servo scan")
    lines.append("==========")
    lines.append(f"Status: {result.status}")
    lines.append(f"Port: {result.port}")
    lines.append(f"Baud: {result.baud}")
    lines.append(f"Requested IDs: {result.requested_ids}")
    lines.append(f"Found IDs: {result.found_ids}")
    lines.append(f"Message: {result.message}")
    lines.append("")

    if not result.servos:
        lines.append("No servo status records.")
        return "\n".join(lines)

    for servo_status in result.servos:
        lines.append(
            f"ID {servo_status.servo_id}: "
            f"present={servo_status.present} "
            f"position={servo_status.position} "
            f"message={servo_status.message}"
        )

    return "\n".join(lines)


def format_move_results(results: list[ServoMoveResult]) -> str:
    """
    Format movement result list for terminal output.
    """

    lines: list[str] = []

    lines.append("Servo movement results")
    lines.append("======================")

    if not results:
        lines.append("No movement results.")
        return "\n".join(lines)

    for result in results:
        lines.append(
            f"ID {result.servo_id}: "
            f"status={result.status} "
            f"start={result.start_position} "
            f"target={result.target_position} "
            f"final={result.final_position} "
            f"message={result.message}"
        )

    return "\n".join(lines)


def parse_ids(ids_text: str) -> tuple[int, ...]:
    """
    Parse comma-separated servo IDs.
    """

    values: list[int] = []

    for item in ids_text.split(","):
        clean = item.strip()

        if clean:
            values.append(int(clean))

    return tuple(values)


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.
    """

    parser = argparse.ArgumentParser(
        description="MicroBot Round V0 SCS0009 / SC09 servo helper."
    )

    parser.add_argument(
        "--port",
        default=SERVO_PORT,
        help="Servo serial port.",
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=SERVO_BAUD,
        help="Servo serial baud rate.",
    )

    parser.add_argument(
        "--ids",
        default=",".join(str(item) for item in (*SERVO_IDS, 3, 4, 5, 6)),
        help="Comma-separated servo IDs to scan or test.",
    )

    parser.add_argument(
        "--scan",
        action="store_true",
        help="Run read-only servo scan.",
    )

    parser.add_argument(
        "--safe-nudge",
        action="store_true",
        help="Run safe nudge on detected/requested servos. Use only after power validation.",
    )

    parser.add_argument(
        "--delta",
        type=int,
        default=SAFE_NUDGE,
        help="Nudge delta in encoder units.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output.",
    )

    return parser


def main() -> int:
    """
    CLI entry point.

    Safe read-only scan:

        python setup/microbot/servos.py --scan

    Safe nudge after validation:

        python setup/microbot/servos.py --safe-nudge --ids 1,2

    On Raspberry Pi Zero 2 W, the servo bus should normally be /dev/serial0.
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    ids = parse_ids(args.ids)

    config = ServoConfig(
        port=args.port,
        baud=args.baud,
    )

    if args.safe_nudge:
        results = safe_nudge_all(
            servo_ids=ids,
            delta=args.delta,
            config=config,
        )

        if args.json:
            print(json.dumps([move_result_to_dict(item) for item in results], indent=2, default=str))
        else:
            print(format_move_results(results))

        return 0 if all(item.status == "OK" for item in results) else 1

    result = scan_servos(
        servo_ids=ids,
        config=config,
    )

    if args.json:
        print(json.dumps(scan_result_to_dict(result), indent=2, default=str))
    else:
        print(format_scan_result(result))

    return 0 if result.status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())