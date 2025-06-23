"""Test suite for the twat_video package."""

import logging
import pytest

from twat_video import Config, process_data, main as twat_video_main
from twat_video import __version__


def test_version_is_exposed():
    """Verify that the package exposes a version string."""
    assert isinstance(__version__, str)
    assert len(__version__) > 0  # Basic check that it's not empty


def test_config_instantiation_defaults():
    """Test Config dataclass instantiation with default values."""
    config = Config()
    assert config.name == "default_config"
    assert config.value == "default_value"
    assert config.options == {}


def test_config_instantiation_custom_values():
    """Test Config dataclass instantiation with custom values."""
    custom_name = "my_config"
    custom_value = 12345
    custom_options = {"key1": "value1", "feature_enabled": True}
    config = Config(name=custom_name, value=custom_value, options=custom_options)
    assert config.name == custom_name
    assert config.value == custom_value
    assert config.options == custom_options


def test_process_data_valid_input():
    """Test process_data with valid data and configuration."""
    sample_data = ["item1", "item2"]
    sample_config = Config(name="test_processing", value="sample_value")
    result = process_data(data=sample_data, config=sample_config)

    assert result["status"] == "processed"
    assert result["item_count"] == len(sample_data)
    assert result["config_name"] == sample_config.name
    assert result["first_item"] == sample_data[0]


def test_process_data_empty_data_raises_valueerror():
    """Test process_data raises ValueError when input data is empty."""
    with pytest.raises(ValueError, match="Input data cannot be empty"):
        process_data(data=[], config=Config())


def test_process_data_debug_mode(caplog):
    """Test process_data with debug mode enabled.
    Checks if debug messages are logged.
    """
    sample_data = ["debug_item"]
    sample_config = Config(name="debug_config")

    with caplog.at_level(logging.DEBUG, logger="twat_video.twat_video"):
        process_data(data=sample_data, config=sample_config, debug=True)

    assert "Debug mode enabled for process_data" in caplog.text
    assert f"Input data: {sample_data}" in caplog.text
    # Check that the logger level was reset (indirectly, by checking no further debug messages from this logger after call)
    # This is tricky to assert perfectly without more complex logger manipulation.
    # For now, primarily ensuring the debug log within the function was emitted.


def test_process_data_no_config():
    """Test process_data when no config is provided."""
    sample_data = ["item_no_config"]
    result = process_data(data=sample_data, config=None) # type: ignore # Testing None explicitly

    assert result["status"] == "processed"
    assert result["item_count"] == len(sample_data)
    assert result["config_name"] == "N/A" # As per current implementation
    assert result["first_item"] == sample_data[0]


def test_main_runs_without_error(caplog):
    """
    Test if the main function runs without raising unhandled exceptions.
    This is a basic integration test for the main script's happy path.
    """
    try:
        # Capture logs to see if main function runs as expected
        with caplog.at_level(logging.INFO, logger="twat_video.twat_video"):
            twat_video_main()
        assert "Starting twat_video application" in caplog.text
        assert "Processing completed. Result:" in caplog.text
        assert "twat_video application finished." in caplog.text
    except Exception as e:
        pytest.fail(f"main() function raised an unexpected exception: {e}")

# Example of a test that might be skipped if a dependency is missing
# @pytest.mark.skipif(not pytest.importorskip("some_optional_dependency"), reason="some_optional_dependency not installed")
# def test_optional_feature():
#     pass

# Example of a parameterized test
# @pytest.mark.parametrize(
#     "input_val, expected_output",
#     [
#         (1, 2),
#         (2, 3),
#         # (val, val + 1)
#     ]
# )
# def test_increment(input_val, expected_output):
#     assert input_val + 1 == expected_output
