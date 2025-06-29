# twat-video: Modern Python Project Scaffold & Toolkit

[![Build & Test](https://github.com/twardoch/twat-video/actions/workflows/push.yml/badge.svg)](https://github.com/twardoch/twat-video/actions/workflows/push.yml)
[![Release](https://github.com/twardoch/twat-video/actions/workflows/release.yml/badge.svg)](https://github.com/twardoch/twat-video/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/twat-video.svg)](https://badge.fury.io/py/twat-video)

**`twat-video` is a comprehensive template repository and toolkit designed to accelerate the development of modern Python projects. It provides a robust foundation built upon current best practices for packaging, dependency management, code quality, testing, and automated workflows.**

This project serves as both a ready-to-use scaffold for new Python applications and libraries, and an example of integrating modern Python development tools.

## Part 1: For a Wider Audience

### What is `twat-video`?

At its core, `twat-video` is a **project starter template**. Think of it as a pre-configured blueprint for your next Python project. Instead of setting up build systems, linters, testers, and automation from scratch, `twat-video` gives you a fully equipped workshop.

It also includes a sample Python module (`src/twat_video/twat_video.py`) that demonstrates some of these features and can be replaced with your actual project code.

### Who is it for?

`twat-video` is for **Python developers** who want to:

*   Quickly bootstrap new projects.
*   Adhere to modern Python development standards.
*   Incorporate best practices for code quality and maintainability from day one.
*   Spend more time writing application logic and less time on project setup.
*   Learn how to use tools like Hatch, `uv`, Ruff, MyPy, and GitHub Actions effectively.

Whether you're building a small utility, a complex library, or a web application, `twat-video` provides a solid starting point.

### Why is it useful?

Starting a Python project correctly involves many decisions and setup tasks. `twat-video` simplifies this by providing:

*   **Speed & Efficiency:** Get your project up and running in minutes, not hours.
*   **Best Practices Included:** Built-in support for modern packaging (PEP 621), linting, formatting, type checking, and testing.
*   **Fast Dependency Management:** Utilizes `uv` for rapid package installation and virtual environment management.
*   **Automated Quality Checks:** Pre-commit hooks and CI pipelines ensure code quality before and after changes are integrated.
*   **Reproducible Builds:** Consistent development and build environments using Hatch.
*   **Automated Versioning & Release:** Semantic versioning based on git tags and automated publishing to PyPI.
*   **Learning Resource:** Serves as a practical example of a well-structured Python project.

### Installation and Setup

There are two main ways to use `twat-video`: as a template for a new project, or by cloning it to explore its features.

#### Using `twat-video` as a Template (Recommended for New Projects)

1.  **Create a new repository from this template:**
    *   Navigate to the [main page of the `twat-video` repository](https://github.com/twardoch/twat-video) on GitHub.
    *   Click the "Use this template" button and select "Create a new repository".
    *   Choose an owner, repository name, and other settings for your new project.

2.  **Clone your newly created repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_NEW_REPOSITORY_NAME.git
    cd YOUR_NEW_REPOSITORY_NAME
    ```

3.  **Set up the development environment:**
    This project uses [Hatch](https://hatch.pypa.io/) for environment and project management. It's recommended to install Hatch first. `uv` is used by Hatch for faster operations if available.
    ```bash
    # Install Hatch (using uv is recommended)
    uv pip install hatch
    # Or using pip
    # python -m pip install hatch
    ```
    Once Hatch is installed, activate the project's managed environment:
    ```bash
    hatch shell
    ```
    This command creates a virtual environment (using `uv` if configured), installs all dependencies (including development tools), and makes your project editable within this environment.

#### For Developers (Exploring or Contributing to `twat-video` itself)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/twardoch/twat-video.git
    cd twat-video
    ```

2.  **Set up the development environment (as above):**
    ```bash
    uv pip install hatch  # Or pip install hatch
    hatch shell
    ```

### How to Use It

#### As a Project Scaffold

Once you've created your project from the template and activated the Hatch shell:

1.  **Rename the package:**
    *   The default package name is `twat_video`. You'll likely want to rename this to match your project.
    *   Search and replace `twat_video` and `twat-video` (in `pyproject.toml` and directory names) with your desired project name.
    *   Key files/directories to update:
        *   `src/twat_video` directory -> `src/your_package_name`
        *   `pyproject.toml`:
            *   `name = "twat-video"` -> `name = "your-project-name"`
            *   `tool.hatch.build.targets.wheel.packages = ["src/twat_video"]` -> `tool.hatch.build.targets.wheel.packages = ["src/your_package_name"]`
            *   `tool.hatch.build.hooks.vcs.version-file = "src/twat_video/__version__.py"` -> `tool.hatch.build.hooks.vcs.version-file = "src/your_package_name/__version__.py"`
            *   References in `[tool.ruff.lint.isort]`, `[tool.coverage.run]`, `[tool.coverage.paths]`.
        *   `tests/` directory: update imports.
        *   `src/your_package_name/__init__.py`: update imports if necessary.
        *   GitHub Workflows (`.github/workflows/*.yml`): update paths if they reference `src/twat_video`.

2.  **Customize `pyproject.toml`:**
    *   Update metadata like `description`, `authors`, `keywords`, etc.
    *   Add your project's runtime dependencies to the `[project.dependencies]` list.

3.  **Develop your code:**
    *   Replace the example code in `src/your_package_name/your_module.py` (formerly `src/twat_video/twat_video.py`) with your actual application logic.
    *   Add new modules and packages within `src/your_package_name/` as needed.

4.  **Write tests:**
    *   Add your tests to the `tests/` directory. The example `tests/test_twat_video.py` can be a starting point.

#### Interacting with the Example Code (Programmatic Usage)

The included `twat_video.py` module provides a simple `Config` dataclass, a `process_data` function, and a `main` function to demonstrate basic structure and logging.

```python
from twat_video import Config, process_data, main, __version__ # Or your_package_name

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

#### Development Tasks (CLI with Hatch)

Hatch scripts simplify common development tasks. Run these within the activated Hatch shell (`hatch shell`):

*   **Run tests:**
    ```bash
    hatch run test  # Uses uv run pytest ...
    ```
*   **Run linters and formatters:**
    ```bash
    hatch run lint   # Runs Ruff check and format check
    hatch run format # Applies Ruff formatting
    ```
*   **Run type checker:**
    ```bash
    hatch run type-check # Runs MyPy
    ```
*   **Build distributions:**
    ```bash
    hatch build
    ```
    (Outputs will be in `dist/`)

Refer to the "Hatch Environments and Scripts" section in Part 2 for more details.

## Part 2: Technical Details

This section describes how the `twat-video` scaffold is structured and how its components work together.

### Code Architecture

*   **`pyproject.toml`**: This is the central configuration file for the project, adhering to PEP 517, PEP 518, and PEP 621.
    *   **`[build-system]`**: Defines the build backend (Hatchling) and its requirements (`hatch-vcs` for versioning).
    *   **`[project]`**: Contains project metadata such as name, dynamic version, dependencies, Python version compatibility, license, and classifiers.
    *   **`[tool.hatch.version]`**: Configures `hatch-vcs` to derive the project version dynamically from `git` tags. The version format follows Semantic Versioning.
    *   **`[tool.hatch.build.hooks.vcs]`**: Specifies the file where `hatch-vcs` writes the version information (e.g., `src/twat_video/__version__.py`). This file should not be manually edited and is typically gitignored (though tracked if it's essential for non-VCS builds).
    *   **`[tool.hatch.envs.*]`**: Defines Hatch environments for development, testing, and linting, along with scripts for common tasks. These scripts often leverage `uv` for faster execution.
    *   **`[tool.ruff]`**: Configuration for the [Ruff](https://github.com/astral-sh/ruff) linter and formatter, including selected rules, line length, and target Python version.
    *   **`[tool.mypy]`**: Configuration for the [MyPy](http://mypy-lang.org/) static type checker.
    *   **`[tool.pytest.ini_options]`**: Settings for [Pytest](https://pytest.org/), such as test paths and markers.
    *   **`[tool.coverage]`**: Configuration for code coverage analysis with `pytest-cov`.

*   **`src/twat_video/`** (or `src/your_package_name/`): This directory contains the main source code of the Python package.
    *   `__init__.py`: Makes the directory a Python package. It typically imports key components from other modules within the package and defines `__all__` to control what `import *` exposes. It also imports `__version__` from the `__version__.py` file.
    *   `__version__.py`: This file is automatically generated or updated by `hatch-vcs` during the build process (and potentially on version bumps if configured). It contains the `__version__` string. **Do not edit this file manually.**
    *   `twat_video.py` (example module): Contains placeholder logic, including a `Config` dataclass, a `process_data` function, and a `main` entry point. This is where you'd start replacing or adding your project's code.

*   **`tests/`**: This directory houses all automated tests.
    *   `test_twat_video.py` (example tests): Provides basic unit tests for the example logic in `twat_video.py` using Pytest.

### Development Workflow & Quality Assurance

`twat-video` is designed for a streamlined development workflow with a strong emphasis on code quality.

*   **Hatch Environments:**
    Hatch manages isolated development environments defined in `pyproject.toml`.
    *   `default`: The primary environment for general development, including tools for testing, linting, and type checking. Activate with `hatch shell`.
    *   `lint`: A specialized environment for linting and formatting tasks, often used in CI. Access its scripts via `hatch run lint:<script_name>`.
    *   `test`: A specialized environment for running tests, often used in CI. Access its scripts via `hatch run test:<script_name>`.
    Hatch uses `uv` by default (if available and configured via `hatch config set dirs.env.virtual.uv true` or auto-detected) for creating and managing these environments, significantly speeding up dependency installation.

*   **Hatch Scripts:**
    Common tasks are automated via scripts defined under `[tool.hatch.envs.*.scripts]` in `pyproject.toml`. These are typically run using `hatch run <env_name>:<script_name>` or simply `hatch run <script_name>` if the script is in the `default` environment and you're in the Hatch shell.
    *   `test`: `uv run pytest {args:tests}` - Runs Pytest.
    *   `test-cov`: `uv run pytest --cov...` - Runs Pytest with coverage.
    *   `type-check`: `uv run mypy src/twat_video tests` - Runs MyPy.
    *   `lint`: Combines `ruff check` and `ruff format --check`.
    *   `format`: `uv run ruff format src/twat_video tests` - Applies Ruff formatting.
    *   `build`: `hatch build` - Creates sdist and wheel distributions in `dist/`.
    *   `clean`: `hatch clean` - Removes build artifacts.

*   **Pre-commit Hooks (`.pre-commit-config.yaml`):**
    To ensure code quality *before* changes are committed, pre-commit hooks are configured.
    1.  Install pre-commit: `uv pip install pre-commit` (or `pip install pre-commit`).
    2.  Install hooks: `pre-commit install`.
    This setup automatically runs Ruff (for linting and formatting) and MyPy (for type checking) on staged files during `git commit`. This helps catch issues early and maintain consistent code style.
    The configuration includes:
    *   Ruff for formatting and linting.
    *   MyPy for static type checking.
    *   Standard hooks like `check-yaml`, `check-toml`, `check-added-large-files`.

### CI/CD Pipeline (GitHub Actions)

The `.github/workflows/` directory contains GitHub Actions workflows for continuous integration and deployment.

*   **`push.yml` (Build & Test Workflow):**
    *   **Triggers:** Runs on pushes and pull requests to the `main` branch. Also runnable via `workflow_dispatch`.
    *   **Jobs:**
        1.  `quality`:
            *   Checks out code.
            *   Runs Ruff linter (`ruff check`).
            *   Runs Ruff formatter check (`ruff format --check`).
            *   Sets up Python and installs MyPy.
            *   Runs MyPy for static type checking on `src` and `tests`.
        2.  `test`: (Depends on `quality`)
            *   Runs in a matrix across multiple Python versions (e.g., 3.10, 3.11, 3.12) and OS (e.g., ubuntu-latest).
            *   Sets up Python and `uv`.
            *   Installs test dependencies using `uv pip install .[test]`.
            *   Runs Pytest with coverage, generating an XML coverage report.
            *   Uploads the coverage report as an artifact.
        3.  `build`: (Depends on `test`)
            *   Sets up Python and `uv`.
            *   Installs build tools (`build`, `hatchling`, `hatch-vcs`).
            *   Builds sdist and wheel distributions using `python -m build`.
            *   Uploads distribution files as an artifact.

*   **`release.yml` (Release Workflow):**
    *   **Triggers:** Runs when a new tag matching the pattern `v*` (e.g., `v0.1.0`) is pushed.
    *   **Permissions:** Requires `id-token: write` for OIDC publication to PyPI and `contents: write` for creating GitHub Releases.
    *   **Environment:** Configured for PyPI publishing, requiring a `PYPI_TOKEN` secret.
    *   **Jobs:**
        1.  `release`:
            *   Checks out code (fetches all history for `hatch-vcs`).
            *   Sets up Python and `uv`.
            *   Installs build tools.
            *   Builds sdist and wheel distributions.
            *   Verifies that distribution files were created.
            *   Publishes the distributions to PyPI using `pypa/gh-action-pypi-publish`.
            *   Creates a GitHub Release using `softprops/action-gh-release`, automatically generating release notes from commits since the last tag.

### Coding and Contribution Rules

Contributions are highly encouraged! Please adhere to the following:

1.  **Fork the Repository:** Create your own fork of `twat-video` on GitHub.
2.  **Clone Your Fork:** `git clone https://github.com/YOUR_USERNAME/twat-video.git`
3.  **Set Up Environment:**
    ```bash
    uv pip install hatch # if not already installed
    cd twat-video
    hatch shell
    ```
4.  **Install Pre-commit Hooks:**
    ```bash
    uv pip install pre-commit
    pre-commit install
    ```
5.  **Create a Feature Branch:** `git checkout -b feature/your-amazing-feature` or `bugfix/fix-that-bug`.
6.  **Develop:**
    *   Write clean, maintainable code.
    *   Include comprehensive tests for new features or bug fixes in the `tests/` directory.
    *   Update documentation (README.md, docstrings, etc.) as necessary.
7.  **Ensure Quality:**
    *   **Formatting & Linting:** Run `hatch run format` and `hatch run lint`. Pre-commit hooks should handle this automatically.
    *   **Type Checking:** Run `hatch run type-check`. Ensure MyPy passes.
    *   **Tests:** Run `hatch run test`. Ensure all tests pass and coverage is maintained or improved.
8.  **Commit Changes:** Write clear, descriptive commit messages.
9.  **Push to Your Fork:** `git push origin feature/your-amazing-feature`.
10. **Create a Pull Request (PR):** Submit a PR from your fork's branch to the `main` branch of the original `twardoch/twat-video` repository.
11. **CI Checks & Review:** Ensure all CI checks pass on your PR. Address any feedback from reviewers.

#### Versioning and Releases

*   This project follows **Semantic Versioning (SemVer)** (e.g., `vX.Y.Z`).
*   The version is dynamically managed by `hatch-vcs` based on `git` tags.
*   To make a new release:
    1.  Ensure all changes are merged into the `main` branch.
    2.  Pull the latest `main` branch locally: `git checkout main && git pull origin main`.
    3.  Create an annotated git tag: `git tag -a vX.Y.Z -m "Release version X.Y.Z"` (e.g., `git tag -a v0.1.0 -m "Release version 0.1.0"`).
    4.  Push the tag to GitHub: `git push origin vX.Y.Z`.
    5.  The `release.yml` GitHub Actions workflow will automatically build the package, publish it to PyPI, and create a GitHub Release.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*This README provides a comprehensive overview of the `twat-video` project scaffold. Adapt and update it as your project evolves from this template.*
