"""
Tests for CLI module functionality.
"""

import os
import tempfile
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch

from ..common import main


class TestCLIIntegration:
    """Test CLI integration and end-to-end functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_cli_missing_arguments(self):
        """Test CLI with missing required arguments."""
        result = self.runner.invoke(main.cli, [])
        assert result.exit_code != 0
        assert "Missing option" in result.output
    
    def test_cli_help_display(self):
        """Test CLI help text display."""
        result = self.runner.invoke(main.cli, ["--help"])
        assert result.exit_code == 0
        assert "Product crew CLI application" in result.output
        assert "--requirements" in result.output
        assert "--pid" in result.output
        assert "--overwrite" in result.output
        assert "--demo" in result.output
        assert "Enable interactive demo mode" in result.output
        assert "--model" in result.output
        assert "Model to use for agents (default: gpt-4o)" in result.output
    
    def test_cli_validation_failure_nonexistent_requirements(self):
        """Test CLI exit code for non-existent requirements path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pid_file = Path(tmp_dir) / "test.md"
            pid_file.write_text("# Test")
            
            result = self.runner.invoke(main.cli, [
                "-r", "/nonexistent",
                "--pid", str(pid_file)
            ])
            
            assert result.exit_code == 1
            assert "Requirements path does not exist" in result.output
    
    def test_cli_validation_failure_nonexistent_pid(self):
        """Test CLI exit code for non-existent PID file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.runner.invoke(main.cli, [
                "-r", tmp_dir,
                "--pid", "/nonexistent.md"
            ])
            
            assert result.exit_code == 1
            assert "PID path does not exist" in result.output
    
    def test_cli_validation_failure_wrong_pid_extension(self):
        """Test CLI exit code for PID file without .md extension."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pid_file = Path(tmp_dir) / "test.txt"
            pid_file.write_text("Not markdown")
            
            result = self.runner.invoke(main.cli, [
                "-r", tmp_dir,
                "--pid", str(pid_file)
            ])
            
            assert result.exit_code == 1
            assert "PID file must be a markdown file" in result.output
    
    def test_cli_validation_failure_missing_api_key(self):
        """Test CLI exit code when OpenAI API key is missing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pid_file = Path(tmp_dir) / "test.md"
            pid_file.write_text("# Test")
            
            with patch.dict(os.environ, {}, clear=True):
                result = self.runner.invoke(main.cli, [
                    "-r", tmp_dir,
                    "--pid", str(pid_file)
                ])
                
                assert result.exit_code == 1
                assert "OpenAI API key not found" in result.output
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_success_without_overwrite(self, mock_kickoff):
        """Test successful CLI execution without overwrite flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create requirements directory and PID file
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_content = "# Test PID Content"
            pid_file.write_text(pid_content)
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file)
            ])
            
            assert result.exit_code == 0
            assert str(req_dir.resolve()) in result.output
            assert str(pid_file.resolve()) in result.output
            assert "False" in result.output
            
            # Check that timestamped file was created
            timestamped_files = list(req_dir.glob("test-*.md"))
            assert len(timestamped_files) == 1
            assert timestamped_files[0].read_text() == pid_content
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_success_with_overwrite(self, mock_kickoff):
        """Test successful CLI execution with overwrite flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create requirements directory and PID file
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            original_content = "# Original Content"
            pid_file.write_text(original_content)
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--overwrite"
            ])
            
            assert result.exit_code == 0
            assert str(req_dir.resolve()) in result.output
            assert str(pid_file.resolve()) in result.output
            assert "True" in result.output
            
            # Original file should still exist and contain original content
            assert pid_file.exists()
            assert pid_file.read_text() == original_content
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_relative_and_absolute_paths(self, mock_kickoff):
        """Test CLI with both relative and absolute paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test Content")
            
            # Test with absolute paths
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir.resolve()),
                "--pid", str(pid_file.resolve())
            ])
            assert result.exit_code == 0
            
            # The paths in output should be absolute
            assert str(req_dir.resolve()) in result.output
            assert str(pid_file.resolve()) in result.output