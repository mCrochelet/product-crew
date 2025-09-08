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
    """Validate that the model is a supported OpenAI model."""
    # List of valid OpenAI models
    valid_models = {
        'gpt-4',
        'gpt-4-turbo',
        'gpt-4-turbo-preview', 
        'gpt-4-0125-preview',
        'gpt-4-1106-preview',
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-16k',
        'gpt-3.5-turbo-1106',
        'gpt-3.5-turbo-0125',
    }
    
    # Case-insensitive comparison
    model_lower = model.lower()
    valid_models_lower = {m.lower() for m in valid_models}
    
    if model_lower not in valid_models_lower:
        supported_models = ', '.join(sorted(valid_models))
        raise ValueError(f"Invalid model '{model}'. Supported models: {supported_models}")
    
    # Return the original case model name
    return model


def validate_openai_api_key() -> str:
    """Validate that OpenAI API key is available in environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    return api_key