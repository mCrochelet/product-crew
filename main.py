import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

import click
from crewai import Agent, Task, Crew
from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from .env.local file."""
    env_file = Path(".env.local")
    if env_file.exists():
        load_dotenv(env_file)


def validate_requirements_path(requirements_path: str) -> Path:
    """Validate that the requirements path exists and return absolute path."""
    path = Path(requirements_path).resolve()
    if not path.exists():
        raise ValueError(f"Requirements path does not exist: {path}")
    return path


def validate_pid_path(pid_path: str) -> Path:
    """Validate that the pid path exists and is a markdown file, return absolute path."""
    path = Path(pid_path).resolve()
    if not path.exists():
        raise ValueError(f"PID path does not exist: {path}")
    if not path.suffix.lower() == '.md':
        raise ValueError(f"PID file must be a markdown file (.md extension): {path}")
    return path


def get_output_file_path(original_path: Path, overwrite: bool) -> Path:
    """Determine the output file path based on overwrite flag."""
    if overwrite:
        return original_path
    
    # Create new file with timestamp
    today = datetime.now().strftime('%Y-%m-%d')
    stem = original_path.stem  # filename without extension
    suffix = original_path.suffix  # file extension
    parent = original_path.parent  # directory
    
    new_filename = f"{stem}-{today}{suffix}"
    return parent / new_filename


def create_pid_file(output_path: Path, content: str) -> None:
    """Create or overwrite the PID file with the given content."""
    try:
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        click.echo(f"PID file created: {output_path}")
        
    except (IOError, OSError, PermissionError) as e:
        click.echo(f"Failed to create file {output_path}: {e}", err=True)
        sys.exit(1)


def create_path_printer_agent() -> Agent:
    """Create a CrewAI agent that prints file paths."""
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


def create_print_paths_task(requirements_path: Path, pid_path: Path, overwrite: bool) -> Task:
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
        agent=create_path_printer_agent()
    )


def run_crew(requirements_path: Path, pid_path: Path, overwrite: bool) -> None:
    """Run CrewAI agent to process PID file and create output."""
    try:
        # Load environment variables
        load_environment()
        
        # Determine output file path
        output_path = get_output_file_path(pid_path, overwrite)
        
        # Read the original PID file content
        try:
            with open(pid_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except (IOError, OSError) as e:
            click.echo(f"Failed to read PID file {pid_path}: {e}", err=True)
            sys.exit(1)

        # Check if OpenAI API key is available
        if not os.getenv("OPENAI_API_KEY"):
            click.echo("Warning: No OpenAI API key found. Using direct file copy.", err=True)
            create_pid_file(output_path, original_content)
            print(str(requirements_path))
            print(str(pid_path))
            print(overwrite)
            return

        # Create the agent and task for processing the PID content
        agent = create_path_printer_agent()
        task = create_print_paths_task(requirements_path, pid_path, overwrite)

        # Create and run the crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )

        # Run the crew (for now just processing, later will generate content)
        crew.kickoff()
        
        # For now, create the output file with original content
        # In future tasks, this will be enhanced with agent-generated content
        create_pid_file(output_path, original_content)

        # Print the expected output format
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)

    except Exception as e:
        click.echo(f"CrewAI execution error: {e}", err=True)
        # Fallback to direct printing on any error
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)


@click.command()
@click.option('-r', '--requirements', 'requirements_path', required=True,
              help='Path to the project requirements folder')
@click.option('--pid', 'pid_path', required=True,
              help='Path to the product initiative to refine')
@click.option('--overwrite', is_flag=True, default=False,
              help='If true, the pid file will be overwritten, otherwise a new one will be created')
def cli(requirements_path: str, pid_path: str, overwrite: bool) -> None:
    """Product crew CLI application."""

    try:
        # Validate arguments and get absolute paths
        validated_requirements_path = validate_requirements_path(requirements_path)
        validated_pid_path = validate_pid_path(pid_path)

        # Initialize and run CrewAI agent to print paths
        run_crew(validated_requirements_path, validated_pid_path, overwrite)

    except ValueError as e:
        click.echo(str(e), err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
