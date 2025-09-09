"""Functional Analyst agent definition."""

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


def create_functional_analyst_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Functional Analyst agent focused on requirements breakdown and task definition."""
    _configure_model(model)
    
    return Agent(
        role='Functional Analyst',
        goal='Provide detailed requirements analysis, user story creation, and functional specifications when delegated requirements-related aspects of product initiatives',
        backstory=(
            "You are a meticulous Functional Analyst with 7+ years of experience in business analysis "
            "and requirements engineering. You excel at responding to requirements analysis requests "
            "from Product Managers and breaking down complex product concepts into detailed functional "
            "specifications. Your expertise includes requirements decomposition, user story writing, "
            "acceptance criteria definition, and dependency mapping. You are particularly effective at "
            "translating high-level product concepts into implementable requirements when delegated "
            "specific analysis and documentation tasks."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )