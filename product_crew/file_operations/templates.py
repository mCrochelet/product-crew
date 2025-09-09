"""PID template generation and formatting."""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def generate_pid_template(
    initiative_name: str,
    version: str = "1.0",
    iteration: int = 1,
    status: str = "In Progress"
) -> str:
    """Generate a comprehensive PID template."""
    
    return f"""# {initiative_name}
*Version: {version} | Iteration: {iteration}/5 | Status: {status} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## Executive Summary
*[Product Manager Lead]*

### Problem Statement
[Clear definition of the problem this initiative addresses]

### Proposed Solution
[High-level solution approach and key benefits]

### Business Impact
[Expected business outcomes and value creation]

### Success Metrics
[Key performance indicators and success criteria]

---

## Market Analysis
*[Market Analyst Lead]*

### Market Opportunity
- **Target Market Size**: [TAM, SAM, SOM analysis]
- **Growth Potential**: [Market growth trends and drivers]
- **Customer Segments**: [Primary and secondary target customers]

### Competitive Landscape
- **Direct Competitors**: [Head-to-head competitive analysis]
- **Indirect Competitors**: [Alternative solutions and substitutes]
- **Competitive Advantages**: [Our differentiation and positioning]

### Validation Strategy
- **Market Research**: [Required research activities]
- **Customer Discovery**: [Interview and survey plans]
- **Data Gaps**: [Information needed for decision making]

---

## User Experience Design
*[Product Designer Lead]*

### User Journey
- **Primary User Flow**: [Main interaction path]
- **Key Touchpoints**: [Critical user interaction points]
- **Pain Points**: [Current friction areas to address]

### Key Interactions
- **Core Features**: [Primary feature interactions]
- **Navigation**: [Information architecture approach]
- **Accessibility**: [Inclusive design considerations]

### Design Principles
- **Visual Design**: [Style and branding approach]
- **Interaction Design**: [User interface patterns]
- **Usability Standards**: [Design quality criteria]

---

## Technical Architecture
*[Engineering Manager Lead]*

### Technical Approach
- **System Architecture**: [High-level architectural pattern]
- **Technology Stack**: [Recommended technologies]
- **Integration Strategy**: [External system connections]

### Architecture Overview
- **Core Components**: [Major system components]
- **Data Architecture**: [Database and storage design]
- **Security Approach**: [Authentication and data protection]

### Implementation Phases
- **Phase 1 (MVP)**: [Minimum viable implementation]
- **Phase 2 (Enhanced)**: [Feature expansion and optimization]
- **Phase 3 (Advanced)**: [Full feature set and scale]

---

## Functional Requirements
*[Functional Analyst Lead]*

### Core Features
- **Primary Features**: [Essential functionality]
- **Secondary Features**: [Enhanced capabilities]
- **Integration Features**: [External system connections]

### User Stories
- **Epic 1**: [Major user workflow]
- **Epic 2**: [Secondary user workflow]
- **Epic 3**: [Administrative workflow]

### Acceptance Criteria
- **Functional Criteria**: [Expected behavior and outcomes]
- **Performance Criteria**: [Speed and scalability requirements]
- **Quality Criteria**: [Reliability and error handling]

---

## Implementation Plan
*[Scrum Master Lead]*

### Sprint Breakdown
- **Sprint 1**: [Foundation and core infrastructure]
- **Sprint 2**: [Primary feature implementation]
- **Sprint 3**: [Enhanced features and integration]
- **Sprint 4**: [Testing, optimization, and launch]

### Task Estimation
- **Story Points**: [Effort estimation methodology]
- **Team Velocity**: [Projected delivery capacity]
- **Timeline**: [Development and launch schedule]

### Dependencies
- **Technical Dependencies**: [Infrastructure and platform requirements]
- **Business Dependencies**: [Decisions and approvals needed]
- **External Dependencies**: [Third-party services and integrations]

---

## Integration Points
*[Cross-Functional]*

### Technical Dependencies
- **Infrastructure**: [Platform and hosting requirements]
- **APIs and Services**: [External system integrations]
- **Data Sources**: [Required data feeds and connections]

### Design-Dev Handoffs
- **Design Specifications**: [Visual and interaction design deliverables]
- **Component Library**: [Reusable UI components]
- **Asset Requirements**: [Images, icons, and media]

### Testing Strategy
- **Unit Testing**: [Code quality and functionality validation]
- **Integration Testing**: [System interaction validation]
- **User Acceptance Testing**: [End-to-end workflow validation]

---

## Risk Assessment
*[All Agents]*

### Technical Risks
- **High Risk**: [Complex implementation challenges]
- **Medium Risk**: [Standard technical challenges]
- **Low Risk**: [Well-understood implementation patterns]

### Market Risks
- **Competition**: [Competitive response and market changes]
- **Customer Adoption**: [Market acceptance and user engagement]
- **Regulatory**: [Compliance and legal considerations]

### Mitigation Strategies
- **Risk Monitoring**: [Early warning indicators]
- **Contingency Plans**: [Alternative approaches and fallbacks]
- **Decision Points**: [Go/no-go evaluation criteria]

---

## Success Metrics
*[Product Manager + Market Analyst]*

### KPIs and Metrics
- **Business Metrics**: [Revenue, growth, and profitability]
- **Product Metrics**: [Usage, engagement, and retention]
- **Operational Metrics**: [Performance, quality, and efficiency]

### Success Criteria
- **Launch Success**: [Initial adoption and feedback]
- **Growth Success**: [Sustained usage and expansion]
- **Business Success**: [Financial and strategic objectives]

### Monitoring Plan
- **Dashboard**: [Real-time metrics and reporting]
- **Review Schedule**: [Regular assessment and optimization]
- **Success Milestones**: [Key achievement markers]

---

## Resource Requirements

### Team Composition
- **Development Team**: [Required roles and skills]
- **Design Team**: [UX/UI and visual design support]
- **Product Team**: [Product management and analysis]

### Budget Allocation
- **Development Costs**: [Personnel and technology expenses]
- **Infrastructure Costs**: [Platform and operational expenses]
- **Marketing Costs**: [Launch and growth investment]

### Timeline and Milestones
- **Development Timeline**: [Feature delivery schedule]
- **Launch Timeline**: [Go-to-market execution plan]
- **Success Timeline**: [Business objective achievement plan]

---

*This document represents the collective analysis and recommendations of the Product Crew collaborative AI agents. Generated through {iteration} iteration(s) of cross-functional analysis and refinement.*
"""


