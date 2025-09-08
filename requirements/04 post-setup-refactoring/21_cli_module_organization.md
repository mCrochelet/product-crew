# Task 21: CLI Module Organization

## Objective
Create a clean CLI module that serves as the main entry point and orchestrates the refactored modules.

## Requirements
- Create `product_crew/cli/` directory structure
- Create `product_crew/cli/main.py` as the new CLI entry point
- Maintain existing CLI functionality with Click decorators
- Import and orchestrate functions from refactored modules
- Update main.py to be a simple entry point wrapper

## CLI Module Structure
- `product_crew/cli/main.py`: Main CLI logic with Click decorators and argument parsing
- Root `main.py`: Simple wrapper that imports and calls CLI function
- Maintain all existing CLI options and behavior

## Import Organization
The CLI module should import from:
```python
from product_crew.validation import validate_requirements_path, validate_pid_path, validate_model
from product_crew.crew import run_crew
```

## Implementation Details
- Move CLI function and decorators to `product_crew/cli/main.py`
- Keep all Click options identical: `--requirements`, `--pid`, `--overwrite`, `--demo`, `--model`
- Preserve argument validation and error handling
- Maintain exit codes and error messages
- Update root `main.py` to import from CLI module

## CLI Function Flow
1. Parse and validate CLI arguments using validation module
2. Call crew runner with validated parameters
3. Handle errors and exit codes appropriately
4. Maintain identical user experience

## Acceptance Criteria
- CLI help output identical to current implementation
- All CLI options work exactly as before
- Error handling and exit codes preserved
- Integration with all refactored modules working
- Entry point functionality maintained for package installation
- All existing tests pass without modification

## Files to Create/Modify
- `product_crew/__init__.py`
- `product_crew/cli/__init__.py`
- `product_crew/cli/main.py`
- Update root `main.py` to be a simple wrapper