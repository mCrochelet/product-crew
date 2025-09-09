"""Problem understanding analysis task."""

from pathlib import Path
from crewai import Task
from .agents import create_product_manager_agent


def create_problem_understanding_analysis_task(requirements_path: Path, pid_path: Path, overwrite: bool, model: str = 'gpt-4o') -> Task:
    """Create a task that analyzes problem understanding in the PID."""
    
    # Read PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    return Task(
        description=f"""
        Analyze the problem understanding in this Product Initiative Document and assess how well the problem space is defined.
        
        **Current PID Content:**
        {pid_content}
        
        **Requirements Path:** {requirements_path}
        
        **Analysis Framework:**
        Evaluate the problem understanding across these six critical dimensions:
        
        1. **User and Customer Identification**
           - Is there a clear understanding of who the user is?
           - Is there a clear understanding of who the customer is?
           - Are user and customer distinguished (if they are different people)?
           - Are user personas, characteristics, or segments defined?
        
        2. **Job-to-be-Done Understanding**
           - Is the user's job-to-be-done clearly articulated?
           - Is it clear what progress users are trying to make?
           - Are functional, emotional, and social job dimensions considered?
           - Are job triggers and context understood?
        
        3. **Value Proposition Clarity**
           - Is the value for the customer clearly defined?
           - Are financial benefits identified and quantified?
           - Are time savings or other benefits articulated?
           - Is the value proposition differentiated from generic benefits?
        
        4. **Competitive Landscape Analysis**
           - How do users currently solve this job-to-be-done?
           - What existing solutions, tools, or workarounds are being used?
           - How satisfied are users with current solutions?
           - What are the gaps in existing competitive offerings?
        
        5. **Success Metrics Definition**
           - Are success metrics for job completion clearly defined?
           - Are both leading and lagging indicators identified?
           - Are baseline measurements established or planned?
           - Are metrics tied to user progress and value creation?
        
        6. **Service Blueprint Context**
           - How does this problem fit within the broader service ecosystem?
           - What touchpoints and stakeholder interactions are involved?
           - How does this problem influence or get influenced by other parts of the service?
           - Are ecosystem dependencies and relationships understood?
        
        **Critical Instructions:**
        - Focus ONLY on problem understanding - do not suggest any solutions
        - Assess what is well understood vs. what has gaps or assumptions
        - Identify areas where the problem analysis is strong vs. weak
        - Point out missing elements in the problem understanding
        - Do not propose fixes, just assess the current state of understanding
        """,
        expected_output="""
        ## Problem Understanding Assessment
        
        ### Overall Assessment
        - **Problem Understanding Score**: [X/10] with brief rationale
        - **Readiness for Solution Development**: [Ready/Not Ready] with justification
        
        ### Detailed Analysis by Dimension
        
        #### 1. User and Customer Identification
        **Status**: [Well Defined / Partially Defined / Not Defined / Unclear]
        **Findings**:
        - What is clearly understood about users/customers
        - What is missing or assumed
        - Key gaps in user/customer understanding
        
        #### 2. Job-to-be-Done Understanding  
        **Status**: [Well Defined / Partially Defined / Not Defined / Unclear]
        **Findings**:
        - What is clearly understood about the job-to-be-done
        - What is missing or assumed about user progress/goals
        - Key gaps in job understanding
        
        #### 3. Value Proposition Clarity
        **Status**: [Well Defined / Partially Defined / Not Defined / Unclear] 
        **Findings**:
        - What value is clearly articulated
        - What value claims are missing or vague
        - Key gaps in value understanding
        
        #### 4. Competitive Landscape Analysis
        **Status**: [Well Defined / Partially Defined / Not Defined / Unclear]
        **Findings**:
        - What is understood about current solutions
        - What competitive analysis is missing
        - Key gaps in landscape understanding
        
        #### 5. Success Metrics Definition
        **Status**: [Well Defined / Partially Defined / Not Defined / Unclear]
        **Findings**:
        - What metrics are clearly defined
        - What measurement approaches are missing
        - Key gaps in success definition
        
        #### 6. Service Blueprint Context
        **Status**: [Well Defined / Partially Defined / Not Defined / Unclear]
        **Findings**:
        - What ecosystem context is understood
        - What service relationships are missing
        - Key gaps in context understanding
        
        ### Priority Gaps for Problem Understanding
        1. **[Gap 1]**: Brief description of most critical gap
        2. **[Gap 2]**: Brief description of second most critical gap  
        3. **[Gap 3]**: Brief description of third most critical gap
        
        ### Strengths in Current Problem Understanding
        - List the strongest aspects of current problem analysis
        - Highlight what is well-researched or clearly articulated
        
        ### Next Steps for Problem Understanding
        - What specific areas need more research/analysis
        - What assumptions need validation
        - What stakeholder input is needed
        
        **Note**: This assessment focuses purely on problem understanding quality and does not suggest any solutions.
        """,
        agent=create_product_manager_agent(model)
    )