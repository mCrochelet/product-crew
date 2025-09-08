"""
Tests for file operations module functions.
"""

from unittest.mock import patch
from ..common import main


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


class TestEnvironmentHandling:
    """Test environment variable handling."""
    
    @patch("product_crew.file_operations.handlers.Path.exists")
    @patch("product_crew.file_operations.handlers.load_dotenv")
    def test_load_environment_file_exists(self, mock_load_dotenv, mock_exists):
        """Test environment loading when .env.local exists."""
        mock_exists.return_value = True
        
        main.load_environment()
        
        mock_load_dotenv.assert_called_once()
    
    @patch("product_crew.file_operations.handlers.Path.exists")
    @patch("product_crew.file_operations.handlers.load_dotenv")
    def test_load_environment_file_not_exists(self, mock_load_dotenv, mock_exists):
        """Test environment loading when .env.local doesn't exist."""
        mock_exists.return_value = False
        
        main.load_environment()
        
        mock_load_dotenv.assert_not_called()