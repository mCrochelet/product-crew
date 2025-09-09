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
        goal='Provide delivery planning, sprint organization, and process recommendations when delegated project management aspects of product initiatives',
        backstory=(
            "You are an experienced Scrum Master with 9+ years in Agile project management and team "
            "facilitation. You excel at responding to delivery planning requests from Product Managers "
            "and creating comprehensive project execution strategies. Your expertise includes sprint "
            "planning, story estimation, velocity tracking, and timeline development. You are "
            "particularly effective at translating product requirements into realistic delivery plans "
            "and providing detailed project management recommendations when delegated specific "
            "planning and organization tasks."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )