"""Functional Analyst tasks."""

from crewai import Task
from .agent import create_functional_analyst_agent
from ...tools import *


def create_functional_analyst_breakdown_task(solution_results: str, model: str = 'gpt-4o') -> Task:
    """Create Functional Analyst breakdown phase task for requirements and user stories."""
    
    return Task(
        description=f"""
        Break down the solution into detailed requirements and user stories.
        
        Solution Design Results:
        {solution_results}
        
        Your task:
        1. Decompose requirements using requirements_decomposition
        2. Create user stories with user_story_creation
        3. Define acceptance criteria using acceptance_criteria_definition
        4. Map dependencies with dependency_mapping
        5. Ensure all requirements are traceable and testable
        
        Focus on clarity, completeness, and implementation readiness.
        """,
        expected_output="""
        Requirements breakdown including:
        - Detailed functional requirements specification
        - User stories with clear acceptance criteria
        - Dependency mapping and implementation sequence
        - Traceability matrix and testing requirements
        """,
        agent=create_functional_analyst_agent(model)
    )