"""
Tests for validation module functions.
"""

import pytest
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