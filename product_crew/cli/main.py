"""Main CLI entry point for product crew application."""

import sys

import click

from ..validation import validate_requirements_path, validate_pid_path, validate_model, validate_openai_api_key
from ..crew import run_crew


@click.command()
@click.option('-r', '--requirements', 'requirements_path', required=True,
              help='Path to the project requirements folder')
@click.option('--pid', 'pid_path', required=True,
              help='Path to the product initiative to refine')
@click.option('--overwrite', is_flag=True, default=False,
              help='If true, the pid file will be overwritten, otherwise a new one will be created')
@click.option('--demo', is_flag=True, default=False,
              help='Enable interactive demo mode')
@click.option('--model', default='gpt-4',
              help='OpenAI model to use for agents (default: gpt-4)')
def cli(requirements_path: str, pid_path: str, overwrite: bool, demo: bool, model: str) -> None:
    """Product crew CLI application."""

    try:
        # Validate arguments and get absolute paths
        validated_requirements_path = validate_requirements_path(requirements_path)
        validated_pid_path = validate_pid_path(pid_path)
        validated_model = validate_model(model)
        validate_openai_api_key()

        # Initialize and run CrewAI agent to print paths
        run_crew(validated_requirements_path, validated_pid_path, overwrite, demo, validated_model)

    except ValueError as e:
        click.echo(str(e), err=True)
        sys.exit(1)