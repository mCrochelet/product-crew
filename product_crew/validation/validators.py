"""Input validation functions for CLI arguments."""

import os
from pathlib import Path


def validate_requirements_path(requirements_path: str) -> Path:
    """Validate that the requirements path exists and return absolute path."""
    path = Path(requirements_path).resolve()
    if not path.exists():
        raise ValueError(f"Requirements path does not exist: {path}")
    return path


def validate_pid_path(pid_path: str) -> Path:
    """Validate that the pid path exists and is a markdown file, return absolute path."""
    path = Path(pid_path).resolve()
    if not path.exists():
        raise ValueError(f"PID path does not exist: {path}")
    if not path.suffix.lower() == '.md':
        raise ValueError(f"PID file must be a markdown file (.md extension): {path}")
    return path


def validate_model(model: str) -> str:
    """Validate that the model is provided (CrewAI will handle actual model validation)."""
    if not model or not model.strip():
        raise ValueError("Model name cannot be empty")
    
    return model.strip()


def validate_openai_api_key() -> str:
    """Validate that OpenAI API key is available in environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    return api_key


def validate_api_key_for_model(model: str) -> str:
    """Validate that the appropriate API key is available for the selected model."""
    if model.lower().startswith('claude-'):
        # Anthropic model - validate Anthropic API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key not found. Please set ANTHROPIC_API_KEY environment variable.")
        return api_key
    else:
        # Assume OpenAI for non-Claude models - validate OpenAI API key
        return validate_openai_api_key()