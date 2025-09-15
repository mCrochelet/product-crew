"""Product Manager agent for problem understanding analysis."""

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
    """Create a Product Manager agent that analyzes problem understanding in PIDs."""
    _configure_model(model)

    return Agent(
        role='Product Manager',
        goal='Orchestrate comprehensive problem understanding analysis by delegating specialized assessments to domain experts, then synthesizing their insights into a unified evaluation',
        backstory=(
            "You are an experienced Product Manager with 10+ years of experience in product strategy "
            "and problem analysis. You excel at evaluating whether product initiatives have properly "
            "understood the problem space before jumping to solutions. Your strength lies in knowing "
            "which expert to consult for each aspect of problem understanding, then synthesizing their "
            "insights into coherent assessments. You delegate jobs-to-be-done analysis to JTBD experts "
            "while handling overall coordination and integration of findings. You focus on ensuring "
            "teams have clearly identified: who the users and customers are, what job they're trying "
            "to accomplish, what value solving this creates, how the competitive landscape addresses this "
            "job currently, how success would be measured, and how this fits within the broader service "
            "ecosystem. You never suggest solutions, but rather assess the quality of problem understanding."
        ),
        verbose=True,
        allow_delegation=True,
        max_iter=5,
        max_execution_time=600
    )


def create_jobs_to_be_done_expert_agent(model: str = 'gpt-4o') -> Agent:
    """Create a Jobs-to-be-Done Expert agent for specialized JTBD analysis."""
    _configure_model(model)

    return Agent(
        role='Jobs-to-be-Done Expert',
        goal='Analyze Product Initiative Documents specifically from a Jobs-to-be-Done perspective to assess how well the user jobs, desired progress, and job context are understood',
        backstory=(
            "You are a certified Jobs-to-be-Done expert with 7+ years of experience applying Clayton "
            "Christensen's methodology to product innovation and problem analysis. You specialize in "
            "identifying the functional, emotional, and social jobs that customers hire products to do. "
            "Your expertise includes evaluating whether teams understand the user's job-to-be-done, "
            "the progress they're trying to make, the circumstances that trigger job execution, and "
            "the job executor vs. job beneficiary dynamics. You assess problem understanding through "
            "the JTBD lens, identifying gaps in understanding user motivations, job triggers, desired "
            "outcomes, and job context. You never suggest solutions, only assess the depth of job "
            "understanding in problem statements."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )