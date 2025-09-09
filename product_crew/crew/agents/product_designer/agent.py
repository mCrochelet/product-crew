"""Product Designer agent definition."""

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


def create_product_designer_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Product Designer agent focused on user experience and interface design."""
    _configure_model(model)
    
    return Agent(
        role='Product Designer',
        goal='Provide user experience strategy, interface design concepts, and usability assessments when delegated design aspects of product initiatives',
        backstory=(
            "You are a talented Product Designer with 8+ years of experience in UX/UI design and "
            "user research. You excel at responding to design strategy requests from Product Managers "
            "and creating comprehensive user experience plans. Your expertise includes user journey "
            "mapping, wireframing, prototyping, usability evaluation, and design system planning. "
            "You are particularly effective at translating product concepts into user-centered design "
            "strategies and providing detailed design recommendations when delegated specific UX/UI "
            "analysis and planning tasks."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )