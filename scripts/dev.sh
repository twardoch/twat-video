#!/bin/bash
# this_file: scripts/dev.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
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

print_usage() {
    echo "Usage: $0 <command>"
    echo ""
    echo "Development helper script for ${PROJECT_NAME}"
    echo ""
    echo "Commands:"
    echo "  setup          # Set up development environment"
    echo "  clean          # Clean build artifacts and caches"
    echo "  lint           # Run linting checks"
    echo "  format         # Format code"
    echo "  type-check     # Run type checking"
    echo "  test           # Run tests"
    echo "  test-watch     # Run tests in watch mode"
    echo "  coverage       # Run tests with coverage report"
    echo "  build          # Build distribution packages"
    echo "  install-local  # Install package in development mode"
    echo "  pre-commit     # Set up pre-commit hooks"
    echo "  deps           # Update dependencies"
    echo "  version        # Show current version"
    echo "  help           # Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 setup       # Initialize development environment"
    echo "  $0 test        # Run test suite"
    echo "  $0 format      # Format all code"
}

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Parse command
COMMAND="${1:-help}"

case "$COMMAND" in
    setup)
        log_info "Setting up development environment..."
        
        # Install/upgrade uv
        log_info "Installing/upgrading uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh || log_warning "uv installation may have failed"
        
        # Install development dependencies
        log_info "Installing development dependencies..."
        uv pip install --upgrade ".[dev,test]"
        
        # Install pre-commit hooks
        log_info "Installing pre-commit hooks..."
        uv pip install pre-commit
        pre-commit install
        
        # Make scripts executable
        chmod +x scripts/*.sh
        
        log_success "Development environment setup complete!"
        log_info "Try running: $0 test"
        ;;
        
    clean)
        log_info "Cleaning build artifacts and caches..."
        rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage coverage.xml .mypy_cache/ .ruff_cache/
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        log_success "Cleanup complete!"
        ;;
        
    lint)
        log_info "Running linting checks..."
        uv run ruff check src/ tests/
        log_success "Linting complete!"
        ;;
        
    format)
        log_info "Formatting code..."
        uv run ruff format src/ tests/
        log_success "Code formatting complete!"
        ;;
        
    type-check)
        log_info "Running type checking..."
        uv run mypy src/twat_video tests/
        log_success "Type checking complete!"
        ;;
        
    test)
        log_info "Running tests..."
        uv run pytest tests/
        log_success "Tests complete!"
        ;;
        
    test-watch)
        log_info "Running tests in watch mode..."
        log_warning "Press Ctrl+C to stop watching"
        uv run pytest-watch tests/
        ;;
        
    coverage)
        log_info "Running tests with coverage..."
        uv run pytest --cov-report=term-missing --cov-report=html --cov-config=pyproject.toml --cov=src/twat_video --cov=tests tests/
        if [[ -d "htmlcov" ]]; then
            log_success "Coverage report generated: htmlcov/index.html"
        fi
        ;;
        
    build)
        log_info "Building distribution packages..."
        ./scripts/build.sh
        ;;
        
    install-local)
        log_info "Installing package in development mode..."
        uv pip install -e .
        log_success "Package installed in development mode!"
        ;;
        
    pre-commit)
        log_info "Setting up pre-commit hooks..."
        uv pip install pre-commit
        pre-commit install
        log_info "Running pre-commit on all files..."
        pre-commit run --all-files
        log_success "Pre-commit hooks setup complete!"
        ;;
        
    deps)
        log_info "Updating dependencies..."
        uv pip install --upgrade ".[dev,test]"
        if [[ -f "requirements.txt" ]]; then
            uv pip install --upgrade -r requirements.txt
        fi
        log_success "Dependencies updated!"
        ;;
        
    version)
        log_info "Getting current version..."
        if command -v python &> /dev/null; then
            python -c "import twat_video; print(f'Version: {twat_video.__version__}')" 2>/dev/null || echo "Package not installed"
        fi
        
        # Show git tag info
        if git tag --list | tail -5 | grep -q "v"; then
            log_info "Recent git tags:"
            git tag --list | tail -5
        fi
        
        # Show current commit
        log_info "Current commit: $(git rev-parse --short HEAD)"
        ;;
        
    help|--help|-h)
        print_usage
        ;;
        
    *)
        log_error "Unknown command: $COMMAND"
        print_usage
        exit 1
        ;;
esac