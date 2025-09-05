# Task 9: Interactive Step Control

## Objective
Implement keyboard input-based step control for crew interactions in demo mode.

## Requirements
- When `--demo` flag is enabled, enable the verbose mode of the crew
- When `--demo` flag is enabled, pause between crew interaction steps
- Display current step information to the user
- Wait for keyboard input (Enter key) before proceeding to next step
- Provide clear visual indicators of demo mode status
- Allow graceful exit with Ctrl+C

## Implementation Details
- Create a demo controller that intercepts crew execution
- Add pause points between agent tasks and crew steps
- Display step information using Click's styling for better UX
- Use `input()` or `click.pause()` for keyboard interaction
- Handle KeyboardInterrupt gracefully

## Step Points for Demo Mode
1. Before crew initialization
2. Before each agent task execution
3. After each agent completes their task
4. Before final output generation
5. After completion

## Acceptance Criteria
- In demo mode, execution pauses at defined step points
- Clear messages indicate current step and next action
- User can proceed by pressing Enter
- User can exit cleanly with Ctrl+C
- Normal mode execution is unaffected

## Files to Modify
- `main.py`: Add demo control logic to `run_crew()` function
- Consider extracting demo logic to separate module if complex