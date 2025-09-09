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
        goal='Break down solutions into clear, actionable functional increments and detailed requirements',
        backstory=(
            "You are a meticulous Functional Analyst with 7+ years of experience in business analysis "
            "and requirements engineering. You excel at decomposing complex problems into manageable "
            "functional components and translating business needs into clear technical requirements. "
            "Your expertise includes requirements elicitation, user story writing, acceptance criteria "
            "definition, and dependency mapping. You have a keen eye for detail and ensure that "
            "nothing falls through the cracks in the requirements process."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )