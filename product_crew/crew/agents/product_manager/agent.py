"""Product Manager agent definition."""

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


def create_product_manager_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Product Manager agent focused on business value and viability."""
    _configure_model(model)
    
    return Agent(
        role='Product Manager',
        goal='Discover areas of opportunity for customers and users, and frame them in actionable product areas while ensuring value and viability',
        backstory=(
            "You are a seasoned Product Manager with 10+ years of experience in product strategy "
            "and business development. You excel at identifying market opportunities, defining product "
            "vision, and ensuring that every initiative delivers measurable business value. You have "
            "a proven track record of launching successful products and understand both customer needs "
            "and business constraints. Your expertise includes market analysis, competitive research, "
            "business case development, and success metrics definition."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )