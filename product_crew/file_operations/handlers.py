"""File and environment handling functions."""

import sys
from datetime import datetime
from pathlib import Path

import click
from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from .env.local file."""
    env_file = Path(".env.local")
    if env_file.exists():
        load_dotenv(env_file)
    else :
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)



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