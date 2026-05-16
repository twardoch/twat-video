# this_file: src/font_organizer/core/config.py
"""
Configuration management for font organizer.

This module handles loading, saving, and validating configuration settings.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from loguru import logger

from font_organizer.core.exceptions import InvalidConfigError


@dataclass
class OrganizeConfig:
    """Configuration for font organization."""

    default_scheme: str = "family"
    copy_mode: bool = True
    create_dirs: bool = True
    preserve_structure: bool = False
    skip_duplicates: bool = True


@dataclass
class ScanConfig:
    """Configuration for font scanning."""

    include_system_fonts: bool = True
    recursive: bool = True
    font_extensions: list[str] = field(
        default_factory=lambda: [".ttf", ".otf", ".woff", ".woff2", ".eot"]
    )
    exclude_patterns: list[str] = field(default_factory=list)
    follow_symlinks: bool = False


@dataclass
class SubsetConfig:
    """Configuration for font subsetting."""

    default_format: str = "woff2"
    optimize: bool = True
    keep_hints: bool = False
    desubroutinize: bool = True
    drop_tables: list[str] = field(default_factory=list)


@dataclass
class Config:
    """Main configuration class for font organizer."""

    organize: OrganizeConfig = field(default_factory=OrganizeConfig)
    scan: ScanConfig = field(default_factory=ScanConfig)
    subset: SubsetConfig = field(default_factory=SubsetConfig)

    # General settings
    verbose: bool = False
    quiet: bool = False
    log_file: str | None = None
    cache_dir: str = "~/.font-organizer/cache"
    config_dir: str = "~/.font-organizer"

    def validate(self) -> None:
        """Validate configuration settings."""
        # Validate organize scheme
        valid_schemes = ["family", "style", "weight", "format", "custom"]
        if self.organize.default_scheme not in valid_schemes:
            msg = (
                f"Invalid organization scheme: {self.organize.default_scheme}. "
                f"Must be one of: {', '.join(valid_schemes)}"
            )
            raise InvalidConfigError(
                msg
            )

        # Validate font extensions
        for ext in self.scan.font_extensions:
            if not ext.startswith("."):
                msg = f"Font extension must start with '.': {ext}"
                raise InvalidConfigError(msg)

        # Validate subset format
        valid_formats = ["ttf", "otf", "woff", "woff2"]
        if self.subset.default_format not in valid_formats:
            msg = (
                f"Invalid subset format: {self.subset.default_format}. "
                f"Must be one of: {', '.join(valid_formats)}"
            )
            raise InvalidConfigError(
                msg
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "organize": {
                "default_scheme": self.organize.default_scheme,
                "copy_mode": self.organize.copy_mode,
                "create_dirs": self.organize.create_dirs,
                "preserve_structure": self.organize.preserve_structure,
                "skip_duplicates": self.organize.skip_duplicates,
            },
            "scan": {
                "include_system_fonts": self.scan.include_system_fonts,
                "recursive": self.scan.recursive,
                "font_extensions": self.scan.font_extensions,
                "exclude_patterns": self.scan.exclude_patterns,
                "follow_symlinks": self.scan.follow_symlinks,
            },
            "subset": {
                "default_format": self.subset.default_format,
                "optimize": self.subset.optimize,
                "keep_hints": self.subset.keep_hints,
                "desubroutinize": self.subset.desubroutinize,
                "drop_tables": self.subset.drop_tables,
            },
            "verbose": self.verbose,
            "quiet": self.quiet,
            "log_file": self.log_file,
            "cache_dir": self.cache_dir,
            "config_dir": self.config_dir,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        """Create configuration from dictionary."""
        organize_data = data.get("organize", {})
        scan_data = data.get("scan", {})
        subset_data = data.get("subset", {})

        return cls(
            organize=OrganizeConfig(**organize_data),
            scan=ScanConfig(**scan_data),
            subset=SubsetConfig(**subset_data),
            verbose=data.get("verbose", False),
            quiet=data.get("quiet", False),
            log_file=data.get("log_file"),
            cache_dir=data.get("cache_dir", "~/.font-organizer/cache"),
            config_dir=data.get("config_dir", "~/.font-organizer"),
        )


def get_config_path() -> Path:
    """Get the default configuration file path."""
    config_dir = Path.home() / ".font-organizer"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.yaml"


def load_config(path: str | Path | None = None) -> Config:
    """
    Load configuration from file.

    Args:
        path: Path to configuration file. If None, uses default location.

    Returns:
        Configuration object.

    Raises:
        InvalidConfigError: If configuration is invalid.
    """
    if path is None:
        path = get_config_path()
    else:
        path = Path(path)

    if not path.exists():
        logger.debug(f"Config file not found at {path}, using defaults")
        return Config()

    try:
        with open(path) as f:
            if path.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f) or {}
            elif path.suffix == ".json":
                data = json.load(f)
            else:
                msg = f"Unsupported config format: {path.suffix}"
                raise InvalidConfigError(msg)

        config = Config.from_dict(data)
        config.validate()
        logger.debug(f"Loaded configuration from {path}")
        return config

    except (yaml.YAMLError, json.JSONDecodeError) as e:
        msg = f"Failed to parse config file: {e}"
        raise InvalidConfigError(msg)
    except Exception as e:
        msg = f"Failed to load config: {e}"
        raise InvalidConfigError(msg)


def save_config(config: Config, path: str | Path | None = None) -> None:
    """
    Save configuration to file.

    Args:
        config: Configuration object to save.
        path: Path to save configuration. If None, uses default location.

    Raises:
        InvalidConfigError: If configuration cannot be saved.
    """
    if path is None:
        path = get_config_path()
    else:
        path = Path(path)

    # Validate before saving
    config.validate()

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        data = config.to_dict()

        with open(path, "w") as f:
            if path.suffix in [".yaml", ".yml"]:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            elif path.suffix == ".json":
                json.dump(data, f, indent=2)
            else:
                msg = f"Unsupported config format: {path.suffix}"
                raise InvalidConfigError(msg)

        logger.debug(f"Saved configuration to {path}")

    except Exception as e:
        msg = f"Failed to save config: {e}"
        raise InvalidConfigError(msg)
