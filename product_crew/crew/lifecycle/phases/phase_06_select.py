"""Phase 6: Solution Selection - Product Manager synthesizes insights and selects optimal solution."""

from crewai import Task
from ..context import LifecycleContext
from ...agents import create_product_manager_agent


def create_solution_selection_task(context: LifecycleContext) -> Task:
    """Create Phase 6 task: Select the best solution based on comprehensive analysis."""
    
    # Get results from previous phases
    phase_4_results = context.get_phase_result(4)  # Validation results
    phase_5_results = context.get_phase_result(5)  # Refinement results
    
    return Task(
        description=f"""
        **PHASE 6: SELECT BEST SOLUTION**
        
        Make the final solution selection decision by synthesizing all analysis and insights from previous phases. This is a critical Product Manager decision that will determine the direction for implementation.
        
        **Validation Results (Phase 4):**
        {phase_4_results}
        
        **Refinement Results (Phase 5):**
        {phase_5_results}
        
        **Current Context:**
        - Problem Statement: {context.problem_statement}
        - Problem Domain: {context.problem_domain}
        - Solutions Evaluated: {len(context.solution_evaluations)}
        - Solutions Refined: [Based on Phase 5 results]
        
        **NO DELEGATIONS** - This is your executive decision as Product Manager, synthesizing all specialist input received in previous phases.
        
        **Your Solution Selection Framework:**
        
        1. **Comprehensive Analysis Review**:
           - Review all validation scores and specialist feedback
           - Analyze refinement impacts and improvements
           - Assess current solution landscape after all improvements
           - Validate that selection criteria align with business objectives
        
        2. **Multi-Criteria Decision Analysis**:
           
           **Primary Selection Criteria** (Apply weighted scoring):
           - **Composite Score Performance**: Overall 4-dimensional evaluation results
           - **Strategic Alignment**: How well solution aligns with business strategy
           - **Risk Profile**: Acceptable risk level across all dimensions
           - **Implementation Readiness**: Solution maturity and implementability
           - **Resource Optimization**: Best use of available resources and capabilities
           
           **Secondary Selection Criteria**:
           - **Market Timing**: Alignment with market readiness and competitive landscape
           - **Organizational Fit**: Compatibility with company culture and capabilities
           - **Scalability Potential**: Long-term growth and expansion opportunities
           - **Learning Opportunities**: Knowledge and capability building potential
           - **Stakeholder Support**: Likelihood of stakeholder buy-in and adoption
        
        3. **Scenario Analysis**:
           - **Best Case Scenario**: What happens if this solution exceeds expectations
           - **Most Likely Scenario**: Realistic outcome projection based on current data
           - **Worst Case Scenario**: What are the failure modes and mitigation options
           - **Competitive Response**: How competitors might react and counter-strategies
        
        4. **Trade-off Analysis**:
           - Explicitly identify what is being gained and sacrificed with each option
           - Assess opportunity costs of not selecting alternative solutions
           - Evaluate reversibility of the decision and pivot options
           - Consider sequential implementation possibilities
        
        5. **Stakeholder Impact Assessment**:
           - Map solution impact on all identified stakeholders
           - Assess stakeholder acceptance and potential resistance
           - Plan change management and communication strategies
           - Identify success metrics meaningful to each stakeholder group
        
        6. **Implementation Feasibility Review**:
           - Validate that selected solution can be realistically implemented
           - Confirm resource availability and team capabilities
           - Assess timeline requirements and organizational readiness
           - Review integration requirements and dependencies
        
        **Decision Documentation Requirements:**
        
        Your decision must be thoroughly documented with:
        - Clear rationale for why this solution was selected
        - Explicit trade-offs and alternatives considered
        - Risk assessment and mitigation strategies
        - Success metrics and measurement plan
        - Implementation prerequisites and assumptions
        - Stakeholder communication and change management plan
        
        **Selection Quality Criteria:**
        
        Ensure your selected solution:
        - ✅ Clearly addresses the defined problem statement
        - ✅ Achieves acceptable scores across all 4 evaluation dimensions
        - ✅ Aligns with organizational capabilities and resources
        - ✅ Has manageable risk profile with mitigation strategies
        - ✅ Provides clear value proposition to stakeholders
        - ✅ Can be realistically implemented within constraints
        - ✅ Supports measurable business outcomes
        """,
        expected_output="""
        **Phase 6 Results: Solution Selection Decision**
        
        ## Executive Decision Summary
        **Selected Solution**: [Solution Name/ID]
        **Decision Confidence Level**: [High/Medium/Low with rationale]
        **Decision Date**: [Current date]
        **Decision Maker**: Product Manager
        
        ## Selected Solution Overview
        **Solution Name**: [Full solution name and brief description]
        **Solution Category**: [Market-driven/Technical/User-centered/Process-oriented/Hybrid]
        **Core Value Proposition**: [Key benefits and unique selling points]
        
        **Final Evaluation Scores** (Post-Refinement):
        - **Value Score**: [X.X/10] - [Brief rationale]
        - **Viability Score**: [X.X/10] - [Brief rationale]  
        - **Feasibility Score**: [X.X/10] - [Brief rationale]
        - **Usability Score**: [X.X/10] - [Brief rationale]
        - **Composite Score**: [X.X/10]
        - **Final Ranking**: #[X] out of [Y] solutions
        
        ## Selection Rationale
        
        **Primary Reasons for Selection**:
        1. **[Reason 1]**: [Detailed explanation of why this factor drove selection]
        2. **[Reason 2]**: [Detailed explanation of why this factor drove selection]
        3. **[Reason 3]**: [Detailed explanation of why this factor drove selection]
        
        **Key Differentiators** (vs. Alternative Solutions):
        - [Differentiator 1]: [How selected solution is superior]
        - [Differentiator 2]: [How selected solution is superior]
        - [Differentiator 3]: [How selected solution is superior]
        
        **Strategic Alignment Factors**:
        - **Business Strategy**: [How solution supports overall business strategy]
        - **Market Position**: [How solution strengthens competitive position]
        - **Organizational Capabilities**: [How solution leverages existing strengths]
        - **Resource Optimization**: [How solution makes best use of available resources]
        
        ## Trade-off Analysis
        
        **What We're Gaining**:
        - [Benefit 1]: [Specific gain and impact]
        - [Benefit 2]: [Specific gain and impact]
        - [Benefit 3]: [Specific gain and impact]
        
        **What We're Sacrificing**:
        - [Trade-off 1]: [What we're giving up and why it's acceptable]
        - [Trade-off 2]: [What we're giving up and why it's acceptable]
        - [Trade-off 3]: [What we're giving up and why it's acceptable]
        
        **Alternative Solutions Considered**:
        - **[Alternative 1]**: [Why not selected despite strengths]
        - **[Alternative 2]**: [Why not selected despite strengths]
        - **[Alternative 3]**: [Why not selected despite strengths]
        
        ## Risk Assessment and Mitigation
        
        **Primary Risks**:
        1. **[Risk 1]**: 
           - **Probability**: [High/Medium/Low]
           - **Impact**: [High/Medium/Low]
           - **Mitigation Strategy**: [Specific actions to reduce risk]
        
        2. **[Risk 2]**:
           - **Probability**: [High/Medium/Low]
           - **Impact**: [High/Medium/Low]
           - **Mitigation Strategy**: [Specific actions to reduce risk]
        
        3. **[Risk 3]**:
           - **Probability**: [High/Medium/Low] 
           - **Impact**: [High/Medium/Low]
           - **Mitigation Strategy**: [Specific actions to reduce risk]
        
        **Risk Monitoring Plan**:
        - [Key risk indicator 1]: [How to monitor and thresholds]
        - [Key risk indicator 2]: [How to monitor and thresholds]
        - **Risk Review Frequency**: [How often to assess risks]
        
        ## Success Metrics and Measurement Plan
        
        **Primary Success Metrics**:
        1. **[Metric 1]**: [Target value, measurement method, timeline]
        2. **[Metric 2]**: [Target value, measurement method, timeline]
        3. **[Metric 3]**: [Target value, measurement method, timeline]
        
        **Secondary Success Indicators**:
        - [Indicator 1]: [Target and measurement approach]
        - [Indicator 2]: [Target and measurement approach]
        
        **Measurement Timeline**:
        - **30 days**: [Early indicators to track]
        - **90 days**: [Short-term success metrics]
        - **180 days**: [Medium-term impact assessment]
        - **1 year**: [Long-term success evaluation]
        
        ## Stakeholder Impact and Communication Plan
        
        **Primary Stakeholders**:
        - **[Stakeholder 1]**: [Impact description and communication approach]
        - **[Stakeholder 2]**: [Impact description and communication approach]
        - **[Stakeholder 3]**: [Impact description and communication approach]
        
        **Change Management Requirements**:
        - **Training Needs**: [Required training and skill development]
        - **Process Changes**: [Workflow and operational changes needed]
        - **Communication Plan**: [Key messages and communication channels]
        - **Resistance Management**: [Anticipated resistance and management strategies]
        
        ## Implementation Prerequisites
        
        **Required Capabilities**:
        - [Capability 1]: [Current state and gap analysis]
        - [Capability 2]: [Current state and gap analysis]
        - [Capability 3]: [Current state and gap analysis]
        
        **Resource Requirements**:
        - **Team Size**: [Estimated team composition and size]
        - **Skills Needed**: [Key technical and domain skills required]
        - **Budget Requirements**: [High-level budget needs]
        - **Timeline Estimate**: [Realistic implementation timeline]
        
        **Dependencies and Assumptions**:
        - **Critical Dependencies**: [External factors solution depends on]
        - **Key Assumptions**: [Assumptions underlying the selection decision]
        - **Prerequisite Activities**: [What must be completed before starting]
        
        ## Next Steps for Phase 7
        
        **Implementation Planning Priorities**:
        1. [Priority 1]: [What needs detailed planning first]
        2. [Priority 2]: [What needs detailed planning second]
        3. [Priority 3]: [What needs detailed planning third]
        
        **Key Planning Questions for Phase 7**:
        - [Question 1]: [Critical planning question to address]
        - [Question 2]: [Critical planning question to address]
        - [Question 3]: [Critical planning question to address]
        
        **Recommended Planning Approach**:
        - **Functional Analyst Focus**: [Areas requiring detailed requirements work]
        - **Engineering Manager Focus**: [Technical planning priorities]
        - **Scrum Master Focus**: [Delivery planning priorities]
        
        ## Decision Confidence and Validation
        
        **Confidence Level Justification**:
        - **High Confidence Factors**: [What makes this decision reliable]
        - **Uncertainty Areas**: [Where confidence could be improved]
        - **Validation Opportunities**: [How to test decision assumptions]
        
        **Decision Review and Iteration**:
        - **Review Triggers**: [Conditions that would prompt decision reconsideration]
        - **Pivot Options**: [Alternative paths if implementation challenges arise]
        - **Learning Plan**: [How to gather data to validate decision quality]
        """,
        agent=create_product_manager_agent(context.model)
    )