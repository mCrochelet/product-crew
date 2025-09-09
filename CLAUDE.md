# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

This is a Python CLI application called "product-crew" that uses CrewAI to
orchestrate a team of agents acting as a senior product trio. The team helps
discover, research, and design product initiative documents (PIDs) by refining
existing ones through collaborative agent work.

The application consists of:

- Product Manager: Overall product lead for discovering opportunities and
  framing actionable areas
- Engineering Manager: Technical lead for evaluating feasible and cost-effective
  solutions
- Product Designer: Visual lead for creating intuitively usable experiences
- Functional Analyst: Breaks down solutions into functional increments
- Scrum Master: Process guardian ensuring initiatives are broken down into
  manageable tasks
- Market Analyst: Conducts market research and identifies data gaps

## Key Development Commands

### Installation and Setup

```bash
# Sync dependencies using UV (Python package manager)
uv sync

# Install testing dependencies (optional)
uv sync --extra test

# Run the application
uv run product-crew -r <requirements_path> --pid <pid_path> [--overwrite] [--demo] [--model <model_name>]

# Run tests (quiet mode, suppresses CrewAI/Pydantic warnings)
uv run pytest -q

# Run tests with full output
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=main --cov-report=term-missing

# Run tests quietly with coverage
uv run pytest -q --cov=main --cov-report=term-missing

# Run specific test file
uv run pytest test/test_main.py
```

### Application Usage

The CLI accepts these arguments:

- `-r, --requirements`: Path to project requirements folder (required)
- `--pid`: Path to product initiative document to refine (required)
- `--overwrite`: Flag to overwrite existing PID file, otherwise creates new
  timestamped file (optional)
- `--demo`: Enable interactive demo mode (optional)
- `--model`: OpenAI model to use for agents (optional, default: gpt-4)

## Architecture and Code Structure

The application follows a modular architecture with clear separation of
concerns:

### Package Structure

- `product_crew/` - Main package with modular organization
- `main.py` - Simple entry point wrapper

### Modules

- **`cli/`** - Command-line interface and argument parsing
- **`validation/`** - Input validation for CLI arguments
- **`file_operations/`** - File handling and environment management
- **`crew/`** - CrewAI agent management (agents, tasks, execution)
- **`demo/`** - Demo mode utilities and visualization

### Entry Point (`main.py`)

- Simple wrapper that imports and calls the CLI module
- Maintains backwards compatibility for package installation

### Requirements Structure

The `requirements/` directory contains project specifications:

- Structured as directories and markdown files
- Initiative files: either direct children of requirements/ or same name as
  parent folder
- Task files: numbered sequentially (01_task_name.md, 02_task_name.md, etc.)
- Each subfolder should contain one main file matching the folder name
- If a requirement is a direct child of requirements/, always create a new
  folder of the same name, move it in it, and create the task files to plan
  the implementation before starting the work.

### Product Initiative Document Template

The README.md contains a comprehensive PID template with sections for:

- Problem Space: Problem definition with data backing
- Research Summary: Takeaways and conclusions
- Solution Space: Vision, strategic goals, high-level approach, risks, user
  flows

## Testing

When testing, always use the file "test_pid.md".