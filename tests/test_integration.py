"""Integration tests for the twat_video package."""

import pytest
import subprocess
import sys
import os
from pathlib import Path

from twat_video import __version__


class TestIntegration:
    """Integration tests that test the package as a whole."""

    def test_package_import(self):
        """Test that the package can be imported successfully."""
        import twat_video
        assert hasattr(twat_video, '__version__')
        assert hasattr(twat_video, 'Config')
        assert hasattr(twat_video, 'process_data')
        assert hasattr(twat_video, 'main')

    def test_module_execution(self):
        """Test that the module can be executed directly."""
        result = subprocess.run([
            sys.executable, "-m", "twat_video.twat_video"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0
        # Output goes to stderr due to logging configuration
        output = result.stdout + result.stderr
        assert "Starting twat_video application" in output
        assert "twat_video application finished" in output

    def test_cli_execution(self):
        """Test that the CLI can be executed."""
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", "--version"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0
        assert __version__ in result.stdout

    def test_cli_process_command(self):
        """Test CLI process command integration."""
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", "process", "test_item"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0
        assert "Processed 1 items successfully" in result.stdout

    def test_cli_demo_command(self):
        """Test CLI demo command integration."""
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", "demo"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0

    def test_version_consistency(self):
        """Test that version is consistent across different access methods."""
        # Import version
        from twat_video import __version__ as import_version
        
        # CLI version
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", "--version"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0
        assert import_version in result.stdout

    def test_error_handling_integration(self):
        """Test error handling in real execution."""
        # Test with invalid CLI command
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", "invalid_command"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode != 0

    def test_package_structure(self):
        """Test that package structure is correct."""
        import twat_video
        package_path = Path(twat_video.__file__).parent
        
        # Check required files exist
        assert (package_path / "__init__.py").exists()
        assert (package_path / "twat_video.py").exists()
        assert (package_path / "cli.py").exists()
        assert (package_path / "__version__.py").exists()

    def test_config_file_generation(self):
        """Test config file generation integration."""
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_file = os.path.join(tmp_dir, "test_config.yml")
            
            result = subprocess.run([
                sys.executable, "-m", "twat_video.cli", 
                "config", "--output-file", config_file
            ], capture_output=True, text=True, timeout=30)
            
            assert result.returncode == 0
            assert os.path.exists(config_file)
            
            # Check file content
            with open(config_file, 'r') as f:
                content = f.read()
                assert "Sample Configuration" in content
                assert "name: sample_config" in content

    def test_comprehensive_workflow(self):
        """Test a comprehensive workflow using the package."""
        from twat_video import Config, process_data
        
        # Create configuration
        config = Config(
            name="integration_test",
            value=42,
            options={"test": True}
        )
        
        # Process data
        test_data = ["item1", "item2", "item3"]
        result = process_data(test_data, config=config)
        
        # Verify results
        assert result["status"] == "processed"
        assert result["item_count"] == 3
        assert result["config_name"] == "integration_test"

    def test_cli_with_different_options(self):
        """Test CLI with various option combinations."""
        # Test verbose mode
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", 
            "--verbose", "process", "item1"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0
        assert "Processing result" in result.stdout
        
        # Test quiet mode
        result = subprocess.run([
            sys.executable, "-m", "twat_video.cli", 
            "--quiet", "process", "item1"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0

    def test_environment_independence(self):
        """Test that the package works in different environments."""
        # Test with different Python executable paths
        result = subprocess.run([
            sys.executable, "-c", 
            "import twat_video; print(twat_video.__version__)"
        ], capture_output=True, text=True, timeout=30)
        
        assert result.returncode == 0
        assert __version__ in result.stdout

    def test_memory_usage(self):
        """Test basic memory usage patterns."""
        from twat_video import Config, process_data
        
        # Create multiple configs and process data
        configs = [Config(name=f"config_{i}") for i in range(100)]
        
        for config in configs:
            result = process_data([f"item_{i}" for i in range(10)], config=config)
            assert result["status"] == "processed"
            assert result["item_count"] == 10

    def test_concurrent_usage(self):
        """Test concurrent usage patterns."""
        import threading
        from twat_video import Config, process_data
        
        results = []
        
        def worker(thread_id):
            config = Config(name=f"thread_{thread_id}")
            data = [f"item_{i}" for i in range(5)]
            result = process_data(data, config=config)
            results.append(result)
        
        # Run multiple threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Verify all results
        assert len(results) == 5
        for result in results:
            assert result["status"] == "processed"
            assert result["item_count"] == 5

    def test_large_data_processing(self):
        """Test processing large amounts of data."""
        from twat_video import Config, process_data
        
        # Create large dataset
        large_data = list(range(10000))
        config = Config(name="large_test")
        
        result = process_data(large_data, config=config)
        
        assert result["status"] == "processed"
        assert result["item_count"] == 10000
        assert result["first_item"] == 0

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific test")
    def test_unix_permissions(self):
        """Test Unix-specific functionality."""
        # Test that files have correct permissions
        import twat_video
        import stat
        
        package_path = Path(twat_video.__file__).parent
        py_files = list(package_path.glob("*.py"))
        
        for py_file in py_files:
            file_stat = py_file.stat()
            # Check that file is readable
            assert file_stat.st_mode & stat.S_IRUSR

    def test_import_performance(self):
        """Test import performance."""
        import time
        
        start_time = time.time()
        import twat_video
        import_time = time.time() - start_time
        
        # Import should be reasonably fast (less than 1 second)
        assert import_time < 1.0
        
        # Test that subsequent imports are cached
        start_time = time.time()
        import twat_video  # Should be cached
        cached_import_time = time.time() - start_time
        
        # Cached import should be much faster
        assert cached_import_time < 0.1