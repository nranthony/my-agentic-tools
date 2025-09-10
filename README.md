# My Agentic Tools

A comprehensive collection of AI agents, tools, scripts, and notebooks for working with agentic systems including LangGraph, CrewAI, Firecrawl, MCPs, and various APIs.

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd my-agentic-tools
   python setup.py
   ```

2. **Activate environment and configure:**
   ```bash
   source .venv/bin/activate  # Linux/Mac
   # Edit .env file with your API keys
   ```

3. **Verify setup:**
   ```bash
   python scripts/env_checker.py
   ```

## 📁 Project Structure

This repository uses a **multi-project approach** with focused domains:

- **`web-scraping/`** - Firecrawl, BeautifulSoup, Selenium tools
- **`document-generation/`** - LaTeX, PDF generation tools
- **`langgraph-agents/`** - LangGraph-based agent implementations  
- **`crewai-workflows/`** - CrewAI team-based agent workflows
- **`mcp-tools/`** - Model Context Protocol tools and servers
- **`api-integrations/`** - Unified API wrappers for various services
- **`shared/`** - Common utilities and base classes
- **`notebooks/`** - Jupyter notebooks for experimentation
- **`scripts/`** - Standalone utility scripts

## 💻 Installation Options

### Install Everything
```bash
pip install -e .[all]
```

### Install Specific Projects
```bash
pip install -e .[web-scraping,document-generation]
```

### Install Individual Project
```bash
cd web-scraping && pip install -e .
```

## 🛠️ Development

### Code Quality
```bash
python scripts/lint_and_format.py          # Format and lint code
python scripts/lint_and_format.py --check  # Check without changes
```

### Testing
```bash
python -m pytest                           # Run all tests
python -m pytest web-scraping/tests/       # Test specific project
```

### Environment Check
```bash
python scripts/env_checker.py              # Validate setup and APIs
```

## 📊 Features

### Web Scraping
- Firecrawl integration for LLM-ready content
- Browser automation with Selenium/Playwright
- Rate limiting and proxy rotation
- Content extraction pipelines

### Document Generation
- LaTeX template system
- PDF creation with ReportLab
- HTML/CSS to PDF conversion
- Multi-format document export

### Agentic Workflows
- LangGraph state management
- CrewAI team collaboration
- Tool calling and function execution
- Human-in-the-loop workflows

### API Integrations
- OpenAI, Anthropic, Google APIs
- Social media integrations
- Productivity tool connections
- Unified client interfaces

## 🔑 Configuration

Key environment variables (see `.env` template):

```bash
# Core AI APIs
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
LANGSMITH_API_KEY=your_key_here

# Web Scraping
FIRECRAWL_API_KEY=your_key_here

# Productivity APIs
NOTION_API_KEY=your_key_here
SLACK_BOT_TOKEN=your_key_here
```

## 📚 Documentation

Each project folder contains detailed README with:
- Installation instructions
- Usage examples  
- Configuration options
- API documentation

## 🧪 Notebooks

Interactive examples in `notebooks/`:
- Getting started tutorials
- Agent demonstrations
- API integration showcases
- Performance comparisons

## 🤝 Contributing

1. Follow the established project structure
2. Run `python scripts/lint_and_format.py` before commits
3. Add tests for new functionality
4. Update relevant README files

## 📄 License

MIT License - see LICENSE file for details.
