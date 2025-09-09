"""Engineering Manager tasks."""

from crewai import Task
from .agent import create_engineering_manager_agent
from ...tools import *


def create_engineering_manager_solution_task(discovery_results: str, model: str = 'gpt-4o') -> Task:
    """Create Engineering Manager solution design phase task for technical assessment."""
    
    return Task(
        description=f"""
        Assess technical feasibility and design architecture for the initiative.
        
        Discovery Phase Results:
        {discovery_results}
        
        Your task:
        1. Evaluate technical feasibility using technical_feasibility_assessment
        2. Design system architecture with architecture_design
        3. Estimate development costs using cost_estimation
        4. Evaluate and recommend technology stack with technology_stack_evaluation
        5. Identify technical risks and mitigation strategies
        
        Focus on feasibility, scalability, and implementation approach.
        """,
        expected_output="""
        Technical analysis including:
        - Feasibility assessment with risk analysis
        - System architecture design and technology recommendations
        - Development cost estimates and resource requirements
        - Implementation roadmap and technical strategy
        """,
        agent=create_engineering_manager_agent(model)
    )