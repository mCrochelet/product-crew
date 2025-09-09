"""Product Designer tasks."""

from crewai import Task
from .agent import create_product_designer_agent
from ...tools import *


def create_product_designer_solution_task(discovery_results: str, model: str = 'gpt-4o') -> Task:
    """Create Product Designer solution design phase task for UX design and interface planning."""
    
    return Task(
        description=f"""
        Design user experience and interface concepts for the initiative.
        
        Discovery Phase Results:
        {discovery_results}
        
        Your task:
        1. Map user journeys using user_journey_mapping
        2. Create wireframe concepts with wireframe_conceptualization
        3. Evaluate design against usability heuristics
        4. Assess design system requirements with design_system_assessment
        5. Define user experience strategy and design principles
        
        Focus on user-centered design, usability, and interface planning.
        """,
        expected_output="""
        UX design strategy including:
        - User journey maps and interaction flows
        - Wireframe concepts for key interfaces
        - Usability evaluation and design recommendations
        - Design system requirements and visual strategy
        """,
        agent=create_product_designer_agent(model)
    )