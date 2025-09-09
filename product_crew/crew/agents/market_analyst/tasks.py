"""Market Analyst tasks."""

from pathlib import Path
from crewai import Task
from .agent import create_market_analyst_agent
from ...tools import *


def create_market_analyst_discovery_task(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create Market Analyst discovery phase task for market research and competitive analysis."""
    
    # Read the current PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    return Task(
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