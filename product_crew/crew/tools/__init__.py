"""Tools module for CrewAI agents."""

from .product_manager_tools import (
    market_opportunity_analysis,
    business_case_evaluation,
    value_proposition_assessment,
    competitive_analysis
)
from .engineering_manager_tools import (
    technical_feasibility_assessment,
    architecture_design,
    cost_estimation,
    technology_stack_evaluation
)
from .product_designer_tools import (
    user_journey_mapping,
    wireframe_conceptualization,
    usability_heuristic_evaluation,
    design_system_assessment
)
from .functional_analyst_tools import (
    requirements_decomposition,
    user_story_creation,
    acceptance_criteria_definition,
    dependency_mapping
)
from .scrum_master_tools import (
    sprint_planning,
    task_estimation,
    velocity_tracking,
    retrospective_analysis
)
from .market_analyst_tools import (
    market_research,
    data_gap_identification,
    competitive_intelligence,
    trend_analysis
)

__all__ = [
    # Product Manager Tools
    'market_opportunity_analysis',
    'business_case_evaluation', 
    'value_proposition_assessment',
    'competitive_analysis',
    # Engineering Manager Tools
    'technical_feasibility_assessment',
    'architecture_design',
    'cost_estimation',
    'technology_stack_evaluation',
    # Product Designer Tools
    'user_journey_mapping',
    'wireframe_conceptualization',
    'usability_heuristic_evaluation',
    'design_system_assessment',
    # Functional Analyst Tools
    'requirements_decomposition',
    'user_story_creation',
    'acceptance_criteria_definition',
    'dependency_mapping',
    # Scrum Master Tools
    'sprint_planning',
    'task_estimation',
    'velocity_tracking',
    'retrospective_analysis',
    # Market Analyst Tools
    'market_research',
    'data_gap_identification',
    'competitive_intelligence',
    'trend_analysis'
]