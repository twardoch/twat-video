# this_file: src/twat_video/__main__.py
"""Fire CLI entry point for twat-video."""

from __future__ import annotations

import fire


def _version() -> str:
    """Print the installed twat-video version."""
    from twat_video.__version__ import __version__  # noqa: PLC0415

    return __version__


def crop_scale(
    input_path: str,
    output_path: str,
    *,
    crop: str | None = None,
    scale: str | None = None,
    dry_run: bool = False,
) -> object:
    """Crop and/or scale a video with ffmpeg filters."""
    from twat_video.operations import crop_scale as _crop_scale  # noqa: PLC0415

    result = _crop_scale(
        input_path, output_path, crop=crop, scale=scale, dry_run=dry_run
    )
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def fps(
    input_path: str,
    output_path: str,
    fps_value: float,
    *,
    dry_run: bool = False,
) -> object:
    """Change output video frame rate."""
    from twat_video.operations import change_fps  # noqa: PLC0415

    result = change_fps(input_path, output_path, fps_value, dry_run=dry_run)
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def split(
    input_path: str,
    output_path: str,
    *,
    start: float,
    duration: float,
    dry_run: bool = False,
) -> object:
    """Extract a time segment from a video without re-encoding where possible."""
    from twat_video.operations import split_segment  # noqa: PLC0415

    result = split_segment(
        input_path, output_path, start=start, duration=duration, dry_run=dry_run
    )
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def reverse(
    input_path: str,
    output_path: str,
    *,
    no_audio: bool = False,
    dry_run: bool = False,
) -> object:
    """Reverse video frames and optionally audio."""
    from twat_video.operations import reverse_video  # noqa: PLC0415

    result = reverse_video(
        input_path, output_path, include_audio=not no_audio, dry_run=dry_run
    )
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def import_audio(
    video_path: str,
    audio_path: str,
    output_path: str,
    *,
    dry_run: bool = False,
) -> object:
    """Replace or import a video's audio track from another file."""
    from twat_video.operations import import_audio as _import_audio  # noqa: PLC0415

    result = _import_audio(video_path, audio_path, output_path, dry_run=dry_run)
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def extract_subtitles(
    input_path: str,
    output_path: str,
    *,
    stream: str = "0:s:0",
    dry_run: bool = False,
) -> object:
    """Extract a subtitle stream to an SRT file."""
    from twat_video.operations import extract_subtitles as _extract_subtitles  # noqa: PLC0415

    result = _extract_subtitles(input_path, output_path, stream=stream, dry_run=dry_run)
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def ken_burns(  # noqa: PLR0913
    image_path: str,
    output_path: str,
    *,
    duration: float = 5.0,
    fps: int = 30,
    zoom: float = 1.15,
    dry_run: bool = False,
) -> object:
    """Create a Ken Burns pan/zoom video from a still image."""
    from twat_video.operations import ken_burns as _ken_burns  # noqa: PLC0415

    result = _ken_burns(
        image_path, output_path, duration=duration, fps=fps, zoom=zoom, dry_run=dry_run
    )
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def grain(
    input_path: str,
    output_path: str,
    *,
    strength: int = 20,
    dry_run: bool = False,
) -> object:
    """Add deterministic visual grain using ffmpeg noise filter."""
    from twat_video.operations import add_grain  # noqa: PLC0415

    result = add_grain(input_path, output_path, strength=strength, dry_run=dry_run)
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def reverb(
    input_path: str,
    output_path: str,
    *,
    reverberance: float = 50.0,
    dry_run: bool = False,
) -> object:
    """Add audio reverb through ffmpeg's aecho filter."""
    from twat_video.operations import add_reverb  # noqa: PLC0415

    result = add_reverb(
        input_path, output_path, reverberance=reverberance, dry_run=dry_run
    )
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def concat(
    output_path: str,
    *input_paths: str,
    max_gap: float = 0.5,
    dry_run: bool = False,
) -> object:
    """Concatenate video clips in filename order.

    Clips are assigned sequential time slots (0-1, 1-2, …) for gap validation.
    Use --max-gap to control allowable gaps between clips (default 0.5 s).
    """
    from pathlib import Path  # noqa: PLC0415

    from twat_video.operations import VideoClip, merge_by_gap  # noqa: PLC0415

    clips = [
        VideoClip(Path(p), float(i), float(i + 1)) for i, p in enumerate(input_paths)
    ]
    result = merge_by_gap(clips, output_path, max_gap=max_gap, dry_run=dry_run)
    if dry_run:
        return " ".join(result.command)
    return result.returncode


def probe(
    path: str,
    *,
    dry_run: bool = False,
) -> object:
    """Return ffprobe metadata for a video file (JSON)."""
    from twat_video.operations import probe_video  # noqa: PLC0415

    return probe_video(path, dry_run=dry_run)


def genai(
    prompt: str,
    *,
    image: str | None = None,
    output_dir: str = "generated_videos",
) -> object:
    """Generate a video via a twat_genai backend (requires twat-genai)."""
    from twat_video.genai import generate_video  # noqa: PLC0415

    return generate_video(prompt, image=image, output_dir=output_dir)


# Explicit allow-list — only what is actually implemented.
COMMANDS: dict[str, object] = {
    "version": _version,
    "crop-scale": crop_scale,
    "fps": fps,
    "split": split,
    "reverse": reverse,
    "import-audio": import_audio,
    "extract-subtitles": extract_subtitles,
    "ken-burns": ken_burns,
    "grain": grain,
    "reverb": reverb,
    "concat": concat,
    "probe": probe,
    "genai": genai,
}


def main() -> None:
    """Run the twat-video Fire CLI."""
    fire.Fire(COMMANDS, name="twat-video")


# Per-leaf dashed-entry helpers.
def cmd_version() -> None:
    """Entry point: twat-video-version."""
    fire.Fire(_version, name="twat-video-version")


def cmd_crop_scale() -> None:
    """Entry point: twat-video-crop-scale."""
    fire.Fire(crop_scale, name="twat-video-crop-scale")


def cmd_fps() -> None:
    """Entry point: twat-video-fps."""
    fire.Fire(fps, name="twat-video-fps")


def cmd_split() -> None:
    """Entry point: twat-video-split."""
    fire.Fire(split, name="twat-video-split")


def cmd_reverse() -> None:
    """Entry point: twat-video-reverse."""
    fire.Fire(reverse, name="twat-video-reverse")


def cmd_import_audio() -> None:
    """Entry point: twat-video-import-audio."""
    fire.Fire(import_audio, name="twat-video-import-audio")


def cmd_extract_subtitles() -> None:
    """Entry point: twat-video-extract-subtitles."""
    fire.Fire(extract_subtitles, name="twat-video-extract-subtitles")


def cmd_ken_burns() -> None:
    """Entry point: twat-video-ken-burns."""
    fire.Fire(ken_burns, name="twat-video-ken-burns")


def cmd_grain() -> None:
    """Entry point: twat-video-grain."""
    fire.Fire(grain, name="twat-video-grain")


def cmd_reverb() -> None:
    """Entry point: twat-video-reverb."""
    fire.Fire(reverb, name="twat-video-reverb")


def cmd_concat() -> None:
    """Entry point: twat-video-concat."""
    fire.Fire(concat, name="twat-video-concat")


def cmd_probe() -> None:
    """Entry point: twat-video-probe."""
    fire.Fire(probe, name="twat-video-probe")


def cmd_genai() -> None:
    """Entry point: twat-video-genai."""
    fire.Fire(genai, name="twat-video-genai")


if __name__ == "__main__":
    main()
