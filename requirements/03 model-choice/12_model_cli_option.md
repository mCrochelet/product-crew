# Task 12: Model CLI Option

## Objective
Add a `--model` CLI option to allow users to specify the OpenAI model to use for CrewAI agents.

## Requirements
- Add an optional `--model` CLI flag to the existing Click-based CLI
- The flag should accept a string value specifying the OpenAI model name
- Default to `gpt-4` if no model is specified (note: requirement says gpt-5 but that doesn't exist yet)
- The flag should be properly documented in the CLI help text
- Pass the model parameter through the execution pipeline

## Implementation Details
- Extend the existing `@click.command()` decorator in `main.py`
- Add `@click.option('--model', default='gpt-4', help='OpenAI model to use for agents')`
- Update function signatures to include the model parameter
- Pass the model through to CrewAI agent configuration

## Acceptance Criteria
- `product-crew --help` shows the `--model` option with default value
- The application accepts the flag: `uv run product-crew -r requirements --pid sample.md --model gpt-3.5-turbo`
- The model parameter is passed to the crew execution logic
- All existing functionality remains unchanged when flag is not provided

## Files to Modify
- `main.py`: Add CLI option and update function signatures