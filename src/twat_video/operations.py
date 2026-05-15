"""Reusable video operations built as testable ffmpeg commands."""
# this_file: src/twat_video/operations.py

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

from twat_video.ffmpeg import CommandResult, ffprobe_json, run_ffmpeg


@dataclass(frozen=True)
class VideoClip:
    """Video clip item used by merge-by-gap planning."""

    path: Path
    start: float
    end: float


def crop_scale(
    input_path: str | Path,
    output_path: str | Path,
    *,
    crop: str | None = None,
    scale: str | None = None,
    dry_run: bool = False,
) -> CommandResult:
    """Crop and/or scale a video with ffmpeg filters."""
    filters = [
        value
        for value in (
            f"crop={crop}" if crop else None,
            f"scale={scale}" if scale else None,
        )
        if value
    ]
    args = ["-y", "-i", str(input_path)]
    if filters:
        args += ["-vf", ",".join(filters)]
    args += ["-c:a", "copy", str(output_path)]
    return run_ffmpeg(args, dry_run=dry_run)


def change_fps(
    input_path: str | Path,
    output_path: str | Path,
    fps: float,
    *,
    dry_run: bool = False,
) -> CommandResult:
    """Change output video frame rate."""
    return run_ffmpeg(
        ["-y", "-i", str(input_path), "-filter:v", f"fps={fps:g}", str(output_path)],
        dry_run=dry_run,
    )


def split_segment(
    input_path: str | Path,
    output_path: str | Path,
    *,
    start: float,
    duration: float,
    dry_run: bool = False,
) -> CommandResult:
    """Extract a time segment without re-encoding where possible."""
    return run_ffmpeg(
        [
            "-y",
            "-ss",
            f"{start:g}",
            "-i",
            str(input_path),
            "-t",
            f"{duration:g}",
            "-c",
            "copy",
            str(output_path),
        ],
        dry_run=dry_run,
    )


def reverse_video(
    input_path: str | Path,
    output_path: str | Path,
    *,
    include_audio: bool = True,
    dry_run: bool = False,
) -> CommandResult:
    """Reverse video frames and optionally audio."""
    filter_complex = (
        "[0:v]reverse[v];[0:a]areverse[a]" if include_audio else "[0:v]reverse[v]"
    )
    args = [
        "-y",
        "-i",
        str(input_path),
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
    ]
    if include_audio:
        args += ["-map", "[a]"]
    args.append(str(output_path))
    return run_ffmpeg(args, dry_run=dry_run)


def import_audio(
    video_path: str | Path,
    audio_path: str | Path,
    output_path: str | Path,
    *,
    dry_run: bool = False,
) -> CommandResult:
    """Replace or import a video's audio track from another file."""
    return run_ffmpeg(
        [
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-shortest",
            str(output_path),
        ],
        dry_run=dry_run,
    )


def extract_subtitles(
    input_path: str | Path,
    output_path: str | Path,
    *,
    stream: str = "0:s:0",
    dry_run: bool = False,
) -> CommandResult:
    """Extract a subtitle stream to an SRT file."""
    return run_ffmpeg(
        ["-y", "-i", str(input_path), "-map", stream, str(output_path)], dry_run=dry_run
    )


def repair_srt_text(text: str) -> str:
    """Apply conservative subtitle text repairs useful after extraction."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = [block.strip() for block in normalized.split("\n\n") if block.strip()]
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def ken_burns(  # noqa: PLR0913
    image_path: str | Path,
    output_path: str | Path,
    *,
    duration: float = 5.0,
    fps: int = 30,
    zoom: float = 1.15,
    dry_run: bool = False,
) -> CommandResult:
    """Create a simple Ken Burns pan/zoom video from a still image."""
    frames = max(1, round(duration * fps))
    vf = f"zoompan=z='min(zoom+0.0015,{zoom})':d={frames}:s=1920x1080:fps={fps}"
    return run_ffmpeg(
        [
            "-y",
            "-loop",
            "1",
            "-i",
            str(image_path),
            "-vf",
            vf,
            "-t",
            f"{duration:g}",
            "-pix_fmt",
            "yuv420p",
            str(output_path),
        ],
        dry_run=dry_run,
    )


def add_grain(
    input_path: str | Path,
    output_path: str | Path,
    *,
    strength: int = 20,
    dry_run: bool = False,
) -> CommandResult:
    """Add deterministic visual grain using ffmpeg noise filter."""
    return run_ffmpeg(
        [
            "-y",
            "-i",
            str(input_path),
            "-vf",
            f"noise=alls={strength}:allf=t",
            str(output_path),
        ],
        dry_run=dry_run,
    )


def add_reverb(
    input_path: str | Path,
    output_path: str | Path,
    *,
    reverberance: float = 50.0,
    dry_run: bool = False,
) -> CommandResult:
    """Add a simple audio reverb through ffmpeg's aecho filter."""
    decay = max(0.0, min(reverberance, 100.0)) / 100.0
    return run_ffmpeg(
        [
            "-y",
            "-i",
            str(input_path),
            "-af",
            f"aecho=0.8:0.9:1000:{decay:g}",
            str(output_path),
        ],
        dry_run=dry_run,
    )


def merge_by_gap(
    clips: list[VideoClip],
    output_path: str | Path,
    *,
    max_gap: float = 0.5,
    dry_run: bool = False,
) -> CommandResult:
    """Concatenate clips ordered by start time, validating gaps between them."""
    if not clips:
        msg = "at least one clip is required"
        raise ValueError(msg)
    ordered = sorted(clips, key=lambda clip: clip.start)
    for previous, current in pairwise(ordered):
        if current.start - previous.end > max_gap:
            msg = f"gap between {previous.path} and {current.path} exceeds {max_gap:g}s"
            raise ValueError(msg)
    inputs: list[str] = []
    for clip in ordered:
        inputs += ["-i", str(clip.path)]
    concat_inputs = "".join(
        f"[{index}:v:0][{index}:a:0]" for index in range(len(ordered))
    )
    filter_complex = f"{concat_inputs}concat=n={len(ordered)}:v=1:a=1[v][a]"
    return run_ffmpeg(
        [
            "-y",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
            str(output_path),
        ],
        dry_run=dry_run,
    )


def probe_video(
    path: str | Path, *, dry_run: bool = False
) -> dict[str, Any] | CommandResult:
    """Return ffprobe metadata for a video file."""
    return ffprobe_json(path, dry_run=dry_run)
