# CrewAI Workflows  

Team-based AI agent workflows using CrewAI framework for collaborative task execution.

## Crews Included

- **Content Creation Crew**: Writer, Editor, Publisher agents
- **Research & Analysis Crew**: Researcher, Analyst, Reviewer
- **Software Development Crew**: Architect, Developer, Tester
- **Marketing Campaign Crew**: Strategist, Creator, Analyzer

## Key Features

- Multi-agent collaboration
- Role-based task assignment
- Hierarchical and sequential processes
- Memory and context sharing
- Quality control workflows
- Performance monitoring

## Installation

```bash
# From root directory  
pip install -e .[crewai-workflows]

# Or install individually
cd crewai-workflows && pip install -e .
```

## Configuration

Configure your LLM providers:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_MODEL_NAME=gpt-4-turbo-preview
ANTHROPIC_MODEL_NAME=claude-3-sonnet
```

## Quick Start

```python
from crewai_workflows.content_crew import ContentCreationCrew
from crewai_workflows.research_crew import ResearchCrew

# Content creation workflow
crew = ContentCreationCrew()
result = crew.create_article({
    "topic": "Future of AI in Healthcare",
    "target_audience": "Healthcare professionals",
    "word_count": 2000
})

# Research workflow
research_crew = ResearchCrew()
findings = research_crew.conduct_research({
    "topic": "Renewable energy trends",
    "depth": "comprehensive",
    "sources": ["academic", "industry", "news"]
})
```

## Crew Structure

Each crew contains:
- **Agents**: Specialized roles with specific skills
- **Tasks**: Discrete units of work with clear objectives  
- **Process**: Sequential, hierarchical, or custom workflow
- **Tools**: External APIs and utilities agents can use
- **Memory**: Shared context and knowledge base

## Custom Crews

Create your own crews by:
1. Defining agent roles and backstories
2. Creating task definitions with expected outputs
3. Configuring the process flow
4. Adding relevant tools and integrations

## Examples

See `examples/` directory:
- `blog_writing_crew.py`
- `market_research_crew.py`
- `code_review_crew.py`
- `custom_crew_template.py`