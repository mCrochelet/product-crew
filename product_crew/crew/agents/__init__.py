"""Agent definitions module."""

from .product_manager import create_product_manager_agent
from .engineering_manager import create_engineering_manager_agent
from .product_designer import create_product_designer_agent
from .functional_analyst import create_functional_analyst_agent
from .scrum_master import create_scrum_master_agent
from .market_analyst import create_market_analyst_agent

# Legacy function for backwards compatibility with tests
import os
from crewai import Agent


def _is_anthropic_model(model: str) -> bool:
    """Check if the model is an Anthropic model."""
    return model.lower().startswith('claude-')


def _configure_model(model: str) -> None:
    """Configure environment variables for the specified model."""
    if _is_anthropic_model(model):
        os.environ['MODEL'] = model
    else:
        # For OpenAI models, use the legacy environment variable for backwards compatibility
        os.environ['OPENAI_MODEL_NAME'] = model
        os.environ['MODEL'] = model


def create_path_printer_agent(model: str = 'gpt-4o') -> Agent:
    """Legacy function - creates original path printer agent for backwards compatibility."""
    _configure_model(model)
    
    return Agent(
        role='Path Printer',
        goal='Print file paths exactly as provided without any additional formatting',
        backstory=(
            "You are a simple utility agent that takes file paths and prints them "
            "exactly as raw strings with no additional formatting, commentary, or processing."
        ),
        verbose=False,
        allow_delegation=False
    )


__all__ = [
    'create_product_manager_agent',
    'create_engineering_manager_agent',
    'create_product_designer_agent',
    'create_functional_analyst_agent',
    'create_scrum_master_agent',
    'create_market_analyst_agent',
    'create_path_printer_agent'  # Legacy compatibility
]