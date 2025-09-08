"""CrewAI task creation and definition."""

from pathlib import Path
from crewai import Task

from .agents import create_path_printer_agent


def create_print_paths_task(requirements_path: Path, pid_path: Path, overwrite: bool, model: str = 'gpt-4') -> Task:
    """Create a task for printing the validated paths."""
    return Task(
        description=(
            f"Print exactly these three values as separate lines:\n"
            f"1. {requirements_path}\n"
            f"2. {pid_path}\n"
            f"3. {overwrite}\n\n"
            f"Output only these values, nothing else. No explanations, no formatting."
        ),
        expected_output=(
            f"Three lines containing:\n"
            f"Line 1: {requirements_path}\n"
            f"Line 2: {pid_path}\n"
            f"Line 3: {overwrite}"
        ),
        agent=create_path_printer_agent(model)
    )