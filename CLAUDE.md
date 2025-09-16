# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

This project uses conda for environment management with automatic pip installation. The setup script handles the complete environment creation and project installation:

```bash
# Complete setup (creates conda env + installs project)
./setup_conda_env.sh

# Update existing environment (preserves env, uses --prune)
./setup_conda_env.sh --update

# Manual activation if needed
conda activate mygentic
```

The script:

- Creates conda environment from `environment.yml` (Python 3.12)
- Automatically installs the project in development mode via `pip install -e ./mygentic`
- Uses `pyproject.toml` for package configuration

## Core Architecture

**MyGentic** is a modular agentic AI toolkit organized into specialized domains:

- `mygentic/web_scraping/` - Web scraping tools, primarily YC job board scraper
- `mygentic/api_integrations/` - External API clients and integrations
- `mygentic/crewai_workflows/` - CrewAI-based multi-agent workflows
- `mygentic/langgraph_agents/` - LangGraph-based agent implementations
- `mygentic/document_generation/` - Document creation and formatting
- `mygentic/mcp_tools/` - MCP (Model Control Protocol) tools
- `mygentic/shared/` - Common utilities, logging, and configuration

### Key Components

**Web Scraping Architecture** (primary focus):

- `YCJobScraper` in `mygentic/web_scraping/yc_scraper/core/scraper.py` - Main orchestrator
- Uses Firecrawl for web scraping and Gemini for content extraction
- Modular extractors: `CompanyExtractor`, `JobExtractor`, `PaginationHandler`
- Data models: `Company`, `Job`, `SearchParams` with Pydantic validation
- Authentication via `AuthHandler` with session cookies

**Shared Infrastructure**:

- Centralized logging via loguru in `mygentic/shared/logging/logger.py`
- Configuration management in `mygentic/shared/config/settings.py` with pydantic-settings
- Base agent classes in `mygentic/shared/base/`

## Development Commands

### Testing

```bash
# Run tests with pytest
python -m pytest mygentic/web_scraping/tests/ -v

# Run individual test files
python test_scraper.py
python test_firecrawl_access.py
python test_gemini_extraction.py
```

### Environment Variables

Set required API keys in `.env`:

```bash
FIRECRAWL_API_KEY=your_key
GEMINI_API_KEY=your_key
YC_SESSION_COOKIE=your_cookie
```

### Package Installation

The project uses pyproject.toml and is auto-installed by the setup script:

```bash
# Manual installation if needed
pip install -e .
```

## Important Patterns

- **Always use loguru for logging** - Import from `mygentic.shared.logging.logger`
- **Environment-based configuration** - Use `mygentic.shared.config.settings` for API keys and settings
- **Pydantic models** - All data structures use Pydantic for validation and serialization
- **Modular extractors** - Web scraping uses specialized extractor classes for different data types
- **Client abstractions** - External services wrapped in dedicated client classes

## Project Structure Notes

- Each domain has its own README with specific documentation
- Examples and notebooks in `mygentic/web_scraping/examples/` and `notebooks/`
- Test files follow `test_*.py` naming convention
- Uses conda for dependencies (environment.yml) and pip for project installation (pyproject.toml)
