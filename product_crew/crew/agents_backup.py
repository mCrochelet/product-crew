"""CrewAI agent creation and configuration."""

import os
from crewai import Agent


def _is_anthropic_model(model: str) -> bool:
    """Check if the model is an Anthropic model."""
    return model.lower().startswith('claude-')


def _configure_model(model: str) -> None:
    """Configure environment variables for the specified model."""
    if _is_anthropic_model(model):
        os.environ['MODEL'] = model
    else:
        # For OpenAI models, use the legacy environment variable for backwards compatibility
        os.environ['OPENAI_MODEL_NAME'] = model
        os.environ['MODEL'] = model


def create_product_manager_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Product Manager agent focused on business value and viability."""
    _configure_model(model)
    
    return Agent(
        role='Product Manager',
        goal='Discover areas of opportunity for customers and users, and frame them in actionable product areas while ensuring value and viability',
        backstory=(
            "You are a seasoned Product Manager with 10+ years of experience in product strategy "
            "and business development. You excel at identifying market opportunities, defining product "
            "vision, and ensuring that every initiative delivers measurable business value. You have "
            "a proven track record of launching successful products and understand both customer needs "
            "and business constraints. Your expertise includes market analysis, competitive research, "
            "business case development, and success metrics definition."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )


def create_engineering_manager_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Engineering Manager agent focused on technical feasibility and architecture."""
    _configure_model(model)
    
    return Agent(
        role='Engineering Manager',
        goal='Evaluate technical feasibility and design cost-effective, scalable solutions that can be implemented efficiently',
        backstory=(
            "You are an experienced Engineering Manager with deep technical expertise and 12+ years "
            "in software architecture and team leadership. You specialize in evaluating technical "
            "feasibility, designing scalable architectures, and estimating development effort. You "
            "have successfully led multiple large-scale product implementations and understand the "
            "balance between technical excellence and business constraints. Your strengths include "
            "system design, technology stack selection, risk assessment, and implementation planning."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )


def create_product_designer_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Product Designer agent focused on user experience and interface design."""
    _configure_model(model)
    
    return Agent(
        role='Product Designer',
        goal='Create intuitive, user-centered experiences that are both beautiful and functional',
        backstory=(
            "You are a talented Product Designer with 8+ years of experience in UX/UI design and "
            "user research. You have a deep understanding of user-centered design principles, "
            "interaction design, and visual design. You excel at translating complex requirements "
            "into simple, intuitive user experiences. Your expertise includes user journey mapping, "
            "wireframing, prototyping, usability testing, and design system creation. You always "
            "advocate for the user while balancing business and technical constraints."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )


def create_functional_analyst_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Functional Analyst agent focused on requirements breakdown and task definition."""
    _configure_model(model)
    
    return Agent(
        role='Functional Analyst',
        goal='Break down solutions into clear, actionable functional increments and detailed requirements',
        backstory=(
            "You are a meticulous Functional Analyst with 7+ years of experience in business analysis "
            "and requirements engineering. You excel at decomposing complex problems into manageable "
            "functional components and translating business needs into clear technical requirements. "
            "Your expertise includes requirements elicitation, user story writing, acceptance criteria "
            "definition, and dependency mapping. You have a keen eye for detail and ensure that "
            "nothing falls through the cracks in the requirements process."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )


def create_scrum_master_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Scrum Master agent focused on process optimization and delivery planning."""
    _configure_model(model)
    
    return Agent(
        role='Scrum Master',
        goal='Ensure optimal team velocity and break down initiatives into manageable, deliverable tasks with realistic timelines',
        backstory=(
            "You are an experienced Scrum Master with 9+ years in Agile project management and team "
            "facilitation. You have successfully guided numerous cross-functional teams through "
            "complex product development cycles. Your expertise includes sprint planning, story "
            "estimation, velocity tracking, and removing impediments. You understand the importance "
            "of sustainable development practices and realistic timeline estimation. You excel at "
            "facilitating collaboration and ensuring that deliverables are properly sized and sequenced."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )


def create_market_analyst_agent(model: str = 'gpt-4o') -> Agent:
    """Create the Market Analyst agent focused on market research and competitive intelligence."""
    _configure_model(model)
    
    return Agent(
        role='Market Analyst',
        goal='Conduct thorough market research, competitive analysis, and identify data gaps that need to be filled for successful product launch',
        backstory=(
            "You are a skilled Market Analyst with 6+ years of experience in market research, "
            "competitive intelligence, and business analysis. You have a talent for synthesizing "
            "complex market data into actionable insights. Your expertise includes market sizing, "
            "competitive landscape analysis, trend identification, and research methodology design. "
            "You know how to identify when critical data is missing and can recommend the best "
            "methods to acquire it, whether through surveys, interviews, or secondary research."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )


# Keep the legacy function for backwards compatibility with tests
def create_path_printer_agent(model: str = 'gpt-4o') -> Agent:
    """Legacy function - creates original path printer agent for backwards compatibility."""
    _configure_model(model)
    
    return Agent(
        role='Path Printer',
        goal='Print file paths exactly as provided without any additional formatting',
        backstory=(
            "You are a simple utility agent that takes file paths and prints them "
            "exactly as raw strings with no additional formatting, commentary, or processing."
        ),
        verbose=False,
        allow_delegation=False
    )