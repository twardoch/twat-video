# this_file: src/font_organizer/core/font_manager.py
"""
Main font management class that coordinates all font operations.

This module provides the central FontManager class that integrates all
font organization functionality.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from loguru import logger

from .config import Config, load_config
from .font_info import FontInfo


class FontManager:
    """
    Central manager for font organization operations.

    This class coordinates scanning, organizing, analyzing, and subsetting fonts.
    """

    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize FontManager.

        Args:
            config: Configuration object. If None, loads default config.
        """
        self.config = config or load_config()
        self._setup_logging()
        self._font_cache: dict[str, FontInfo] = {}

    def _setup_logging(self) -> None:
        """Configure logging based on config settings."""
        if self.config.quiet:
            logger.remove()
        elif self.config.verbose:
            logger.level("DEBUG")

        if self.config.log_file:
            log_path = Path(self.config.log_file).expanduser()
            log_path.parent.mkdir(parents=True, exist_ok=True)
            logger.add(
                log_path,
                rotation="10 MB",
                retention="1 week",
                compression="zip",
            )

    def get_font_info(self, font_path: str | Path) -> FontInfo:
        """
        Get font information with caching.

        Args:
            font_path: Path to the font file.

        Returns:
            FontInfo object for the font.
        """
        font_path = Path(font_path).resolve()
        path_str = str(font_path)

        if path_str not in self._font_cache:
            self._font_cache[path_str] = FontInfo(font_path)
            logger.debug(f"Cached font info for: {font_path.name}")

        return self._font_cache[path_str]

    def scan_directory(
        self,
        directory: str | Path,
        recursive: bool | None = None,
        extensions: list[str] | None = None,
    ) -> list[Path]:
        """
        Scan directory for font files.

        Args:
            directory: Directory to scan.
            recursive: Whether to scan recursively. Uses config default if None.
            extensions: Font file extensions to look for. Uses config default if None.

        Returns:
            List of found font file paths.
        """
        directory = Path(directory).resolve()

        if not directory.exists():
            logger.error(f"Directory does not exist: {directory}")
            return []

        if not directory.is_dir():
            logger.error(f"Path is not a directory: {directory}")
            return []

        # Use config defaults if not specified
        if recursive is None:
            recursive = self.config.scan.recursive
        if extensions is None:
            extensions = self.config.scan.font_extensions

        # Normalize extensions
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]

        logger.info(f"Scanning directory: {directory}")
        logger.debug(f"Recursive: {recursive}, Extensions: {extensions}")

        font_files = []

        # Define search pattern
        if recursive:
            patterns = [f"**/*{ext}" for ext in extensions]
        else:
            patterns = [f"*{ext}" for ext in extensions]

        # Search for files
        for pattern in patterns:
            for path in directory.glob(pattern):
                if path.is_file():
                    # Check exclude patterns
                    skip = False
                    for exclude in self.config.scan.exclude_patterns:
                        if path.match(exclude):
                            logger.debug(f"Skipping excluded file: {path}")
                            skip = True
                            break

                    if not skip:
                        font_files.append(path)

        # Remove duplicates and sort
        font_files = sorted(set(font_files))

        logger.info(f"Found {len(font_files)} font files")
        return font_files

    def analyze_fonts(self, font_paths: list[Path]) -> dict[str, Any]:
        """
        Analyze a collection of fonts.

        Args:
            font_paths: List of font file paths to analyze.

        Returns:
            Dictionary containing analysis results.
        """
        logger.info(f"Analyzing {len(font_paths)} fonts")

        analysis = {
            "total_fonts": len(font_paths),
            "total_size": 0,
            "formats": {},
            "families": {},
            "weights": {},
            "styles": {},
            "vendors": {},
            "features": {},
            "errors": [],
        }

        for font_path in font_paths:
            try:
                info = self.get_font_info(font_path)

                # Update total size
                analysis["total_size"] += info.metadata.file_size

                # Count formats
                fmt = info.metadata.format
                analysis["formats"][fmt] = analysis["formats"].get(fmt, 0) + 1

                # Count families
                family = info.family
                if family not in analysis["families"]:
                    analysis["families"][family] = []
                analysis["families"][family].append(str(font_path))

                # Count weights
                weight = info.weight.name
                analysis["weights"][weight] = analysis["weights"].get(weight, 0) + 1

                # Count styles
                style = info.style.name
                analysis["styles"][style] = analysis["styles"].get(style, 0) + 1

                # Count vendors
                if info.metadata.vendor:
                    vendor = info.metadata.vendor
                    analysis["vendors"][vendor] = analysis["vendors"].get(vendor, 0) + 1

                # Count features
                for feature in info.features:
                    analysis["features"][feature] = (
                        analysis["features"].get(feature, 0) + 1
                    )

            except Exception as e:
                logger.error(f"Error analyzing {font_path}: {e}")
                analysis["errors"].append(
                    {
                        "path": str(font_path),
                        "error": str(e),
                    }
                )

        # Calculate additional statistics
        analysis["unique_families"] = len(analysis["families"])
        analysis["average_size"] = (
            analysis["total_size"] / len(font_paths) if font_paths else 0
        )

        return analysis

    def find_duplicates(self, font_paths: list[Path]) -> list[list[Path]]:
        """
        Find duplicate fonts based on file hash.

        Args:
            font_paths: List of font file paths to check.

        Returns:
            List of duplicate groups. Each group contains paths with identical content.
        """
        logger.info(f"Checking {len(font_paths)} fonts for duplicates")

        hash_map: dict[str, list[Path]] = {}

        for font_path in font_paths:
            try:
                info = self.get_font_info(font_path)
                file_hash = info.metadata.file_hash

                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(font_path)

            except Exception as e:
                logger.error(f"Error processing {font_path}: {e}")

        # Find groups with more than one file
        duplicates = [paths for paths in hash_map.values() if len(paths) > 1]

        logger.info(f"Found {len(duplicates)} duplicate groups")
        return duplicates

    def get_system_font_dirs(self) -> list[Path]:
        """
        Get system font directories for the current platform.

        Returns:
            List of system font directory paths.
        """
        import platform

        system = platform.system()
        dirs = []

        if system == "Windows":
            import os

            windows_dir = os.environ.get("WINDIR", "C:\\Windows")
            dirs.append(Path(windows_dir) / "Fonts")

            # User fonts
            local_appdata = os.environ.get("LOCALAPPDATA")
            if local_appdata:
                dirs.append(Path(local_appdata) / "Microsoft" / "Windows" / "Fonts")

        elif system == "Darwin":  # macOS
            dirs.extend(
                [
                    Path("/Library/Fonts"),
                    Path("/System/Library/Fonts"),
                    Path.home() / "Library" / "Fonts",
                ]
            )

        else:  # Linux and others
            dirs.extend(
                [
                    Path("/usr/share/fonts"),
                    Path("/usr/local/share/fonts"),
                    Path.home() / ".fonts",
                    Path.home() / ".local" / "share" / "fonts",
                ]
            )

        # Filter out non-existent directories
        existing_dirs = [d for d in dirs if d.exists()]
        logger.debug(f"System font directories: {existing_dirs}")

        return existing_dirs

    def scan_system_fonts(self) -> list[Path]:
        """
        Scan system font directories.

        Returns:
            List of font files found in system directories.
        """
        if not self.config.scan.include_system_fonts:
            logger.debug("System font scanning disabled in config")
            return []

        logger.info("Scanning system font directories")

        all_fonts = []
        for font_dir in self.get_system_font_dirs():
            fonts = self.scan_directory(font_dir)
            all_fonts.extend(fonts)

        # Remove duplicates
        all_fonts = sorted(set(all_fonts))

        logger.info(f"Found {len(all_fonts)} system fonts")
        return all_fonts
