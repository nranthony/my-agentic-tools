# Scripts

Standalone utility scripts and command-line tools for common tasks.

## Available Scripts

### Setup and Development
- `setup.py` - Initialize development environment
- `install_all.py` - Install all projects and dependencies
- `run_tests.py` - Execute test suites across all projects
- `lint_and_format.py` - Code quality checks and formatting

### Data Processing  
- `batch_scraper.py` - Bulk web scraping operations
- `document_converter.py` - Convert between document formats
- `api_data_sync.py` - Synchronize data across different APIs
- `cleanup_outputs.py` - Clean up generated files and artifacts

### Agent Management
- `agent_benchmark.py` - Performance testing for agents
- `workflow_validator.py` - Validate agent workflow configurations
- `memory_manager.py` - Manage agent memory and context

### Utilities
- `env_checker.py` - Validate environment setup and API keys
- `backup_configs.py` - Backup configuration files
- `monitor_usage.py` - Track API usage and costs

## Usage

All scripts are executable from the command line:

```bash
# From root directory
python scripts/setup.py
python scripts/batch_scraper.py --config scraping_config.yaml
python scripts/agent_benchmark.py --agent research --iterations 10
```

## Configuration

Scripts use configuration files from `config/`:
- `default.yaml` - Default settings for all scripts
- `scraping.yaml` - Web scraping configurations  
- `agents.yaml` - Agent-specific settings
- `apis.yaml` - API endpoints and credentials

## Creating New Scripts

Follow the template in `script_template.py`:

```python
#!/usr/bin/env python3
"""
Script description here.
"""
import argparse
from pathlib import Path
from shared.config import Settings
from shared.logging import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--input", required=True, help="Input parameter")
    args = parser.parse_args()
    
    # Implementation here
    logger.info(f"Processing {args.input}")

if __name__ == "__main__":
    main()
```

## Automation

Scripts can be run via cron jobs or task schedulers:
- `crontab_examples.txt` - Example cron configurations
- `systemd_services/` - Systemd service files for long-running scripts