def format_agent_contribution(agent_role: str, content: str, section_title: str) -> str:
    """Format an individual agent's contribution to the PID."""
    
    return f"""
## {section_title}
*[{agent_role} Lead]*

{content}

---
"""


def combine_agent_outputs(agent_outputs: Dict[str, str], initiative_name: str) -> str:
    """Combine all agent outputs into a comprehensive PID."""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    pid_content = f"""# {initiative_name}
*Collaborative Product Initiative Document*
*Generated: {timestamp} by Product Crew AI Agents*

---

"""
    
    # Define the section mapping for each agent
    section_mapping = {
        'Product Manager': 'Executive Summary & Business Case',
        'Market Analyst': 'Market Analysis & Competitive Intelligence',
        'Product Designer': 'User Experience & Interface Strategy',
        'Engineering Manager': 'Technical Architecture & Implementation',
        'Functional Analyst': 'Requirements & User Stories',
        'Scrum Master': 'Sprint Planning & Delivery Strategy'
    }
    
    # Add each agent's contribution
    for agent_role, content in agent_outputs.items():
        if agent_role in section_mapping:
            section_title = section_mapping[agent_role]
            pid_content += format_agent_contribution(agent_role, content, section_title)
    
    # Add integration summary if available
    if 'Integration' in agent_outputs:
        pid_content += f"""
## Integration Summary & Recommendations
*[Cross-Functional Analysis]*

{agent_outputs['Integration']}

---
"""
    
    pid_content += f"""
## Document Metadata

- **Generation Method**: Collaborative AI Agent Analysis
- **Agents Involved**: {', '.join(agent_outputs.keys())}
- **Analysis Depth**: Multi-perspective cross-functional review
- **Last Updated**: {timestamp}
- **Version Control**: Iteration-based refinement process

---

*This Product Initiative Document was generated through collaborative analysis by specialized AI agents representing different functional roles in product development. Each section reflects the expertise and perspective of the respective agent role.*
"""
    
    return pid_content


def extract_initiative_name(pid_content: str) -> str:
    """Extract initiative name from existing PID content."""
    lines = pid_content.split('\n')
    
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if line.startswith('# ') and not line.startswith('## '):
            # Remove markdown header and clean up
            name = line[2:].strip()
            # Remove version/status info if present
            if '|' in name:
                name = name.split('|')[0].strip()
            if '*' in name:
                name = name.split('*')[0].strip()
            return name if name else "Product Initiative"
    
    return "Product Initiative"


def create_enhanced_pid(original_content: str, agent_results: Dict[str, str]) -> str:
    """Create an enhanced PID from original content and agent analysis."""
    
    # Extract the initiative name from original content
    initiative_name = extract_initiative_name(original_content)
    
    # If we have agent results, combine them
    if agent_results:
        return combine_agent_outputs(agent_results, initiative_name)
    else:
        # Fallback to template with extracted name
        return generate_pid_template(initiative_name)