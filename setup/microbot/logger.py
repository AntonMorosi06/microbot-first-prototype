"""
MicroBot Round V0 logger module.

This module provides lightweight session logging for the first MicroBot Round V0
hardware bring-up.

The logger is designed for:

- self-check reports
- hardware test evidence
- camera/IMU/audio/servo test sessions
- demo runs
- safety events
- portfolio-ready evidence files

It does not require external dependencies.

Runtime outputs:

- logs/<session_id>.jsonl
- evidence/reports/<session_id>_report.md

The logger should never control hardware directly. It only records what happened.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json
import time
import traceback


try:
    from .config import get_config, make_session_id
except ImportError:
    get_config = None

    def make_session_id(prefix: str = "microbot_session") -> str:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        return f"{prefix}_{timestamp}"


EVENT_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


@dataclass(frozen=True)
class LogEvent:
    """
    One structured MicroBot log event.
    """

    timestamp: float
    level: str
    event_type: str
    subsystem: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SessionPaths:
    """
    Runtime paths for one MicroBot session.
    """

    session_id: str
    logs_dir: Path
    reports_dir: Path

    @property
    def jsonl_path(self) -> Path:
        return self.logs_dir / f"{self.session_id}.jsonl"

    @property
    def json_path(self) -> Path:
        return self.logs_dir / f"{self.session_id}.json"

    @property
    def markdown_report_path(self) -> Path:
        return self.reports_dir / f"{self.session_id}_report.md"


def now_iso() -> str:
    """
    Return local timestamp in readable ISO-like format.
    """

    return time.strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(path: str | Path) -> Path:
    """
    Create a directory if needed and return it as a Path.
    """

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def default_session_paths(session_id: str | None = None) -> SessionPaths:
    """
    Build default session paths.

    If config.py is available, use the configured project paths.
    Otherwise, use repository-style fallback paths from the current directory.
    """

    sid = session_id or make_session_id()

    if get_config is not None:
        try:
            config = get_config()
            logs_dir = config.paths.logs_dir
            reports_dir = config.paths.reports_dir
            ensure_directory(logs_dir)
            ensure_directory(reports_dir)
            return SessionPaths(
                session_id=sid,
                logs_dir=logs_dir,
                reports_dir=reports_dir,
            )
        except Exception:
            pass

    logs_dir = ensure_directory("logs")
    reports_dir = ensure_directory("evidence/reports")

    return SessionPaths(
        session_id=sid,
        logs_dir=logs_dir,
        reports_dir=reports_dir,
    )


def event_to_dict(event: LogEvent) -> dict[str, Any]:
    """
    Convert LogEvent to a JSON-compatible dictionary.
    """

    data = asdict(event)
    data["timestamp_readable"] = time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime(event.timestamp),
    )
    return data


def safe_json_dumps(value: Any) -> str:
    """
    Serialize a value to JSON safely.
    """

    try:
        return json.dumps(value, indent=2, sort_keys=True, default=str)
    except TypeError:
        return json.dumps(str(value), indent=2)


class MicroBotLogger:
    """
    Session logger for MicroBot Round V0.

    Example:

        logger = MicroBotLogger()
        logger.info("system", "Boot started")
        logger.log_event("INFO", "self_check", "imu", "IMU OK", {"who_am_i": "0x68"})
        logger.close()

    Or as a context manager:

        with MicroBotLogger() as logger:
            logger.info("system", "Demo started")
    """

    def __init__(
        self,
        session_id: str | None = None,
        session_name: str = "MicroBot Round V0 Session",
        write_jsonl: bool = True,
        print_to_terminal: bool = True,
    ) -> None:
        self.paths = default_session_paths(session_id=session_id)
        self.session_id = self.paths.session_id
        self.session_name = session_name
        self.write_jsonl = write_jsonl
        self.print_to_terminal = print_to_terminal
        self.events: list[LogEvent] = []
        self.started_at = time.time()
        self.closed = False

        ensure_directory(self.paths.logs_dir)
        ensure_directory(self.paths.reports_dir)

        self.info(
            subsystem="logger",
            message="MicroBot logging session started.",
            data={
                "session_id": self.session_id,
                "session_name": self.session_name,
                "jsonl_path": str(self.paths.jsonl_path),
                "report_path": str(self.paths.markdown_report_path),
            },
        )

    def __enter__(self) -> "MicroBotLogger":
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if exc_type is not None:
            self.exception(
                subsystem="logger",
                message="Unhandled exception captured by logger context manager.",
                exc=exc_value,
            )

        self.close()

    def _normalize_level(self, level: str) -> str:
        """
        Normalize log level.
        """

        normalized = level.strip().upper()

        if normalized not in EVENT_LEVELS:
            return "INFO"

        return normalized

    def _write_jsonl_event(self, event: LogEvent) -> None:
        """
        Append one event to the JSONL log file.
        """

        if not self.write_jsonl:
            return

        payload = event_to_dict(event)

        try:
            with self.paths.jsonl_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(payload, sort_keys=True, default=str) + "\n")
        except OSError as exc:
            if self.print_to_terminal:
                print(f"[LOGGER ERROR] Could not write JSONL log: {exc}")

    def _print_event(self, event: LogEvent) -> None:
        """
        Print one event to terminal.
        """

        if not self.print_to_terminal:
            return

        readable_time = time.strftime("%H:%M:%S", time.localtime(event.timestamp))
        print(
            f"[{readable_time}] "
            f"{event.level:<8} "
            f"{event.subsystem:<14} "
            f"{event.event_type:<14} "
            f"{event.message}"
        )

    def log_event(
        self,
        level: str,
        event_type: str,
        subsystem: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        """
        Record one structured event.
        """

        event = LogEvent(
            timestamp=time.time(),
            level=self._normalize_level(level),
            event_type=event_type.strip() or "event",
            subsystem=subsystem.strip() or "system",
            message=message.strip(),
            data=data or {},
        )

        self.events.append(event)
        self._write_jsonl_event(event)
        self._print_event(event)

        return event

    def debug(
        self,
        subsystem: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        return self.log_event("DEBUG", "debug", subsystem, message, data)

    def info(
        self,
        subsystem: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        return self.log_event("INFO", "info", subsystem, message, data)

    def warning(
        self,
        subsystem: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        return self.log_event("WARNING", "warning", subsystem, message, data)

    def error(
        self,
        subsystem: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        return self.log_event("ERROR", "error", subsystem, message, data)

    def critical(
        self,
        subsystem: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        return self.log_event("CRITICAL", "critical", subsystem, message, data)

    def exception(
        self,
        subsystem: str,
        message: str,
        exc: BaseException | None = None,
        data: dict[str, Any] | None = None,
    ) -> LogEvent:
        """
        Log an exception with traceback text.
        """

        payload = dict(data or {})

        if exc is not None:
            payload["exception_type"] = type(exc).__name__
            payload["exception_message"] = str(exc)

        payload["traceback"] = traceback.format_exc()

        return self.log_event(
            level="ERROR",
            event_type="exception",
            subsystem=subsystem,
            message=message,
            data=payload,
        )

    def log_subsystem_result(
        self,
        subsystem: str,
        result: Any,
        event_type: str = "self_check",
    ) -> LogEvent:
        """
        Log a subsystem result object or dictionary.

        This works with dataclasses, dictionaries and simple objects.
        """

        if hasattr(result, "__dataclass_fields__"):
            payload = asdict(result)
        elif isinstance(result, dict):
            payload = result
        else:
            payload = {"result": str(result)}

        status = str(payload.get("status", "UNKNOWN")).upper()
        message = str(payload.get("message", f"{subsystem} result recorded."))

        if status in {"OK", "PASSED"}:
            level = "INFO"
        elif status in {"WARNING", "UNAVAILABLE"}:
            level = "WARNING"
        elif status in {"FAILED", "ERROR", "CRITICAL"}:
            level = "ERROR"
        else:
            level = "INFO"

        return self.log_event(
            level=level,
            event_type=event_type,
            subsystem=subsystem,
            message=message,
            data=payload,
        )

    def save_json_snapshot(self) -> Path:
        """
        Save the full session as a JSON file.
        """

        payload = {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "started_at": self.started_at,
            "started_at_readable": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(self.started_at),
            ),
            "updated_at": time.time(),
            "updated_at_readable": now_iso(),
            "event_count": len(self.events),
            "events": [event_to_dict(event) for event in self.events],
        }

        with self.paths.json_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, sort_keys=True, default=str)

        return self.paths.json_path

    def build_markdown_report(self) -> str:
        """
        Build a Markdown report for the session.
        """

        ended_at = time.time()
        duration = ended_at - self.started_at

        lines: list[str] = []

        lines.append(f"# {self.session_name}")
        lines.append("")
        lines.append(f"Session ID: `{self.session_id}`")
        lines.append(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.started_at))}")
        lines.append(f"Generated: {now_iso()}")
        lines.append(f"Duration: {duration:.2f} seconds")
        lines.append(f"Event count: {len(self.events)}")
        lines.append("")
        lines.append("## Summary")
        lines.append("")

        counts = {level: 0 for level in EVENT_LEVELS}
        for event in self.events:
            counts[event.level] = counts.get(event.level, 0) + 1

        for level in EVENT_LEVELS:
            lines.append(f"- {level}: {counts.get(level, 0)}")

        lines.append("")
        lines.append("## Events")
        lines.append("")

        if not self.events:
            lines.append("No events recorded.")
            lines.append("")
            return "\n".join(lines)

        for index, event in enumerate(self.events, start=1):
            readable_time = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(event.timestamp),
            )

            lines.append(f"### {index}. {event.level} — {event.subsystem} — {event.event_type}")
            lines.append("")
            lines.append(f"Time: {readable_time}")
            lines.append("")
            lines.append(f"Message: {event.message}")
            lines.append("")

            if event.data:
                lines.append("Data:")
                lines.append("")
                lines.append("```json")
                lines.append(safe_json_dumps(event.data))
                lines.append("```")
                lines.append("")

        lines.append("## Notes")
        lines.append("")
        lines.append(
            "This report records software and hardware bring-up evidence for "
            "MicroBot Round V0. Hardware validation claims should only be made "
            "when the corresponding real test has been executed and documented."
        )
        lines.append("")

        return "\n".join(lines)

    def write_markdown_report(self) -> Path:
        """
        Write the Markdown report to evidence/reports.
        """

        report = self.build_markdown_report()

        with self.paths.markdown_report_path.open("w", encoding="utf-8") as file:
            file.write(report)

        return self.paths.markdown_report_path

    def close(self) -> None:
        """
        Close the session and write final outputs.

        Calling close multiple times is safe.
        """

        if self.closed:
            return

        self.info(
            subsystem="logger",
            message="MicroBot logging session completed.",
            data={
                "session_id": self.session_id,
                "event_count": len(self.events),
            },
        )

        json_path = self.save_json_snapshot()
        report_path = self.write_markdown_report()

        self.closed = True

        if self.print_to_terminal:
            print()
            print("Logger outputs")
            print("==============")
            print(f"JSONL:  {self.paths.jsonl_path}")
            print(f"JSON:   {json_path}")
            print(f"Report: {report_path}")


def create_logger(
    session_id: str | None = None,
    session_name: str = "MicroBot Round V0 Session",
    print_to_terminal: bool = True,
) -> MicroBotLogger:
    """
    Convenience factory for creating a MicroBotLogger.
    """

    return MicroBotLogger(
        session_id=session_id,
        session_name=session_name,
        print_to_terminal=print_to_terminal,
    )


def logger_self_check() -> dict[str, str | int | float]:
    """
    Run a small logger self-check.
    """

    logger = MicroBotLogger(
        session_name="MicroBot Logger Self-Check",
        print_to_terminal=False,
    )

    logger.info("logger", "Logger self-check event written.")
    logger.warning("logger", "Example warning event for logger validation.")
    logger.close()

    return {
        "status": "OK",
        "message": "Logger self-check completed.",
        "session_id": logger.session_id,
        "event_count": len(logger.events),
        "jsonl_path": str(logger.paths.jsonl_path),
        "json_path": str(logger.paths.json_path),
        "report_path": str(logger.paths.markdown_report_path),
        "timestamp": time.time(),
    }


def main() -> int:
    """
    CLI entry point.

    Run:

        python setup/microbot/logger.py
    """

    result = logger_self_check()

    print("Logger self-check")
    print("=================")
    for key, value in result.items():
        print(f"{key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())