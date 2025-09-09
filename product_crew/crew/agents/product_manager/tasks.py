"""Product Manager tasks."""

from pathlib import Path
from crewai import Task
from .agent import create_product_manager_agent
from ...tools import *


def create_product_manager_discovery_task(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create Product Manager discovery phase task for market opportunity analysis."""
    
    # Read the current PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    return Task(
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


def create_product_manager_integration_task(all_results: str, requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create Product Manager integration task to combine all agent outputs."""
    
    return Task(
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