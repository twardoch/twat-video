# this_file: src/font_organizer/core/__init__.py
"""
Core module for font organization functionality.

This module provides the fundamental classes and functions for font management.
"""

from font_organizer.core.config import Config, load_config, save_config
from font_organizer.core.exceptions import FontOrganizerError, FontNotFoundError, FontParseError, InvalidConfigError
from font_organizer.core.font_info import FontInfo, FontMetadata, FontStyle, FontWeight
from font_organizer.core.font_manager import FontManager

__all__ = [
    # Configuration
    "Config",
    # Font information
    "FontInfo",
    # Manager
    "FontManager",
    "FontMetadata",
    "FontNotFoundError",
    # Exceptions
    "FontOrganizerError",
    "FontParseError",
    "FontStyle",
    "FontWeight",
    "InvalidConfigError",
    "load_config",
    "save_config",
]
