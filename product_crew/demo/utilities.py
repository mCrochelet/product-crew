"""Demo mode display and interaction utilities."""

import sys

import click
from crewai import Agent, Task


def demo_pause(message: str, step: str = "") -> None:
    """Pause execution in demo mode and wait for user input."""
    try:
        if step:
            click.echo(f"\n{click.style('=== DEMO MODE ===', fg='cyan', bold=True)} {click.style(step, fg='yellow')}")
        click.echo(f"{click.style('📍', fg='blue')} {message}")
        click.echo(f"{click.style('Press Enter to continue, or Ctrl+C to exit...', fg='green')}", nl=False)
        input()
        click.echo()  # Add blank line after input
    except KeyboardInterrupt:
        click.echo(f"\n{click.style('Demo mode interrupted by user. Exiting...', fg='red')}")
        sys.exit(0)


def demo_display_agent_info(agent: Agent) -> None:
    """Display detailed agent information in demo mode."""
    click.echo(f"\n{click.style('🤖 AGENT PROFILE', fg='magenta', bold=True)}")
    click.echo(f"{click.style('═' * 50, fg='magenta')}")
    click.echo(f"{click.style('Role:', fg='cyan', bold=True)} {click.style(agent.role, fg='white', bold=True)}")
    click.echo(f"{click.style('Goal:', fg='cyan', bold=True)} {agent.goal}")
    click.echo(f"{click.style('Backstory:', fg='cyan', bold=True)}")
    # Split backstory into lines for better readability
    backstory_lines = agent.backstory.split('. ')
    for line in backstory_lines:
        if line.strip():
            click.echo(f"  • {line.strip()}{'.' if not line.strip().endswith('.') else ''}")
    click.echo(f"{click.style('═' * 50, fg='magenta')}")


def demo_display_task_info(task: Task, task_number: int = 1) -> None:
    """Display detailed task information in demo mode."""
    click.echo(f"\n{click.style(f'📋 TASK #{task_number}', fg='yellow', bold=True)}")
    click.echo(f"{click.style('─' * 50, fg='yellow')}")
    click.echo(f"{click.style('Description:', fg='cyan', bold=True)}")
    # Split description into readable chunks
    desc_lines = task.description.split('\n')
    for line in desc_lines[:3]:  # Show first 3 lines
        if line.strip():
            click.echo(f"  {line.strip()}")
    if len(desc_lines) > 3:
        click.echo(f"  {click.style('... (description continues)', fg='bright_black')}")
    
    click.echo(f"\n{click.style('Expected Output:', fg='cyan', bold=True)}")
    expected_lines = task.expected_output.split('\n')
    for line in expected_lines[:3]:  # Show first 3 lines
        if line.strip():
            click.echo(f"  {line.strip()}")
    if len(expected_lines) > 3:
        click.echo(f"  {click.style('... (output continues)', fg='bright_black')}")
    click.echo(f"{click.style('─' * 50, fg='yellow')}")


def demo_section_separator(title: str) -> None:
    """Display a visual section separator in demo mode."""
    click.echo(f"\n{click.style('│', fg='bright_blue')} {click.style(title, fg='bright_white', bold=True)} {click.style('│', fg='bright_blue')}")
    click.echo(f"{click.style('┌' + '─' * (len(title) + 4) + '┐', fg='bright_blue')}")