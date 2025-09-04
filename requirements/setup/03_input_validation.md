# Task 3: Input Validation

## Objective
Implement validation logic for the requirements path and PID path according to the specified criteria.

## Acceptance Criteria
- [ ] Validate that the requirements path exists on the file system
- [ ] Validate that the PID path exists on the file system
- [ ] Validate that the PID file has a .md extension (is a markdown file)
- [ ] Support both relative and absolute paths
- [ ] Exit with error code -1 when validation fails
- [ ] Display clear, easy-to-understand error messages for each validation failure
- [ ] Return validated paths if all checks pass

## Implementation Details
- Use `os.path.exists()` or `pathlib.Path.exists()` to check path existence
- Use `pathlib.Path.suffix` or similar to check file extension
- Convert relative paths to absolute paths for consistency
- Create specific error messages for each validation failure:
  - "Requirements path does not exist: {path}"
  - "PID path does not exist: {path}" 
  - "PID file must be a markdown file (.md extension): {path}"

## Definition of Done
- All three validation checks are implemented
- Appropriate error messages are displayed for each failure type
- Application exits with code -1 on any validation failure
- Both relative and absolute paths are handled correctly
- Validation passes when all criteria are met