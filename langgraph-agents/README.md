# LangGraph Agents

LangGraph-based agent implementations for complex multi-step workflows.

## Agents Included

- **Research Agent**: Web research with source verification
- **Code Analysis Agent**: Code review and documentation
- **Data Processing Agent**: ETL workflows with validation
- **Multi-Agent Orchestrator**: Coordinate multiple specialized agents

## Key Features

- State management with LangGraph
- Tool calling and function execution
- Human-in-the-loop workflows  
- Persistent conversation memory
- Error handling and retry logic
- Integration with LangSmith for tracing

## Installation

```bash
# From root directory
pip install -e .[langgraph-agents]

# Or install individually
cd langgraph-agents && pip install -e .
```

## Configuration

Set up your API keys:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_TRACING=true
TAVILY_API_KEY=your_tavily_key
```

## Quick Start

```python
from langgraph_agents.research_agent import ResearchAgent
from langgraph_agents.orchestrator import MultiAgentOrchestrator

# Single agent
agent = ResearchAgent()
result = agent.research_topic("AI safety research trends 2024")

# Multi-agent workflow
orchestrator = MultiAgentOrchestrator()
orchestrator.add_agent("researcher", ResearchAgent())
orchestrator.add_agent("analyst", CodeAnalysisAgent())

workflow = orchestrator.create_workflow([
    "researcher.gather_info",
    "analyst.analyze_findings"
])
```

## Agent Architecture

Each agent follows the pattern:
1. **State Definition**: Pydantic models for state management
2. **Tool Registration**: Available functions and APIs
3. **Workflow Graph**: Node and edge definitions
4. **Execution Engine**: LangGraph compilation and running

## Notebooks

See `notebooks/` for examples:
- `research_agent_demo.ipynb`
- `multi_agent_workflow.ipynb`
- `custom_agent_creation.ipynb`