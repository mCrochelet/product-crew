"""CrewAI task creation and definition."""

from pathlib import Path
from crewai import Task
from typing import List

from .agents import (
    create_product_manager_agent,
    create_engineering_manager_agent,
    create_product_designer_agent,
    create_functional_analyst_agent,
    create_scrum_master_agent,
    create_market_analyst_agent,
    create_path_printer_agent
)
from .tools import *


def create_discovery_phase_tasks(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> List[Task]:
    """Create tasks for the Discovery Phase (Product Manager + Market Analyst)."""
    
    # Read the current PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    # Product Manager: Market Opportunity Analysis
    pm_market_task = Task(
        description=f"""
        Analyze the market opportunity for the product initiative described in the PID file.
        
        Current PID Content:
        {pid_content}
        
        Requirements Folder: {requirements_path}
        
        Your task:
        1. Review the initiative description and extract key product concepts
        2. Use the market_opportunity_analysis tool to assess market size and potential
        3. Create a preliminary business case using business_case_evaluation
        4. Define the value proposition using value_proposition_assessment
        5. Provide strategic recommendations for the initiative
        
        Focus on business value, market opportunity, and strategic alignment.
        """,
        expected_output="""
        Market opportunity analysis with:
        - Market size assessment and growth potential
        - Business case evaluation with financial projections
        - Value proposition definition for target customers
        - Strategic recommendations and next steps
        """,
        agent=create_product_manager_agent(model)
    )
    
    # Market Analyst: Market Research and Competitive Analysis
    ma_research_task = Task(
        description=f"""
        Conduct comprehensive market research and competitive analysis for the initiative.
        
        Current PID Content:
        {pid_content}
        
        Requirements Folder: {requirements_path}
        
        Your task:
        1. Perform market research using the market_research tool
        2. Identify data gaps with data_gap_identification
        3. Conduct competitive intelligence analysis
        4. Analyze market trends that could impact the initiative
        5. Provide research-backed insights and recommendations
        
        Focus on market validation, competitive landscape, and data-driven insights.
        """,
        expected_output="""
        Comprehensive market research including:
        - Market size analysis and customer segmentation
        - Competitive landscape and positioning opportunities
        - Key market trends and their implications
        - Data gaps and recommended research activities
        """,
        agent=create_market_analyst_agent(model)
    )
    
    return [pm_market_task, ma_research_task]


def create_solution_design_phase_tasks(discovery_results: str, model: str = 'gpt-4o') -> List[Task]:
    """Create tasks for the Solution Design Phase (Engineering Manager + Product Designer)."""
    
    # Engineering Manager: Technical Assessment
    em_tech_task = Task(
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
    
    # Product Designer: UX Design and Interface Planning
    pd_design_task = Task(
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
    
    return [em_tech_task, pd_design_task]


def create_breakdown_phase_tasks(solution_results: str, model: str = 'gpt-4o') -> List[Task]:
    """Create tasks for the Breakdown Phase (Functional Analyst + Scrum Master)."""
    
    # Functional Analyst: Requirements and User Stories
    fa_requirements_task = Task(
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
    
    # Scrum Master: Sprint Planning and Estimation
    sm_planning_task = Task(
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
    
    return [fa_requirements_task, sm_planning_task]


def create_integration_task(all_results: str, requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create final integration task to combine all agent outputs."""
    
    integration_task = Task(
        description=f"""
        Integrate all agent contributions into a comprehensive Product Initiative Document.
        
        All Phase Results:
        {all_results}
        
        Your task:
        1. Review all agent contributions for consistency and completeness
        2. Identify any gaps or conflicts in the analysis
        3. Synthesize insights into coherent recommendations
        4. Create executive summary highlighting key findings
        5. Provide final recommendations and next steps
        
        Focus on creating a complete, actionable PID that incorporates all perspectives.
        """,
        expected_output="""
        Final integrated analysis including:
        - Executive summary of key findings and recommendations
        - Consolidated business case and market analysis
        - Integrated technical and design strategy
        - Complete implementation roadmap with realistic timelines
        - Risk assessment and mitigation strategies across all dimensions
        """,
        agent=create_product_manager_agent(model),
        context_str=f"Requirements: {requirements_path}, PID: {pid_path}"
    )
    
    return integration_task


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