---
this_file: LOG.md
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.1] - 2025-02-15

Initial release of the twat-video package.

### Added

- Basic project structure with modern Python packaging (PEP 621 compliant)
- Initial implementation of `twat_video.py` with:
  - Configuration class with type hints
  - Data processing functionality
  - Logging setup
- Added `videoextendprompt.py` script for:
  - Generating video continuation prompts based on image frame analysis
  - Support for multiple AI models (Gemini, GPT-4, Claude-3, Grok-2)
  - Image pair processing functionality
  - Markdown output generation
- Project setup with Hatch for development workflow
- Basic documentation in README.md
- MIT License

### Changed

- Moved `twat_video.py` to proper module structure
- Updated .gitignore to exclude private files

## [Initial Commit] - 2025-02-09

- Repository initialization
- Basic project structure setup

[v0.0.1]: https://github.com/twardoch/twat-video/releases/tag/v0.0.1 
