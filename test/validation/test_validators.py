"""
Tests for validation module functions.
"""

import os
import pytest
from unittest.mock import patch
from ..common import main, ARTIFACTS_DIR


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


class TestModelAndAPIKeyValidation:
    """Test model validation and API key validation for both providers."""
    
    def test_validate_model_basic(self):
        """Test basic model validation (non-empty)."""
        # Valid models - CrewAI will handle the actual validation
        models = ['gpt-4', 'gpt-4o', 'claude-3-5-sonnet-20241022', 'some-future-model']
        
        for model in models:
            result = main.validate_model(model)
            assert result == model
    
    def test_validate_model_with_whitespace(self):
        """Test model validation strips whitespace."""
        result = main.validate_model('  gpt-4o  ')
        assert result == 'gpt-4o'
    
    def test_validate_model_empty(self):
        """Test validation fails with empty model."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_model('')
        
        assert "Model name cannot be empty" in str(exc_info.value)
    
    def test_validate_model_whitespace_only(self):
        """Test validation fails with whitespace-only model."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_model('   ')
        
        assert "Model name cannot be empty" in str(exc_info.value)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_openai_key"})
    def test_validate_api_key_openai_valid(self):
        """Test API key validation for OpenAI models with valid key."""
        result = main.validate_api_key_for_model("gpt-4o")
        assert result == "test_openai_key"
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_anthropic_key"})
    def test_validate_api_key_anthropic_valid(self):
        """Test API key validation for Anthropic models with valid key."""
        result = main.validate_api_key_for_model("claude-3-5-sonnet-20241022")
        assert result == "test_anthropic_key"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_validate_api_key_openai_missing(self):
        """Test API key validation for OpenAI models with missing key."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_api_key_for_model("gpt-4o")
        
        assert "OpenAI API key not found" in str(exc_info.value)
        assert "OPENAI_API_KEY environment variable" in str(exc_info.value)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_validate_api_key_anthropic_missing(self):
        """Test API key validation for Anthropic models with missing key."""
        with pytest.raises(ValueError) as exc_info:
            main.validate_api_key_for_model("claude-3-5-sonnet-20241022")
        
        assert "Anthropic API key not found" in str(exc_info.value)
        assert "ANTHROPIC_API_KEY environment variable" in str(exc_info.value)
    
    def test_provider_detection_openai(self):
        """Test that OpenAI models are correctly identified."""
        openai_models = ['gpt-4', 'gpt-4o', 'gpt-3.5-turbo', 'GPT-4-TURBO']
        
        for model in openai_models:
            # Should not start with claude-, so should use OpenAI validation
            with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
                result = main.validate_api_key_for_model(model)
                assert result == "test_key"
    
    def test_provider_detection_anthropic(self):
        """Test that Anthropic models are correctly identified."""
        anthropic_models = [
            'claude-3-5-sonnet-20241022', 'CLAUDE-3-OPUS-20240229',
            'claude-3-haiku-20240307'
        ]
        
        for model in anthropic_models:
            # Should start with claude-, so should use Anthropic validation
            with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"}):
                result = main.validate_api_key_for_model(model)
                assert result == "test_key"