"""Shared Utilities

Common utilities, base classes, logging, config, and testing infrastructure
used across all projects in the mygentic package.
"""

from .base.agent import BaseAgent
from .config.settings import Settings, settings
from .logging.logger import get_logger

__version__ = "0.1.0"
__all__ = [
    "BaseAgent",
    "Settings", 
    "settings",
    "get_logger"
]