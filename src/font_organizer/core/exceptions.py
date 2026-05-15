# this_file: src/font_organizer/core/exceptions.py
"""
Custom exceptions for the font organizer application.

This module defines all custom exceptions used throughout the application.
"""


class FontOrganizerError(Exception):
    """Base exception for all font organizer errors."""

    pass


class FontNotFoundError(FontOrganizerError):
    """Raised when a font file cannot be found."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Font file not found: {path}")
        self.path = path


class FontParseError(FontOrganizerError):
    """Raised when a font file cannot be parsed."""

    def __init__(self, path: str, reason: str) -> None:
        super().__init__(f"Failed to parse font {path}: {reason}")
        self.path = path
        self.reason = reason


class InvalidConfigError(FontOrganizerError):
    """Raised when configuration is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid configuration: {message}")


class DuplicateFileError(FontOrganizerError):
    """Raised when attempting to overwrite an existing file."""

    def __init__(self, path: str) -> None:
        super().__init__(f"File already exists: {path}")
        self.path = path


class OrganizationError(FontOrganizerError):
    """Raised when font organization fails."""

    pass


class SubsetError(FontOrganizerError):
    """Raised when font subsetting fails."""

    def __init__(self, message: str, font_path: str | None = None) -> None:
        if font_path:
            super().__init__(f"Subsetting failed for {font_path}: {message}")
        else:
            super().__init__(f"Subsetting failed: {message}")
        self.font_path = font_path
