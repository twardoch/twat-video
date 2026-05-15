"""Tests for twat_video command construction."""
# this_file: tests/test_video_operations.py

from pathlib import Path

import pytest

from twat_video import (
    VideoClip,
    crop_scale,
    import_audio,
    merge_by_gap,
    repair_srt_text,
    reverse_video,
    split_segment,
)


def test_crop_scale_builds_ffmpeg_command() -> None:
    result = crop_scale(
        "in.mp4", "out.mp4", crop="100:100:0:0", scale="320:240", dry_run=True
    )
    assert result.command[:2] == ["ffmpeg", "-hide_banner"]
    assert "crop=100:100:0:0,scale=320:240" in result.command


def test_split_reverse_and_import_audio_commands() -> None:
    split = split_segment("in.mp4", "clip.mp4", start=1.5, duration=2.0, dry_run=True)
    assert "-ss" in split.command and "1.5" in split.command
    reverse = reverse_video("in.mp4", "rev.mp4", include_audio=False, dry_run=True)
    assert "[0:v]reverse[v]" in reverse.command
    imported = import_audio("video.mp4", "audio.wav", "muxed.mp4", dry_run=True)
    assert imported.command.count("-i") == 2


def test_merge_by_gap_rejects_large_gap() -> None:
    clips = [VideoClip(Path("a.mp4"), 0.0, 1.0), VideoClip(Path("b.mp4"), 3.0, 4.0)]
    with pytest.raises(ValueError, match="gap"):
        merge_by_gap(clips, "out.mp4", max_gap=0.5, dry_run=True)


def test_merge_by_gap_builds_concat_command() -> None:
    clips = [VideoClip(Path("a.mp4"), 0.0, 1.0), VideoClip(Path("b.mp4"), 1.1, 2.0)]
    result = merge_by_gap(clips, "out.mp4", max_gap=0.2, dry_run=True)
    assert any("concat=n=2:v=1:a=1[v][a]" in part for part in result.command)


def test_repair_srt_text_normalizes_blocks() -> None:
    text = "1\r\n00:00:00,000 --> 00:00:01,000\r\nHello\r\n\r\n\r\n"
    assert repair_srt_text(text) == "1\n00:00:00,000 --> 00:00:01,000\nHello\n"
