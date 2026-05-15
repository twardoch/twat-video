# this_file: src/font_organizer/core/__init__.py
"""
Core module for font organization functionality.

This module provides the fundamental classes and functions for font management.
"""

from .config import Config, load_config, save_config
from .exceptions import (
    FontOrganizerError,
    FontNotFoundError,
    FontParseError,
    InvalidConfigError,
)
from .font_info import FontInfo, FontMetadata, FontStyle, FontWeight
from .font_manager import FontManager

__all__ = [
    # Configuration
    "Config",
    "load_config",
    "save_config",
    # Exceptions
    "FontOrganizerError",
    "FontNotFoundError",
    "FontParseError",
    "InvalidConfigError",
    # Font information
    "FontInfo",
    "FontMetadata",
    "FontStyle",
    "FontWeight",
    # Manager
    "FontManager",
]
