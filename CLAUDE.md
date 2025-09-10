# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup and Validation
```bash
python setup.py                      # Complete development environment setup
python scripts/env_checker.py        # Validate setup, packages, and API connections
source .venv/bin/activate            # Activate virtual environment (Linux/Mac)
```

### Code Quality and Linting
```bash
python scripts/lint_and_format.py          # Format and lint all code
python scripts/lint_and_format.py --check  # Check code quality without changes
python scripts/lint_and_format.py --skip-mypy  # Skip type checking
```

### Testing
```bash
python -m pytest                           # Run all tests
python -m pytest web-scraping/tests/       # Test specific project
python -m pytest -k "test_specific"        # Run specific test
python -m pytest --cov-report=html         # Generate HTML coverage report
```

### Installation Options
```bash
pip install -e .[all]                      # Install all projects
pip install -e .[web-scraping,langgraph-agents]  # Install specific projects
cd web-scraping && pip install -e .        # Install individual project
```

## Architecture Overview

This repository implements a **multi-project architecture** designed for working with agentic AI systems. Each domain is isolated but shares common infrastructure.

### Core Architecture Principles

1. **Domain Separation**: Each project folder (`web-scraping/`, `langgraph-agents/`, etc.) is self-contained with its own dependencies and concerns
2. **Shared Foundation**: The `shared/` project provides common utilities, base classes, and infrastructure used across all projects
3. **Flexible Installation**: Projects can be installed independently or together via optional dependencies in the root `pyproject.toml`

### Project Domains

- **`web-scraping/`**: Firecrawl, BeautifulSoup, Selenium tools for content extraction
- **`document-generation/`**: LaTeX, PDF, and multi-format document creation
- **`langgraph-agents/`**: LangGraph-based state management and agent workflows  
- **`crewai-workflows/`**: Multi-agent collaboration using CrewAI framework
- **`mcp-tools/`**: Model Context Protocol servers and client implementations
- **`api-integrations/`**: Unified wrappers for OpenAI, Anthropic, Google, and other APIs
- **`shared/`**: Common utilities, base classes, logging, config, and testing infrastructure

### Key Architectural Patterns

#### Base Class Inheritance
All agents inherit from `shared.base.agent.BaseAgent`:
```python
from shared.base.agent import BaseAgent

class CustomAgent(BaseAgent):
    async def execute(self, task: str) -> str:
        # Implementation follows common interface
```

#### Configuration Management
Centralized config via `shared.config.Settings`:
- Loads from `.env` files and environment variables
- Pydantic validation and type safety
- Shared across all projects

#### Logging Infrastructure  
Structured logging via `shared.logging.get_logger()`:
- Rich formatting with context
- Consistent across all projects
- Configurable levels and outputs

#### API Client Pattern
All API integrations follow `api_integrations.base.BaseAPIClient`:
- Retry logic with exponential backoff
- Rate limiting and quota management
- Consistent error handling

### Cross-Project Dependencies

Projects can import from each other using absolute imports:
```python
from shared.models import TaskRequest, TaskResponse
from api_integrations.openai_client import OpenAIClient
from web_scraping.firecrawl_client import FirecrawlClient
```

### Testing Architecture

- **Per-project tests**: Each project has its own `tests/` directory
- **Shared test utilities**: Common fixtures and mocks in `shared.testing`
- **Integration tests**: Cross-project functionality testing
- **Configuration**: Unified pytest config in root `pyproject.toml`

## Key Environment Variables

Essential configuration (create `.env` file):
```bash
# Core AI APIs (required for most functionality)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# LangChain/LangSmith (for agent workflows)
LANGSMITH_API_KEY=your_key_here
LANGSMITH_TRACING=true

# Web scraping
FIRECRAWL_API_KEY=your_key_here

# Search and data
TAVILY_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

## Development Workflow

1. **New Features**: Determine appropriate project domain, create in that folder
2. **Cross-project Utilities**: Add to `shared/` if used by multiple projects
3. **API Integrations**: Add new clients to `api-integrations/`
4. **Code Quality**: Always run `python scripts/lint_and_format.py` before commits
5. **Testing**: Add tests in relevant `tests/` directory, run full suite

## Project-Specific Notes

- **Document Generation**: Requires LaTeX installation for PDF compilation
- **Web Scraping**: May need ChromeDriver/GeckoDriver for Selenium
- **CrewAI**: Requires Python 3.10+ (higher than project minimum)
- **Jupyter Notebooks**: Located in `notebooks/` with sample data in `notebooks/data/`

## Project Tracking

This section serves as a lightweight project management system using Markdown. Keep it updated to track your progress and maintain a record of completed work.

### 🟢 Feature Development

**To Do:** Backlog. Add new tasks here.  
**In Progress:** Tasks you are currently working on. Move from To Do.  
**Completed:** Finished tasks. Move from In Progress.

#### Completed
* [x] Y Combinator Job Board Scraper - Complete modular architecture with Firecrawl + Gemini AI
* [x] Infinite scroll pagination handling for dynamic content loading
* [x] Cookie-based authentication for premium YC content access
* [x] Structured data extraction with Pydantic models (Company, Job, SearchParams)
* [x] Multi-format export (JSON, CSV) with automatic deduplication and cleaning
* [x] Comprehensive test suite and documentation

#### In Progress
* [ ] 

#### To Do
* [ ] Test YCJobScraper() with real API keys and validate data extraction
* [ ] Create daily auto-trigger system for automated job scraping
* [ ] Plan output integration - Google Sheets, Database, Notion, Streamlit webapp? 

### 🔵 Project Log

**Daily Entries:** Record completed work each day under a `YYYY-MM-DD` heading.  
**Notes:** Not for future tasks. Just an archive of what's done.

#### 2025-09-10
* [x] Built complete Y Combinator Job Board Scraper with modular architecture
* [x] Implemented Firecrawl client with intelligent infinite scroll handling
* [x] Created Gemini AI integration for structured data extraction from messy HTML
* [x] Added cookie-based authentication system for YC premium content access
* [x] Built comprehensive data models (Company, Job, SearchParams) with Pydantic validation
* [x] Implemented data cleaning, deduplication, and multi-format export (JSON/CSV)
* [x] Created complete test suite and documentation with usage examples
* [x] Set up project structure: 13 modules across core/, clients/, extractors/, models/, utils/

#### 2025-09-09
* [x] Added project tracking system to CLAUDE.md
* [x] Integrated feature development workflow tracking
* [x] Established project log structure

### Usage Tips
- Move tasks between sections as they progress
- Date your daily entries for easy reference
- Keep the Project Log as a record, don't delete old entries
- Use checkboxes `[ ]` for pending tasks and `[x]` for completed ones