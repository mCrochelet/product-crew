"""CrewAI management module."""

from .agents import (
    create_product_manager_agent,
    create_engineering_manager_agent, 
    create_product_designer_agent,
    create_functional_analyst_agent,
    create_scrum_master_agent,
    create_market_analyst_agent,
    create_path_printer_agent  # Legacy compatibility
)
from .tasks import create_print_paths_task
from .runner import run_crew

__all__ = [
    'create_product_manager_agent',
    'create_engineering_manager_agent',
    'create_product_designer_agent', 
    'create_functional_analyst_agent',
    'create_scrum_master_agent',
    'create_market_analyst_agent',
    'create_path_printer_agent',  # Legacy compatibility
    'create_print_paths_task',
    'run_crew'
]