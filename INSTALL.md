# Installation Guide

This guide covers different ways to install and use twat-video.

## Table of Contents

- [Quick Installation](#quick-installation)
- [Installation Methods](#installation-methods)
  - [From PyPI](#from-pypi)
  - [From Source](#from-source)
  - [Binary Downloads](#binary-downloads)
- [Development Installation](#development-installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Quick Installation

### Python Package (Recommended)

```bash
pip install twat-video
```

### Binary Download

Download the appropriate binary for your system from the [releases page](https://github.com/twardoch/twat-video/releases):

- **Linux**: `twat-video-linux-x64`
- **Windows**: `twat-video-windows-x64.exe`
- **macOS**: `twat-video-macos-x64`

## Installation Methods

### From PyPI

Install the latest stable version:

```bash
pip install twat-video
```

Install a specific version:

```bash
pip install twat-video==1.0.0
```

Install with all optional dependencies:

```bash
pip install "twat-video[all]"
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/twat-video.git
   cd twat-video
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev,test]"
   ```

3. Run tests to verify installation:
   ```bash
   pytest
   ```

### Binary Downloads

Binary distributions are available for each release and don't require Python to be installed.

1. Download the appropriate binary from the [releases page](https://github.com/twardoch/twat-video/releases)

2. Make it executable (Linux/macOS):
   ```bash
   chmod +x twat-video-linux-x64  # or twat-video-macos-x64
   ```

3. Optionally, move to a directory in your PATH:
   ```bash
   sudo mv twat-video-linux-x64 /usr/local/bin/twat-video
   ```

## Development Installation

For contributors and developers:

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/twat-video.git
   cd twat-video
   ```

2. Set up development environment:
   ```bash
   ./scripts/dev.sh setup
   ```

3. Run the test suite:
   ```bash
   ./scripts/test.sh
   ```

4. Build the package:
   ```bash
   ./scripts/build.sh
   ```

## Usage

### Command Line Interface

After installation, you can use the CLI:

```bash
# Show version
twat-video --version

# Show help
twat-video --help

# Process data
twat-video process item1 item2 item3

# Run demo
twat-video demo

# Generate config file
twat-video config --output-file config.yml
```

### Python API

```python
from twat_video import Config, process_data

# Create configuration
config = Config(
    name="my_config",
    value=42,
    options={"feature": True}
)

# Process data
result = process_data(["item1", "item2"], config=config)
print(result)
```

### Advanced Usage

```python
from twat_video import Config, process_data, main

# Run with debug mode
result = process_data(
    ["data1", "data2"], 
    config=Config(name="debug_config"),
    debug=True
)

# Run the main demo
main()
```

## Requirements

### Python Package Requirements

- Python 3.10 or higher
- Dependencies are automatically installed with pip

### Binary Requirements

- No Python installation required
- Compatible with:
  - Linux x86_64
  - Windows x86_64
  - macOS x86_64

## Troubleshooting

### Common Issues

#### ImportError: No module named 'twat_video'

**Solution**: Make sure the package is installed:
```bash
pip install twat-video
```

#### Permission denied (Binary)

**Solution**: Make the binary executable:
```bash
chmod +x twat-video-linux-x64
```

#### Version conflicts

**Solution**: Use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install twat-video
```

### Development Issues

#### Tests failing

**Solution**: Install test dependencies:
```bash
pip install ".[test]"
```

#### Build errors

**Solution**: Install build dependencies:
```bash
pip install ".[build]"
```

### Getting Help

- Check the [README](README.md) for detailed documentation
- View [examples](examples/) for usage patterns
- Report issues on [GitHub Issues](https://github.com/twardoch/twat-video/issues)

## Verification

Verify your installation:

```bash
# Python package
python -c "import twat_video; print(twat_video.__version__)"

# CLI
twat-video --version

# Binary
./twat-video-linux-x64 --version  # Adjust filename for your platform
```

## Uninstallation

### Python Package

```bash
pip uninstall twat-video
```

### Binary

Simply delete the binary file:

```bash
rm /usr/local/bin/twat-video  # Or wherever you installed it
```

## Next Steps

- Read the [README](README.md) for comprehensive documentation
- Check out the [examples](examples/) directory
- Explore the [API documentation](https://twat-video.readthedocs.io/) (if available)
- Join the community discussions on [GitHub Discussions](https://github.com/twardoch/twat-video/discussions)