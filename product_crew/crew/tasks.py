"""CrewAI task creation and definition - lifecycle-based workflow."""

from pathlib import Path
from crewai import Task
from typing import List

# Import lifecycle system
from .lifecycle import LifecycleContext, ProductLifecycleController

# Import legacy orchestration task from Product Manager for backward compatibility
from .agents.product_manager.tasks import create_product_manager_orchestration_task

# Import all agents for delegation workflow
from .agents import (
    create_product_manager_agent,
    create_market_analyst_agent,
    create_engineering_manager_agent,
    create_product_designer_agent,
    create_functional_analyst_agent,
    create_scrum_master_agent,
    create_path_printer_agent  # Legacy compatibility
)


def create_lifecycle_workflow_task(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create lifecycle-based task using the 7-phase product refinement approach."""
    
    # Read PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    return Task(
        description=f"""
        Execute the comprehensive 7-phase product refinement lifecycle for creating a high-quality Product Initiative Document.
        
        **Current PID Content:**
        {pid_content}
        
        **Requirements Folder:** {requirements_path}
        
        **7-Phase Lifecycle Approach:**
        
        1. **Understand Problem**: Analyze existing data and determine research needs
        2. **Define Problem**: Create clear problem statement and domain definition
        3. **Ideate Solutions**: Generate multiple solution alternatives with all specialists
        4. **Validate Solutions**: Evaluate solutions across Value, Viability, Feasibility, Usability
        5. **Refine Solutions**: Improve top candidates based on validation feedback
        6. **Select Best Solution**: Make informed selection decision with clear rationale
        7. **Plan Implementation**: Create comprehensive implementation roadmap and tasks
        
        **Your Role**: As Product Manager, orchestrate this structured approach by:
        - Leading each phase with appropriate specialist delegation
        - Making conditional delegation decisions based on data quality and needs
        - Synthesizing insights from all specialists into coherent recommendations
        - Ensuring quality gates are met before phase transitions
        - Creating a comprehensive, actionable Product Initiative Document
        
        This structured approach ensures thorough analysis, stakeholder alignment, and implementation readiness.
        """,
        expected_output="""
        A comprehensive Product Initiative Document created through the 7-phase lifecycle containing:
        
        ## Executive Summary
        - Key findings and strategic recommendations
        - Selected solution and rationale
        - Implementation readiness assessment
        
        ## Problem Space (Phases 1-2)
        - Thorough problem understanding and context analysis
        - Clear problem statement and domain definition
        - Stakeholder impact analysis
        
        ## Solution Space (Phases 3-6)
        - Multiple solution alternatives explored
        - Comprehensive evaluation across 4 dimensions (Value/Viability/Feasibility/Usability)
        - Solution refinement based on validation feedback
        - Clear selection decision with detailed rationale
        
        ## Implementation Planning (Phase 7)
        - Detailed implementation roadmap and timeline
        - Resource requirements and team planning
        - Risk assessment and mitigation strategies
        - Success metrics and measurement plan
        
        ## Lifecycle Quality Metrics
        - Problem clarity progression
        - Solution evaluation completeness
        - Decision rationale documentation
        - Implementation readiness validation
        
        The final PID represents a thoroughly analyzed, well-validated, and implementation-ready product initiative.
        """,
        agent=create_product_manager_agent(model)
    )


def create_delegation_workflow_task(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Legacy function - Create a single delegation-based task (now redirects to lifecycle)."""
    
    return create_lifecycle_workflow_task(requirements_path, pid_path, model)


def create_delegation_crew_agents(model: str = 'gpt-4o') -> List:
    """Create all agents needed for the delegation workflow."""
    
    return [
        create_product_manager_agent(model),  # The orchestrator
        create_market_analyst_agent(model),
        create_engineering_manager_agent(model),
        create_product_designer_agent(model),
        create_functional_analyst_agent(model),
        create_scrum_master_agent(model)
    ]


# Legacy functions for backwards compatibility
def create_discovery_phase_tasks(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> List[Task]:
    """Legacy function - now uses delegation workflow."""
    return [create_delegation_workflow_task(requirements_path, pid_path, model)]


def create_solution_design_phase_tasks(discovery_results: str, model: str = 'gpt-4o') -> List[Task]:
    """Legacy function - now returns empty list as delegation handles all phases."""
    return []


def create_breakdown_phase_tasks(solution_results: str, model: str = 'gpt-4o') -> List[Task]:
    """Legacy function - now returns empty list as delegation handles all phases."""
    return []


def create_integration_task(all_results: str, requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Legacy function - now returns a simple pass-through task."""
    return Task(
        description="Integration already handled by delegation workflow. Pass through results.",
        expected_output="Results from delegation workflow",
        agent=create_product_manager_agent(model)
    )


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