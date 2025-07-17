# Development Guide

This guide covers the development workflow, tools, and practices for the twat-video project.

## Quick Start

1. **Set up development environment:**
   ```bash
   ./scripts/dev.sh setup
   ```

2. **Run tests:**
   ```bash
   ./scripts/test.sh
   ```

3. **Build the project:**
   ```bash
   ./scripts/build.sh
   ```

## Project Structure

```
twat-video/
├── src/twat_video/           # Main package source code
│   ├── __init__.py          # Package initialization
│   ├── twat_video.py        # Core functionality
│   ├── cli.py               # Command-line interface
│   └── __version__.py       # Auto-generated version file
├── tests/                   # Test suite
│   ├── test_twat_video.py   # Core functionality tests
│   ├── test_cli.py          # CLI tests
│   └── test_integration.py  # Integration tests
├── scripts/                 # Development and build scripts
│   ├── build.sh             # Build distributions
│   ├── build-binary.sh      # Build standalone binaries
│   ├── test.sh              # Run comprehensive tests
│   ├── release.sh           # Create releases
│   └── dev.sh               # Development helper
├── .github/workflows/       # GitHub Actions CI/CD
│   ├── push.yml             # Build and test on push
│   └── release.yml          # Release on git tags
└── pyproject.toml          # Project configuration
```

## Development Scripts

### `./scripts/dev.sh`
Development helper script with multiple commands:

- `setup` - Set up development environment
- `clean` - Clean build artifacts
- `lint` - Run linting checks
- `format` - Format code
- `test` - Run tests
- `build` - Build distributions
- `version` - Show version information

### `./scripts/test.sh`
Comprehensive test runner that:
- Runs linting (Ruff)
- Checks code formatting
- Runs type checking (MyPy)
- Executes test suite with coverage
- Generates coverage reports

### `./scripts/build.sh`
Build script that:
- Cleans previous builds
- Installs build dependencies
- Creates wheel and source distributions
- Validates built packages

### `./scripts/build-binary.sh`
Binary build script that:
- Builds standalone executables using PyInstaller
- Supports multiple platforms
- Creates single-file executables
- Tests built binaries

### `./scripts/release.sh`
Release script that:
- Validates git state
- Runs comprehensive tests
- Creates git tags
- Triggers automated releases

## Testing

### Test Categories

1. **Unit Tests** (`test_twat_video.py`)
   - Core functionality testing
   - Configuration handling
   - Data processing logic
   - Error handling

2. **CLI Tests** (`test_cli.py`)
   - Command-line interface
   - Argument parsing
   - Error handling
   - Integration with core functionality

3. **Integration Tests** (`test_integration.py`)
   - End-to-end workflows
   - Cross-module integration
   - Performance testing
   - Environment compatibility

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Run specific test file
pytest tests/test_twat_video.py -v

# Run with coverage
pytest --cov=src/twat_video --cov-report=html tests/

# Run performance tests
pytest tests/ -m benchmark --benchmark-only
```

## Code Quality

### Linting and Formatting

- **Ruff**: Used for linting and code formatting
- **MyPy**: Static type checking
- **Pre-commit**: Automated checks before commits

### Configuration

All tools are configured in `pyproject.toml`:

- `[tool.ruff]` - Linting and formatting rules
- `[tool.mypy]` - Type checking configuration
- `[tool.pytest.ini_options]` - Test configuration
- `[tool.coverage]` - Coverage reporting

### Pre-commit Hooks

Set up pre-commit hooks to ensure code quality:

```bash
./scripts/dev.sh pre-commit
```

## Build System

### Python Package Build

The project uses modern Python packaging:

- **Build backend**: Hatchling
- **Version management**: hatch-vcs (git-tag based)
- **Distribution**: PyPI compatible wheel and sdist

### Binary Build

Standalone executables are built using:

- **PyInstaller**: Primary tool for binary creation
- **cx-Freeze**: Alternative build tool
- **Multiplatform**: Linux, Windows, macOS support

## CI/CD Pipeline

### GitHub Actions Workflows

1. **Push Workflow** (`.github/workflows/push.yml`)
   - Triggered on push/PR to main
   - Runs quality checks (linting, formatting, type checking)
   - Executes tests across multiple Python versions and platforms
   - Builds distributions and binaries
   - Uploads artifacts

2. **Release Workflow** (`.github/workflows/release.yml`)
   - Triggered on git tags (v*)
   - Builds Python packages
   - Creates multiplatform binaries
   - Publishes to PyPI
   - Creates GitHub releases with artifacts

### Supported Platforms

- **Python versions**: 3.10, 3.11, 3.12
- **Operating systems**: Ubuntu, Windows, macOS
- **Architectures**: x86_64

## Release Process

### Semantic Versioning

The project follows semantic versioning (semver):

- **Major** (X.0.0): Breaking changes
- **Minor** (X.Y.0): New features, backward compatible
- **Patch** (X.Y.Z): Bug fixes, backward compatible

### Creating a Release

1. **Ensure clean state:**
   ```bash
   git status  # Should be clean
   git checkout main
   git pull origin main
   ```

2. **Run release script:**
   ```bash
   ./scripts/release.sh 1.0.0  # Replace with desired version
   ```

3. **Monitor automation:**
   - GitHub Actions will automatically build and publish
   - Check the Actions tab for progress
   - Verify PyPI publication
   - Check GitHub releases

### Manual Release Steps

If needed, you can perform manual steps:

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Build and publish manually
./scripts/build.sh
twine upload dist/*
```

## Development Workflow

### Contributing

1. **Fork and clone:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/twat-video.git
   cd twat-video
   ```

2. **Set up environment:**
   ```bash
   ./scripts/dev.sh setup
   ```

3. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature
   ```

4. **Develop and test:**
   ```bash
   # Make your changes
   ./scripts/dev.sh format  # Format code
   ./scripts/dev.sh test    # Run tests
   ```

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature
   ```

6. **Create pull request:**
   - Open PR on GitHub
   - Wait for CI checks
   - Address review feedback

### Best Practices

- **Write tests** for new functionality
- **Update documentation** as needed
- **Follow code style** (enforced by Ruff)
- **Use type hints** (checked by MyPy)
- **Keep commits focused** and descriptive
- **Test across platforms** when possible

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure package is installed in development mode
2. **Test failures**: Check if dependencies are up to date
3. **Build failures**: Verify build tools are installed
4. **Binary issues**: Check PyInstaller compatibility

### Debug Tips

- Use `--verbose` flag for detailed output
- Check GitHub Actions logs for CI failures
- Run tests locally before pushing
- Use `./scripts/dev.sh clean` to reset environment

## Tools and Dependencies

### Development Tools

- **uv**: Fast Python package manager
- **Hatch**: Build system and environment management
- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **PyInstaller**: Binary building
- **Pre-commit**: Git hooks

### Optional Dependencies

- **pytest-benchmark**: Performance testing
- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel test execution

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)