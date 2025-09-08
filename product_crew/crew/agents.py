"""CrewAI agent creation and configuration."""

import os
from crewai import Agent


def create_path_printer_agent(model: str = 'gpt-4') -> Agent:
    """Create a CrewAI agent that prints file paths."""
    # Set the model via environment variable for CrewAI
    os.environ['OPENAI_MODEL_NAME'] = model
    
    return Agent(
        role='Path Printer',
        goal='Print file paths exactly as provided without any additional formatting',
        backstory=(
            "You are a simple utility agent that takes file paths and prints them "
            "exactly as raw strings with no additional formatting, commentary, or processing."
        ),
        verbose=False,
        allow_delegation=False
    )