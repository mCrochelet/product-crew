"""
Tests for demo module utility functions.
"""

import os
import tempfile
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch

from ..common import main


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


class TestDemoMode:
    """Test demo mode functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_demo_flag_acceptance(self, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_demo_mode_with_overwrite(self, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_demo_mode_interactive_steps(self, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_demo_mode_visualization_elements(self, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_demo_mode_keyboard_interrupt_handling(self, mock_input, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_demo_mode_agent_information_display(self, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_demo_mode_task_information_display(self, mock_kickoff):
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_normal_mode_unaffected_by_demo_changes(self, mock_kickoff):
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
                
                assert result.exit_code == 1
                assert "OpenAI API key not found" in result.output