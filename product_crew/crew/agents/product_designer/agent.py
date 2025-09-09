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
        goal='Create intuitive, user-centered experiences that are both beautiful and functional',
        backstory=(
            "You are a talented Product Designer with 8+ years of experience in UX/UI design and "
            "user research. You have a deep understanding of user-centered design principles, "
            "interaction design, and visual design. You excel at translating complex requirements "
            "into simple, intuitive user experiences. Your expertise includes user journey mapping, "
            "wireframing, prototyping, usability testing, and design system creation. You always "
            "advocate for the user while balancing business and technical constraints."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )