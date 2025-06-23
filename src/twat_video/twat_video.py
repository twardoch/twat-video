#!/usr/bin/env python3
"""
twat_video

This module provides a basic scaffolding for a Python project.
It includes a sample configuration class, a data processing function,
and a main entry point. It is intended to be a starting point for
developing more complex applications.

Created by Adam Twardoch
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

# Import the version from the dedicated file, which is managed by hatch-vcs
from .__version__ import __version__

# Define what is publicly available when importing *
__all__ = ["Config", "process_data", "main", "__version__"]

# Configure basic logging
# Applications using this library should configure their own logging handlers.
# This basicConfig is primarily for the library's own execution if run directly.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """
    Configuration settings for the application.

    This class serves as a placeholder for more complex configuration
    that your application might need.
    """

    name: str = "default_config"
    """A descriptive name for the configuration set."""

    value: str | int | float = "default_value"
    """A sample configuration value. Can be a string, integer, or float."""

    options: dict[str, Any] = field(default_factory=dict)
    """Optional dictionary for more detailed settings."""


def process_data(
    data: list[Any], config: Config | None = None, *, debug: bool = False
) -> dict[str, Any]:
    """
    Processes the input data according to the provided configuration.

    This is a placeholder function. Replace its contents with your
    project's specific data processing logic.

    Args:
        data: A list of items to process. For this placeholder, it expects non-empty data.
        config: An optional `Config` object to guide processing.
                If None, default processing parameters might be applied.
        debug: If True, enables verbose debug logging for this operation.

    Returns:
        A dictionary containing the results of the processing.
        The structure of this dictionary will depend on the actual implementation.

    Raises:
        ValueError: If input data is empty, as this placeholder requires data.
                    This behavior can be modified to suit actual requirements.
    """
    if debug:
        # Temporarily set logger level for this specific call if debug is true
        current_level = logger.level
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled for process_data")

    if not data:
        msg = "Input data cannot be empty for this placeholder function."
        logger.error(msg)
        raise ValueError(msg)

    logger.info("Processing data with config: %s", config.name if config else "No Config")
    logger.debug("Input data: %s", data)

    # --- TODO: Implement actual data processing logic here ---
    # Example: Transform data, perform calculations, interact with other services, etc.
    # For now, it returns a simple dictionary with input metadata.
    result: dict[str, Any] = {
        "status": "processed",
        "item_count": len(data),
        "config_name": config.name if config else "N/A",
        "first_item": data[0] if data else None,
    }
    # --- End of TODO section ---

    logger.info("Data processing complete.")
    if debug:
        logger.debug("Result: %s", result)
        logger.setLevel(current_level)  # Reset logger level

    return result


def main() -> None:
    """
    Main entry point for the twat_video application when run as a script.

    This function demonstrates example usage of the `process_data` function.
    It sets up a sample configuration and data, then calls `process_data`.
    """
    logger.info("Starting twat_video application (version %s)...", __version__)

    try:
        # Example: Create a configuration object
        sample_config = Config(
            name="example_run_config",
            value=123,
            options={"feature_x": True, "mode": "alpha"},
        )
        logger.info("Using configuration: %s", sample_config)

        # Example: Prepare sample data
        sample_data = ["item1", {"id": 2, "value": "data_point"}, 42]
        logger.info("Prepared sample data: %s", sample_data)

        # Call the processing function with the sample data and config
        # Set debug=True for more verbose output during this example run
        processed_result = process_data(sample_data, config=sample_config, debug=True)
        logger.info("Processing completed. Result: %s", processed_result)

    except ValueError as ve:
        logger.error("A ValueError occurred during processing: %s", ve, exc_info=True)
        # Depending on the application, you might want to exit differently or re-raise
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.critical("An unexpected critical error occurred: %s", e, exc_info=True)
        # Re-raise the exception after logging, or handle it as appropriate
        raise
    finally:
        logger.info("twat_video application finished.")


if __name__ == "__main__":
    # This block executes if the script is run directly (e.g., python -m twat_video.twat_video)
    main()
