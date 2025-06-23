# twat-video: Modern Python Project Scaffold

[![Build & Test](https://github.com/twardoch/twat-video/actions/workflows/push.yml/badge.svg)](https://github.com/twardoch/twat-video/actions/workflows/push.yml)
[![Release](https://github.com/twardoch/twat-video/actions/workflows/release.yml/badge.svg)](https://github.com/twardoch/twat-video/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/twat-video.svg)](https://badge.fury.io/py/twat-video) <!-- TODO: Update once actually published -->

`twat-video` is a template repository that provides a modern scaffolding for Python projects. It's designed to kickstart development with best practices for packaging, testing, linting, type checking, versioning, and CI/CD.

## Rationale

Starting a new Python project often involves repetitive setup of build systems, quality assurance tools, and CI/CD pipelines. This project aims to provide a ready-to-use foundation incorporating:

-   **Modern Packaging:** PEP 621 (`pyproject.toml`) based packaging using [Hatch](https://hatch.pypa.io/) as the build backend.
-   **Fast Dependency Management:** Uses [uv](https://github.com/astral-sh/uv) for fast Python package installation and resolution.
-   **Automated Versioning:** Semantic versioning based on git tags, powered by `hatch-vcs`.
-   **Quality Assurance:**
    -   Linting and formatting with [Ruff](https://github.com/astral-sh/ruff).
    -   Type checking with [MyPy](http://mypy-lang.org/).
    -   Testing with [Pytest](https://pytest.org/).
-   **CI/CD:** GitHub Actions workflows for automated testing, building, and releasing to PyPI.
-   **Pre-commit Hooks:** Ensures code quality before commits.

This scaffold allows developers to focus on writing application logic rather than boilerplate.

## Features

-   PEP 621 compliant `pyproject.toml`.
-   Build backend: Hatchling with `hatch-vcs` for versioning.
-   Package management and virtual environments with `uv`.
-   Comprehensive Hatch scripts for common development tasks (testing, linting, building).
-   Pre-configured Ruff for linting and formatting.
-   Pre-configured MyPy for static type checking.
-   Example Pytest setup with basic tests.
-   GitHub Actions for:
    -   Running linters and type checkers.
    -   Running tests across multiple Python versions.
    -   Building distributions (sdist and wheel).
    -   Publishing to PyPI on tagged commits.
-   Pre-commit hooks for Ruff and MyPy.
-   Clear documentation structure (this README).

## Installation

### For Users (from PyPI)

Once the package is published to PyPI, users can install it using `pip` or `uv`:

```bash
pip install twat-video
```
Or with `uv`:
```bash
uv pip install twat-video
```

*(Note: Replace `twat-video` with your actual package name if you rename this scaffold).*

### For Developers (Editable Install from Local Clone)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/twardoch/twat-video.git # Or your fork
    cd twat-video
    ```

2.  **Set up the development environment:**
    This project uses [Hatch](https://hatch.pypa.io/) for managing development environments and running tasks. It's recommended to install Hatch first. You can use `uv` or `pip` to install Hatch:
    ```bash
    uv pip install hatch  # Recommended
    # or
    # pip install hatch
    ```

3.  **Activate the Hatch environment:**
    Hatch will automatically create and manage a virtual environment for the project using `uv` by default if `uv` is available and configured in `hatch config set dirs.env.virtual.uv true` (or if Hatch's uv feature detection works).
    ```bash
    hatch shell
    ```
    This command drops you into a shell with the project's virtual environment activated and the project installed in editable mode. Dependencies, including development tools, will be installed.

    Alternatively, if you prefer to manage your virtual environment manually (e.g., with `uv venv`):
    ```bash
    uv venv .venv # Create a virtual environment
    source .venv/bin/activate # Activate it
    uv pip install -e .[dev,test] # Install package in editable mode with dev/test dependencies
    ```

## Usage

This scaffold includes placeholder logic. Here's how you might import and use its components:

```python
from twat_video import Config, process_data, main, __version__

# Get the current version (derived from git tags)
print(f"Version: {__version__}")

# Use the example Config dataclass
my_config = Config(name="MyCustomConfig", value=42, options={"detail": True})
print(f"Config: {my_config.name}, Value: {my_config.value}")

# Use the example process_data function
sample_data = ["apple", "banana", 123]
try:
    result = process_data(sample_data, config=my_config, debug=True)
    print(f"Processed Data: {result}")
except ValueError as e:
    print(f"Error processing data: {e}")

# The main() function can be called to run the example script logic
# main()
```

Replace this placeholder logic with your project's actual functionality.

## Development

This project uses [Hatch](https://hatch.pypa.io/) for most development tasks, which in turn utilizes `uv` for faster environment and package management where configured.

### Initial Setup

1.  **Install Hatch:**
    ```bash
    uv pip install hatch  # Or pip install hatch
    ```
2.  **Install pre-commit hooks** (optional but recommended):
    Ensure `pre-commit` is installed (`uv pip install pre-commit` or `pip install pre-commit`), then run:
    ```bash
    pre-commit install
    ```
    This will run checks automatically before each commit.

### Hatch Environments and Scripts

Hatch environments are defined in `pyproject.toml`. You can activate the default environment (which includes test and linting tools) using:

```bash
hatch shell
```

Common tasks are available as Hatch scripts:

-   **Run tests:**
    ```bash
    hatch run default:test
    # or with specific pytest arguments:
    # hatch run default:test -- -k "some_test_name"
    ```

-   **Run tests with coverage:**
    ```bash
    hatch run default:test-cov
    ```
    (Coverage configuration is in `pyproject.toml` under `[tool.coverage]`)

-   **Run linters (Ruff check and format check):**
    ```bash
    hatch run default:lint
    ```

-   **Apply formatting (Ruff format):**
    ```bash
    hatch run default:format
    ```

-   **Run type checker (MyPy):**
    ```bash
    hatch run default:type-check
    ```

-   **Build distributions (sdist and wheel):**
    ```bash
    hatch build
    ```
    Outputs will be in the `dist/` directory.

-   **Clean build artifacts:**
    ```bash
    hatch clean
    ```

-   **Update development tools (pytest, mypy, ruff):**
    ```bash
    hatch run default:tools-install
    ```

There's also a dedicated `lint` environment for more focused linting tasks (e.g., in CI):
```bash
hatch run lint:all # Runs all linting and typing checks
hatch run lint:style # Runs ruff check and ruff format --check
hatch run lint:fmt # Applies formatting and fixes with ruff
hatch run lint:typing # Runs mypy
```

Refer to `pyproject.toml` under `[tool.hatch.envs.*.scripts]` for all available scripts.

## Codebase Structure (Technical Explanation)

-   **`.github/workflows/`**: Contains GitHub Actions workflows.
    -   `push.yml`: Runs on pushes and pull requests to `main`. Executes linters, type checkers, and tests across multiple Python versions. Also builds the package.
    -   `release.yml`: Runs on tagged commits (e.g., `v1.2.3`). Builds and publishes the package to PyPI.
-   **`.gitignore`**: Specifies intentionally untracked files that Git should ignore.
-   **`.pre-commit-config.yaml`**: Configuration for pre-commit hooks (Ruff, MyPy).
-   **`LICENSE`**: Project license file (default is MIT).
-   **`README.md`**: This file – project documentation.
-   **`pyproject.toml`**: The heart of the project configuration.
    -   `[build-system]`: Specifies build dependencies (Hatchling, hatch-vcs).
    -   `[project]`: PEP 621 metadata (name, version (dynamic), dependencies, classifiers, etc.).
    -   `[tool.hatch.version]`: Configures `hatch-vcs` to derive version from git tags.
    -   `[tool.hatch.build.hooks.vcs]`: Tells `hatch-vcs` where to write the version file (`src/twat_video/__version__.py`).
    -   `[tool.hatch.envs.*]`: Defines Hatch environments and scripts for development tasks (e.g., `default`, `lint`, `test`).
    -   `[tool.ruff]`: Configuration for Ruff linter and formatter.
    -   `[tool.mypy]`: Configuration for MyPy static type checker.
    -   `[tool.pytest.ini_options]`: Configuration for Pytest.
    -   `[tool.coverage]`: Configuration for code coverage.
-   **`src/twat_video/`**: Main package source code directory.
    -   `__init__.py`: Makes the directory a package and exposes public interfaces. Imports version from `__version__.py`.
    -   `__version__.py`: Version file automatically generated by `hatch-vcs` during the build process. **Do not edit manually.**
    -   `twat_video.py`: Example module with placeholder logic.
-   **`tests/`**: Contains test files.
    -   `test_twat_video.py`: Example tests for the placeholder logic.

## Contribution Guidelines

Contributions are welcome! Please follow these guidelines:

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally: `git clone https://github.com/YOUR_USERNAME/twat-video.git`
3.  **Set up the development environment** as described in the "Development" section (install Hatch, run `hatch shell`).
4.  **Install pre-commit hooks:** `pre-commit install`
5.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/your-bug-fix`.
6.  **Make your changes.** Write code, add tests, and update documentation as needed.
7.  **Ensure code quality:**
    -   Run linters: `hatch run default:lint`
    -   Apply formatting: `hatch run default:format`
    -   Run type checker: `hatch run default:type-check`
    -   Run tests: `hatch run default:test` (ensure all tests pass and coverage is maintained or improved).
    -   Pre-commit hooks should also run automatically when you `git commit`.
8.  **Commit your changes** with a clear and descriptive commit message.
9.  **Push your branch** to your fork: `git push origin feature/your-feature-name`.
10. **Create a Pull Request** from your fork's branch to the `main` branch of the original `twardoch/twat-video` repository.
11. **Wait for CI checks** to pass and for a review. Address any feedback.

### Versioning and Releases

-   This project uses **semantic versioning (SemVer)**.
-   The version is automatically determined from `git` tags using `hatch-vcs`.
-   To make a new release:
    1.  Ensure all changes are merged to `main` and `main` is up-to-date locally.
    2.  Create an annotated git tag: `git tag -a vX.Y.Z -m "Version X.Y.Z"` (e.g., `git tag -a v0.1.0 -m "Version 0.1.0"`).
    3.  Push the tag to GitHub: `git push origin vX.Y.Z`.
    4.  The `release.yml` GitHub Actions workflow will automatically build the package and publish it to PyPI. It will also create a GitHub Release.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---

*This README provides a comprehensive overview. Adapt and update it as your project evolves.*
