"""Test suite for the twat_video package."""

import logging
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from dataclasses import FrozenInstanceError

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


# Additional comprehensive tests

def test_config_dataclass_features():
    """Test Config dataclass specific features."""
    config = Config()
    # Test field access
    assert hasattr(config, 'name')
    assert hasattr(config, 'value')
    assert hasattr(config, 'options')
    
    # Test that options field has default factory
    config1 = Config()
    config2 = Config()
    assert config1.options is not config2.options  # Different dict instances
    
    # Test mutation of options
    config.options['test'] = 'value'
    assert config.options['test'] == 'value'


def test_config_different_value_types():
    """Test Config with different value types."""
    # String value
    config_str = Config(value="string_value")
    assert config_str.value == "string_value"
    
    # Integer value
    config_int = Config(value=42)
    assert config_int.value == 42
    
    # Float value
    config_float = Config(value=3.14)
    assert config_float.value == 3.14


@pytest.mark.parametrize("data,expected_count", [
    (["single_item"], 1),
    ([1, 2, 3], 3),
    (["a", "b", "c", "d", "e"], 5),
    ([{"key": "value"}, [1, 2, 3]], 2),
])
def test_process_data_different_inputs(data, expected_count):
    """Test process_data with various input types and sizes."""
    result = process_data(data)
    assert result["status"] == "processed"
    assert result["item_count"] == expected_count
    assert result["first_item"] == data[0]
    assert result["config_name"] == "N/A"


def test_process_data_logging_levels(caplog):
    """Test that process_data logs at appropriate levels."""
    sample_data = ["test_item"]
    sample_config = Config(name="logging_test")
    
    with caplog.at_level(logging.INFO):
        process_data(sample_data, sample_config)
    
    # Check INFO level logs
    assert "Processing data with config: logging_test" in caplog.text
    assert "Data processing complete." in caplog.text


def test_process_data_debug_logger_reset():
    """Test that debug mode properly resets logger level."""
    import twat_video.twat_video as module
    original_level = module.logger.level
    
    sample_data = ["debug_test"]
    process_data(sample_data, debug=True)
    
    # Logger level should be reset to original
    assert module.logger.level == original_level


def test_main_exception_handling(caplog):
    """Test main function exception handling."""
    with patch('twat_video.twat_video.process_data') as mock_process:
        mock_process.side_effect = ValueError("Test error")
        
        with caplog.at_level(logging.ERROR):
            twat_video_main()
        
        assert "A ValueError occurred during processing" in caplog.text


def test_main_critical_exception_handling(caplog):
    """Test main function critical exception handling."""
    with patch('twat_video.twat_video.process_data') as mock_process:
        mock_process.side_effect = RuntimeError("Critical error")
        
        with caplog.at_level(logging.CRITICAL):
            with pytest.raises(RuntimeError):
                twat_video_main()
        
        assert "An unexpected critical error occurred" in caplog.text


def test_version_format():
    """Test that version follows expected format."""
    # Should be a valid version string (basic check)
    assert isinstance(__version__, str)
    assert len(__version__) > 0
    # Could add more specific version format checks if needed


def test_module_imports():
    """Test that all expected symbols are properly imported."""
    import twat_video
    
    # Check __all__ exports
    expected_exports = ["Config", "process_data", "main", "__version__"]
    for export in expected_exports:
        assert hasattr(twat_video, export)


def test_config_repr():
    """Test Config string representation."""
    config = Config(name="test_config", value=123)
    repr_str = repr(config)
    assert "Config" in repr_str
    assert "test_config" in repr_str
    assert "123" in repr_str


def test_process_data_with_complex_config():
    """Test process_data with complex configuration."""
    complex_config = Config(
        name="complex_test",
        value=999,
        options={
            "nested": {"key": "value"},
            "list": [1, 2, 3],
            "boolean": True
        }
    )
    
    result = process_data(["test"], complex_config)
    assert result["config_name"] == "complex_test"
    assert result["status"] == "processed"


def test_logging_configuration():
    """Test that logging is properly configured."""
    import twat_video.twat_video as module
    
    # Logger should be configured
    assert module.logger.name == "twat_video.twat_video"
    assert isinstance(module.logger, logging.Logger)


# Performance and edge case tests

def test_process_data_large_dataset():
    """Test process_data with a large dataset."""
    large_data = list(range(10000))
    result = process_data(large_data)
    
    assert result["status"] == "processed"
    assert result["item_count"] == 10000
    assert result["first_item"] == 0


def test_process_data_mixed_types():
    """Test process_data with mixed data types."""
    mixed_data = [
        "string",
        42,
        [1, 2, 3],
        {"key": "value"},
        None,
        True,
        3.14
    ]
    
    result = process_data(mixed_data)
    assert result["status"] == "processed"
    assert result["item_count"] == 7
    assert result["first_item"] == "string"


def test_config_equality():
    """Test Config equality comparison."""
    config1 = Config(name="test", value=123)
    config2 = Config(name="test", value=123)
    config3 = Config(name="different", value=123)
    
    assert config1 == config2
    assert config1 != config3


# Integration test
def test_full_workflow_integration():
    """Test the full workflow from config creation to processing."""
    # Create configuration
    config = Config(
        name="integration_test",
        value="test_value",
        options={"mode": "test", "debug": True}
    )
    
    # Create test data
    test_data = ["item1", "item2", "item3"]
    
    # Process data
    result = process_data(test_data, config, debug=True)
    
    # Verify results
    assert result["status"] == "processed"
    assert result["item_count"] == 3
    assert result["config_name"] == "integration_test"
    assert result["first_item"] == "item1"


# Boundary condition tests
def test_process_data_single_item():
    """Test process_data with single item."""
    result = process_data(["single"])
    assert result["item_count"] == 1
    assert result["first_item"] == "single"


def test_config_empty_options():
    """Test Config with explicitly empty options."""
    config = Config(options={})
    assert config.options == {}
    assert isinstance(config.options, dict)


# Error condition tests
def test_process_data_with_none_items():
    """Test process_data handles None items in data."""
    data_with_none = ["item1", None, "item3"]
    result = process_data(data_with_none)
    
    assert result["status"] == "processed"
    assert result["item_count"] == 3
    assert result["first_item"] == "item1"
