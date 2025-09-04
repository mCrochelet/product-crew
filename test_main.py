"""
Comprehensive tests for the product-crew CLI application.
Implements Task 7: Testing and Validation requirements.
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

# Import the main module
import main


class TestValidationFunctions:
    """Test validation functions."""
    
    def test_validate_requirements_path_valid(self, tmp_path):
        """Test validation with valid requirements path."""
        result = main.validate_requirements_path(str(tmp_path))
        assert result == tmp_path.resolve()
    
    def test_validate_requirements_path_nonexistent(self):
        """Test validation with non-existent requirements path."""
        with pytest.raises(ValueError, match="Requirements path does not exist"):
            main.validate_requirements_path("/nonexistent/path")
    
    def test_validate_pid_path_valid(self, tmp_path):
        """Test validation with valid PID file."""
        pid_file = tmp_path / "test.md"
        pid_file.write_text("# Test PID")
        
        result = main.validate_pid_path(str(pid_file))
        assert result == pid_file.resolve()
    
    def test_validate_pid_path_nonexistent(self):
        """Test validation with non-existent PID file."""
        with pytest.raises(ValueError, match="PID path does not exist"):
            main.validate_pid_path("/nonexistent/file.md")
    
    def test_validate_pid_path_wrong_extension(self, tmp_path):
        """Test validation with non-markdown PID file."""
        pid_file = tmp_path / "test.txt"
        pid_file.write_text("Not markdown")
        
        with pytest.raises(ValueError, match="PID file must be a markdown file"):
            main.validate_pid_path(str(pid_file))


class TestFileOperations:
    """Test file creation and path operations."""
    
    def test_get_output_file_path_overwrite_true(self, tmp_path):
        """Test output path when overwrite is True."""
        original_path = tmp_path / "test.md"
        result = main.get_output_file_path(original_path, True)
        assert result == original_path
    
    def test_get_output_file_path_overwrite_false(self, tmp_path):
        """Test output path when overwrite is False (should add timestamp)."""
        original_path = tmp_path / "test.md"
        result = main.get_output_file_path(original_path, False)
        
        # Should have format: test-YYYY-MM-DD.md
        expected_pattern = r"test-\d{4}-\d{2}-\d{2}\.md$"
        assert str(result.name).endswith(".md")
        assert "test-" in str(result.name)
        assert result.parent == original_path.parent
    
    def test_create_pid_file(self, tmp_path):
        """Test PID file creation."""
        output_path = tmp_path / "output.md"
        content = "# Test Content"
        
        main.create_pid_file(output_path, content)
        
        assert output_path.exists()
        assert output_path.read_text() == content
    
    def test_create_pid_file_creates_directories(self, tmp_path):
        """Test PID file creation creates parent directories."""
        output_path = tmp_path / "subdir" / "output.md"
        content = "# Test Content"
        
        main.create_pid_file(output_path, content)
        
        assert output_path.exists()
        assert output_path.read_text() == content


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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=True)
    def test_cli_success_without_overwrite(self):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=True)
    def test_cli_success_with_overwrite(self):
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
    
    def test_cli_relative_and_absolute_paths(self):
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


class TestCrewAIAgent:
    """Test CrewAI agent functionality."""
    
    def test_create_path_printer_agent(self):
        """Test CrewAI agent creation."""
        agent = main.create_path_printer_agent()
        
        assert agent.role == "Path Printer"
        assert "Print file paths exactly" in agent.goal
        assert agent.verbose is False
        assert agent.allow_delegation is False
    
    def test_create_print_paths_task(self, tmp_path):
        """Test CrewAI task creation."""
        req_path = tmp_path / "requirements"
        pid_path = tmp_path / "test.md"
        
        task = main.create_print_paths_task(req_path, pid_path, True)
        
        assert str(req_path) in task.description
        assert str(pid_path) in task.description
        assert "True" in task.description
        assert task.agent is not None


class TestEnvironmentHandling:
    """Test environment variable handling."""
    
    @patch("main.Path.exists")
    @patch("main.load_dotenv")
    def test_load_environment_file_exists(self, mock_load_dotenv, mock_exists):
        """Test environment loading when .env.local exists."""
        mock_exists.return_value = True
        
        main.load_environment()
        
        mock_load_dotenv.assert_called_once()
    
    @patch("main.Path.exists")
    @patch("main.load_dotenv")
    def test_load_environment_file_not_exists(self, mock_load_dotenv, mock_exists):
        """Test environment loading when .env.local doesn't exist."""
        mock_exists.return_value = False
        
        main.load_environment()
        
        mock_load_dotenv.assert_not_called()


class TestErrorMessages:
    """Test that error messages are user-friendly."""
    
    def test_requirements_path_error_message(self):
        """Test requirements path error message is descriptive."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_requirements_path("/nonexistent")
        
        assert "Requirements path does not exist" in str(exc_info.value)
        assert "/nonexistent" in str(exc_info.value)
    
    def test_pid_path_error_message(self):
        """Test PID path error message is descriptive."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_pid_path("/nonexistent.md")
        
        assert "PID path does not exist" in str(exc_info.value)
    
    def test_pid_extension_error_message(self, tmp_path):
        """Test PID extension error message is descriptive."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("content")
        
        with pytest.raises(ValueError) as exc_info:
            main.validate_pid_path(str(txt_file))
        
        assert "PID file must be a markdown file" in str(exc_info.value)
        assert ".md extension" in str(exc_info.value)


# Test fixtures for pytest
@pytest.fixture
def tmp_path():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


if __name__ == "__main__":
    pytest.main([__file__])