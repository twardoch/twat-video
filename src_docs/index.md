# twat-video

`twat-video` is the video domain plugin for the [`twat`](https://github.com/twardoch/twat) ecosystem. It provides reusable, testable ffmpeg command wrappers and a thin adapter layer for AI video generation via `twat_genai`.

## Role in the twat ecosystem

The `twat` framework discovers plugins by the `twat.plugins` entry-point group. `twat-video` registers under the `video` key, making its helpers available to any code that loads the twat plugin registry.

## Requirements

- Python 3.10+
- `ffmpeg` and `ffprobe` on `PATH` for real media processing (tests use `dry_run=True` and do not require them)

## Installation

```bash
pip install twat-video
```

## Python API

```python
from twat_video import (
    crop_scale,
    change_fps,
    split_segment,
    reverse_video,
    merge_by_gap,
    import_audio,
    extract_subtitles,
    repair_srt_text,
    add_grain,
    add_reverb,
    ken_burns,
    probe_video,
    VideoClip,
)

# Crop and scale in one pass
crop_scale("input.mp4", "square.mp4", crop="1080:1080:420:0", scale="720:720")

# Extract a segment without re-encoding
split_segment("input.mp4", "clip.mp4", start=12.5, duration=4.0)

# Replace audio track
import_audio("silent.mp4", "voice.wav", "dubbed.mp4")

# Concatenate ordered clips
from pathlib import Path
clips = [VideoClip(Path("a.mp4"), 0.0, 10.0), VideoClip(Path("b.mp4"), 10.0, 20.0)]
merge_by_gap(clips, "merged.mp4", max_gap=1.0)
```

All functions accept a `dry_run=True` keyword argument that returns the constructed `CommandResult` without invoking ffmpeg — useful for testing and previewing commands.

## CLI

```bash
python -m twat_video --help
python -m twat_video version

# Dry-run examples (no ffmpeg required)
python -m twat_video crop-scale in.mp4 out.mp4 --crop 1080:1080:420:0 --dry-run
python -m twat_video fps in.mp4 out.mp4 24 --dry-run
python -m twat_video split in.mp4 clip.mp4 --start 1.5 --duration 3 --dry-run
python -m twat_video reverse in.mp4 rev.mp4 --dry-run
python -m twat_video import-audio silent.mp4 voice.wav dubbed.mp4 --dry-run
python -m twat_video ken-burns still.png out.mp4 --duration 5 --zoom 1.2 --dry-run
python -m twat_video grain in.mp4 out.mp4 --strength 30 --dry-run
python -m twat_video reverb in.mp4 out.mp4 --reverberance 75 --dry-run
python -m twat_video concat out.mp4 a.mp4 b.mp4 c.mp4 --dry-run
python -m twat_video probe video.mp4
```

## Available commands

| Command | Description |
|---|---|
| `version` | Print installed version |
| `crop-scale` | Crop and/or scale video |
| `fps` | Change frame rate |
| `split` | Extract a time segment |
| `reverse` | Reverse frames (and optionally audio) |
| `import-audio` | Replace/import audio track |
| `extract-subtitles` | Extract subtitle stream to SRT |
| `ken-burns` | Pan/zoom slideshow from still image |
| `grain` | Add film grain |
| `reverb` | Add audio reverb |
| `concat` | Concatenate clips in order |
| `probe` | Show ffprobe metadata |
| `genai` | Generate video via twat_genai (optional) |

## AI video boundary

`generate_video()` is a narrow adapter. It imports `twat_genai` at runtime and delegates to `twat_genai.generate_video` — no provider SDKs are bundled. Install `twat-genai` and configure a video provider separately.

## API reference

See the [API Reference](api.md) for full module documentation.
