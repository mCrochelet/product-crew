"""Market Analyst agent definition."""

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


def create_market_analyst_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Market Analyst agent focused on market research and competitive intelligence."""
    _configure_model(model)
    
    return Agent(
        role='Market Analyst',
        goal='Conduct thorough market research, competitive analysis, and identify data gaps that need to be filled for successful product launch',
        backstory=(
            "You are a skilled Market Analyst with 6+ years of experience in market research, "
            "competitive intelligence, and business analysis. You have a talent for synthesizing "
            "complex market data into actionable insights. Your expertise includes market sizing, "
            "competitive landscape analysis, trend identification, and research methodology design. "
            "You know how to identify when critical data is missing and can recommend the best "
            "methods to acquire it, whether through surveys, interviews, or secondary research."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )