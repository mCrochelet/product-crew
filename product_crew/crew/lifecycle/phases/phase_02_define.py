"""Phase 2: Problem Definition - Create clear problem statement and domain definition."""

from crewai import Task
from ..context import LifecycleContext
from ..delegation import DelegationDecisionEngine
from ...agents import create_product_manager_agent


def create_problem_definition_task(context: LifecycleContext) -> Task:
    """Create Phase 2 task: Define the problem statement and problem domain."""
    
    # Get Phase 1 results
    phase_1_results = context.get_phase_result(1)
    
    # Determine delegations needed
    needs_market_research = DelegationDecisionEngine.should_delegate_market_research(context, 2)
    needs_functional_analysis = DelegationDecisionEngine.should_delegate_functional_analysis(context, 2)
    
    delegation_instructions = ""
    
    if needs_market_research and needs_functional_analysis:
        delegation_instructions = """
        
        **DELEGATION REQUIRED**: Problem clarity is insufficient for proper definition.
        
        1. **Delegate to Market Analyst**:
           "Please provide market context for problem definition:
           - Industry analysis and market dynamics
           - Competitive landscape assessment
           - Customer segmentation and personas
           - Market size and opportunity validation
           - Key market trends affecting this problem"
        
        2. **Delegate to Functional Analyst**:
           "Please help clarify the problem domain:
           - Business process analysis
           - Functional requirements implications
           - System boundaries and scope
           - Integration touchpoints
           - Compliance and regulatory considerations"
        """
    elif needs_market_research:
        delegation_instructions = """
        
        **DELEGATION REQUIRED**: Market context needed for problem definition.
        
        **Delegate to Market Analyst**:
        "Please provide market validation for our problem definition:
        - Confirm problem relevance in current market
        - Validate target customer segments
        - Assess competitive solutions addressing this problem
        - Provide market sizing for this problem space"
        """
    elif needs_functional_analysis:
        delegation_instructions = """
        
        **DELEGATION REQUIRED**: Functional clarity needed for problem domain.
        
        **Delegate to Functional Analyst**:
        "Please help define the functional problem domain:
        - Map business processes affected by this problem
        - Define system and functional boundaries
        - Identify integration requirements
        - Clarify compliance and regulatory aspects"
        """
    else:
        delegation_instructions = """
        
        **NO DELEGATION NEEDED**: Problem clarity is sufficient for direct definition.
        Proceed with creating clear problem statement and domain definition.
        """
    
    return Task(
        description=f"""
        **PHASE 2: DEFINE PROBLEM**
        
        Create a clear, comprehensive problem statement and define the problem domain based on Phase 1 understanding.
        
        **Phase 1 Results:**
        {phase_1_results}
        
        **Context Information:**
        - Problem Clarity Score: {context.problem_clarity_score}
        - Research Completed: {context.is_phase_complete(1)}
        - Existing Problem Statement: {context.problem_statement or "None"}
        - Existing Problem Domain: {context.problem_domain or "None"}
        
        **Your Definition Tasks:**
        
        1. **Problem Statement Creation**:
           - Write a clear, concise problem statement (1-2 sentences)
           - Ensure it captures WHO has the problem, WHAT the problem is, and WHY it matters
           - Make it specific and measurable where possible
           - Validate it against Phase 1 findings
        
        2. **Problem Domain Definition**:
           - Define the scope and boundaries of the problem space
           - Identify what IS and IS NOT included in this problem
           - Map relationships to other problems/systems
           - Establish context and constraints
        
        3. **Stakeholder Impact Analysis**:
           - Define primary and secondary stakeholders affected
           - Quantify impact where possible
           - Prioritize stakeholder importance
           - Identify decision makers and influencers
        
        4. **Success Criteria Definition**:
           - Define what "solving this problem" means
           - Establish measurable success metrics
           - Set realistic expectations and timelines
           - Align with business objectives
        
        {delegation_instructions}
        
        **Validation**: Ensure problem definition is clear enough to generate focused solutions in Phase 3.
        """,
        expected_output="""
        **Phase 2 Results: Problem Definition**
        
        ## Problem Statement
        **Primary Problem**: [Clear 1-2 sentence problem statement]
        
        **Problem Context**:
        - **Who**: [Primary stakeholders affected]
        - **What**: [Specific problem manifestation] 
        - **Where**: [Context/environment where problem occurs]
        - **When**: [Timing/frequency of problem]
        - **Why**: [Root causes and business impact]
        
        ## Problem Domain Definition
        **Scope & Boundaries**:
        - **Included in Scope**: [What this problem encompasses]
        - **Excluded from Scope**: [What is explicitly out of scope]
        - **Adjacent Problems**: [Related problems not being solved]
        - **System Boundaries**: [Technical/functional boundaries]
        
        **Domain Characteristics**:
        - **Complexity Level**: [Simple/Moderate/Complex]
        - **Domain Maturity**: [Emerging/Established/Legacy]
        - **Regulatory Factors**: [Compliance requirements if any]
        - **Integration Requirements**: [Systems/processes that must connect]
        
        ## Stakeholder Analysis
        **Primary Stakeholders**:
        - [Stakeholder 1]: [Role, impact level, importance]
        - [Stakeholder 2]: [Role, impact level, importance]
        
        **Secondary Stakeholders**:
        - [List with brief impact description]
        
        **Decision Makers**: [Key people who approve solutions]
        
        ## Success Criteria
        **Primary Success Metrics**:
        1. [Measurable outcome 1]
        2. [Measurable outcome 2]
        3. [Measurable outcome 3]
        
        **Secondary Success Indicators**:
        - [Supporting metric 1]
        - [Supporting metric 2]
        
        **Timeline Expectations**: [Realistic timeframe for problem resolution]
        
        ## Problem Definition Quality Check
        - **Clarity Score**: [Updated 0.0 to 1.0 based on definition quality]
        - **Completeness**: [Assessment of definition completeness]
        - **Actionability**: [Can solutions be generated from this definition?]
        - **Stakeholder Alignment**: [Would stakeholders agree with this definition?]
        
        ## Next Phase Readiness
        **Ready for Solution Ideation**: [Yes/No with rationale]
        **Key Constraints for Solutions**: [Critical constraints solutions must respect]
        **Innovation Opportunities**: [Areas where creative solutions could add value]
        """,
        agent=create_product_manager_agent(context.model)
    )