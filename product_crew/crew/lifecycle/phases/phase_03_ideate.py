"""Phase 3: Solution Ideation - Generate multiple solution alternatives using all agents."""

from crewai import Task
from ..context import LifecycleContext
from ...agents import create_product_manager_agent


def create_solution_ideation_task(context: LifecycleContext) -> Task:
    """Create Phase 3 task: Generate multiple solution options using all available agents."""
    
    # Get results from previous phases
    phase_1_results = context.get_phase_result(1)
    phase_2_results = context.get_phase_result(2)
    
    return Task(
        description=f"""
        **PHASE 3: IDEATE SOLUTIONS**
        
        Generate multiple solution alternatives by leveraging the expertise of all available agents to create a diverse portfolio of potential solutions.
        
        **Problem Understanding (Phase 1):**
        {phase_1_results}
        
        **Problem Definition (Phase 2):**  
        {phase_2_results}
        
        **Current Problem Statement:** {context.problem_statement}
        **Problem Domain:** {context.problem_domain}
        
        **Your Solution Ideation Strategy:**
        
        **DELEGATE TO ALL AGENTS** - Coordinate with each specialist to generate diverse solution approaches:
        
        1. **Market Analyst - Market-Driven Solutions**:
           "Based on the defined problem, please generate solution ideas that:
           - Leverage current market trends and opportunities
           - Address competitive gaps in the market
           - Align with customer segment preferences
           - Consider market timing and adoption factors
           - Suggest 2-3 market-oriented solution approaches"
        
        2. **Engineering Manager - Technical Solutions**:
           "Based on the problem definition, please propose technical solution approaches that:
           - Leverage appropriate technology stacks and architectures
           - Consider scalability and performance requirements
           - Address integration and system constraints
           - Balance innovation with implementation feasibility
           - Suggest 2-3 technically-focused solution approaches"
        
        3. **Product Designer - User-Centered Solutions**:
           "Based on the problem and stakeholder analysis, please design solution concepts that:
           - Prioritize user experience and usability
           - Address user journey pain points
           - Consider accessibility and inclusive design
           - Leverage design thinking methodologies
           - Suggest 2-3 user-experience-focused solution approaches"
        
        4. **Functional Analyst - Process-Oriented Solutions**:
           "Based on the problem domain, please develop solution frameworks that:
           - Optimize business processes and workflows
           - Address functional requirements systematically
           - Consider integration with existing systems
           - Ensure compliance and governance requirements
           - Suggest 2-3 process-improvement-focused solution approaches"
        
        5. **Scrum Master - Delivery-Optimized Solutions**:
           "Considering the problem scope and constraints, please propose solution approaches that:
           - Optimize for iterative delivery and quick wins
           - Consider team capacity and skill requirements
           - Address risk management and mitigation
           - Enable measurable progress and feedback loops
           - Suggest 2-3 delivery-optimized solution approaches"
        
        **Your Integration Tasks:**
        
        After receiving input from all agents:
        
        1. **Solution Portfolio Creation**:
           - Compile all suggested solutions from specialists
           - Remove duplicates and consolidate similar approaches
           - Ensure each solution addresses the core problem statement
           - Organize solutions by approach type (market-driven, tech-focused, user-centered, etc.)
        
        2. **Solution Enhancement**:
           - Combine complementary elements from different agents' suggestions
           - Create hybrid solutions that leverage multiple perspectives
           - Ensure solution diversity (avoid too many similar approaches)
           - Add your product management perspective to enhance solutions
        
        3. **Solution Documentation**:
           - Document each solution with clear descriptions
           - Include key features and capabilities for each
           - Note the primary approach/philosophy of each solution
           - Estimate high-level scope and complexity
        
        **Target**: Generate 4-6 distinct solution alternatives that offer different approaches to solving the defined problem.
        """,
        expected_output="""
        **Phase 3 Results: Solution Portfolio**
        
        ## Solution Overview
        **Total Solutions Generated**: [Number of distinct solutions]
        **Solution Categories Covered**: [List of approach types represented]
        **Agent Contributions**: [Summary of each agent's input]
        
        ## Solution Portfolio
        
        ### Solution 1: [Solution Name]
        **Approach Type**: [Market-driven/Technical/User-centered/Process-oriented/Hybrid]
        **Core Concept**: [2-3 sentence description of the solution]
        
        **Key Features**:
        - [Feature 1]
        - [Feature 2] 
        - [Feature 3]
        
        **Primary Benefits**:
        - [Benefit 1]
        - [Benefit 2]
        
        **Contributing Agent Perspectives**:
        - [Which agents contributed to this solution and how]
        
        **Estimated Scope**: [High/Medium/Low complexity]
        
        ---
        
        ### Solution 2: [Solution Name]
        [Repeat structure for each solution]
        
        ---
        
        [Continue for all solutions...]
        
        ## Solution Analysis
        
        **Diversity Assessment**:
        - **Technical Approaches**: [Range of technical strategies covered]
        - **User Experience Approaches**: [Range of UX strategies covered]
        - **Market Approaches**: [Range of market strategies covered]
        - **Implementation Approaches**: [Range of delivery strategies covered]
        
        **Coverage Analysis**:
        - **Problem Statement Coverage**: [How well solutions address core problem]
        - **Stakeholder Coverage**: [Which stakeholders are addressed by solutions]
        - **Constraint Compliance**: [How solutions respect identified constraints]
        
        **Innovation Spectrum**:
        - **Conservative Solutions**: [Number of low-risk, proven approaches]
        - **Moderate Innovation**: [Number of balanced risk/innovation solutions]
        - **High Innovation**: [Number of cutting-edge, higher-risk solutions]
        
        ## Readiness for Validation
        **Solution Quality**: [Assessment of solution depth and clarity]
        **Portfolio Completeness**: [Are major solution categories covered?]
        **Validation Readiness**: [Can these solutions be properly evaluated?]
        
        **Recommended Next Steps**: [Brief guidance for Phase 4 validation approach]
        
        ## Agent Collaboration Summary
        **Market Analyst Contribution**: [Summary of market-driven insights]
        **Engineering Manager Contribution**: [Summary of technical solutions]
        **Product Designer Contribution**: [Summary of user-centered approaches]
        **Functional Analyst Contribution**: [Summary of process solutions]
        **Scrum Master Contribution**: [Summary of delivery-optimized approaches]
        
        **Cross-Functional Synergies**: [Where agent perspectives combined effectively]
        """,
        agent=create_product_manager_agent(context.model)
    )