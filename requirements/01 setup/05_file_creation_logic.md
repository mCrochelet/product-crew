# Task 5: File Creation Logic

## Objective
Implement file creation/overwriting logic based on the `--overwrite` flag for the PID file.

## Acceptance Criteria
- [ ] When `--overwrite` is True: overwrite the existing PID file
- [ ] When `--overwrite` is False: create a new file next to the PID file
- [ ] New file naming format: append date `YYYY-MM-DD` to the filename (before extension)
- [ ] Handle file creation errors gracefully
- [ ] Preserve original file when creating new version
- [ ] Use current system date for the timestamp

## Implementation Details
- Use `datetime.now().strftime('%Y-%m-%d')` for date formatting
- For new file creation, modify filename like: `original-name-2025-0115.md`
- Use `pathlib.Path` for robust file path manipulation
- Ensure the new file is created in the same directory as the original
- Handle potential file write permissions and disk space issues

## Examples
Original file: `/path/to/initiative.md`
- If `--overwrite`: overwrite `/path/to/initiative.md`
- If not `--overwrite`: create `/path/to/initiative-2025-0115.md`

## Definition of Done
- Overwrite functionality works when flag is set
- New file creation works with correct date format when flag is not set
- Original file is preserved when creating new version
- File operations handle errors gracefully
- Date format is exactly `YYYY-MM-DD`