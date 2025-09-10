# Shared Utilities

Common utilities, base classes, and helper functions used across all agentic tools projects.

## Components

- **Base Classes**: Abstract classes for agents, tools, and clients
- **Configuration**: Environment and settings management
- **Logging**: Structured logging with context
- **Validation**: Pydantic models and validators  
- **CLI**: Command-line interface utilities
- **Testing**: Test fixtures and utilities

## Key Features

- Standardized interfaces across projects
- Configuration management with validation
- Structured logging with rich formatting
- Common data models and schemas
- CLI framework with rich output
- Testing utilities and fixtures

## Installation

```bash
# Automatically included with any project installation
# Or install individually
cd shared && pip install -e .
```

## Base Classes

### Agent Base Class
```python
from shared.base.agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
    
    async def execute(self, task: str) -> str:
        # Implementation here
        pass
```

### Tool Base Class  
```python
from shared.base.tool import BaseTool

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "A custom tool implementation"
    
    def run(self, input_data: str) -> str:
        # Implementation here
        pass
```

## Configuration Management

```python
from shared.config import Settings

settings = Settings()
# Automatically loads from .env files and environment variables
print(settings.api_key)  # Validated and typed
```

## Logging

```python
from shared.logging import get_logger

logger = get_logger(__name__)
logger.info("Starting process", extra={"task_id": "123"})
```

## CLI Utilities

```python
from shared.cli import create_app
import typer

app = create_app()

@app.command()
def my_command(input_file: str = typer.Option(..., help="Input file path")):
    """Process an input file."""
    # Implementation here
    pass
```

## Data Models

Common Pydantic models used across projects:

```python
from shared.models import TaskRequest, TaskResponse, AgentConfig

request = TaskRequest(
    task_type="research",
    content="Find information about AI trends",
    parameters={"depth": "comprehensive"}
)
```

## Testing Utilities

```python
from shared.testing import MockAPIClient, temporary_file

# Mock API responses for testing
with MockAPIClient() as mock:
    mock.add_response("GET", "/api/data", {"result": "test"})
    # Run your tests

# Temporary file handling
with temporary_file(".txt") as temp_path:
    # Use temp file in tests
    pass
```