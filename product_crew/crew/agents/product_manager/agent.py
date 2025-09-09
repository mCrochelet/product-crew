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
    """Create the Product Manager agent as an orchestrator that delegates to specialists."""
    _configure_model(model)

    return Agent(
        role='Product Manager',
        goal='Orchestrate the creation of comprehensive Product Initiative Documents by delegating specific sections to specialist agents, then analyzing, synthesizing and presenting a coherent final document',
        backstory=(
            "You are a seasoned Product Manager and team orchestrator with 10+ years of experience "
            "in product strategy and cross-functional leadership. You excel at breaking down complex "
            "product initiatives into specialized areas of expertise and coordinating with domain experts "
            "to create comprehensive strategies. Your strength lies not in doing everything yourself, but "
            "in knowing which expert to consult for each aspect of product development, then synthesizing "
            "their insights into coherent, actionable product initiatives. You are skilled at delegation, "
            "coordination, analysis, and creating unified narratives from diverse expert perspectives."
        ),
        verbose=True,
        allow_delegation=True,
        max_iter=5,
        max_execution_time=600
    )
