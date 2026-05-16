# this_file: src/font_organizer/core/font_info.py
"""
Font information extraction and metadata handling.

This module provides classes and functions for extracting and managing font metadata.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._n_a_m_e import table__n_a_m_e
from loguru import logger

from font_organizer.core.exceptions import FontNotFoundError, FontParseError


class FontStyle(Enum):
    """Font style enumeration."""

    REGULAR = auto()
    ITALIC = auto()
    OBLIQUE = auto()


class FontWeight(Enum):
    """Standard font weight values."""

    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    REGULAR = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900

    @classmethod
    def from_value(cls, value: int) -> FontWeight:
        """Get FontWeight from numeric value."""
        # Find closest weight
        closest = min(cls, key=lambda w: abs(w.value - value))
        return closest

    @classmethod
    def from_string(cls, weight_str: str) -> FontWeight:
        """Parse font weight from string."""
        weight_str = weight_str.lower().strip()

        # Map common weight names
        weight_map = {
            "thin": cls.THIN,
            "hairline": cls.THIN,
            "extralight": cls.EXTRA_LIGHT,
            "extra-light": cls.EXTRA_LIGHT,
            "ultra-light": cls.EXTRA_LIGHT,
            "light": cls.LIGHT,
            "regular": cls.REGULAR,
            "normal": cls.REGULAR,
            "book": cls.REGULAR,
            "medium": cls.MEDIUM,
            "semibold": cls.SEMI_BOLD,
            "semi-bold": cls.SEMI_BOLD,
            "demi-bold": cls.SEMI_BOLD,
            "demibold": cls.SEMI_BOLD,
            "bold": cls.BOLD,
            "extrabold": cls.EXTRA_BOLD,
            "extra-bold": cls.EXTRA_BOLD,
            "ultra-bold": cls.EXTRA_BOLD,
            "black": cls.BLACK,
            "heavy": cls.BLACK,
        }

        return weight_map.get(weight_str, cls.REGULAR)


@dataclass
class FontMetadata:
    """Container for font metadata."""

    # Basic identification
    family: str = ""
    subfamily: str = ""
    full_name: str = ""
    postscript_name: str = ""

    # Style information
    style: FontStyle = FontStyle.REGULAR
    weight: FontWeight = FontWeight.REGULAR
    width: str = "Normal"

    # Version and vendor
    version: str = ""
    vendor: str = ""
    designer: str = ""

    # Copyright and license
    copyright: str = ""
    license: str = ""
    license_url: str = ""

    # Technical details
    units_per_em: int = 0
    ascent: int = 0
    descent: int = 0
    line_gap: int = 0

    # Character coverage
    glyph_count: int = 0
    unicode_ranges: list[tuple[int, int]] = field(default_factory=list)

    # OpenType features
    features: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)

    # File information
    format: str = ""
    file_size: int = 0
    file_hash: str = ""


class FontInfo:
    """Extract and manage font information."""

    def __init__(self, font_path: str | Path) -> None:
        """
        Initialize FontInfo with a font file path.

        Args:
            font_path: Path to the font file.

        Raises:
            FontNotFoundError: If the font file doesn't exist.
            FontParseError: If the font file cannot be parsed.
        """
        self.path = Path(font_path)

        if not self.path.exists():
            raise FontNotFoundError(str(self.path))

        self._font: TTFont | None = None
        self._metadata: FontMetadata | None = None
        self._load_font()

    def _load_font(self) -> None:
        """Load the font file."""
        try:
            self._font = TTFont(self.path, recalcBBoxes=False)
            logger.debug(f"Loaded font: {self.path}")
        except Exception as e:
            raise FontParseError(str(self.path), str(e))

    def _calculate_file_hash(self) -> str:
        """Calculate SHA256 hash of the font file."""
        sha256_hash = hashlib.sha256()
        with open(self.path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_name_record(self, name_id: int, platform_id: int = 3) -> str:
        """Get a name record from the font's name table."""
        if "name" not in self._font:
            return ""

        name_table: table__n_a_m_e = self._font["name"]
        for record in name_table.names:
            if record.nameID == name_id and record.platformID == platform_id:
                try:
                    return record.toUnicode()
                except UnicodeDecodeError:
                    continue
        return ""

    def _extract_metadata(self) -> FontMetadata:
        """Extract metadata from the font."""
        metadata = FontMetadata()

        # File information
        metadata.file_size = self.path.stat().st_size
        metadata.file_hash = self._calculate_file_hash()
        metadata.format = self.path.suffix[1:].upper()

        # Basic names
        metadata.family = self._get_name_record(1) or self.path.stem
        metadata.subfamily = self._get_name_record(2) or "Regular"
        metadata.full_name = self._get_name_record(4) or metadata.family
        metadata.postscript_name = self._get_name_record(6) or metadata.family.replace(
            " ", ""
        )

        # Version and vendor
        metadata.version = self._get_name_record(5)
        metadata.vendor = self._get_name_record(8)
        metadata.designer = self._get_name_record(9)

        # Copyright and license
        metadata.copyright = self._get_name_record(0)
        metadata.license = self._get_name_record(13)
        metadata.license_url = self._get_name_record(14)

        # Parse style and weight from subfamily
        subfamily_lower = metadata.subfamily.lower()
        if "italic" in subfamily_lower:
            metadata.style = FontStyle.ITALIC
        elif "oblique" in subfamily_lower:
            metadata.style = FontStyle.OBLIQUE
        else:
            metadata.style = FontStyle.REGULAR

        # Extract weight
        if "OS/2" in self._font:
            weight_value = self._font["OS/2"].usWeightClass
            metadata.weight = FontWeight.from_value(weight_value)
        else:
            # Fallback to parsing from subfamily name
            metadata.weight = FontWeight.from_string(metadata.subfamily)

        # Metrics
        if "head" in self._font:
            metadata.units_per_em = self._font["head"].unitsPerEm

        if "hhea" in self._font:
            metadata.ascent = self._font["hhea"].ascent
            metadata.descent = self._font["hhea"].descent
            metadata.line_gap = self._font["hhea"].lineGap

        # Glyph count
        if "maxp" in self._font:
            metadata.glyph_count = self._font["maxp"].numGlyphs

        # Character coverage
        if "cmap" in self._font:
            cmap = self._font["cmap"].getBestCmap()
            if cmap:
                characters = sorted(cmap.keys())
                # Group into ranges
                ranges = []
                if characters:
                    start = characters[0]
                    end = characters[0]

                    for char in characters[1:]:
                        if char == end + 1:
                            end = char
                        else:
                            ranges.append((start, end))
                            start = end = char
                    ranges.append((start, end))

                metadata.unicode_ranges = ranges

        # OpenType features
        if "GSUB" in self._font:
            gsub_table = self._font["GSUB"].table
            if hasattr(gsub_table, "FeatureList"):
                metadata.features = [
                    f.FeatureTag for f in gsub_table.FeatureList.FeatureRecord
                ]
            if hasattr(gsub_table, "ScriptList"):
                metadata.scripts = [
                    s.ScriptTag for s in gsub_table.ScriptList.ScriptRecord
                ]

        return metadata

    @property
    def metadata(self) -> FontMetadata:
        """Get font metadata (lazy loading)."""
        if self._metadata is None:
            self._metadata = self._extract_metadata()
        return self._metadata

    @property
    def family(self) -> str:
        """Get font family name."""
        return self.metadata.family

    @property
    def subfamily(self) -> str:
        """Get font subfamily name."""
        return self.metadata.subfamily

    @property
    def style(self) -> FontStyle:
        """Get font style."""
        return self.metadata.style

    @property
    def weight(self) -> FontWeight:
        """Get font weight."""
        return self.metadata.weight

    @property
    def full_name(self) -> str:
        """Get font full name."""
        return self.metadata.full_name

    @property
    def postscript_name(self) -> str:
        """Get font PostScript name."""
        return self.metadata.postscript_name

    @property
    def features(self) -> list[str]:
        """Get list of OpenType features."""
        return self.metadata.features

    @property
    def glyph_count(self) -> int:
        """Get number of glyphs in the font."""
        return self.metadata.glyph_count

    @property
    def characters(self) -> set[int]:
        """Get set of Unicode characters supported by the font."""
        chars = set()
        for start, end in self.metadata.unicode_ranges:
            chars.update(range(start, end + 1))
        return chars

    def has_character(self, char: str | int) -> bool:
        """
        Check if font supports a specific character.

        Args:
            char: Character to check (string or Unicode codepoint).

        Returns:
            True if character is supported, False otherwise.
        """
        if isinstance(char, str):
            if len(char) != 1:
                msg = "Only single characters are supported"
                raise ValueError(msg)
            char = ord(char)

        return char in self.characters

    def get_info_dict(self) -> dict[str, Any]:
        """Get font information as a dictionary."""
        return {
            "path": str(self.path),
            "family": self.family,
            "subfamily": self.subfamily,
            "full_name": self.full_name,
            "postscript_name": self.postscript_name,
            "style": self.style.name,
            "weight": f"{self.weight.name} ({self.weight.value})",
            "version": self.metadata.version,
            "vendor": self.metadata.vendor,
            "designer": self.metadata.designer,
            "copyright": self.metadata.copyright,
            "license": self.metadata.license,
            "format": self.metadata.format,
            "file_size": self.metadata.file_size,
            "file_hash": self.metadata.file_hash,
            "glyph_count": self.glyph_count,
            "character_count": len(self.characters),
            "features": self.features,
            "scripts": self.metadata.scripts,
        }

    def __repr__(self) -> str:
        """String representation of FontInfo."""
        return f"FontInfo('{self.path.name}', family='{self.family}', style={self.style.name}, weight={self.weight.name})"
