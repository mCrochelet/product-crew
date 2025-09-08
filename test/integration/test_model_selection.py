"""
Integration tests for model selection functionality.
"""

import os
import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch

from ..common import main


class TestModelSelection:
    """Test model selection functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_model_validation_valid_models(self):
        """Test validation with valid OpenAI models."""
        valid_models = [
            'gpt-4', 'gpt-4-turbo', 'gpt-4-turbo-preview',
            'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'
        ]
        
        for model in valid_models:
            result = main.validate_model(model)
            assert result == model
    
    def test_model_validation_case_insensitive(self):
        """Test case-insensitive model validation."""
        result1 = main.validate_model('GPT-4')
        assert result1 == 'GPT-4'
        
        result2 = main.validate_model('gpt-3.5-turbo')
        assert result2 == 'gpt-3.5-turbo'
        
        result3 = main.validate_model('GPT-3.5-TURBO')
        assert result3 == 'GPT-3.5-TURBO'
    
    def test_model_validation_invalid_model(self):
        """Test validation with invalid model."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_model('invalid-model')
        
        assert "Invalid model 'invalid-model'" in str(exc_info.value)
        assert "Supported models:" in str(exc_info.value)
        assert "gpt-4" in str(exc_info.value)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_model_flag_acceptance(self, mock_kickoff):
        """Test that --model flag is accepted without errors."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "gpt-3.5-turbo"
            ])
            
            assert result.exit_code == 0
    
    def test_cli_invalid_model_exit_code(self):
        """Test that invalid model triggers exit code 1."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "invalid-model"
            ])
            
            assert result.exit_code == 1
            assert "Invalid model" in result.output
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_default_model_behavior(self, mock_kickoff):
        """Test default model behavior when no model specified."""
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
            # Should use default gpt-4 model
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_model_with_demo_mode(self, mock_kickoff):
        """Test model selection with demo mode."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--model", "gpt-3.5-turbo",
                    "--demo"
                ])
                
                assert result.exit_code == 0
                assert "gpt-3.5-turbo" in result.output
                assert "DEMO MODE" in result.output
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_model_with_overwrite_flag(self, mock_kickoff):
        """Test model selection combined with overwrite flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "gpt-4-turbo",
                "--overwrite"
            ])
            
            assert result.exit_code == 0
    
    def test_agent_creation_with_model(self):
        """Test agent creation with specific model."""
        model = "gpt-3.5-turbo"
        agent = main.create_path_printer_agent(model)
        
        assert agent.role == "Path Printer"
        assert "Print file paths exactly" in agent.goal
        # Check that environment variable was set
        assert os.getenv("OPENAI_MODEL_NAME") == model
    
    def test_task_creation_with_model(self, tmp_path):
        """Test task creation with model parameter."""
        model = "gpt-4-turbo"
        task = main.create_print_paths_task(tmp_path, tmp_path / "test.md", False, model)
        
        assert task.agent is not None
        assert task.agent.role == "Path Printer"