"""Command-line interface for twat-video."""
# this_file: src/twat_video/__main__.py

from __future__ import annotations

import argparse
import sys

from twat_video.operations import (
    add_grain,
    add_reverb,
    change_fps,
    crop_scale,
    extract_subtitles,
    import_audio,
    ken_burns,
    reverse_video,
    split_segment,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="twat-video", description="Video processing helpers built around ffmpeg."
    )
    sub = parser.add_subparsers(dest="command")

    crop = sub.add_parser("crop-scale", help="Crop and/or scale a video.")
    crop.add_argument("input")
    crop.add_argument("output")
    crop.add_argument("--crop")
    crop.add_argument("--scale")
    crop.add_argument("--dry-run", action="store_true")

    fps = sub.add_parser("fps", help="Change frame rate.")
    fps.add_argument("input")
    fps.add_argument("output")
    fps.add_argument("fps", type=float)
    fps.add_argument("--dry-run", action="store_true")

    split = sub.add_parser("split", help="Extract a segment.")
    split.add_argument("input")
    split.add_argument("output")
    split.add_argument("--start", type=float, required=True)
    split.add_argument("--duration", type=float, required=True)
    split.add_argument("--dry-run", action="store_true")

    rev = sub.add_parser("reverse", help="Reverse video.")
    rev.add_argument("input")
    rev.add_argument("output")
    rev.add_argument("--no-audio", action="store_true")
    rev.add_argument("--dry-run", action="store_true")

    audio = sub.add_parser("import-audio", help="Replace/import audio track.")
    audio.add_argument("video")
    audio.add_argument("audio")
    audio.add_argument("output")
    audio.add_argument("--dry-run", action="store_true")

    subs = sub.add_parser("extract-subtitles", help="Extract subtitle stream.")
    subs.add_argument("input")
    subs.add_argument("output")
    subs.add_argument("--stream", default="0:s:0")
    subs.add_argument("--dry-run", action="store_true")

    ken = sub.add_parser("ken-burns", help="Create video from still image.")
    ken.add_argument("image")
    ken.add_argument("output")
    ken.add_argument("--duration", type=float, default=5.0)
    ken.add_argument("--fps", type=int, default=30)
    ken.add_argument("--dry-run", action="store_true")

    grain = sub.add_parser("grain", help="Add visual grain.")
    grain.add_argument("input")
    grain.add_argument("output")
    grain.add_argument("--strength", type=int, default=20)
    grain.add_argument("--dry-run", action="store_true")

    reverb = sub.add_parser("reverb", help="Add audio reverb.")
    reverb.add_argument("input")
    reverb.add_argument("output")
    reverb.add_argument("--reverberance", type=float, default=50.0)
    reverb.add_argument("--dry-run", action="store_true")
    return parser


def _print(result: object) -> None:
    command = getattr(result, "command", None)
    if command:
        sys.stdout.write(f"{' '.join(command)}\n")


def _dispatch(args: argparse.Namespace) -> object | None:
    handlers = {
        "crop-scale": lambda: crop_scale(
            args.input,
            args.output,
            crop=args.crop,
            scale=args.scale,
            dry_run=args.dry_run,
        ),
        "fps": lambda: change_fps(
            args.input, args.output, args.fps, dry_run=args.dry_run
        ),
        "split": lambda: split_segment(
            args.input,
            args.output,
            start=args.start,
            duration=args.duration,
            dry_run=args.dry_run,
        ),
        "reverse": lambda: reverse_video(
            args.input,
            args.output,
            include_audio=not args.no_audio,
            dry_run=args.dry_run,
        ),
        "import-audio": lambda: import_audio(
            args.video, args.audio, args.output, dry_run=args.dry_run
        ),
        "extract-subtitles": lambda: extract_subtitles(
            args.input, args.output, stream=args.stream, dry_run=args.dry_run
        ),
        "ken-burns": lambda: ken_burns(
            args.image,
            args.output,
            duration=args.duration,
            fps=args.fps,
            dry_run=args.dry_run,
        ),
        "grain": lambda: add_grain(
            args.input, args.output, strength=args.strength, dry_run=args.dry_run
        ),
        "reverb": lambda: add_reverb(
            args.input,
            args.output,
            reverberance=args.reverberance,
            dry_run=args.dry_run,
        ),
    }
    handler = handlers.get(args.command)
    return handler() if handler is not None else None


def main() -> None:
    """Run the twat-video CLI."""
    parser = _parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    _print(_dispatch(args))


if __name__ == "__main__":
    main()
