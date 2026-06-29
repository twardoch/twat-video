# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- `pyproject.toml`: corrected `all` optional-dependency group — entries were mistakenly
  referencing extras group names (`test`, `dev`, etc.) as PyPI package names, causing
  `uv` dependency resolution to fail.
- Removed stray `src/font_organizer/` tree (leftover from a prior refactor; the canonical
  copy lives in `twat_font`).
- `tests/test_cli.py`: subprocess helper `_run` now injects the project `src/` directory
  via `PYTHONPATH` so the dev-version `twat_video` is always used, not an older
  system-installed copy.

### Changed
- `README.md`: rewritten to describe `twat-video` video utilities; removed obsolete
  font-organizer preservation note.
- `mkdocs.yml`: corrected site name, URLs, and nav structure from font-organizer to
  twat-video.
- `src_docs/index.md`: replaced font-organizer content with twat-video documentation
  covering API, CLI, and twat ecosystem role.
- Added `src_docs/api.md` with mkdocstrings directives for the three public modules.

## [2.7.6] - 2026-05-01

### Added
- Full Fire CLI with per-leaf entry-points for every operation.
- `dry_run=True` mode across all operations — returns constructed command without
  invoking ffmpeg, enabling tests without media binaries.
- `COMMANDS` dict in `__main__` as single source of truth for the CLI surface.

### Changed
- Package reoriented from font-organizer prototype to video utilities under the twat
  plugin ecosystem.

## [2.7.0] - 2025-12-01

### Added
- Initial `twat_video` package structure with `src/` layout.
- `ffmpeg.py`: `run_command`, `run_ffmpeg`, `ffprobe_json`, `CommandResult`.
- `operations.py`: `crop_scale`, `change_fps`, `split_segment`, `reverse_video`,
  `import_audio`, `extract_subtitles`, `repair_srt_text`, `ken_burns`, `add_grain`,
  `add_reverb`, `merge_by_gap`, `probe_video`, `VideoClip`.
- `genai.py`: narrow `generate_video` adapter delegating to `twat_genai`.
- `hatchling` + `hatch-vcs` build system; version sourced from VCS tags.
- MkDocs Material documentation scaffold.
- CI workflow for linting (ruff), type-checking (mypy), and multi-platform tests.

[Unreleased]: https://github.com/twardoch/twat-video/compare/v2.7.6...HEAD
[2.7.6]: https://github.com/twardoch/twat-video/compare/v2.7.0...v2.7.6
[2.7.0]: https://github.com/twardoch/twat-video/releases/tag/v2.7.0
