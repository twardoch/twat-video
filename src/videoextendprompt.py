#!/usr/bin/env python
"""Generate video continuation prompts based on image frame analysis.

This script analyzes pairs of video frames (images) and generates creative prompts
for unfortunate events that could occur between them.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from fire import Fire
from llm.cli import load_template
from loguru import logger
from mallmo import ask
from rich.console import Console


def beep():
    if sys.platform.startswith("win"):
        import winsound

        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    elif sys.platform.startswith("darwin"):
        subprocess.run(["afplay", "/System/Library/Sounds/Blow.aiff"], check=False)
    else:
        subprocess.run(["beep"], check=False)


console = Console()

MODELS = (
    "openrouter/google/gemini-2.0-flash-exp:free",
    "openrouter/openai/gpt-4o-mini",
    "openrouter/anthropic/claude-3-haiku:beta",
    "openrouter/x-ai/grok-2-vision-1212",
)


def extract_samp_content(text: str) -> str:
    """Extract content from <samp> tags in text.

    Finds the last <samp> tag in the text and extracts its content, normalizing whitespace.
    Falls back to the original text if no tags are found or parsing fails.

    Args:
        text: Input text that may contain <samp> tags

    Returns:
        Normalized content from the last <samp> tag, or the original text if no tags found
    """
    if not text:
        return ""

    try:
        # Find all <samp> tag contents, taking the last one if present
        samp_matches = re.findall(r"<samp>(.*?)</samp>", text, re.DOTALL)
        content = samp_matches[-1] if samp_matches else text

        # Normalize whitespace - strip edges and collapse internal spaces
        return " ".join(content.split())

    except Exception as e:
        logger.warning("Failed to parse <samp> tags: %s", e)
        return " ".join(text.split())


def find_image_pairs(folder: Path) -> list[tuple[Path, Path]]:
    """Find pairs of images in the given folder and its subfolders.

    Args:
        folder: Root folder to search for images

    Returns:
        List of tuples containing pairs of image paths
    """
    image_extensions = {".png", ".jpg", ".jpeg"}
    folder_images: dict[Path, list[Path]] = {}

    # Group images by folder
    for img_path in folder.rglob("*"):
        if img_path.is_file() and img_path.suffix.lower() in image_extensions:
            parent = img_path.parent
            if parent not in folder_images:
                folder_images[parent] = []
            folder_images[parent].append(img_path)

    # Create pairs from first and last images in each folder
    image_pairs = []
    for images in sorted(folder_images.values(), key=lambda x: x[0].name):
        if len(images) >= 2:
            sorted_images = sorted(images)
            image_pairs.append((sorted_images[0], sorted_images[-1]))

    return image_pairs


def make_full_prompt() -> str:
    """Generate a creative prompt for the given image pair.

    Args:
        image_pair: Tuple of paths to two image frames

    Returns:
        Generated prompt text
    """
    base_prompt = "Inside the <aside> XML tag, you may think aloud. Analyze both frames. Infer the story that happens between the two frames, and imagine the type of shot that the two frames are part of. Then your main task: imagine a prompt for the continuation of this video shot that shows a SUDDENLY UNFORTUNATE BUT FUNNY (!!!) MISHAP which happens right after the provided 2nd frame. Specifically, in one sentence, describe the type of shot and briefly say what happens. Then in 2-3 short sentences, write a more detailed description of the subject and setting (observed in the provided frames), and the visible action. Finish with a stylistic description of the shot. Print that prompt inside a <samp> XML tag. Remember, it needs to be sudden, unfortunate, and funny (cute, not serious), and the mishap should be of slapstick nature, it must work without sound!"

    template = load_template("video")
    return template.prompt.replace("$input", base_prompt)


def get_full_answer(prompt: str, image_pair: tuple[Path, Path], model: str) -> str:
    response = ask(prompt=prompt, media_paths=image_pair, model_ids=[model])
    return extract_samp_content(response)


def process_pair(prompt: str, image_pair: tuple[Path, Path]) -> None:
    report = {}
    folder = image_pair[0].parent
    console.print(f"\n\n[blue]{folder}[/blue]")
    for model in MODELS:
        try:
            answer = get_full_answer(prompt, image_pair, model)
            report[model] = answer
            console.print(f"[yellow]{model}[/yellow]")
            console.print(f"[green]{answer}[/green]")
        except Exception as e:
            console.print(f"[red]{model}: {e}[/red]")
    with open(Path(folder, "video_prompt.md"), "w") as f:
        for model, prompt in report.items():
            f.write(f"## {model}\n\n")
            f.write(f"{prompt}\n\n")


def process_folder(folder: str | Path | None = None) -> None:
    """Process images in the given folder to generate video continuation prompts.

    Args:
        folder: Path to folder containing image pairs. Uses current directory if None.
    """
    root = Path(folder) if folder else Path.cwd()
    logger.info(f"Processing images in {root}")

    image_pairs = find_image_pairs(root)
    if not image_pairs:
        console.print("[yellow]No image pairs found![/yellow]")
        return

    full_prompt = make_full_prompt()
    for pair in image_pairs:
        process_pair(full_prompt, pair)


def main() -> None:
    """Entry point for the script."""
    try:
        logger.remove()  # Remove default handler
        logger.add(
            "videoextend.log",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )
        Fire(process_folder)
    finally:
        beep()


if __name__ == "__main__":
    main()
