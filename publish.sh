#!/usr/bin/env bash
# publish.sh — Build and publish to PyPI using hatch-vcs semver from git tags.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

uvx hatch clean
uvx hatch build
uvx gitnextver .
uv publish
