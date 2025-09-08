# Task 19: Crew Module Extraction

## Objective
Extract CrewAI-related functionality into a dedicated crew management module.

## Requirements
- Create `product_crew/crew/` directory structure with multiple files
- Organize CrewAI functionality by responsibility:
  - `agents.py`: Agent creation and configuration
  - `tasks.py`: Task creation and definition
  - `runner.py`: Crew execution and orchestration
- Maintain all existing CrewAI functionality and model integration

## Functions to Extract
1. **`agents.py`**: 
   - `create_path_printer_agent(model: str)`: Agent creation with model configuration
2. **`tasks.py`**:
   - `create_print_paths_task()`: Task definition and creation  
3. **`runner.py`**:
   - `run_crew()`: Main crew execution logic with demo integration

## Implementation Details
- Create proper module structure with `__init__.py` exports
- Maintain OpenAI model environment variable setting in agents
- Preserve demo mode integration in runner
- Keep all CrewAI imports and dependencies contained
- Ensure model parameter flows correctly through all modules

## CrewAI Integration Requirements
- Model parameter passes from CLI → runner → agents → tasks
- Environment variable `OPENAI_MODEL_NAME` set correctly
- Demo mode integration preserved with all visualization
- Error handling and fallback behavior maintained
- Verbose mode controlled by demo flag

## Acceptance Criteria
- CrewAI functionality identical to current implementation
- Model selection works with all supported OpenAI models
- Demo mode integration fully preserved
- All error handling and fallback logic maintained
- Existing tests pass without modification
- Clean import structure between crew modules

## Files to Create/Modify
- `product_crew/crew/__init__.py`
- `product_crew/crew/agents.py`
- `product_crew/crew/tasks.py` 
- `product_crew/crew/runner.py`
- Update imports in CLI module