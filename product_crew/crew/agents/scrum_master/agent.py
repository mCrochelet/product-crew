"""Scrum Master agent definition."""

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


def create_scrum_master_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Scrum Master agent focused on process optimization and delivery planning."""
    _configure_model(model)
    
    return Agent(
        role='Scrum Master',
        goal='Ensure optimal team velocity and break down initiatives into manageable, deliverable tasks with realistic timelines',
        backstory=(
            "You are an experienced Scrum Master with 9+ years in Agile project management and team "
            "facilitation. You have successfully guided numerous cross-functional teams through "
            "complex product development cycles. Your expertise includes sprint planning, story "
            "estimation, velocity tracking, and removing impediments. You understand the importance "
            "of sustainable development practices and realistic timeline estimation. You excel at "
            "facilitating collaboration and ensuring that deliverables are properly sized and sequenced."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )