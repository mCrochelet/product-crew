"""
Common test utilities and fixtures for the product-crew test suite.
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Import the modules from the new structure
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from new modular structure
from product_crew.validation import validate_requirements_path, validate_pid_path, validate_model, validate_openai_api_key
from product_crew.file_operations import create_pid_file, get_output_file_path, load_environment
from product_crew.crew import create_path_printer_agent, create_print_paths_task, run_crew
from product_crew.demo import demo_display_agent_info, demo_display_task_info, demo_section_separator
from product_crew.cli.main import cli

# Create a mock main module for backwards compatibility with existing tests
class MockMain:
    def __init__(self):
        # Validation functions
        self.validate_requirements_path = validate_requirements_path
        self.validate_pid_path = validate_pid_path
        self.validate_model = validate_model
        self.validate_openai_api_key = validate_openai_api_key
        
        # File operations
        self.create_pid_file = create_pid_file
        self.get_output_file_path = get_output_file_path
        self.load_environment = load_environment
        
        # Crew functions
        self.create_path_printer_agent = create_path_printer_agent
        self.create_print_paths_task = create_print_paths_task
        self.run_crew = run_crew
        
        # Demo functions
        self.demo_display_agent_info = demo_display_agent_info
        self.demo_display_task_info = demo_display_task_info
        self.demo_section_separator = demo_section_separator
        
        # CLI
        self.cli = cli

main = MockMain()

# Test artifacts directory
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"