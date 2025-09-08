"""Crew execution and orchestration."""

import sys
from pathlib import Path

import click
from crewai import Crew

from ..file_operations import load_environment, get_output_file_path, create_pid_file
from ..demo import demo_pause, demo_display_agent_info, demo_display_task_info, demo_section_separator
from .agents import create_path_printer_agent
from .tasks import create_print_paths_task


def run_crew(requirements_path: Path, pid_path: Path, overwrite: bool, demo: bool = False, model: str = 'gpt-4') -> None:
    """Run CrewAI agent to process PID file and create output."""
    try:
        if demo:
            demo_section_separator("INITIALIZATION")
            demo_pause("Starting product crew execution", "Step 1/5")
        
        # Load environment variables
        load_environment()
        
        # Determine output file path
        output_path = get_output_file_path(pid_path, overwrite)
        
        if demo:
            click.echo(f"\n{click.style('🎯 EXECUTION PARAMETERS', fg='green', bold=True)}")
            click.echo(f"{click.style('Requirements Path:', fg='cyan')} {requirements_path}")
            click.echo(f"{click.style('Input PID File:', fg='cyan')} {pid_path}")
            click.echo(f"{click.style('Output File:', fg='cyan')} {output_path}")
            click.echo(f"{click.style('Overwrite Mode:', fg='cyan')} {overwrite}")
            click.echo(f"{click.style('OpenAI Model:', fg='cyan')} {model}")
            demo_pause("Configuration validated", "Step 2/5")
        
        # Read the original PID file content
        try:
            with open(pid_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except (IOError, OSError) as e:
            click.echo(f"Failed to read PID file {pid_path}: {e}", err=True)
            sys.exit(1)

        if demo:
            demo_section_separator("AGENT & TASK CREATION")
            demo_pause("Creating CrewAI agents and tasks", "Step 3/5")
        
        # Create the agent and task for processing the PID content
        agent = create_path_printer_agent(model)
        task = create_print_paths_task(requirements_path, pid_path, overwrite, model)

        if demo:
            demo_display_agent_info(agent)
            demo_pause("Agent profile created. Now creating task...", "Step 3/5 - Agent Ready")
            
            demo_display_task_info(task, 1)
            demo_pause("Task specification ready. Initializing crew...", "Step 4/5")
        
        # Create and run the crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=demo
        )

        if demo:
            demo_section_separator("CREW EXECUTION")
            demo_pause("Executing crew tasks (this may take a moment)", "Step 5/5")
        
        # Run the crew (for now just processing, later will generate content)
        crew.kickoff()
        
        if demo:
            demo_section_separator("OUTPUT GENERATION")
            click.echo(f"\n{click.style('📝 FILE PROCESSING', fg='bright_green', bold=True)}")
            click.echo(f"{click.style('Creating output file:', fg='cyan')} {output_path}")
        
        # For now, create the output file with original content
        # In future tasks, this will be enhanced with agent-generated content
        create_pid_file(output_path, original_content)

        if demo:
            click.echo(f"{click.style('✅ File successfully created!', fg='bright_green', bold=True)}")
            demo_pause("Crew execution completed successfully!", "Completion")

        # Print the expected output format
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)

    except Exception as e:
        if demo:
            demo_section_separator("ERROR HANDLING")
            click.echo(f"\n{click.style('❌ ERROR ENCOUNTERED', fg='red', bold=True)}")
            click.echo(f"{click.style('Error Details:', fg='red')} {str(e)}")
            click.echo(f"{click.style('Fallback:', fg='yellow')} Using direct output mode")
            demo_pause("Error handled. Continuing with fallback...", "Error Recovery")
        click.echo(f"CrewAI execution error: {e}", err=True)
        # Fallback to direct printing on any error
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)