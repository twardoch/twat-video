# twat-video

`twat-video` is the video domain plugin for the [`twat`](https://github.com/twardoch/twat) ecosystem. It provides reusable, testable ffmpeg command wrappers and a thin adapter layer for AI video generation via `twat_genai`.

## Requirements

- Python 3.10+
- `ffmpeg` and `ffprobe` on `PATH` for real media processing

Tests exercise command construction with `dry_run=True` and do not require media binaries.

## Installation

```bash
pip install twat-video
```

## Python API

```python
from twat_video import (
    crop_scale, change_fps, split_segment, reverse_video,
    merge_by_gap, import_audio, extract_subtitles, repair_srt_text,
    add_grain, add_reverb, ken_burns, probe_video, VideoClip,
)

# Crop and scale in one pass
crop_scale("input.mp4", "square.mp4", crop="1080:1080:420:0", scale="720:720")

# Extract a segment without re-encoding
split_segment("input.mp4", "clip.mp4", start=12.5, duration=4.0)

# Replace audio track
import_audio("silent.mp4", "voice.wav", "dubbed.mp4")
```

All functions accept `dry_run=True` — returns a `CommandResult` with the constructed command without invoking ffmpeg.

## CLI

```bash
python -m twat_video --help
python -m twat_video crop-scale in.mp4 out.mp4 --crop 1080:1080:420:0 --dry-run
python -m twat_video fps in.mp4 out.mp4 24 --dry-run
python -m twat_video split in.mp4 clip.mp4 --start 1.5 --duration 3 --dry-run
python -m twat_video import-audio silent.mp4 voice.wav dubbed.mp4 --dry-run
python -m twat_video ken-burns still.png out.mp4 --duration 5 --dry-run
python -m twat_video probe video.mp4
```

Available subcommands: `version`, `crop-scale`, `fps`, `split`, `reverse`, `import-audio`, `extract-subtitles`, `ken-burns`, `grain`, `reverb`, `concat`, `probe`, `genai`.

## AI video boundary

`generate_video()` imports `twat_genai` at runtime and delegates to its video generation API — no provider SDKs are bundled. Install `twat-genai` and configure a provider separately.

## twat plugin registration

Registered under the `video` key in the `twat.plugins` entry-point group.

## License

MIT
