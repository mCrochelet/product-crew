"""Phase 5: Solution Refinement - Improve solutions based on validation feedback."""

from crewai import Task
from ..context import LifecycleContext
from ...agents import create_product_manager_agent


def create_solution_refinement_task(context: LifecycleContext) -> Task:
    """Create Phase 5 task: Refine solutions based on validation feedback."""
    
    # Get results from previous phases
    phase_4_results = context.get_phase_result(4)
    
    return Task(
        description=f"""
        **PHASE 5: REFINE SOLUTIONS**
        
        Refine and improve the top solution candidates based on validation feedback, focusing on addressing identified weaknesses while preserving strengths.
        
        **Validation Results (Phase 4):**
        {phase_4_results}
        
        **Current Solution Evaluations:** {len(context.solution_evaluations)} solutions evaluated
        
        **Refinement Strategy:**
        
        Based on Phase 4 validation, focus refinement efforts on the top 2-3 solution candidates that show the highest potential. For each selected solution, coordinate targeted improvements with specialist agents.
        
        **REQUIRED DELEGATIONS** - Targeted refinement by specialists:
        
        1. **Product Designer - UX/UI REFINEMENT**:
           "Based on the usability assessment from Phase 4, please refine the user experience for the top solution candidates:
           
           **For each selected solution, improve**:
           - **User Journey Optimization**: Streamline workflows and reduce friction points
           - **Interface Design Enhancement**: Improve visual hierarchy and interaction patterns
           - **Accessibility Improvements**: Ensure compliance with accessibility standards
           - **User Onboarding**: Design intuitive first-time user experiences
           - **Responsive Design**: Optimize for multiple devices and screen sizes
           
           **Focus Areas**:
           - Address specific usability weaknesses identified in validation
           - Enhance features that scored below 7.0 in usability assessment
           - Leverage design patterns that improve user adoption
           - Ensure design consistency and scalability
           
           Provide refined UX/UI specifications and updated usability projections."
        
        2. **Functional Analyst - REQUIREMENTS REFINEMENT**:
           "Based on the validation results, please refine the functional requirements for the top solution candidates:
           
           **For each selected solution, enhance**:
           - **Functional Specifications**: Detail core functionality and edge cases
           - **User Story Refinement**: Improve user stories with better acceptance criteria
           - **Integration Requirements**: Clarify system interfaces and data flows
           - **Business Rules**: Define business logic and validation rules
           - **Non-Functional Requirements**: Specify performance, security, and compliance needs
           
           **Focus Areas**:
           - Address gaps identified during feasibility assessment
           - Clarify ambiguous requirements that could impact implementation
           - Optimize business processes and workflows
           - Ensure requirements support scalability and maintainability
           
           Provide detailed functional specifications and requirement impact analysis."
        
        3. **Engineering Manager - TECHNICAL REFINEMENT**:
           "Based on the feasibility assessment, please refine the technical approach for the top solution candidates:
           
           **For each selected solution, improve**:
           - **Architecture Optimization**: Refine system architecture for better scalability
           - **Technology Stack Refinement**: Optimize technology choices for efficiency
           - **Implementation Strategy**: Develop phased implementation approach
           - **Risk Mitigation**: Address technical risks identified in validation
           - **Performance Optimization**: Improve system performance characteristics
           
           **Focus Areas**:
           - Reduce implementation complexity where possible
           - Address feasibility concerns that scored below 7.0
           - Optimize for team capabilities and resources
           - Improve maintainability and operational efficiency
           
           Provide refined technical specifications and updated feasibility projections."
        
        **Your Integration and Enhancement Tasks:**
        
        After receiving refinements from all specialists:
        
        1. **Solution Integration**:
           - Integrate improvements from all specialists into cohesive solution designs
           - Ensure refinements are compatible and don't conflict
           - Validate that improvements address validation weaknesses
           - Maintain solution strengths while addressing weaknesses
        
        2. **Business Viability Refinement**:
           - Update business model based on technical and UX refinements
           - Refine cost estimates based on updated technical approach
           - Assess impact of changes on revenue projections
           - Update timeline and resource requirements
        
        3. **Value Proposition Enhancement**:
           - Strengthen value propositions based on UX improvements
           - Clarify customer benefits from functional enhancements
           - Update competitive positioning based on technical capabilities
           - Refine go-to-market considerations
        
        4. **Quality Assessment**:
           - Evaluate improvement quality across all dimensions
           - Assess whether refinements adequately address validation concerns
           - Identify any new risks introduced by changes
           - Validate solution readiness for selection decision
        
        **Refinement Success Criteria**:
        - Address major weaknesses identified in Phase 4
        - Maintain or improve strengths from original solutions
        - Achieve target scores (>7.0) in critical dimensions
        - Ensure solution implementability and market viability
        """,
        expected_output="""
        **Phase 5 Results: Refined Solution Portfolio**
        
        ## Refinement Overview
        **Solutions Refined**: [Number of solutions improved]
        **Specialist Contributions**: [Summary of each agent's refinement work]
        **Refinement Focus Areas**: [Primary areas of improvement]
        
        ## Refined Solution Portfolio
        
        ### Refined Solution 1: [Solution Name]
        **Original Scores**: Value: [X.X] | Viability: [X.X] | Feasibility: [X.X] | Usability: [X.X]
        **Projected New Scores**: Value: [X.X] | Viability: [X.X] | Feasibility: [X.X] | Usability: [X.X]
        **Overall Improvement**: [+/- X.X points, % improvement]
        
        **Key Refinements Made**:
        
        **UX/UI Improvements** (Product Designer):
        - [Improvement 1]: [Specific change and expected impact]
        - [Improvement 2]: [Specific change and expected impact]
        - **Usability Impact**: [Expected improvement in usability score]
        
        **Functional Enhancements** (Functional Analyst):
        - [Enhancement 1]: [Specific change and business impact]
        - [Enhancement 2]: [Specific change and business impact]
        - **Requirements Impact**: [How changes improve implementability]
        
        **Technical Optimizations** (Engineering Manager):
        - [Optimization 1]: [Technical change and feasibility impact]
        - [Optimization 2]: [Technical change and feasibility impact]  
        - **Feasibility Impact**: [Expected improvement in feasibility score]
        
        **Business Model Refinements** (Product Manager):
        - [Refinement 1]: [Business change and viability impact]
        - [Refinement 2]: [Business change and viability impact]
        - **Viability Impact**: [Expected improvement in business viability]
        
        **Weaknesses Addressed**:
        - [Original weakness 1]: [How it was addressed]
        - [Original weakness 2]: [How it was addressed]
        
        **Strengths Preserved/Enhanced**:
        - [Strength 1]: [How it was maintained or improved]
        - [Strength 2]: [How it was maintained or improved]
        
        **New Risks Introduced**: [Any new risks from refinements]
        **Risk Mitigations**: [Strategies to address new risks]
        
        ---
        
        [Repeat structure for each refined solution]
        
        ## Refinement Impact Analysis
        
        **Improvement Summary by Dimension**:
        - **Value Improvements**: [Average improvement across solutions]
        - **Viability Improvements**: [Average improvement across solutions]
        - **Feasibility Improvements**: [Average improvement across solutions]
        - **Usability Improvements**: [Average improvement across solutions]
        
        **Cross-Solution Comparison**:
        | Solution | Pre-Refinement Score | Post-Refinement Score | Improvement |
        |----------|---------------------|----------------------|-------------|
        | Solution 1 | [X.X] | [X.X] | [+X.X] |
        | Solution 2 | [X.X] | [X.X] | [+X.X] |
        | Solution 3 | [X.X] | [X.X] | [+X.X] |
        
        ## Specialist Contribution Analysis
        
        **Product Designer Impact**:
        - **Most Significant UX Improvement**: [Description]
        - **Usability Score Improvements**: [List by solution]
        - **Design Innovation Highlights**: [Notable design solutions]
        
        **Functional Analyst Impact**:
        - **Most Critical Requirement Clarification**: [Description]
        - **Process Optimization Highlights**: [Key improvements]
        - **Integration Improvements**: [System interface enhancements]
        
        **Engineering Manager Impact**:
        - **Most Significant Technical Optimization**: [Description]
        - **Feasibility Score Improvements**: [List by solution]
        - **Architecture Improvements**: [Key technical enhancements]
        
        ## Quality Assessment
        
        **Refinement Effectiveness**:
        - **Target Achievement**: [How well refinements met improvement goals]
        - **Weakness Resolution**: [Percentage of validation concerns addressed]
        - **Strength Preservation**: [How well original strengths were maintained]
        
        **Solution Readiness for Selection**:
        - **Decision-Ready Solutions**: [Solutions ready for Phase 6 selection]
        - **Remaining Concerns**: [Any unresolved issues]
        - **Recommendation Confidence**: [Confidence level in refined solutions]
        
        ## Recommendations for Phase 6
        
        **Top Solution Candidate**: [Highest scoring refined solution]
        **Alternative Recommendations**: [Other strong candidates]
        **Selection Criteria Emphasis**: [What factors should drive final selection]
        
        **Critical Success Factors**:
        1. [Factor 1 for successful implementation]
        2. [Factor 2 for successful implementation] 
        3. [Factor 3 for successful implementation]
        
        **Implementation Readiness**: [Overall assessment of solution readiness for planning phase]
        """,
        agent=create_product_manager_agent(context.model)
    )