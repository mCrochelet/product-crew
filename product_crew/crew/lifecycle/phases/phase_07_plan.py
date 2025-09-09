"""Phase 7: Implementation Planning - Create comprehensive implementation roadmap and tasks."""

from crewai import Task
from ..context import LifecycleContext
from ...agents import create_product_manager_agent


def create_implementation_planning_task(context: LifecycleContext) -> Task:
    """Create Phase 7 task: Plan comprehensive implementation approach."""
    
    # Get results from previous phases
    phase_6_results = context.get_phase_result(6)  # Solution selection results
    
    return Task(
        description=f"""
        **PHASE 7: PLAN IMPLEMENTATION**
        
        Create a comprehensive implementation plan for the selected solution, coordinating with specialist agents to develop detailed roadmaps, requirements, and delivery strategies.
        
        **Selected Solution (Phase 6):**
        {phase_6_results}
        
        **Selected Solution Details:** {context.selected_solution}
        
        **REQUIRED DELEGATIONS** - Comprehensive implementation planning across all dimensions:
        
        1. **Functional Analyst - REQUIREMENTS BREAKDOWN**:
           "Please create detailed implementation requirements for the selected solution:
           
           **Requirements Decomposition**:
           - Break down solution into detailed functional requirements
           - Create comprehensive user stories with acceptance criteria
           - Map requirements to business processes and workflows
           - Define data requirements and information architecture
           - Specify integration requirements with existing systems
           
           **Requirement Organization**:
           - Prioritize requirements using MoSCoW method (Must have, Should have, Could have, Won't have)
           - Group requirements into logical implementation phases
           - Create requirement dependencies and sequencing
           - Define requirement traceability matrix
           - Establish requirement validation and testing criteria
           
           **Scope Management**:
           - Define MVP (Minimum Viable Product) scope
           - Identify requirements for subsequent releases
           - Create requirement change management process
           - Define scope boundaries and what's explicitly excluded
           
           Provide detailed functional specification document with prioritized requirement backlog."
        
        2. **Engineering Manager - TECHNICAL IMPLEMENTATION PLANNING**:
           "Please create comprehensive technical implementation plan for the selected solution:
           
           **Architecture and Design**:
           - Finalize system architecture and component design
           - Define technology stack and development framework
           - Create detailed technical specifications
           - Design database schema and data architecture
           - Plan integration patterns and API specifications
           
           **Development Planning**:
           - Estimate development effort for each component (person-hours/days)
           - Define development phases and technical milestones
           - Create technical task breakdown structure
           - Identify technical dependencies and critical path
           - Plan development environment and tooling setup
           
           **Quality and Operations**:
           - Define testing strategy (unit, integration, system, UAT)
           - Plan deployment pipeline and DevOps approach
           - Create monitoring and observability strategy
           - Define performance benchmarks and SLAs
           - Plan security implementation and compliance measures
           
           **Risk Management**:
           - Identify technical implementation risks
           - Create risk mitigation strategies and contingency plans
           - Define technical proof-of-concepts if needed
           - Plan capacity and scalability testing approach
           
           Provide detailed technical implementation plan with effort estimates and timeline."
        
        3. **Scrum Master - DELIVERY PLANNING AND PROJECT MANAGEMENT**:
           "Please create comprehensive delivery plan and project management approach:
           
           **Sprint and Release Planning**:
           - Design sprint structure and cadence
           - Create release plan with incremental value delivery
           - Define sprint goals and deliverable objectives
           - Plan sprint capacity based on team availability
           - Create dependency management across sprints
           
           **Team Organization**:
           - Recommend team structure and composition
           - Define roles and responsibilities matrix
           - Plan team onboarding and skill development
           - Create communication and collaboration protocols
           - Define decision-making processes and escalation paths
           
           **Process and Methodology**:
           - Design Agile/Scrum implementation approach
           - Create definition of done and quality criteria
           - Plan retrospectives and continuous improvement
           - Define velocity tracking and progress measurement
           - Create risk management and issue escalation processes
           
           **Timeline and Milestones**:
           - Create detailed project timeline with key milestones
           - Plan buffer time and risk contingencies
           - Define checkpoint reviews and go/no-go decisions
           - Coordinate with business stakeholder availability
           - Plan user acceptance testing and feedback cycles
           
           Provide comprehensive project plan with timeline, milestones, and delivery approach."
        
        **Your Integration and Strategic Planning Tasks:**
        
        After receiving detailed plans from all specialists:
        
        1. **Plan Integration and Synthesis**:
           - Integrate all specialist plans into coherent implementation strategy
           - Resolve conflicts and dependencies between different planning perspectives
           - Ensure functional, technical, and delivery plans are aligned
           - Create master timeline incorporating all workstreams
        
        2. **Resource Planning and Budget**:
           - Consolidate resource requirements from all specialists
           - Create comprehensive budget estimates (development, infrastructure, operations)
           - Plan resource allocation and capacity management
           - Identify external vendor or consultant needs
           - Create hiring plan if additional team members needed
        
        3. **Stakeholder and Change Management**:
           - Create stakeholder engagement and communication plan
           - Plan user training and change management activities
           - Design feedback collection and iteration processes
           - Plan marketing and launch activities if applicable
           - Create success measurement and KPI tracking plan
        
        4. **Risk and Contingency Planning**:
           - Consolidate risks from all planning perspectives
           - Create comprehensive risk register and mitigation strategies
           - Plan contingency scenarios and fallback options
           - Define risk monitoring and escalation procedures
           - Create decision points for plan adjustments
        
        5. **Implementation Readiness Assessment**:
           - Validate organizational readiness for implementation
           - Assess team capabilities vs. requirements
           - Confirm stakeholder commitment and resource availability
           - Validate technical infrastructure and dependencies
           - Create implementation readiness checklist
        """,
        expected_output="""
        **Phase 7 Results: Comprehensive Implementation Plan**
        
        ## Implementation Plan Overview
        **Selected Solution**: [Solution name and brief description]
        **Planning Completion Date**: [Current date]
        **Estimated Implementation Duration**: [X months/weeks]
        **Total Estimated Effort**: [Person-months or person-weeks]
        **Target Go-Live Date**: [Planned launch date]
        
        ## Executive Summary
        **Implementation Approach**: [High-level implementation strategy]
        **Key Success Factors**: [3-4 critical factors for success]
        **Major Milestones**: [Key delivery milestones and dates]
        **Resource Requirements**: [High-level team and budget needs]
        **Primary Risks**: [Top 3 implementation risks and mitigation approaches]
        
        ## Functional Implementation Plan
        *Based on Functional Analyst input*
        
        **Requirements Summary**:
        - **Total Requirements**: [Number of functional requirements]
        - **MVP Requirements**: [Number of must-have requirements]
        - **User Stories**: [Total number of user stories created]
        - **Integration Points**: [Number of system integrations required]
        
        **Implementation Phases**:
        
        **Phase 1 - MVP Foundation** ([X weeks]):
        - [Key functionality group 1]: [X requirements, effort estimate]
        - [Key functionality group 2]: [X requirements, effort estimate]
        - **Deliverables**: [Core functionality delivered]
        - **Success Criteria**: [MVP success measures]
        
        **Phase 2 - Enhanced Functionality** ([X weeks]):
        - [Enhancement group 1]: [X requirements, effort estimate]
        - [Enhancement group 2]: [X requirements, effort estimate]
        - **Deliverables**: [Enhanced capabilities]
        - **Success Criteria**: [Phase 2 success measures]
        
        **Phase 3 - Full Feature Set** ([X weeks]):
        - [Advanced functionality]: [X requirements, effort estimate]
        - [Nice-to-have features]: [X requirements, effort estimate]
        - **Deliverables**: [Complete solution]
        - **Success Criteria**: [Final success measures]
        
        **Requirement Priorities**:
        - **Must Have**: [X requirements - critical for success]
        - **Should Have**: [X requirements - important for adoption]
        - **Could Have**: [X requirements - valuable but not critical]
        - **Won't Have (this release)**: [X requirements - future consideration]
        
        ## Technical Implementation Plan
        *Based on Engineering Manager input*
        
        **Architecture Overview**:
        - **System Architecture**: [High-level architecture approach]
        - **Technology Stack**: [Key technologies and frameworks]
        - **Integration Approach**: [How system integrates with existing infrastructure]
        - **Data Architecture**: [Database design and data management approach]
        
        **Development Timeline**:
        
        **Technical Foundation** ([X weeks], [Y person-weeks]):
        - Infrastructure setup and DevOps pipeline: [X person-days]
        - Core architecture and framework setup: [X person-days]
        - Database design and setup: [X person-days]
        - Authentication and security implementation: [X person-days]
        
        **Core Development** ([X weeks], [Y person-weeks]):
        - [Component 1]: [X person-days, dependencies]
        - [Component 2]: [X person-days, dependencies]
        - [Component 3]: [X person-days, dependencies]
        - Integration development: [X person-days]
        
        **Quality Assurance and Testing** ([X weeks], [Y person-weeks]):
        - Unit testing development: [X person-days]
        - Integration testing: [X person-days]
        - System testing and UAT: [X person-days]
        - Performance and security testing: [X person-days]
        
        **Technical Risks and Mitigations**:
        1. **[Technical Risk 1]**: [Mitigation strategy and contingency]
        2. **[Technical Risk 2]**: [Mitigation strategy and contingency]
        3. **[Technical Risk 3]**: [Mitigation strategy and contingency]
        
        ## Delivery Plan and Project Management
        *Based on Scrum Master input*
        
        **Sprint Structure**:
        - **Sprint Duration**: [X weeks]
        - **Total Sprints**: [X sprints across all phases]
        - **Team Velocity Assumption**: [X story points per sprint]
        - **Sprint Planning Approach**: [Planning methodology]
        
        **Release Schedule**:
        
        **Release 1 - MVP** (Sprint [X-Y], [Date]):
        - **Goal**: [Core functionality delivery]
        - **User Stories**: [X stories, Y story points]
        - **Key Features**: [List of MVP features]
        - **Success Criteria**: [Release success measures]
        
        **Release 2 - Enhanced** (Sprint [X-Y], [Date]):
        - **Goal**: [Enhanced functionality delivery]
        - **User Stories**: [X stories, Y story points]
        - **Key Features**: [List of enhanced features]
        - **Success Criteria**: [Release success measures]
        
        **Release 3 - Complete** (Sprint [X-Y], [Date]):
        - **Goal**: [Full solution delivery]
        - **User Stories**: [X stories, Y story points]
        - **Key Features**: [List of complete features]
        - **Success Criteria**: [Final success measures]
        
        **Team Organization**:
        - **Recommended Team Size**: [X people]
        - **Key Roles Needed**: [List of required roles]
        - **Skills Requirements**: [Critical skills and experience needed]
        - **Team Formation Timeline**: [When team needs to be assembled]
        
        **Process Framework**:
        - **Methodology**: [Agile/Scrum approach details]
        - **Ceremonies**: [Sprint planning, dailies, reviews, retros]
        - **Tools**: [Project management and collaboration tools]
        - **Quality Gates**: [Definition of done, review criteria]
        
        ## Resource Planning and Budget
        
        **Human Resources**:
        - **Development Team**: [X FTEs, roles, duration]
        - **Product Team**: [X FTEs, roles, duration]  
        - **QA Team**: [X FTEs, roles, duration]
        - **DevOps/Infrastructure**: [X FTEs, roles, duration]
        - **External Consultants**: [If needed, roles, duration]
        
        **Budget Estimates**:
        - **Personnel Costs**: $[X] ([Y person-months at $Z average rate])
        - **Infrastructure Costs**: $[X] (cloud, licensing, tools)
        - **External Services**: $[X] (consultants, vendors, APIs)
        - **Training and Development**: $[X]
        - **Contingency (10-20%)**: $[X]
        - **Total Estimated Budget**: $[X]
        
        **Resource Timeline**:
        - **Team Ramp-up**: [When resources needed]
        - **Peak Resource Period**: [When most resources required]
        - **Resource Ramp-down**: [When resources can be released]
        
        ## Risk Management Plan
        
        **Consolidated Risk Register**:
        
        1. **[Risk 1 - e.g., Technical Complexity]**:
           - **Probability**: [High/Medium/Low]
           - **Impact**: [High/Medium/Low]
           - **Risk Score**: [1-9]
           - **Mitigation Strategy**: [Specific actions to reduce risk]
           - **Contingency Plan**: [What to do if risk materializes]
           - **Risk Owner**: [Who monitors and manages this risk]
        
        [Continue for all major risks...]
        
        **Risk Monitoring Plan**:
        - **Risk Review Frequency**: [Weekly/bi-weekly during implementation]
        - **Risk Escalation Criteria**: [When to escalate risks]
        - **Risk Communication Plan**: [How risks are communicated to stakeholders]
        
        ## Stakeholder Engagement Plan
        
        **Communication Strategy**:
        - **Executive Sponsors**: [Monthly updates on progress and risks]
        - **End Users**: [Bi-weekly demos and feedback sessions]
        - **IT Operations**: [Weekly technical coordination meetings]
        - **Business Stakeholders**: [Sprint reviews and milestone presentations]
        
        **Change Management**:
        - **Training Plan**: [User training schedule and approach]
        - **Communication Plan**: [Key messages and timing]
        - **Feedback Mechanisms**: [How to collect and incorporate feedback]
        - **Adoption Strategy**: [How to ensure solution adoption]
        
        ## Success Measurement Plan
        
        **Key Performance Indicators (KPIs)**:
        - **Delivery KPIs**: [On-time, on-budget, scope completion]
        - **Quality KPIs**: [Defect rates, performance metrics, user satisfaction]
        - **Business KPIs**: [Business value delivered, ROI metrics]
        - **Team KPIs**: [Velocity, team satisfaction, knowledge transfer]
        
        **Measurement Timeline**:
        - **Weekly**: [Development progress, sprint metrics]
        - **Monthly**: [Budget, timeline, quality metrics]
        - **Quarterly**: [Business value, stakeholder satisfaction]
        - **Post-Launch**: [Adoption, performance, ROI measurement]
        
        ## Implementation Readiness Assessment
        
        **Readiness Checklist**:
        - [ ] **Team Assembled**: All required team members identified and available
        - [ ] **Budget Approved**: Implementation budget secured and approved
        - [ ] **Infrastructure Ready**: Technical infrastructure and tools available
        - [ ] **Stakeholder Buy-in**: Key stakeholders committed and supportive
        - [ ] **Requirements Finalized**: MVP requirements clearly defined and agreed
        - [ ] **Risk Mitigation Plans**: Key risks identified with mitigation strategies
        
        **Prerequisites for Implementation Start**:
        1. [Prerequisite 1]: [What must be completed before starting]
        2. [Prerequisite 2]: [What must be completed before starting]
        3. [Prerequisite 3]: [What must be completed before starting]
        
        **Go/No-Go Decision Criteria**:
        - [Criterion 1]: [Minimum requirement for proceeding]
        - [Criterion 2]: [Minimum requirement for proceeding]
        - [Criterion 3]: [Minimum requirement for proceeding]
        
        ## Next Steps and Immediate Actions
        
        **Immediate Actions (Next 1-2 weeks)**:
        1. [Action 1]: [Specific action and owner]
        2. [Action 2]: [Specific action and owner]  
        3. [Action 3]: [Specific action and owner]
        
        **Short-term Actions (Next 4 weeks)**:
        1. [Action 1]: [Specific action and timeline]
        2. [Action 2]: [Specific action and timeline]
        3. [Action 3]: [Specific action and timeline]
        
        **Implementation Kickoff Plan**:
        - **Kickoff Meeting**: [Planned date and agenda]
        - **Team Formation**: [Timeline for team assembly]
        - **First Sprint Planning**: [When first sprint planning occurs]
        - **Stakeholder Alignment**: [Initial stakeholder communication]
        
        ## Plan Confidence and Validation
        
        **Plan Confidence Assessment**:
        - **Requirements Confidence**: [High/Medium/Low - how well requirements understood]
        - **Technical Confidence**: [High/Medium/Low - technical approach certainty]
        - **Timeline Confidence**: [High/Medium/Low - schedule reliability]
        - **Resource Confidence**: [High/Medium/Low - resource availability certainty]
        
        **Plan Validation Approach**:
        - **Stakeholder Review**: [Who needs to review and approve plan]
        - **Technical Review**: [Technical validation and sign-off process]
        - **Budget Validation**: [Financial review and approval process]
        - **Timeline Validation**: [Schedule review with all stakeholders]
        
        **Plan Iteration and Updates**:
        - **Plan Review Frequency**: [How often plan will be updated]
        - **Change Management Process**: [How plan changes will be managed]
        - **Version Control**: [How plan versions will be tracked]
        - **Communication of Changes**: [How plan updates will be communicated]
        """,
        agent=create_product_manager_agent(context.model)
    )