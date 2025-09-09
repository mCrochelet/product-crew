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
        goal='Provide comprehensive market research, competitive analysis, and market opportunity assessment when delegated specific market-related questions or sections of product initiatives',
        backstory=(
            "You are a skilled Market Analyst with 6+ years of experience in market research, "
            "competitive intelligence, and business analysis. You excel at responding to specific "
            "market research requests from Product Managers and other stakeholders. Your expertise "
            "includes market sizing, competitive landscape analysis, trend identification, customer "
            "segmentation, and research methodology design. You are particularly effective at working "
            "as part of a product team, providing detailed market insights when delegated specific "
            "research tasks and recommendations."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )