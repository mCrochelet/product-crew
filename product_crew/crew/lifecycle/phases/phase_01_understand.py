"""Phase 1: Problem Understanding - Analyze existing data and determine research needs."""

from crewai import Task
from pathlib import Path
from ..context import LifecycleContext
from ..delegation import DelegationDecisionEngine
from ...agents import create_product_manager_agent


def create_problem_understanding_task(context: LifecycleContext) -> Task:
    """Create Phase 1 task: Understand the problem and assess research needs."""
    
    # Determine if Market Analyst delegation is needed
    needs_market_research = DelegationDecisionEngine.should_delegate_market_research(context, 1)
    
    delegation_instructions = ""
    if needs_market_research:
        delegation_instructions = """
        
        **DELEGATION REQUIRED**: The available data is insufficient for proper problem understanding.
        
        Delegate to the Market Analyst with this request:
        "Please conduct comprehensive market research to understand:
        1. The problem space and market context
        2. Current solutions and their limitations
        3. Target user segments and their pain points
        4. Market size and opportunity assessment
        5. Key trends affecting this problem domain
        
        Provide a detailed analysis that will help us better understand the problem we're trying to solve."
        """
    else:
        delegation_instructions = """
        
        **NO DELEGATION NEEDED**: The available data appears sufficient for initial problem understanding.
        Proceed with analysis of existing information.
        """
    
    return Task(
        description=f"""
        **PHASE 1: UNDERSTAND PROBLEM**
        
        Analyze the current product initiative to understand the problem space and determine if additional research is necessary.
        
        **Current PID Content:**
        {context.original_pid_content}
        
        **Requirements Folder:** {context.requirements_path}
        
        **Your Analysis Tasks:**
        
        1. **Data Completeness Assessment**:
           - Evaluate the quality and completeness of existing information
           - Rate data completeness on a scale of 0.0 to 1.0
           - Identify specific information gaps
        
        2. **Problem Clarity Analysis**:
           - Assess how clearly the problem is defined
           - Rate problem clarity on a scale of 0.0 to 1.0
           - Note areas requiring clarification
        
        3. **Context Understanding**:
           - Extract key stakeholders and users
           - Identify business context and constraints
           - Understand success criteria and objectives
        
        4. **Research Needs Decision**:
           - Determine if additional market research is required
           - Specify what additional information would be valuable
           - Make a clear recommendation for next steps
        
        {delegation_instructions}
        
        **Decision Point**: Based on your analysis, decide whether to proceed with problem definition or conduct additional research first.
        """,
        expected_output="""
        **Phase 1 Results: Problem Understanding Assessment**
        
        ## Data Completeness Analysis
        - **Completeness Score**: [0.0 to 1.0]
        - **Available Information**: [List key data points present]
        - **Information Gaps**: [List missing critical information]
        - **Data Quality Assessment**: [Evaluation of information reliability]
        
        ## Problem Clarity Assessment  
        - **Clarity Score**: [0.0 to 1.0]
        - **Clear Aspects**: [What is well-defined about the problem]
        - **Unclear Areas**: [What needs clarification]
        - **Ambiguities**: [Conflicting or vague statements]
        
        ## Context Analysis
        - **Stakeholders**: [Key people/groups affected]
        - **Users**: [Primary and secondary user groups]
        - **Business Context**: [Strategic and operational factors]
        - **Constraints**: [Technical, resource, timeline limitations]
        - **Success Criteria**: [How success will be measured]
        
        ## Research Recommendation
        - **Additional Research Needed**: [Yes/No with rationale]
        - **Research Priorities**: [What specific information to gather]
        - **Research Approach**: [Recommended methods if research needed]
        - **Next Steps**: [Clear recommendation for Phase 2]
        
        ## Executive Summary
        [2-3 sentences summarizing problem understanding and readiness for next phase]
        """,
        agent=create_product_manager_agent(context.model)
    )