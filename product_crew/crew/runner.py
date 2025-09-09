"""Product Manager crew execution for problem understanding analysis."""

from pathlib import Path
from crewai import Crew
from .tasks import create_problem_understanding_analysis_task
from .agents import create_product_manager_agent
from ..file_operations import load_environment, get_output_file_path, create_pid_file


def run_crew(requirements_path: Path, pid_path: Path, overwrite: bool, demo: bool = False,
             model: str = 'gpt-4o') -> None:
    """Run Product Manager crew to analyze problem understanding in PID."""
    try:
        load_environment()
        
        # Determine output file path
        output_path = get_output_file_path(pid_path, overwrite)
        
        # Create problem understanding analysis task and agent
        task = create_problem_understanding_analysis_task(requirements_path, pid_path, overwrite, model)
        agent = create_product_manager_agent(model)
        
        # Create and run crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=demo
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Save analysis results to output file
        analysis_content = str(result)
        create_pid_file(output_path, analysis_content)
        
        # Print the expected output format
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Print the expected output format even on error
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)