#!/bin/bash
# this_file: scripts/build.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.12"
PROJECT_NAME="twat-video"

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Create scripts directory if it doesn't exist
mkdir -p scripts

log_info "Building ${PROJECT_NAME}..."

# Clean previous builds
log_info "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage coverage.xml
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Install/upgrade build tools
log_info "Installing/upgrading build tools..."
uv pip install --upgrade build hatchling hatch-vcs twine

# Build the package
log_info "Building distributions..."
python -m build --outdir dist/

# Verify build artifacts
log_info "Verifying build artifacts..."
if [[ ! -d "dist" ]] || [[ -z "$(ls -A dist)" ]]; then
    log_error "No distribution files found in dist/"
    exit 1
fi

# Check for required files
WHEEL_FILE=$(find dist -name "*.whl" | head -1)
SDIST_FILE=$(find dist -name "*.tar.gz" | head -1)

if [[ -z "$WHEEL_FILE" ]]; then
    log_error "No wheel file found in dist/"
    exit 1
fi

if [[ -z "$SDIST_FILE" ]]; then
    log_error "No source distribution found in dist/"
    exit 1
fi

log_success "Build artifacts created:"
ls -la dist/

# Basic validation of the built package
log_info "Validating built package..."
python -m twine check dist/*

log_success "Build completed successfully!"
log_info "Distribution files are available in: $(pwd)/dist/"