# SPDX-FileCopyrightText: 2024-present Adam Twardoch <adam+github@twardoch.com>
#
# SPDX-License-Identifier: MIT
# this_file: src/font_organizer/__init__.py
"""
font_organizer

Modern font organization tool for managing and curating font collections.
"""

# Import the version from the .__version__ file, which is managed by hatch-vcs
from font_organizer.__version__ import __version__

# Import core components from the main module to make them available at the package level
from font_organizer.font_organizer import Config as LegacyConfig, main, process_data

# Import new core components
from font_organizer.core import Config, FontInfo, FontManager, FontMetadata, FontStyle, FontWeight, FontOrganizerError, FontNotFoundError, FontParseError, InvalidConfigError, load_config, save_config

# Define what is publicly available when importing * from the package
# This makes core classes and functions available directly
# e.g., from font_organizer import FontInfo, FontManager
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
    # Legacy exports (will be removed in future)
    "LegacyConfig",
    # Version
    "__version__",
    "load_config",
    "main",
    "process_data",
    "save_config",
]
