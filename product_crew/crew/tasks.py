"""CrewAI task creation and definition - refactored version."""

from pathlib import Path
from crewai import Task
from typing import List

# Import task functions from individual agent modules
from .agents.product_manager.tasks import (
    create_product_manager_discovery_task,
    create_product_manager_integration_task
)
from .agents.market_analyst.tasks import create_market_analyst_discovery_task
from .agents.engineering_manager.tasks import create_engineering_manager_solution_task
from .agents.product_designer.tasks import create_product_designer_solution_task
from .agents.functional_analyst.tasks import create_functional_analyst_breakdown_task
from .agents.scrum_master.tasks import create_scrum_master_breakdown_task

# Import legacy function for backwards compatibility
from .agents import create_path_printer_agent


def create_discovery_phase_tasks(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> List[Task]:
    """Create tasks for the Discovery Phase (Product Manager + Market Analyst)."""
    
    pm_market_task = create_product_manager_discovery_task(requirements_path, pid_path, model)
    ma_research_task = create_market_analyst_discovery_task(requirements_path, pid_path, model)
    
    return [pm_market_task, ma_research_task]


def create_solution_design_phase_tasks(discovery_results: str, model: str = 'gpt-4o') -> List[Task]:
    """Create tasks for the Solution Design Phase (Engineering Manager + Product Designer)."""
    
    em_tech_task = create_engineering_manager_solution_task(discovery_results, model)
    pd_design_task = create_product_designer_solution_task(discovery_results, model)
    
    return [em_tech_task, pd_design_task]


def create_breakdown_phase_tasks(solution_results: str, model: str = 'gpt-4o') -> List[Task]:
    """Create tasks for the Breakdown Phase (Functional Analyst + Scrum Master)."""
    
    fa_requirements_task = create_functional_analyst_breakdown_task(solution_results, model)
    sm_planning_task = create_scrum_master_breakdown_task(solution_results, model)
    
    return [fa_requirements_task, sm_planning_task]


def create_integration_task(all_results: str, requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create final integration task to combine all agent outputs."""
    
    return create_product_manager_integration_task(all_results, requirements_path, pid_path, model)


# Legacy function for backwards compatibility
def create_print_paths_task(requirements_path: Path, pid_path: Path, overwrite: bool, model: str = 'gpt-4') -> Task:
    """Legacy function - creates a simple path printing task for backwards compatibility."""
    return Task(
        description=(
            f"Print exactly these three values as separate lines:\n"
            f"1. {requirements_path}\n"
            f"2. {pid_path}\n"
            f"3. {overwrite}\n\n"
            f"Output only these values, nothing else. No explanations, no formatting."
        ),
        expected_output=(
            f"Three lines containing:\n"
            f"Line 1: {requirements_path}\n"
            f"Line 2: {pid_path}\n"
            f"Line 3: {overwrite}"
        ),
        agent=create_path_printer_agent(model)
    )