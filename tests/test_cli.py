# this_file: tests/test_cli.py
"""Fire CLI smoke tests for twat-video."""

from __future__ import annotations

import subprocess
import sys

import twat_video
from twat_video.__main__ import COMMANDS


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [sys.executable, "-m", "twat_video", *args],
        capture_output=True,
        text=True,
        check=False,
    )


# ---------------------------------------------------------------------------
# Import-level smoke
# ---------------------------------------------------------------------------


def test_twat_video_imports() -> None:
    assert twat_video.__version__
    assert callable(twat_video.crop_scale)


# ---------------------------------------------------------------------------
# --help / top-level
# ---------------------------------------------------------------------------


def test_help_exits_zero() -> None:
    result = _run("--help")
    assert result.returncode == 0, result.stderr


def test_help_lists_commands() -> None:
    result = _run("--help")
    assert result.returncode == 0
    output = result.stdout + result.stderr
    for cmd in (
        "version",
        "crop-scale",
        "fps",
        "split",
        "reverse",
        "import-audio",
        "extract-subtitles",
        "ken-burns",
        "grain",
        "reverb",
        "concat",
        "probe",
        "genai",
    ):
        assert cmd in output, f"'{cmd}' not found in --help output"


# ---------------------------------------------------------------------------
# version leaf
# ---------------------------------------------------------------------------


def test_version_leaf() -> None:
    result = _run("version")
    assert result.returncode == 0, result.stderr
    output = (result.stdout + result.stderr).strip()
    assert twat_video.__version__ in output


# ---------------------------------------------------------------------------
# Per-leaf --help (exit 0 and non-empty output)
# ---------------------------------------------------------------------------


def test_leaf_help_crop_scale() -> None:
    r = _run("crop-scale", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_fps() -> None:
    r = _run("fps", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_split() -> None:
    r = _run("split", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_reverse() -> None:
    r = _run("reverse", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_import_audio() -> None:
    r = _run("import-audio", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_extract_subtitles() -> None:
    r = _run("extract-subtitles", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_ken_burns() -> None:
    r = _run("ken-burns", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_grain() -> None:
    r = _run("grain", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_reverb() -> None:
    r = _run("reverb", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_concat() -> None:
    r = _run("concat", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_probe() -> None:
    r = _run("probe", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


def test_leaf_help_genai() -> None:
    r = _run("genai", "--help")
    assert r.returncode == 0, r.stderr
    assert r.stdout + r.stderr


# ---------------------------------------------------------------------------
# dry-run functional tests (no ffmpeg needed)
# ---------------------------------------------------------------------------


def test_crop_scale_dry_run() -> None:
    r = _run("crop-scale", "in.mp4", "out.mp4", "--crop=100:100:0:0", "--dry-run")
    assert r.returncode == 0, r.stderr
    output = (r.stdout + r.stderr).strip()
    assert "ffmpeg" in output
    assert "crop=100:100:0:0" in output


def test_fps_dry_run() -> None:
    r = _run("fps", "in.mp4", "out.mp4", "24", "--dry-run")
    assert r.returncode == 0, r.stderr
    output = (r.stdout + r.stderr).strip()
    assert "ffmpeg" in output
    assert "fps=24" in output


def test_split_dry_run() -> None:
    r = _run(
        "split", "in.mp4", "clip.mp4", "--start=1.5", "--duration=2.0", "--dry-run"
    )
    assert r.returncode == 0, r.stderr
    output = (r.stdout + r.stderr).strip()
    assert "ffmpeg" in output
    assert "-ss" in output


def test_reverse_dry_run() -> None:
    r = _run("reverse", "in.mp4", "rev.mp4", "--dry-run")
    assert r.returncode == 0, r.stderr
    output = (r.stdout + r.stderr).strip()
    assert "ffmpeg" in output


def test_grain_dry_run() -> None:
    r = _run("grain", "in.mp4", "out.mp4", "--strength=30", "--dry-run")
    assert r.returncode == 0, r.stderr
    output = (r.stdout + r.stderr).strip()
    assert "ffmpeg" in output
    assert "noise" in output


def test_reverb_dry_run() -> None:
    r = _run("reverb", "in.mp4", "out.mp4", "--reverberance=75", "--dry-run")
    assert r.returncode == 0, r.stderr
    output = (r.stdout + r.stderr).strip()
    assert "ffmpeg" in output
    assert "aecho" in output


# ---------------------------------------------------------------------------
# COMMANDS dict integrity
# ---------------------------------------------------------------------------


def test_commands_dict_populated() -> None:
    expected = {
        "version",
        "crop-scale",
        "fps",
        "split",
        "reverse",
        "import-audio",
        "extract-subtitles",
        "ken-burns",
        "grain",
        "reverb",
        "concat",
        "probe",
        "genai",
    }
    assert expected == set(COMMANDS.keys())
    for name, obj in COMMANDS.items():
        assert callable(obj), f"COMMANDS['{name}'] is not callable"
