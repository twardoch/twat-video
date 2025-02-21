#!/usr/bin/env -S uv run -s
# /// script
# dependencies = [
#   "ruff>=0.9.6",
#   "pytest>=8.3.4",
#   "mypy>=1.15.0",
# ]
# ///
# this_file: cleanup.py

"""
Cleanup tool for managing repository tasks and maintaining code quality.

This script provides a comprehensive set of commands for repository maintenance:

When to use each command:

- `cleanup.py status`: Use this FIRST when starting work to check the current state
  of the repository. It shows file structure, git status, and runs all code quality
  checks. Run this before making any changes to ensure you're starting from a clean state.

- `cleanup.py venv`: Run this when setting up the project for the first time or if
  your virtual environment is corrupted/missing. Creates a new virtual environment
  using uv.

- `cleanup.py install`: Use after `venv` or when dependencies have changed. Installs
  the package and all development dependencies in editable mode.

- `cleanup.py update`: Run this when you've made changes and want to commit them.
  It will:
  1. Show current status (like `status` command)
  2. Stage and commit any changes with a generic message
  Use this for routine maintenance commits.

- `cleanup.py push`: Run this after `update` when you want to push your committed
  changes to the remote repository.

Workflow Example:
1. Start work: `cleanup.py status`
2. Make changes to code
3. Commit changes: `cleanup.py update`
4. Push to remote: `cleanup.py push`

The script maintains a CLEANUP.log file that records all operations with timestamps.
It also includes content from README.md at the start and TODO.md at the end of logs
for context.

Required Files:
- LOG.md: Project changelog
- README.md: Project documentation
- TODO.md: Pending tasks and future plans
"""

import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn

# Configuration
IGNORE_PATTERNS = [
    ".git",
    ".venv",
    "__pycache__",
    "*.pyc",
    "dist",
    "build",
    "*.egg-info",
]
REQUIRED_FILES = ["LOG.md", ".cursor/rules/0project.mdc", "TODO.md"]
LOG_FILE = Path("CLEANUP.log")

# Ensure we're working from the script's directory
os.chdir(Path(__file__).parent)


def new() -> None:
    """Remove existing log file."""
    if LOG_FILE.exists():
        LOG_FILE.unlink()


def prefix() -> None:
    """Write README.md content to log file."""
    readme = Path(".cursor/rules/0project.mdc")
    if readme.exists():
        log_message("\n=== PROJECT STATEMENT ===")
        content = readme.read_text()
        log_message(content)


def suffix() -> None:
    """Write TODO.md content to log file."""
    todo = Path("TODO.md")
    if todo.exists():
        log_message("\n=== TODO.md ===")
        content = todo.read_text()
        log_message(content)


