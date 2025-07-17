#!/bin/bash
# this_file: scripts/release.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="twat-video"
MAIN_BRANCH="main"

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
    echo "Usage: $0 <version>"
    echo ""
    echo "Creates a new release by:"
    echo "  1. Running full test suite"
    echo "  2. Building distributions"
    echo "  3. Creating and pushing a git tag"
    echo "  4. Optionally publishing to PyPI"
    echo ""
    echo "Examples:"
    echo "  $0 1.0.0       # Create release v1.0.0"
    echo "  $0 1.0.1       # Create release v1.0.1"
    echo "  $0 2.0.0-beta1 # Create pre-release v2.0.0-beta1"
    echo ""
    echo "Options:"
    echo "  --dry-run      # Don't actually create tags or push"
    echo "  --no-pypi      # Skip PyPI publication"
    echo "  --help         # Show this help"
}

# Parse command line arguments
DRY_RUN=false
NO_PYPI=false
VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-pypi)
            NO_PYPI=true
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        -*)
            log_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
        *)
            if [[ -z "$VERSION" ]]; then
                VERSION="$1"
            else
                log_error "Multiple versions specified"
                print_usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate input
if [[ -z "$VERSION" ]]; then
    log_error "Version is required"
    print_usage
    exit 1
fi

# Validate version format (basic semver check)
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$ ]]; then
    log_error "Invalid version format. Use semantic versioning (e.g., 1.0.0, 2.1.0-beta1)"
    exit 1
fi

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Check if git is clean
if [[ -n "$(git status --porcelain)" ]]; then
    log_error "Git working directory is not clean. Please commit or stash changes."
    git status --short
    exit 1
fi

# Check if we're on the main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]]; then
    log_warning "Not on $MAIN_BRANCH branch (currently on $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if tag already exists
TAG_NAME="v$VERSION"
if git tag -l | grep -q "^$TAG_NAME$"; then
    log_error "Tag $TAG_NAME already exists"
    exit 1
fi

# Display release plan
echo ""
echo "=== RELEASE PLAN ==="
echo "Project: $PROJECT_NAME"
echo "Version: $VERSION"
echo "Tag: $TAG_NAME"
echo "Branch: $CURRENT_BRANCH"
echo "Dry run: $DRY_RUN"
echo "Skip PyPI: $NO_PYPI"
echo ""

if [[ "$DRY_RUN" == "false" ]]; then
    read -p "Proceed with release? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Release cancelled"
        exit 0
    fi
fi

# Pull latest changes
log_info "Pulling latest changes..."
git pull origin "$CURRENT_BRANCH"

# Run tests
log_info "Running comprehensive test suite..."
if ! ./scripts/test.sh; then
    log_error "Tests failed. Cannot proceed with release."
    exit 1
fi

# Build distributions
log_info "Building distributions..."
if ! ./scripts/build.sh; then
    log_error "Build failed. Cannot proceed with release."
    exit 1
fi

# Create git tag
log_info "Creating git tag: $TAG_NAME"
if [[ "$DRY_RUN" == "false" ]]; then
    git tag -a "$TAG_NAME" -m "Release version $VERSION"
    log_success "Created tag: $TAG_NAME"
else
    log_info "[DRY RUN] Would create tag: $TAG_NAME"
fi

# Push tag
log_info "Pushing tag to remote..."
if [[ "$DRY_RUN" == "false" ]]; then
    git push origin "$TAG_NAME"
    log_success "Pushed tag: $TAG_NAME"
else
    log_info "[DRY RUN] Would push tag: $TAG_NAME"
fi

# Optional PyPI publication
if [[ "$NO_PYPI" == "false" ]]; then
    log_info "Publishing to PyPI..."
    if [[ "$DRY_RUN" == "false" ]]; then
        if command -v twine &> /dev/null; then
            log_info "Using twine to publish to PyPI..."
            echo "Note: You'll need to configure PyPI credentials or use API tokens"
            echo "Run: twine upload dist/*"
            log_warning "PyPI upload not automated - run manually if needed"
        else
            log_warning "Twine not found. Install with: uv pip install twine"
        fi
    else
        log_info "[DRY RUN] Would publish to PyPI"
    fi
else
    log_info "Skipping PyPI publication"
fi

# Summary
echo ""
echo "=== RELEASE SUMMARY ==="
echo "✓ Tests passed"
echo "✓ Build completed"
echo "✓ Git tag created: $TAG_NAME"
echo "✓ Tag pushed to remote"
if [[ "$NO_PYPI" == "false" ]]; then
    echo "- PyPI publication: Manual step required"
else
    echo "- PyPI publication: Skipped"
fi
echo ""

if [[ "$DRY_RUN" == "false" ]]; then
    log_success "Release $VERSION completed successfully!"
    log_info "GitHub Actions will automatically:"
    log_info "  - Build distributions"
    log_info "  - Publish to PyPI (if configured)"
    log_info "  - Create GitHub release"
    log_info ""
    log_info "Monitor the progress at: https://github.com/twardoch/twat-video/actions"
else
    log_success "Dry run completed successfully!"
    log_info "Run without --dry-run to create the actual release"
fi