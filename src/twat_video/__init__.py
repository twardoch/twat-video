# SPDX-FileCopyrightText: 2024-present Adam Twardoch <adam+github@twardoch.com>
#
# SPDX-License-Identifier: MIT
"""
twat_video

This package provides a basic scaffolding for a Python project.
It serves as a starting point for developing more complex applications.
"""

# Import the version from the .__version__ file, which is managed by hatch-vcs
from .__version__ import __version__

# Import core components from the main module to make them available at the package level
from .twat_video import Config, main, process_data

# Define what is publicly available when importing * from the package
# This makes Config, process_data, main, and __version__ available directly
# e.g., from twat_video import Config
__all__ = ["Config", "process_data", "main", "__version__"]
