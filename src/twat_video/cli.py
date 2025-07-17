#!/usr/bin/env python3
"""
Command-line interface for twat_video.

This module provides a CLI interface using Click for the twat_video package.
"""
# this_file: src/twat_video/cli.py

from __future__ import annotations

import sys
import logging
from typing import Any

import click

from . import __version__, Config, process_data, main as lib_main


# Configure logging for CLI
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--verbose", "-v", 
    is_flag=True, 
    help="Enable verbose output"
)
@click.option(
    "--quiet", "-q", 
    is_flag=True, 
    help="Suppress output"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """twat-video: A modern Python project scaffold and toolkit."""
    ctx.ensure_object(dict)
    
    # Configure logging level
    if quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet


@cli.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Show version information."""
    click.echo(f"twat-video version {__version__}")
    
    if ctx.obj.get("verbose"):
        click.echo(f"Python version: {sys.version}")
        click.echo(f"Platform: {sys.platform}")


@cli.command()
@click.option(
    "--config-name", 
    default="cli_config",
    help="Configuration name to use"
)
@click.option(
    "--config-value", 
    default="cli_value",
    help="Configuration value to use"
)
@click.option(
    "--debug", 
    is_flag=True, 
    help="Enable debug mode for processing"
)
@click.argument("data", nargs=-1, required=True)
@click.pass_context
def process(
    ctx: click.Context, 
    config_name: str, 
    config_value: str, 
    debug: bool, 
    data: tuple[str, ...]
) -> None:
    """Process data with the specified configuration.
    
    DATA: One or more data items to process
    """
    if not data:
        click.echo("Error: No data provided to process", err=True)
        sys.exit(1)
    
    # Convert data tuple to list for processing
    data_list: list[Any] = list(data)
    
    # Create configuration
    config = Config(
        name=config_name,
        value=config_value,
        options={"cli": True, "debug": debug}
    )
    
    try:
        result = process_data(data_list, config=config, debug=debug)
        
        if ctx.obj.get("verbose"):
            click.echo(f"Processing result: {result}")
        else:
            click.echo(f"Processed {result['item_count']} items successfully")
            
    except Exception as e:
        click.echo(f"Error processing data: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def demo(ctx: click.Context) -> None:
    """Run the demo application."""
    try:
        if ctx.obj.get("verbose"):
            click.echo("Running demo application...")
        
        lib_main()
        
        if ctx.obj.get("verbose"):
            click.echo("Demo completed successfully")
            
    except Exception as e:
        click.echo(f"Error running demo: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--output-file", 
    type=click.Path(), 
    help="Output file for configuration"
)
@click.pass_context
def config(ctx: click.Context, output_file: str | None) -> None:
    """Generate or display configuration."""
    sample_config = Config(
        name="sample_config",
        value=42,
        options={
            "feature_enabled": True,
            "mode": "production",
            "logging_level": "INFO"
        }
    )
    
    config_text = f"""# Sample Configuration
name: {sample_config.name}
value: {sample_config.value}
options:
  feature_enabled: {sample_config.options.get('feature_enabled', False)}
  mode: {sample_config.options.get('mode', 'default')}
  logging_level: {sample_config.options.get('logging_level', 'INFO')}
"""
    
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(config_text)
            click.echo(f"Configuration written to: {output_file}")
        except Exception as e:
            click.echo(f"Error writing configuration: {e}", err=True)
            sys.exit(1)
    else:
        click.echo(config_text)


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()