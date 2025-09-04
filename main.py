import sys
from pathlib import Path
import click


def validate_requirements_path(requirements_path):
    """Validate that the requirements path exists and return absolute path."""
    path = Path(requirements_path).resolve()
    if not path.exists():
        raise ValueError(f"Requirements path does not exist: {path}")
    return path


def validate_pid_path(pid_path):
    """Validate that the pid path exists and is a markdown file, return absolute path."""
    path = Path(pid_path).resolve()
    if not path.exists():
        raise ValueError(f"PID path does not exist: {path}")
    if not path.suffix.lower() == '.md':
        raise ValueError(f"PID file must be a markdown file (.md extension): {path}")
    return path


@click.command()
@click.option('-r', '--requirements', 'requirements_path', required=True,
              help='Path to the project requirements folder')
@click.option('--pid', 'pid_path', required=True,
              help='Path to the product initiative to refine')
@click.option('--overwrite', is_flag=True, default=False,
              help='If true, the pid file will be overwritten, otherwise a new one will be created')
def cli(requirements_path, pid_path, overwrite):
    """Product crew CLI application."""

    try:
        # Validate arguments and get absolute paths
        validated_requirements_path = validate_requirements_path(requirements_path)
        validated_pid_path = validate_pid_path(pid_path)
        
        # Print the validated absolute paths as raw strings as required by the specification
        print(str(validated_requirements_path))
        print(str(validated_pid_path))
        print(overwrite)
        
    except ValueError as e:
        click.echo(str(e), err=True)
        sys.exit(-1)


if __name__ == '__main__':
    cli()
