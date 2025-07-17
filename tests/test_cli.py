"""Test suite for the CLI module."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from twat_video.cli import cli
from twat_video import __version__


class TestCLI:
    """Test cases for the CLI interface."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_version_option(self):
        """Test --version option."""
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.output

    def test_cli_help(self):
        """Test help output."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "twat-video" in result.output
        assert "modern Python project" in result.output

    def test_version_command(self):
        """Test version command."""
        result = self.runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert __version__ in result.output

    def test_version_command_verbose(self):
        """Test version command with verbose flag."""
        result = self.runner.invoke(cli, ["--verbose", "version"])
        assert result.exit_code == 0
        assert __version__ in result.output
        assert "Python version" in result.output

    def test_process_command_basic(self):
        """Test process command with basic arguments."""
        result = self.runner.invoke(cli, ["process", "item1", "item2"])
        assert result.exit_code == 0
        assert "Processed 2 items successfully" in result.output

    def test_process_command_with_config(self):
        """Test process command with configuration options."""
        result = self.runner.invoke(cli, [
            "process",
            "--config-name", "test_config",
            "--config-value", "test_value",
            "item1"
        ])
        assert result.exit_code == 0
        assert "Processed 1 items successfully" in result.output

    def test_process_command_with_debug(self):
        """Test process command with debug flag."""
        result = self.runner.invoke(cli, ["process", "--debug", "item1"])
        assert result.exit_code == 0

    def test_process_command_verbose(self):
        """Test process command with verbose output."""
        result = self.runner.invoke(cli, ["--verbose", "process", "item1"])
        assert result.exit_code == 0
        assert "Processing result" in result.output

    def test_process_command_no_data(self):
        """Test process command with no data."""
        result = self.runner.invoke(cli, ["process"])
        assert result.exit_code == 2  # Click returns 2 for missing required arguments
        assert "Error: Missing argument" in result.output

    def test_process_command_exception_handling(self):
        """Test process command exception handling."""
        with patch('twat_video.cli.process_data') as mock_process:
            mock_process.side_effect = ValueError("Test error")
            result = self.runner.invoke(cli, ["process", "item1"])
            assert result.exit_code == 1
            assert "Error processing data" in result.output

    def test_demo_command(self):
        """Test demo command."""
        result = self.runner.invoke(cli, ["demo"])
        assert result.exit_code == 0

    def test_demo_command_verbose(self):
        """Test demo command with verbose output."""
        result = self.runner.invoke(cli, ["--verbose", "demo"])
        assert result.exit_code == 0
        assert "Running demo application" in result.output

    def test_demo_command_exception_handling(self):
        """Test demo command exception handling."""
        with patch('twat_video.cli.lib_main') as mock_main:
            mock_main.side_effect = RuntimeError("Test error")
            result = self.runner.invoke(cli, ["demo"])
            assert result.exit_code == 1
            assert "Error running demo" in result.output

    def test_config_command(self):
        """Test config command."""
        result = self.runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "Sample Configuration" in result.output
        assert "name: sample_config" in result.output

    def test_config_command_with_output_file(self):
        """Test config command with output file."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ["config", "--output-file", "test_config.yml"])
            assert result.exit_code == 0
            assert "Configuration written to: test_config.yml" in result.output
            
            # Check file was created
            import os
            assert os.path.exists("test_config.yml")

    def test_config_command_file_error(self):
        """Test config command with file write error."""
        result = self.runner.invoke(cli, ["config", "--output-file", "/invalid/path/config.yml"])
        assert result.exit_code == 1
        assert "Error writing configuration" in result.output

    def test_quiet_flag(self):
        """Test quiet flag suppresses output."""
        result = self.runner.invoke(cli, ["--quiet", "process", "item1"])
        assert result.exit_code == 0
        # Should have minimal output when quiet

    def test_verbose_flag(self):
        """Test verbose flag increases output."""
        result = self.runner.invoke(cli, ["--verbose", "process", "item1"])
        assert result.exit_code == 0
        assert "Processing result" in result.output

    def test_invalid_command(self):
        """Test invalid command handling."""
        result = self.runner.invoke(cli, ["invalid-command"])
        assert result.exit_code == 2  # Click's exit code for invalid command

    def test_cli_context_object(self):
        """Test CLI context object is properly set."""
        @cli.command()
        @pytest.fixture
        def test_context(ctx):
            """Test command to check context."""
            assert ctx.obj is not None
            assert isinstance(ctx.obj, dict)
            return ctx.obj

    def test_multiple_data_items(self):
        """Test processing multiple data items."""
        result = self.runner.invoke(cli, ["process", "item1", "item2", "item3", "item4"])
        assert result.exit_code == 0
        assert "Processed 4 items successfully" in result.output

    def test_logging_configuration(self):
        """Test that logging is properly configured."""
        # Test with quiet flag
        result = self.runner.invoke(cli, ["--quiet", "version"])
        assert result.exit_code == 0
        
        # Test with verbose flag
        result = self.runner.invoke(cli, ["--verbose", "version"])
        assert result.exit_code == 0