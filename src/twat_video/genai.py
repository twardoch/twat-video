"""Thin optional video adapters to twat_genai."""
# this_file: src/twat_video/genai.py

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any


def generate_video(
    prompt: str,
    *,
    image: str | Path | None = None,
    output_dir: str | Path = "generated_videos",
    **kwargs: Any,
) -> Any:
    """Call a future twat_genai video backend without embedding provider clients."""
    try:
        twat_genai = import_module("twat_genai")
    except ImportError as exc:
        msg = "twat_genai is required for AI video generation. Install twat-genai and configure a video provider."
        raise RuntimeError(msg) from exc
    generator = getattr(twat_genai, "generate_video", None)
    if generator is None:
        msg = "Installed twat_genai does not expose a video generation API yet."
        raise NotImplementedError(msg)
    return generator(prompt=prompt, image=image, output_dir=output_dir, **kwargs)
