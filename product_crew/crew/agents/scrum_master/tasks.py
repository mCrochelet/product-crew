"""Scrum Master tasks."""

from crewai import Task
from .agent import create_scrum_master_agent
from ...tools import *


def create_scrum_master_breakdown_task(solution_results: str, model: str = 'gpt-4o') -> Task:
    """Create Scrum Master breakdown phase task for sprint planning and estimation."""
    
    return Task(
        description=f"""
        Plan sprints and estimate effort for the initiative delivery.
        
        Solution Design Results:
        {solution_results}
        
        Your task:
        1. Plan sprints using sprint_planning
        2. Estimate tasks with task_estimation
        3. Track velocity considerations with velocity_tracking
        4. Plan retrospectives with retrospective_analysis
        5. Ensure realistic timelines and deliverable scope
        
        Focus on delivery planning, risk mitigation, and team efficiency.
        """,
        expected_output="""
        Delivery planning including:
        - Sprint breakdown with clear goals and deliverables
        - Task estimation and velocity projections
        - Risk assessment and mitigation strategies
        - Retrospective planning and process improvements
        """,
        agent=create_scrum_master_agent(model)
    )