"""MyGentic: A comprehensive toolkit for agentic AI systems.

This package provides tools and utilities for building AI agents, web scraping,
document generation, API integrations, and workflow orchestration.
"""

# Import key classes from each submodule for convenient access
from . import web_scraping
from . import api_integrations  
from . import crewai_workflows
from . import langgraph_agents
from . import document_generation
from . import mcp_tools
from . import shared

# Version info
__version__ = "0.1.0"
__author__ = "Your Name"

# Main exports - users can import these directly from mygentic
try:
    # Web scraping tools
    from .web_scraping import YCJobScraper, Company, Job, SearchParams
    
    # Shared utilities
    from .shared import BaseAgent, get_logger, Settings
    
    __all__ = [
        # Submodules
        "web_scraping",
        "api_integrations", 
        "crewai_workflows",
        "langgraph_agents",
        "document_generation",
        "mcp_tools",
        "shared",
        
        # Key classes
        "YCJobScraper",
        "Company", 
        "Job",
        "SearchParams",
        "BaseAgent",
        "get_logger",
        "Settings",
    ]
    
except ImportError as e:
    # Graceful handling if some modules aren't available
    print(f"Warning: Some modules not available: {e}")
    __all__ = [
        "web_scraping",
        "api_integrations", 
        "crewai_workflows",
        "langgraph_agents", 
        "document_generation",
        "mcp_tools",
        "shared",
    ]