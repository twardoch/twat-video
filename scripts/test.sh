#!/bin/bash
# this_file: scripts/test.sh

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

log_info "Running comprehensive tests for ${PROJECT_NAME}..."

# Install test dependencies
log_info "Installing test dependencies..."
uv pip install --upgrade ".[test,dev]"

# Run code quality checks
log_info "Running code quality checks..."

# Linting with Ruff
log_info "Running Ruff linter..."
if ! uv run ruff check src/ tests/; then
    log_error "Ruff linting failed"
    exit 1
fi
log_success "Ruff linting passed"

# Format checking with Ruff
log_info "Checking code formatting..."
if ! uv run ruff format --check src/ tests/; then
    log_error "Code formatting check failed"
    log_info "Run 'uv run ruff format src/ tests/' to fix formatting"
    exit 1
fi
log_success "Code formatting check passed"

# Type checking with MyPy
log_info "Running type checks..."
if ! uv run mypy src/twat_video tests/; then
    log_error "Type checking failed"
    exit 1
fi
log_success "Type checking passed"

# Run tests with coverage
log_info "Running tests with coverage..."
if ! uv run pytest -n auto --maxfail=5 --tb=short --cov-report=term-missing --cov-report=xml --cov-config=pyproject.toml --cov=src/twat_video --cov=tests tests/; then
    log_error "Tests failed"
    exit 1
fi

# Coverage report
log_info "Coverage report generated"
if [[ -f "coverage.xml" ]]; then
    log_success "Coverage XML report: $(pwd)/coverage.xml"
fi

# Run performance benchmarks if available
if grep -q "benchmark" tests/*.py 2>/dev/null; then
    log_info "Running performance benchmarks..."
    uv run pytest -v tests/ -m benchmark --benchmark-only 2>/dev/null || log_warning "No benchmark tests found or benchmark plugin not available"
fi

log_success "All tests passed successfully!"

# Display summary
echo ""
echo "=== TEST SUMMARY ==="
echo "✓ Linting (Ruff)"
echo "✓ Code formatting (Ruff)"
echo "✓ Type checking (MyPy)"
echo "✓ Unit tests (Pytest)"
echo "✓ Code coverage analysis"
echo ""
log_success "Test suite completed successfully!"