def log_message(message: str) -> None:
    """Log a message to file and console with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {message}\n"
    with LOG_FILE.open("a") as f:
        f.write(log_line)


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            log_message(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        log_message(f"Command failed: {' '.join(cmd)}")
        log_message(f"Error: {e.stderr}")
        if check:
            raise
        return subprocess.CompletedProcess(cmd, 1, "", str(e))


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in the system."""
    try:
        subprocess.run(["which", cmd], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


class Cleanup:
    """Main cleanup tool class."""

    def __init__(self) -> None:
        self.workspace = Path.cwd()

    def _print_header(self, message: str) -> None:
        """Print a section header."""
        log_message(f"\n=== {message} ===")

    def _check_required_files(self) -> bool:
        """Check if all required files exist."""
        missing = False
        for file in REQUIRED_FILES:
            if not (self.workspace / file).exists():
                log_message(f"Error: {file} is missing")
                missing = True
        return not missing

    def _generate_tree(self) -> None:
        """Generate and display tree structure of the project."""
        if not check_command_exists("tree"):
            log_message("Warning: 'tree' command not found. Skipping tree generation.")
            return None

        try:
            run_command(["sh", "filetree.sh"])
            with open(".cursor/rules/filetree.mdc") as f:
                log_message("\nProject structure:")
                log_message(f.read())
        except Exception as e:
            log_message(f"Failed to generate tree: {e}")
        return None

    def _git_status(self) -> bool:
        """Check git status and return True if there are changes."""
        result = run_command(["git", "status", "--porcelain"], check=False)
        return bool(result.stdout.strip())

    def _venv(self) -> None:
        """Create and activate virtual environment using uv."""
        log_message("Setting up virtual environment")
        try:
            run_command(["uv", "venv"])
            # Activate the virtual environment
            venv_path = self.workspace / ".venv" / "bin" / "activate"
            if venv_path.exists():
                os.environ["VIRTUAL_ENV"] = str(self.workspace / ".venv")
                os.environ["PATH"] = (
                    f"{self.workspace / '.venv' / 'bin'}{os.pathsep}{os.environ['PATH']}"
                )
                log_message("Virtual environment created and activated")
            else:
                log_message("Virtual environment created but activation failed")
        except Exception as e:
            log_message(f"Failed to create virtual environment: {e}")

    def _install(self) -> None:
        """Install package in development mode with all extras."""
        log_message("Installing package with all extras")
        try:
            self._venv()
            run_command(["uv", "pip", "install", "-e", ".[test,dev]"])
            log_message("Package installed successfully")
        except Exception as e:
            log_message(f"Failed to install package: {e}")

    def _run_checks(self) -> None:
        """Run code quality checks using ruff and pytest."""
        log_message("Running code quality checks")

        try:
            # Run ruff checks
            log_message(">>> Running code fixes...")
            run_command(
                [
                    "python",
                    "-m",
                    "ruff",
                    "check",
                    "--fix",
                    "--unsafe-fixes",
                    "src",
                    "tests",
                ],
                check=False,
            )
            run_command(
                [
                    "python",
                    "-m",
                    "ruff",
                    "format",
                    "--respect-gitignore",
                    "src",
                    "tests",
                ],
                check=False,
            )

            # Run type checks
            log_message(">>>Running type checks...")
            run_command(["python", "-m", "mypy", "src", "tests"], check=False)

            # Run tests
            log_message(">>> Running tests...")
            run_command(["python", "-m", "pytest", "tests"], check=False)

            log_message("All checks completed")
        except Exception as e:
            log_message(f"Failed during checks: {e}")

    def status(self) -> None:
        """Show current repository status: tree structure, git status, and run checks."""
        prefix()  # Add README.md content at start
        self._print_header("Current Status")

        # Check required files
        self._check_required_files()

        # Show tree structure
        self._generate_tree()

        # Show git status
        result = run_command(["git", "status"], check=False)
        log_message(result.stdout)

        # Run additional checks
        self._print_header("Environment Status")
        self._venv()
        self._install()
        self._run_checks()

        suffix()  # Add TODO.md content at end

    def venv(self) -> None:
        """Create and activate virtual environment."""
        self._print_header("Virtual Environment Setup")
        self._venv()

    def install(self) -> None:
        """Install package with all extras."""
        self._print_header("Package Installation")
        self._install()

    def update(self) -> None:
        """Show status and commit any changes if needed."""
        # First show current status
        self.status()

        # Then handle git changes if any
        if self._git_status():
            log_message("Changes detected in repository")
            try:
                # Add all changes
                run_command(["git", "add", "."])
                # Commit changes
                commit_msg = "Update repository files"
                run_command(["git", "commit", "-m", commit_msg])
                log_message("Changes committed successfully")
            except Exception as e:
                log_message(f"Failed to commit changes: {e}")
        else:
            log_message("No changes to commit")

    def push(self) -> None:
        """Push changes to remote repository."""
        self._print_header("Pushing Changes")
        try:
            run_command(["git", "push"])
            log_message("Changes pushed successfully")
        except Exception as e:
            log_message(f"Failed to push changes: {e}")


def print_usage() -> None:
    """Print usage information."""
    log_message("Usage:")
    log_message("  cleanup.py status   # Show current status and run all checks")
    log_message("  cleanup.py venv     # Create virtual environment")
    log_message("  cleanup.py install  # Install package with all extras")
    log_message("  cleanup.py update   # Update and commit changes")
    log_message("  cleanup.py push     # Push changes to remote")


def main() -> NoReturn:
    """Main entry point."""
    new()  # Clear log file

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    cleanup = Cleanup()

    try:
        if command == "status":
            cleanup.status()
        elif command == "venv":
            cleanup.venv()
        elif command == "install":
            cleanup.install()
        elif command == "update":
            cleanup.update()
        elif command == "push":
            cleanup.push()
        else:
            print_usage()
            sys.exit(1)
    except Exception as e:
        log_message(f"Error: {e}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
