#!/bin/bash
# this_file: scripts/build-binary.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="twat-video"
BINARY_NAME="twat-video"
BUILD_DIR="build-binary"
DIST_DIR="dist-binary"

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
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Build standalone binary executables for ${PROJECT_NAME}"
    echo ""
    echo "Options:"
    echo "  --tool <tool>      # Build tool: pyinstaller (default) or cx-freeze"
    echo "  --onefile          # Create single executable file (default: directory)"
    echo "  --windowed         # Build windowed app (no console)"
    echo "  --clean            # Clean build directories before building"
    echo "  --help             # Show this help"
    echo ""
    echo "Examples:"
    echo "  $0                 # Build with PyInstaller (default)"
    echo "  $0 --onefile       # Build single executable"
    echo "  $0 --tool cx-freeze # Build with cx-freeze"
}

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Parse command line arguments
TOOL="pyinstaller"
ONEFILE=false
WINDOWED=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --tool)
            TOOL="$2"
            shift 2
            ;;
        --onefile)
            ONEFILE=true
            shift
            ;;
        --windowed)
            WINDOWED=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Validate tool
if [[ "$TOOL" != "pyinstaller" && "$TOOL" != "cx-freeze" ]]; then
    log_error "Invalid tool: $TOOL. Use 'pyinstaller' or 'cx-freeze'"
    exit 1
fi

log_info "Building binary with $TOOL..."

# Clean build directories if requested
if [[ "$CLEAN" == "true" ]]; then
    log_info "Cleaning build directories..."
    rm -rf "$BUILD_DIR" "$DIST_DIR" build/ dist-binary/
fi

# Create build directories
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Install binary dependencies
log_info "Installing binary build dependencies..."
uv pip install --upgrade ".[binary]"

# Get the version for the binary
VERSION=$(python -c "import twat_video; print(twat_video.__version__)" 2>/dev/null || echo "unknown")

case "$TOOL" in
    pyinstaller)
        log_info "Building with PyInstaller..."
        
        # Build PyInstaller arguments
        PYINSTALLER_ARGS=(
            "--name=$BINARY_NAME"
            "--workpath=$BUILD_DIR"
            "--distpath=$DIST_DIR"
            "--specpath=$BUILD_DIR"
        )
        
        if [[ "$ONEFILE" == "true" ]]; then
            PYINSTALLER_ARGS+=("--onefile")
        fi
        
        if [[ "$WINDOWED" == "true" ]]; then
            PYINSTALLER_ARGS+=("--windowed")
        fi
        
        # Add version info and icon if available
        if [[ -f "assets/icon.ico" ]]; then
            PYINSTALLER_ARGS+=("--icon=assets/icon.ico")
        fi
        
        # Build the binary
        uv run pyinstaller "${PYINSTALLER_ARGS[@]}" src/twat_video/cli.py
        
        if [[ "$ONEFILE" == "true" ]]; then
            BINARY_PATH="$DIST_DIR/$BINARY_NAME"
        else
            BINARY_PATH="$DIST_DIR/$BINARY_NAME/$BINARY_NAME"
        fi
        ;;
        
    cx-freeze)
        log_info "Building with cx-freeze..."
        
        # Create setup script for cx-freeze
        cat > "$BUILD_DIR/setup_freeze.py" << EOF
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["twat_video"],
    "include_files": [],
    "excludes": [],
    "build_exe": "$DIST_DIR",
}

base = None
if sys.platform == "win32":
    base = "Win32GUI" if $WINDOWED else None

setup(
    name="$BINARY_NAME",
    version="$VERSION",
    description="$PROJECT_NAME standalone binary",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/twat_video/cli.py", base=base, target_name="$BINARY_NAME")]
)
EOF
        
        # Build with cx-freeze
        cd "$BUILD_DIR"
        uv run python setup_freeze.py build
        cd ..
        
        BINARY_PATH="$DIST_DIR/$BINARY_NAME"
        ;;
esac

# Verify binary was created
if [[ -f "$BINARY_PATH" ]] || [[ -f "$BINARY_PATH.exe" ]]; then
    log_success "Binary built successfully!"
    
    # Test the binary
    log_info "Testing binary..."
    if [[ -f "$BINARY_PATH" ]]; then
        chmod +x "$BINARY_PATH"
        if "$BINARY_PATH" --version >/dev/null 2>&1; then
            log_success "Binary test passed!"
        else
            log_warning "Binary test failed - but binary exists"
        fi
    elif [[ -f "$BINARY_PATH.exe" ]]; then
        log_info "Windows binary created: $BINARY_PATH.exe"
    fi
    
    # Show binary info
    log_info "Binary information:"
    if [[ -f "$BINARY_PATH" ]]; then
        ls -lh "$BINARY_PATH"
    elif [[ -f "$BINARY_PATH.exe" ]]; then
        ls -lh "$BINARY_PATH.exe"
    fi
    
    # Show contents of dist directory
    log_info "Distribution directory contents:"
    ls -la "$DIST_DIR"
    
else
    log_error "Binary build failed - no executable found"
    exit 1
fi

log_success "Binary build completed!"
log_info "Binary location: $BINARY_PATH"
log_info "Distribution directory: $DIST_DIR"