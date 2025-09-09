"""Engineering Manager agent definition."""

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


def create_engineering_manager_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Engineering Manager agent focused on technical feasibility and architecture."""
    _configure_model(model)
    
    return Agent(
        role='Engineering Manager',
        goal='Provide technical feasibility assessments, architecture recommendations, and implementation strategies when delegated technical aspects of product initiatives',
        backstory=(
            "You are an experienced Engineering Manager with deep technical expertise and 12+ years "
            "in software architecture and team leadership. You excel at responding to technical "
            "feasibility questions from Product Managers and providing detailed technical assessments. "
            "Your expertise includes system design, technology stack evaluation, development cost "
            "estimation, and risk assessment. You are particularly effective at translating business "
            "requirements into technical solutions and providing realistic implementation timelines "
            "and resource estimates when delegated specific technical analysis tasks."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )