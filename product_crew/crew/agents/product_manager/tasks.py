"""Product Manager tasks focused on delegation and orchestration."""

from pathlib import Path
from crewai import Task
from .agent import create_product_manager_agent


def create_product_manager_orchestration_task(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create Product Manager orchestration task that delegates PID sections to specialists."""
    
    # Read the current PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    return Task(
        description=f"""
        Orchestrate the creation of a comprehensive Product Initiative Document by delegating specific sections to specialist agents.
        
        Current PID Content:
        {pid_content}
        
        Requirements Folder: {requirements_path}
        
        Your delegation strategy:
        
        1. **Market Research & Analysis** - Delegate to Market Analyst:
           - Ask the Market Analyst to conduct comprehensive market research
           - Request competitive landscape analysis
           - Get market sizing and opportunity assessment
           - Obtain customer segmentation insights
        
        2. **Technical Feasibility & Architecture** - Delegate to Engineering Manager:
           - Ask the Engineering Manager to assess technical feasibility
           - Request system architecture recommendations
           - Get development cost estimates and timeline projections
           - Obtain technology stack recommendations
        
        3. **User Experience & Design Strategy** - Delegate to Product Designer:
           - Ask the Product Designer to create user journey maps
           - Request wireframe concepts and design system requirements
           - Get usability assessment and design principles
           - Obtain interface planning and user experience strategy
        
        4. **Requirements & User Stories** - Delegate to Functional Analyst:
           - Ask the Functional Analyst to break down requirements
           - Request detailed user stories with acceptance criteria
           - Get dependency mapping and traceability matrix
           - Obtain testing requirements and implementation sequence
        
        5. **Delivery Planning & Sprint Organization** - Delegate to Scrum Master:
           - Ask the Scrum Master to create sprint breakdown
           - Request effort estimation and velocity projections
           - Get risk assessment and mitigation strategies
           - Obtain delivery timeline and process improvements
        
        After receiving all delegated work, synthesize the insights into a coherent, comprehensive PID.
        """,
        expected_output="""
        A comprehensive Product Initiative Document containing:
        
        ## Executive Summary
        - Key findings synthesis from all specialist areas
        - Strategic recommendations and value proposition
        - High-level implementation roadmap
        
        ## Market Analysis 
        - Market research findings and competitive landscape
        - Customer segmentation and market opportunity
        - Data gaps and research recommendations
        
        ## Technical Strategy  
        - Technical feasibility assessment and architecture
        - Technology recommendations and cost estimates
        - Implementation timeline and technical risks
        
        ## User Experience Strategy
        - User journey maps and design principles
        - Interface concepts and design system requirements
        - Usability guidelines and user experience strategy
        
        ## Requirements & Implementation 
        - Detailed functional requirements and user stories
        - Acceptance criteria and dependency mapping
        - Testing strategy and traceability matrix
        
        ## Delivery Plan
        - Sprint breakdown and effort estimates
        - Delivery timeline and risk mitigation
        - Process recommendations and success metrics
        
        ## Integrated Recommendations
        - Coherent action plan combining all perspectives
        - Risk assessment across all dimensions  
        - Success metrics and next steps
        """,
        agent=create_product_manager_agent(model)
    )