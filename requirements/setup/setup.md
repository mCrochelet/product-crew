# Product Crew CLI Setup

## Problem Space

As a developer, I need to kick off a new run of the crew by providing the following information:

- requirements: the path to the project requirements folder
- pid: the path to the product initiative to refine
- overwrite: boolean. If true, the pid file will be overwritten, otherwise a new one will be created next to the pid file.

## Solution Space

### Vision

Create a command-line application that validates inputs and uses CrewAI to orchestrate crew runs with the provided requirements and product initiative document paths.

### High-Level Approach

The crew run should be limited to a simple CrewAI agent that will print the paths provided as arguments. The arguments should be validated, and the application should exit with an error if the arguments are not valid.

### Technical Requirements

- The application should be written in Python 3.13
- It should use CrewAI to orchestrate the crews
- It should be a command line application
- Command structure: `product-crew -r requirements_path -pid pid_path [--overwrite]`

### Validation Requirements

The application should validate:
- The requirements path must exist
- The pid path must exist
- The pid file must be a markdown file

If validation fails, the application should exit with error code -1.

### File Structure Requirements

The `requirements` folder can contain both directories and files. Each file must be in markdown format. Files describe either an initiative or a task:

- A file describes an initiative if it is a child of `requirements` or has the same name as the subfolder it belongs to
- Otherwise, it describes a task
- Task files must be named with format `[number][task_name_in_snake_case].md` where `[number]` follows the format `0[number]` if less than 10, otherwise just `[number]`

### Output Requirements

- The CrewAI agent should print the paths provided as arguments as raw strings
- When overwrite=false and creating a new file next to the pid file, append the date `YYYY-MM-DD` to the file name
- Error messages should be easy to understand

### Success Criteria

The application successfully:
1. Parses command line arguments
2. Validates input paths and file types
3. Creates a CrewAI agent that prints the provided paths
4. Handles file creation/overwriting based on the overwrite flag
5. Exits with appropriate error codes when validation fails