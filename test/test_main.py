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
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Import the main module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

# Test artifacts directory
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"


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
    
    def test_validate_pid_path_valid(self):
        """Test validation with valid PID file."""
        pid_file = ARTIFACTS_DIR / "sample_pid.md"
        
        result = main.validate_pid_path(str(pid_file))
        assert result == pid_file.resolve()
    
    def test_validate_pid_path_nonexistent(self):
        """Test validation with non-existent PID file."""
        with pytest.raises(ValueError, match="PID path does not exist"):
            main.validate_pid_path("/nonexistent/file.md")
    
    def test_validate_pid_path_wrong_extension(self):
        """Test validation with non-markdown PID file."""
        pid_file = ARTIFACTS_DIR / "invalid_file.txt"
        
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
        assert "--demo" in result.output
        assert "Enable interactive demo mode" in result.output
    
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


class TestDemoMode:
    """Test demo mode functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_demo_flag_acceptance(self):
        """Test that --demo flag is accepted without errors."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            # Mock input to simulate Enter key presses
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo"
                ])
                
                assert result.exit_code == 0
                # Verify demo mode specific output
                assert "DEMO MODE" in result.output
    
    def test_demo_mode_with_overwrite(self):
        """Test demo mode combined with overwrite flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo",
                    "--overwrite"
                ])
                
                assert result.exit_code == 0
                assert "DEMO MODE" in result.output
                assert "True" in result.output  # Overwrite flag value
    
    def test_demo_mode_interactive_steps(self):
        """Test that demo mode shows interactive steps."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo"
                ])
                
                # Verify step indicators
                assert "Step 1/5" in result.output
                assert "Step 2/5" in result.output
                assert "Step 3/5" in result.output
                assert "Step 4/5" in result.output
                assert "Step 5/5" in result.output
                assert "Completion" in result.output
    
    def test_demo_mode_visualization_elements(self):
        """Test demo mode visualization elements."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo"
                ])
                
                # Verify visualization elements
                assert "AGENT PROFILE" in result.output
                assert "TASK #1" in result.output
                assert "EXECUTION PARAMETERS" in result.output
                assert "INITIALIZATION" in result.output
                assert "AGENT & TASK CREATION" in result.output
                assert "CREW EXECUTION" in result.output
                assert "OUTPUT GENERATION" in result.output
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_demo_mode_keyboard_interrupt_handling(self, mock_input):
        """Test graceful handling of Ctrl+C in demo mode."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--demo"
            ])
            
            assert result.exit_code == 0  # Graceful exit
            assert "Demo mode interrupted" in result.output
    
    def test_demo_mode_agent_information_display(self):
        """Test that agent information is displayed in demo mode."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo"
                ])
                
                # Verify agent details are shown
                assert "Role: Path Printer" in result.output
                assert "Goal:" in result.output
                assert "Backstory:" in result.output
    
    def test_demo_mode_task_information_display(self):
        """Test that task information is displayed in demo mode."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo"
                ])
                
                # Verify task details are shown
                assert "Description:" in result.output
                assert "Expected Output:" in result.output
    
    def test_normal_mode_unaffected_by_demo_changes(self):
        """Test that normal mode execution is unaffected by demo mode additions."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file)
            ])
            
            assert result.exit_code == 0
            # Verify no demo mode elements in normal mode
            assert "DEMO MODE" not in result.output
            assert "AGENT PROFILE" not in result.output
            assert "Press Enter to continue" not in result.output
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=True)
    def test_demo_mode_without_api_key(self):
        """Test demo mode behavior when OpenAI API key is missing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--demo"
                ])
                
                assert result.exit_code == 0
                assert "Warning: No OpenAI API key found" in result.output
                assert "Using direct file copy mode" in result.output


class TestDemoUtilityFunctions:
    """Test demo mode utility functions."""
    
    def test_demo_display_agent_info(self, capsys):
        """Test demo agent info display function."""
        agent = main.create_path_printer_agent()
        
        main.demo_display_agent_info(agent)
        
        captured = capsys.readouterr()
        assert "AGENT PROFILE" in captured.out
        assert "Role: Path Printer" in captured.out
        assert "Goal:" in captured.out
        assert "Backstory:" in captured.out
    
    def test_demo_display_task_info(self, capsys, tmp_path):
        """Test demo task info display function."""
        task = main.create_print_paths_task(tmp_path, tmp_path / "test.md", False)
        
        main.demo_display_task_info(task, 1)
        
        captured = capsys.readouterr()
        assert "TASK #1" in captured.out
        assert "Description:" in captured.out
        assert "Expected Output:" in captured.out
    
    def test_demo_section_separator(self, capsys):
        """Test demo section separator function."""
        main.demo_section_separator("TEST SECTION")
        
        captured = capsys.readouterr()
        assert "TEST SECTION" in captured.out
        assert "│" in captured.out
        assert "┌" in captured.out


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
    
    def test_pid_extension_error_message(self):
        """Test PID extension error message is descriptive."""
        txt_file = ARTIFACTS_DIR / "invalid_file.txt"
        
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