"""Small ffmpeg command boundary for twat-video."""
# this_file: src/twat_video/ffmpeg.py

from __future__ import annotations

from collections.abc import Sequence
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CommandResult:
    """Result from a completed subprocess command."""

    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(command: Sequence[str], *, dry_run: bool = False) -> CommandResult:
    """Run a command, or return a dry-run result with the constructed command."""
    cmd = [str(part) for part in command]
    if dry_run:
        return CommandResult(cmd, 0, "", "")
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)  # noqa: S603
    if completed.returncode != 0:
        msg = (
            completed.stderr.strip()
            or f"command failed with exit code {completed.returncode}"
        )
        raise RuntimeError(msg)
    return CommandResult(cmd, completed.returncode, completed.stdout, completed.stderr)


def run_ffmpeg(args: Sequence[str], *, dry_run: bool = False) -> CommandResult:
    """Run ffmpeg with the provided arguments."""
    return run_command(["ffmpeg", "-hide_banner", *args], dry_run=dry_run)


def ffprobe_json(
    path: str | Path, *, dry_run: bool = False
) -> dict[str, Any] | CommandResult:
    """Probe a media file with ffprobe and return parsed JSON metadata."""
    command = [
        "ffprobe",
        "-hide_banner",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(path),
    ]
    result = run_command(command, dry_run=dry_run)
    if dry_run:
        return result
    data = json.loads(result.stdout)
    if not isinstance(data, dict):
        msg = "ffprobe did not return a JSON object"
        raise RuntimeError(msg)
    return data
