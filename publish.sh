#!/usr/bin/env bash
# publish.sh — Build and publish to PyPI using hatch-vcs semver from git tags.
# Order matters: clean → bump tag → build (so version is clean, not local-dev) → publish.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

uvx hatch clean
uvx gitnextver .
uvx hatch build
uv publish
