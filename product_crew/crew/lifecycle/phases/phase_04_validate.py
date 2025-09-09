"""Phase 4: Solution Validation - Evaluate solutions across Value, Viability, Feasibility, and Usability."""

from crewai import Task
from ..context import LifecycleContext
from ..delegation import DelegationDecisionEngine
from ...agents import create_product_manager_agent


def create_solution_validation_task(context: LifecycleContext) -> Task:
    """Create Phase 4 task: Validate solutions using 4-dimensional evaluation framework."""
    
    # Get results from previous phases
    phase_3_results = context.get_phase_result(3)
    
    # Determine required delegations
    delegations = DelegationDecisionEngine.get_required_delegations(context, 4)
    
    # Engineering Manager and Product Designer are always needed for Phase 4
    delegation_instructions = f"""
    
    **REQUIRED DELEGATIONS** - Systematic evaluation across 4 dimensions:
    
    1. **Engineering Manager - FEASIBILITY ASSESSMENT**:
       "Please evaluate each solution for technical feasibility. For each solution, assess:
       
       **Technical Complexity** (1-10 scale):
       - Implementation difficulty and technical challenges
       - Required expertise and team capabilities
       - Integration complexity with existing systems
       - Technology stack maturity and stability
       
       **Resource Requirements** (1-10 scale):
       - Development time estimates (person-months)
       - Required team size and skills
       - Infrastructure and tooling needs
       - Third-party dependencies and costs
       
       **Technical Risks** (1-10 scale, 1=high risk):
       - Technical uncertainty and unknowns
       - Scalability and performance risks
       - Security and compliance considerations
       - Maintenance and support complexity
       
       Provide detailed feasibility score (average of the three factors) and rationale for each solution."
    
    2. **Product Designer - USABILITY ASSESSMENT**:
       "Please evaluate each solution for user experience and usability. For each solution, assess:
       
       **User Experience Quality** (1-10 scale):
       - Intuitiveness and ease of use
       - User journey flow and efficiency
       - Accessibility and inclusive design
       - Visual design and interface quality
       
       **User Adoption Potential** (1-10 scale):
       - Learning curve and onboarding ease
       - User motivation and engagement factors
       - Change management requirements
       - User feedback and iteration opportunities
       
       **Design Implementation** (1-10 scale):
       - Design system integration
       - Consistency with brand and standards
       - Responsiveness and multi-platform support
       - Design maintenance and scalability
       
       Provide detailed usability score (average of the three factors) and rationale for each solution."
    """
    
    # Add Market Analyst if needed for value assessment
    if delegations.get("market_analyst", False):
        delegation_instructions += """
        
    3. **Market Analyst - VALUE ASSESSMENT**:
       "Please evaluate each solution for market value and customer impact. For each solution, assess:
       
       **User Value Delivery** (1-10 scale):
       - Jobs-to-be-done fulfillment
       - Pain point resolution effectiveness
       - User outcome improvement
       - Competitive advantage creation
       
       **Market Opportunity** (1-10 scale):
       - Market size and growth potential
       - Customer willingness to pay
       - Market timing and readiness
       - Competitive positioning strength
       
       **Value Realization** (1-10 scale):
       - Time to value delivery
       - Value measurement and tracking
       - Customer success enablement
       - Network effects and virality
       
       Provide detailed value score (average of the three factors) and rationale for each solution."
        """
    
    return Task(
        description=f"""
        **PHASE 4: VALIDATE SOLUTIONS**
        
        Conduct comprehensive 4-dimensional validation of all generated solutions using the Value, Viability, Feasibility, and Usability framework.
        
        **Solutions to Evaluate (Phase 3):**
        {phase_3_results}
        
        **Current Solutions Count:** {len(context.solutions)}
        
        **Evaluation Framework Overview:**
        
        This phase evaluates each solution across four critical dimensions:
        - **VALUE**: User value and jobs-to-be-done served (Market Analyst + Product Manager)
        - **VIABILITY**: Business model and financial sustainability (Product Manager)
        - **FEASIBILITY**: Technical implementation complexity and risks (Engineering Manager)
        - **USABILITY**: User experience quality and adoption potential (Product Designer)
        
        {delegation_instructions}
        
        **Your Viability Assessment Tasks:**
        
        For each solution, conduct comprehensive business viability analysis:
        
        **Revenue Model Assessment** (1-10 scale):
        - Revenue generation potential and mechanisms
        - Monetization strategy clarity and viability
        - Customer lifetime value projections
        - Revenue scalability and growth potential
        
        **Cost Structure Analysis** (1-10 scale):
        - Development and implementation costs
        - Ongoing operational expenses
        - Customer acquisition costs
        - Support and maintenance costs
        
        **Financial Performance** (1-10 scale):
        - Return on investment projections
        - Break-even timeline analysis
        - Profitability potential and margins
        - Financial risk assessment
        
        **Solution Integration and Analysis:**
        
        After receiving all specialist evaluations:
        
        1. **Compile Evaluation Matrix**:
           - Create comprehensive scoring matrix for all solutions
           - Calculate composite scores using weighted averages
           - Identify top performers in each dimension
           - Note solutions with exceptional strengths or weaknesses
        
        2. **Cross-Dimensional Analysis**:
           - Identify solutions with balanced scores across all dimensions
           - Flag solutions with extreme high/low scores in any dimension
           - Analyze trade-offs between dimensions
           - Consider organizational priorities and constraints
        
        3. **Risk Assessment**:
           - Compile risks identified by each specialist
           - Assess overall risk profile for each solution
           - Identify risk mitigation strategies
           - Consider risk tolerance and management capabilities
        
        **Evaluation Weights (Default)**:
        - Value: 30%
        - Viability: 30%
        - Feasibility: 25%
        - Usability: 15%
        """,
        expected_output="""
        **Phase 4 Results: Solution Validation Matrix**
        
        ## Evaluation Overview
        **Solutions Evaluated**: [Number of solutions assessed]
        **Evaluation Dimensions**: Value, Viability, Feasibility, Usability
        **Specialist Contributions**: [List of agents who provided assessments]
        
        ## Solution Evaluation Matrix
        
        | Solution | Value | Viability | Feasibility | Usability | Composite | Rank |
        |----------|-------|-----------|-------------|-----------|-----------|------|
        | Solution 1 | 8.2 | 7.5 | 6.8 | 8.9 | 7.8 | 1 |
        | Solution 2 | 7.1 | 8.3 | 8.1 | 7.2 | 7.7 | 2 |
        | [Continue for all solutions...] | | | | | | |
        
        ## Detailed Solution Analysis
        
        ### Solution 1: [Solution Name] - Rank #1
        **Composite Score**: [Weighted average score]
        
        **Dimension Scores**:
        - **Value Score**: [X.X/10] - [Brief assessment summary]
        - **Viability Score**: [X.X/10] - [Brief assessment summary]
        - **Feasibility Score**: [X.X/10] - [Brief assessment summary]  
        - **Usability Score**: [X.X/10] - [Brief assessment summary]
        
        **Strengths**:
        - [Key strength 1]
        - [Key strength 2]
        
        **Weaknesses**:
        - [Key weakness 1]
        - [Key weakness 2]
        
        **Key Risks**:
        - [Risk 1 with mitigation approach]
        - [Risk 2 with mitigation approach]
        
        **Specialist Insights**:
        - **Engineering Manager**: [Key feasibility insights]
        - **Product Designer**: [Key usability insights]
        - **Market Analyst** (if applicable): [Key value insights]
        
        ---
        
        [Repeat detailed analysis for top 3 solutions]
        
        ## Cross-Dimensional Analysis
        
        **Balanced Solutions**: [Solutions with consistent scores across dimensions]
        **Specialized Solutions**: [Solutions excelling in specific dimensions]
        **High-Risk Solutions**: [Solutions with concerning weaknesses]
        **Safe Choices**: [Solutions with acceptable scores across all dimensions]
        
        ## Risk Assessment Summary
        
        **Technical Risks**:
        - [Common technical challenges across solutions]
        - [Highest risk solutions and concerns]
        
        **Market Risks**:
        - [Market-related risks and uncertainties]
        - [Value delivery challenges]
        
        **Business Risks**:
        - [Financial and operational risks]
        - [Resource and timeline concerns]
        
        **User Experience Risks**:
        - [Usability and adoption concerns]
        - [Design implementation challenges]
        
        ## Evaluation Quality Assessment
        **Data Completeness**: [Quality of evaluation data received]
        **Specialist Engagement**: [Effectiveness of delegation and responses]
        **Evaluation Consistency**: [Consistency across specialist assessments]
        
        ## Recommendations for Phase 5
        **Top Candidates for Refinement**: [2-3 highest scoring solutions]
        **Critical Refinement Areas**: [Dimensions needing improvement]
        **Solutions to Discontinue**: [Clearly inferior solutions if any]
        
        **Refinement Priorities**:
        1. [Priority area 1 for selected solutions]
        2. [Priority area 2 for selected solutions]
        3. [Priority area 3 for selected solutions]
        """,
        agent=create_product_manager_agent(context.model)
    )