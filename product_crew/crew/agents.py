"""Product Manager agent for problem understanding analysis."""

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
    """Create a Product Manager agent that analyzes problem understanding in PIDs."""
    _configure_model(model)

    return Agent(
        role='Product Manager',
        goal='Analyze Product Initiative Documents to assess the depth and quality of problem understanding, focusing on user identification, jobs-to-be-done, value proposition, competitive landscape, success metrics, and service blueprint context',
        backstory=(
            "You are an experienced Product Manager with 10+ years of experience in product strategy "
            "and problem analysis. You excel at evaluating whether product initiatives have properly "
            "understood the problem space before jumping to solutions. You focus specifically on ensuring "
            "that teams have clearly identified: who the users and customers are, what job they're trying "
            "to accomplish, what value solving this creates, how the competitive landscape addresses this "
            "job currently, how success would be measured, and how this fits within the broader service "
            "ecosystem. You never suggest solutions, but rather assess the quality of problem understanding "
            "and identify gaps in the problem analysis."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )