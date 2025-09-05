# Task 8: Demo Mode CLI Flag

## Objective
Add a `--demo` CLI flag to the existing Click-based CLI to enable interactive demo mode.

## Requirements
- Add an optional `--demo` flag to the main CLI command
- The flag should be a boolean flag (no value required)
- When enabled, the application should run in interactive demo mode
- The flag should be properly documented in the CLI help text

## Implementation Details
- Extend the existing `@click.command()` decorator in `main.py`
- Add `@click.option('--demo', is_flag=True, default=False, help='Enable interactive demo mode')`
- Pass the demo flag through the validation and crew execution pipeline
- Update function signatures to include the demo parameter

## Acceptance Criteria
- `product-crew --help` shows the `--demo` option
- The application accepts the flag without errors: `uv run product-crew -r requirements --pid sample.md --demo`
- The demo flag is passed to the crew execution logic
- All existing functionality remains unchanged when flag is not provided

## Files to Modify
- `main.py`: Add CLI option and update function signatures