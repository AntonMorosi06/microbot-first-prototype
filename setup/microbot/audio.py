"""
MicroBot Round V0 audio module.

This module provides safe, minimal audio helpers for the first hardware bring-up:

- text-to-speech using system tools such as espeak-ng or flite
- optional WAV playback through aplay
- optional microphone recording through arecord
- simple WAV RMS analysis for microphone testing

The module is intentionally based on Python standard library tools plus common
Raspberry Pi OS command-line utilities. It should not crash the robot if audio
tools are missing. Instead, it returns structured results that can be logged by
the caller.

Expected optional system packages on Raspberry Pi OS:

    sudo apt update
    sudo apt install -y espeak-ng flite alsa-utils

Audio is not safety-critical for MicroBot Round V0. If audio fails, the robot
should continue using terminal output and LED status.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import shutil
import struct
import subprocess
import wave


DEFAULT_STARTUP_PHRASE = "MicroBot Round V0 online. System check started."
DEFAULT_COMPLETE_PHRASE = "MicroBot Round V0. Autonomous safety demo completed."
DEFAULT_WARNING_PHRASE = "Warning. Safe mode active."


@dataclass(frozen=True)
class AudioResult:
    """
    Result object returned by audio operations.

    status:
        OK, WARNING, FAILED, or UNAVAILABLE.

    message:
        Human-readable explanation.

    command:
        Command executed, if any.

    path:
        File path produced or used, if any.
    """

    status: str
    message: str
    command: str | None = None
    path: str | None = None


def command_exists(command: str) -> bool:
    """
    Return True if a command-line tool is available on the system.
    """

    return shutil.which(command) is not None


def _run_command(command: list[str], timeout: float = 10.0) -> AudioResult:
    """
    Run a command safely and return an AudioResult.

    This function avoids raising exceptions to the caller during normal hardware
    bring-up. Failures are returned as structured status values.
    """

    command_text = " ".join(command)

    try:
        completed = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except FileNotFoundError:
        return AudioResult(
            status="UNAVAILABLE",
            message=f"Command not found: {command[0]}",
            command=command_text,
        )
    except subprocess.TimeoutExpired:
        return AudioResult(
            status="FAILED",
            message=f"Command timed out after {timeout} seconds.",
            command=command_text,
        )
    except Exception as exc:
        return AudioResult(
            status="FAILED",
            message=f"Audio command failed unexpectedly: {exc}",
            command=command_text,
        )

    if completed.returncode == 0:
        return AudioResult(
            status="OK",
            message="Audio command completed successfully.",
            command=command_text,
        )

    error = completed.stderr.strip() or completed.stdout.strip() or "Unknown error"
    return AudioResult(
        status="FAILED",
        message=f"Audio command returned exit code {completed.returncode}: {error}",
        command=command_text,
    )


def available_speech_engine() -> str | None:
    """
    Return the first available speech engine.

    Priority:
    1. espeak-ng
    2. flite
    3. say, useful on macOS development machines
    """

    for engine in ("espeak-ng", "flite", "say"):
        if command_exists(engine):
            return engine

    return None


def speak(text: str, timeout: float = 15.0) -> AudioResult:
    """
    Speak text using the first available system speech engine.

    This function is safe for early demos. If no speech engine is installed,
    it returns UNAVAILABLE instead of crashing.
    """

    clean_text = text.strip()

    if not clean_text:
        return AudioResult(
            status="WARNING",
            message="No speech text provided.",
        )

    engine = available_speech_engine()

    if engine is None:
        return AudioResult(
            status="UNAVAILABLE",
            message="No speech engine available. Install espeak-ng or flite on Raspberry Pi OS.",
        )

    if engine == "espeak-ng":
        command = ["espeak-ng", clean_text]
    elif engine == "flite":
        command = ["flite", "-t", clean_text]
    elif engine == "say":
        command = ["say", clean_text]
    else:
        return AudioResult(
            status="FAILED",
            message=f"Unsupported speech engine selected: {engine}",
        )

    return _run_command(command, timeout=timeout)


def speak_startup() -> AudioResult:
    """
    Speak the default MicroBot startup phrase.
    """

    return speak(DEFAULT_STARTUP_PHRASE)


def speak_complete() -> AudioResult:
    """
    Speak the default MicroBot demo completion phrase.
    """

    return speak(DEFAULT_COMPLETE_PHRASE)


def speak_warning() -> AudioResult:
    """
    Speak the default safe-mode warning phrase.
    """

    return speak(DEFAULT_WARNING_PHRASE)


def play_wav(path: str | Path, timeout: float = 10.0) -> AudioResult:
    """
    Play a WAV file using aplay if available.

    This is intended for Raspberry Pi OS / ALSA.
    """

    wav_path = Path(path)

    if not wav_path.exists():
        return AudioResult(
            status="FAILED",
            message=f"WAV file not found: {wav_path}",
            path=str(wav_path),
        )

    if not command_exists("aplay"):
        return AudioResult(
            status="UNAVAILABLE",
            message="aplay is not available. Install alsa-utils.",
            path=str(wav_path),
        )

    return _run_command(["aplay", str(wav_path)], timeout=timeout)


def record_microphone(
    output_path: str | Path = "/tmp/microbot_microphone_test.wav",
    duration_seconds: float = 2.0,
    sample_rate: int = 16000,
    channels: int = 1,
    device: str | None = None,
    timeout_margin_seconds: float = 3.0,
) -> AudioResult:
    """
    Record a short microphone sample using arecord.

    This is intended for Raspberry Pi OS / ALSA.

    Parameters:
        output_path:
            Where the WAV file should be saved.

        duration_seconds:
            Recording duration.

        sample_rate:
            Audio sample rate.

        channels:
            Number of channels.

        device:
            Optional ALSA device string, for example "hw:1,0".
    """

    if duration_seconds <= 0:
        return AudioResult(
            status="FAILED",
            message="duration_seconds must be greater than zero.",
        )

    if not command_exists("arecord"):
        return AudioResult(
            status="UNAVAILABLE",
            message="arecord is not available. Install alsa-utils.",
        )

    wav_path = Path(output_path)
    wav_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "arecord",
        "-f",
        "S16_LE",
        "-r",
        str(sample_rate),
        "-c",
        str(channels),
        "-d",
        str(int(math.ceil(duration_seconds))),
        str(wav_path),
    ]

    if device:
        command = [
            "arecord",
            "-D",
            device,
            "-f",
            "S16_LE",
            "-r",
            str(sample_rate),
            "-c",
            str(channels),
            "-d",
            str(int(math.ceil(duration_seconds))),
            str(wav_path),
        ]

    result = _run_command(
        command,
        timeout=float(duration_seconds) + timeout_margin_seconds,
    )

    if result.status == "OK":
        return AudioResult(
            status="OK",
            message="Microphone sample recorded successfully.",
            command=result.command,
            path=str(wav_path),
        )

    return AudioResult(
        status=result.status,
        message=result.message,
        command=result.command,
        path=str(wav_path),
    )


def wav_rms(path: str | Path) -> AudioResult:
    """
    Compute a simple RMS value from a 16-bit PCM WAV file.

    This is useful for microphone tests. A higher RMS value usually means
    louder recorded input.

    The function currently supports PCM WAV files with 16-bit samples.
    """

    wav_path = Path(path)

    if not wav_path.exists():
        return AudioResult(
            status="FAILED",
            message=f"WAV file not found: {wav_path}",
            path=str(wav_path),
        )

    try:
        with wave.open(str(wav_path), "rb") as wav_file:
            sample_width = wav_file.getsampwidth()
            frames = wav_file.readframes(wav_file.getnframes())
    except wave.Error as exc:
        return AudioResult(
            status="FAILED",
            message=f"Invalid WAV file: {exc}",
            path=str(wav_path),
        )
    except Exception as exc:
        return AudioResult(
            status="FAILED",
            message=f"Could not read WAV file: {exc}",
            path=str(wav_path),
        )

    if sample_width != 2:
        return AudioResult(
            status="FAILED",
            message=f"Unsupported WAV sample width: {sample_width}. Expected 16-bit PCM.",
            path=str(wav_path),
        )

    if not frames:
        return AudioResult(
            status="FAILED",
            message="WAV file contains no audio frames.",
            path=str(wav_path),
        )

    sample_count = len(frames) // 2
    samples = struct.unpack("<" + "h" * sample_count, frames)

    if sample_count == 0:
        return AudioResult(
            status="FAILED",
            message="No samples found in WAV file.",
            path=str(wav_path),
        )

    square_sum = sum(sample * sample for sample in samples)
    rms = math.sqrt(square_sum / sample_count)

    return AudioResult(
        status="OK",
        message=f"RMS={rms:.2f}",
        path=str(wav_path),
    )


def microphone_level_test(
    output_path: str | Path = "/tmp/microbot_microphone_test.wav",
    duration_seconds: float = 2.0,
    sample_rate: int = 16000,
    channels: int = 1,
    device: str | None = None,
) -> AudioResult:
    """
    Record a short sample and compute its RMS level.

    This gives a simple microphone test for early hardware validation.
    """

    record_result = record_microphone(
        output_path=output_path,
        duration_seconds=duration_seconds,
        sample_rate=sample_rate,
        channels=channels,
        device=device,
    )

    if record_result.status != "OK":
        return record_result

    return wav_rms(output_path)


def audio_self_check() -> dict[str, str | None]:
    """
    Return a simple audio capability report.

    This can be used by self_check.py later.
    """

    speech_engine = available_speech_engine()

    return {
        "speech_engine": speech_engine,
        "espeak_ng_available": str(command_exists("espeak-ng")),
        "flite_available": str(command_exists("flite")),
        "say_available": str(command_exists("say")),
        "aplay_available": str(command_exists("aplay")),
        "arecord_available": str(command_exists("arecord")),
    }


def print_audio_self_check() -> None:
    """
    Print audio capability status to terminal.
    """

    report = audio_self_check()

    print("Audio self-check")
    print("================")
    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    print_audio_self_check()

    result = speak("MicroBot Round V0 audio test.")
    print(f"Speech test: {result.status} - {result.message}")

    mic_result = microphone_level_test()
    print(f"Microphone test: {mic_result.status} - {mic_result.message}")