# Task 13: Model Validation

## Objective
Implement validation to ensure only valid OpenAI models are accepted by the CLI.

## Requirements
- Create a validation function that checks if the provided model is a valid OpenAI model
- Only accept models that are available through the OpenAI API
- CLI should exit with error code 1 if an invalid model is provided
- Provide clear error messages for invalid models
- Support both current and legacy OpenAI model names

## Implementation Details
- Create a `validate_model()` function that checks against a list of valid OpenAI models
- Include common models: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, etc.
- Consider using OpenAI API to dynamically validate models (optional)
- Integrate validation into the CLI argument processing
- Ensure proper error handling and exit codes

## Valid OpenAI Models to Support
- `gpt-4` (default)
- `gpt-4-turbo` 
- `gpt-4-turbo-preview`
- `gpt-3.5-turbo`
- `gpt-3.5-turbo-16k`
- Other current OpenAI models as appropriate

## Acceptance Criteria
- Valid models are accepted without errors
- Invalid models trigger validation error with exit code 1
- Error message clearly indicates which models are supported
- Validation works for both full model names and common aliases
- Case-insensitive model name matching

## Files to Modify
- `main.py`: Add model validation function and integrate into CLI