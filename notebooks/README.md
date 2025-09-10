# Notebooks

Jupyter notebooks for experimentation, demos, and tutorials with agentic tools.

## Organization

### Tutorials  
- `01_getting_started.ipynb` - Basic setup and first examples
- `02_web_scraping_intro.ipynb` - Web scraping fundamentals  
- `03_langgraph_basics.ipynb` - Building your first LangGraph agent
- `04_crewai_workflows.ipynb` - Multi-agent collaboration
- `05_document_generation.ipynb` - Creating professional documents

### Demos
- `research_agent_demo.ipynb` - Comprehensive research workflow
- `content_pipeline_demo.ipynb` - End-to-end content creation
- `api_integration_showcase.ipynb` - Working with multiple APIs
- `mcp_tools_demo.ipynb` - Custom MCP server implementation

### Experiments
- `agent_performance_comparison.ipynb` - Benchmarking different agents
- `prompt_engineering_lab.ipynb` - Optimizing prompts for tasks
- `multi_modal_experiments.ipynb` - Working with text, images, and code
- `scaling_workflows.ipynb` - Handling large-scale operations

## Setup

Install Jupyter and required extensions:

```bash
# From root directory
pip install jupyter jupyterlab
pip install -e .[dev]

# Launch Jupyter Lab
jupyter lab
```

## Features

- Interactive code examples
- Rich visualizations with matplotlib/plotly
- Integration with all project modules
- Export capabilities (HTML, PDF, slides)
- Version control friendly (using nbstripout)

## Best Practices

1. **Clear Documentation**: Each notebook includes markdown explanations
2. **Modular Code**: Reusable functions extracted to project modules  
3. **Environment Setup**: Each notebook handles its own dependencies
4. **Data Management**: Sample data included in `data/` subdirectory
5. **Output Management**: Results saved to `outputs/` with timestamps

## Data Directory

Sample datasets for experiments:
- `sample_websites.json` - URLs for scraping practice
- `research_topics.csv` - Topics for agent testing  
- `document_templates/` - LaTeX and Word templates
- `api_responses/` - Cached API responses for offline work