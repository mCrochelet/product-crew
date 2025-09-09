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
        goal='Evaluate technical feasibility and design cost-effective, scalable solutions that can be implemented efficiently',
        backstory=(
            "You are an experienced Engineering Manager with deep technical expertise and 12+ years "
            "in software architecture and team leadership. You specialize in evaluating technical "
            "feasibility, designing scalable architectures, and estimating development effort. You "
            "have successfully led multiple large-scale product implementations and understand the "
            "balance between technical excellence and business constraints. Your strengths include "
            "system design, technology stack selection, risk assessment, and implementation planning."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )