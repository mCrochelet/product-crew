# Product Crew

A Python CLI application that uses CrewAI to orchestrate a team of AI agents acting as a senior product trio. The team helps discover, research, and design product initiative documents (PIDs) by refining existing ones through collaborative agent work.

## 🤖 The Team

The product crew is composed of specialized AI agents:

- **Product Manager**: Acting as the overall product lead, responsible for discovering areas of opportunity for customers and users, and framing them in actionable product areas. Ultimately responsible for the value and viability of the product.
- **Engineering Manager**: Acting as the technical lead, responsible for evaluating and designing solutions that will be feasible and cost-effective.
- **Product Designer**: Acting as the visual lead, responsible for creating an experience that is intuitively usable.
- **Functional Analyst**: Acting as the right-hand of the product and engineering manager, responsible for breaking down solutions into functional increments (tasks).
- **Scrum Master**: Acting as the process guardian, responsible for team velocity and ensuring that each initiative document is broken down into manageable tasks.
- **Market Analyst**: Responsible for market research and deep analysis of available information through desk research. Also knows when data is missing and how to acquire it (e.g., qualitative research, interviews, surveys, etc.).

## 🚀 Installation

This project uses [UV](https://docs.astral.sh/uv/) as the Python package manager for fast and reliable dependency management.

### Prerequisites

- Python 3.13 or higher
- UV package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

### Install

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd product-crew
   ```

2. Sync dependencies using UV:
   ```bash
   uv sync
   ```

3. Set up your API keys (choose one or both providers):

   **For OpenAI models:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

   **For Anthropic models:**
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   ```

   Alternatively, create a `.env.local` file in the project root:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

## 📋 Usage

### Basic Usage

```bash
uv run product-crew -r <requirements_path> --pid <pid_path> [OPTIONS]
```

### Required Arguments

- `-r, --requirements`: Path to the project requirements folder
- `--pid`: Path to the product initiative document (PID) to refine (must be a `.md` file)

### Optional Arguments

- `--overwrite`: If set, overwrites the existing PID file. Otherwise, creates a new timestamped file
- `--demo`: Enables interactive demo mode with step-by-step visualization
- `--model`: Specifies the AI model to use (default: `gpt-4o`)

### Examples

**Basic refinement with OpenAI:**
```bash
uv run product-crew -r ./requirements --pid ./docs/my-initiative.md
```

**Use Anthropic Claude with overwrite:**
```bash
uv run product-crew -r ./requirements --pid ./docs/my-initiative.md --model claude-3-5-sonnet-20241022 --overwrite
```

**Interactive demo mode:**
```bash
uv run product-crew -r ./requirements --pid ./docs/my-initiative.md --demo
```

**Custom model:**
```bash
uv run product-crew -r ./requirements --pid ./docs/my-initiative.md --model gpt-4-turbo
```

### Supported Models

The application supports the same models as CrewAI, e.g.:

- **OpenAI**: `gpt-4`, `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`, and others
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, and others

The application automatically detects the provider based on the model name and validates the appropriate API key is available.

## 🏗️ Architecture

### Project Structure

```
product_crew/
├── cli/                    # Command-line interface
│   └── main.py            # CLI entry point with Click
├── validation/            # Input validation
│   └── validators.py      # Path, model, and API key validation
├── file_operations/       # File handling
│   └── handlers.py        # PID file creation and environment loading
├── crew/                  # CrewAI integration
│   ├── agents.py         # AI agent creation and configuration
│   ├── tasks.py          # Task definitions for agents
│   └── runner.py         # Crew orchestration and execution
└── demo/                  # Interactive demo mode
    └── utilities.py       # Demo visualization and user interaction
```

### Key Components

1. **CLI Layer** (`cli/main.py`): 
   - Click-based command-line interface
   - Argument validation and error handling
   - Integration point for all modules

2. **Validation Layer** (`validation/validators.py`):
   - Path existence and format validation
   - API key validation based on model provider
   - Basic model name validation (CrewAI handles model-specific validation)

3. **CrewAI Integration** (`crew/`):
   - Agent creation with provider-specific configuration
   - Task orchestration and execution
   - Environment variable management for different AI providers

4. **File Operations** (`file_operations/handlers.py`):
   - PID file creation with timestamp support
   - Environment file loading (`.env.local`)
   - Output path generation

5. **Demo Mode** (`demo/utilities.py`):
   - Interactive step-by-step execution
   - Agent and task information display
   - User input handling for demo flow

## ✨ Features

### 🎯 Core Capabilities

- **Multi-Provider AI Support**: Seamlessly works with both OpenAI and Anthropic models
- **Collaborative AI Agents**: Six specialized agents work together to refine product initiatives
- **Flexible Output**: Choose to overwrite existing files or create timestamped versions
- **Interactive Demo Mode**: Step-through mode for understanding the agent workflow
- **Robust Validation**: Comprehensive input validation with user-friendly error messages

### 📊 Requirements Structure

The application expects a specific requirements folder structure:

- **Initiative files**: Either direct children of requirements/ or same name as parent folder
- **Task files**: Numbered sequentially (`01_task_name.md`, `02_task_name.md`, etc.)
- **Hierarchical organization**: Subfolders should contain one main file matching the folder name

Example:
```
requirements/
├── user-authentication/
│   ├── user-authentication.md    # Main initiative
│   ├── 01_login_flow.md
│   └── 02_password_reset.md
└── payment-system.md             # Direct initiative file
```

## 🧪 Development

### Running Tests

```bash
# Run all tests with coverage
uv run pytest --cov=product_crew --cov-report=term-missing

# Run tests quietly (suppresses warnings)
uv run pytest -q

# Run specific test files
uv run pytest test/validation/test_validators.py -v
```

### Code Quality

The project includes comprehensive testing:
- **Unit tests** for all validation and utility functions
- **Integration tests** for CLI and end-to-end workflows
- **Demo mode tests** for interactive functionality
- **Provider-specific tests** for both OpenAI and Anthropic integration

### Project Commands

```bash
# Install dependencies
uv sync

# Install with test dependencies
uv sync --extra test

# Run the application
uv run product-crew --help

# Run tests
uv run pytest

# Run with coverage reporting
uv run pytest --cov=product_crew --cov-report=term-missing
```

## 📄 License

This project is part of a private development effort for product initiative document refinement using collaborative AI agents.