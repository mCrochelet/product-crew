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
    
    def test_model_validation_accepts_any_model(self):
        """Test validation accepts any non-empty model (CrewAI handles validation)."""
        models = [
            'gpt-4', 'gpt-4o', 'gpt-4-turbo', 'claude-3-5-sonnet-20241022',
            'future-model-name', 'custom-model'
        ]
        
        for model in models:
            result = main.validate_model(model)
            assert result == model
    
    def test_model_validation_preserves_case(self):
        """Test model validation preserves original case."""
        result1 = main.validate_model('GPT-4')
        assert result1 == 'GPT-4'
        
        result2 = main.validate_model('gpt-3.5-turbo')
        assert result2 == 'gpt-3.5-turbo'
        
        result3 = main.validate_model('Claude-3-OPUS')
        assert result3 == 'Claude-3-OPUS'
    
    def test_model_validation_empty_model(self):
        """Test validation with empty model."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_model('')
        
        assert "Model name cannot be empty" in str(exc_info.value)
    
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
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_accepts_any_model_name(self, mock_kickoff):
        """Test that CLI accepts any model name and passes it to CrewAI."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            # CLI should accept any model name - CrewAI handles validation
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "some-future-model"
            ])
            
            # Should pass CLI validation and reach CrewAI
            assert result.exit_code == 0
    
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
            # Should use default gpt-4o model
    
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
        assert os.getenv("OPENAI_MODEL_NAME") == model or os.getenv("MODEL") == model
    
    def test_task_creation_with_model(self, tmp_path):
        """Test task creation with model parameter."""
        model = "gpt-4-turbo"
        task = main.create_print_paths_task(tmp_path, tmp_path / "test.md", False, model)
        
        assert task.agent is not None
        assert task.agent.role == "Path Printer"
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_cli_anthropic_model_acceptance(self, mock_kickoff):
        """Test that Anthropic models are accepted in CLI."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "claude-3-5-sonnet-20241022"
            ])
            
            assert result.exit_code == 0
    
    @patch.dict(os.environ, {}, clear=True)
    def test_cli_anthropic_missing_api_key(self):
        """Test that CLI fails with missing Anthropic API key."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "claude-3-5-sonnet-20241022"
            ])
            
            assert result.exit_code == 1
            assert "Anthropic API key not found" in result.output
    
    @patch.dict(os.environ, {}, clear=True)
    def test_cli_openai_missing_api_key(self):
        """Test that CLI fails with missing OpenAI API key."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            result = self.runner.invoke(main.cli, [
                "-r", str(req_dir),
                "--pid", str(pid_file),
                "--model", "gpt-4o"
            ])
            
            assert result.exit_code == 1
            assert "OpenAI API key not found" in result.output
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
    @patch('product_crew.crew.runner.Crew.kickoff', return_value="mocked")
    def test_anthropic_model_with_demo_mode(self, mock_kickoff):
        """Test Anthropic model selection with demo mode."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            req_dir = Path(tmp_dir) / "requirements"
            req_dir.mkdir()
            
            pid_file = req_dir / "test.md"
            pid_file.write_text("# Test PID")
            
            with patch('builtins.input', side_effect=[''] * 10):
                result = self.runner.invoke(main.cli, [
                    "-r", str(req_dir),
                    "--pid", str(pid_file),
                    "--model", "claude-3-5-sonnet-20241022",
                    "--demo"
                ])
                
                assert result.exit_code == 0
                assert "claude-3-5-sonnet-20241022" in result.output
                assert "DEMO MODE" in result.output
    
    def test_agent_creation_with_anthropic_model(self):
        """Test agent creation with Anthropic model."""
        model = "claude-3-5-sonnet-20241022"
        agent = main.create_path_printer_agent(model)
        
        assert agent.role == "Path Printer"
        assert "Print file paths exactly" in agent.goal
        # Check that environment variable was set for Anthropic
        assert os.getenv("MODEL") == model
    
    def test_new_default_model_gpt4o(self):
        """Test that the new default model is gpt-4o."""
        agent = main.create_path_printer_agent()  # No model specified, should use default
        
        assert agent.role == "Path Printer"
        # Check that the default model (gpt-4o) was set
        expected_default = "gpt-4o"
        assert os.getenv("OPENAI_MODEL_NAME") == expected_default or os.getenv("MODEL") == expected_default