"""Functional Analyst tools for requirements breakdown and task definition."""

# Simple function-based tools (will be integrated with agents later)
def tool(func):
    """Simple decorator to mark functions as tools."""
    func._is_tool = True
    return func


@tool
def requirements_decomposition(initiative_description: str, business_requirements: str) -> str:
    """Decompose high-level requirements into detailed functional requirements."""
    try:
        return f"""
# Requirements Decomposition

## Initiative Overview
{initiative_description}

## Business Requirements
{business_requirements}

## Functional Requirements
### Core Functionality
- Primary features and capabilities
- Business logic requirements
- Data processing needs
- Integration requirements

### User Requirements
- User roles and permissions
- User interface requirements
- User workflow requirements
- Accessibility requirements

### System Requirements
- Performance requirements
- Security requirements
- Reliability requirements
- Scalability requirements

## Non-Functional Requirements
- Performance benchmarks
- Security standards
- Compliance requirements
- Operational requirements
"""
    except Exception as e:
        return f"Error in requirements decomposition: {str(e)}"


@tool
def user_story_creation(functional_requirements: str, user_personas: str) -> str:
    """Create user stories from functional requirements."""
    try:
        return f"""
# User Story Creation

## Functional Requirements Context
{functional_requirements}

## User Personas
{user_personas}

## Epic-Level Stories
1. **User Management**: As a user, I want to manage my account
2. **Core Functionality**: As a user, I want to use core features
3. **Data Management**: As a user, I want to manage my data
4. **Integration**: As a user, I want to connect with other systems

## Detailed User Stories
### Format: As a [user type], I want [goal] so that [benefit]

#### User Registration & Authentication
- As a new user, I want to create an account so that I can access the platform
- As a returning user, I want to log in securely so that I can access my data
- As a user, I want to reset my password so that I can regain access if forgotten

#### Core Feature Stories
- Feature-specific user stories based on requirements
- Priority and complexity estimates
- Dependencies between stories

## Story Acceptance Criteria
- Detailed acceptance criteria for each story
- Definition of done
- Testing requirements
"""
    except Exception as e:
        return f"Error in user story creation: {str(e)}"


@tool
def acceptance_criteria_definition(user_stories: str, requirements: str) -> str:
    """Define detailed acceptance criteria for user stories."""
    try:
        return f"""
# Acceptance Criteria Definition

## User Stories Context
{user_stories}

## Requirements Reference
{requirements}

## Acceptance Criteria Framework
### Given-When-Then Format
For each user story:
- **Given**: Initial context or preconditions
- **When**: Action performed by user
- **Then**: Expected outcome or result

## Detailed Acceptance Criteria
### Functional Criteria
- Expected behavior and outcomes
- Input validation requirements
- Error handling scenarios
- Edge case handling

### Non-Functional Criteria
- Performance requirements
- Security requirements
- Usability requirements
- Accessibility requirements

## Definition of Done
- Code requirements
- Testing requirements
- Documentation requirements
- Review requirements
"""
    except Exception as e:
        return f"Error in acceptance criteria definition: {str(e)}"


@tool
def dependency_mapping(user_stories: str, technical_requirements: str) -> str:
    """Map dependencies between user stories and technical components."""
    try:
        return f"""
# Dependency Mapping

## User Stories
{user_stories}

## Technical Requirements
{technical_requirements}

## Dependency Analysis
### Story Dependencies
- Prerequisites between user stories
- Blocking relationships
- Optional dependencies

### Technical Dependencies
- System component dependencies
- External service dependencies
- Database schema dependencies
- API dependencies

## Implementation Sequence
1. **Foundation Stories**: Core infrastructure requirements
2. **Core Features**: Primary functionality
3. **Enhanced Features**: Advanced capabilities
4. **Integration Stories**: External system connections

## Risk Assessment
- Critical path dependencies
- High-risk dependencies
- Mitigation strategies
- Alternative approaches
"""
    except Exception as e:
        return f"Error in dependency mapping: {str(e)}"