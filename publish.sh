#!/usr/bin/env bash
# publish.sh — Build and publish to PyPI using hatch-vcs semver from git tags.
# Order: clean → tidy (pre-commit autofixes, then commit) → bump tag → build → publish.
# Uses `uv build` (PEP 517 via hatchling) to avoid hatch's env-plugin sync which
# needs pip in the hatch venv. Tidying upfront keeps gitnextver's atomic commit
# from tripping the pre-commit hook.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

rm -rf dist/ build/ *.egg-info

if [[ -f .pre-commit-config.yaml ]] && command -v pre-commit >/dev/null 2>&1; then
    pre-commit run --all-files || true
fi
if ! git diff --quiet || ! git diff --cached --quiet; then
    git add -A
    git commit -m "chore: pre-publish tidy" || true
fi

uvx gitnextver .
uv build
uv publish
