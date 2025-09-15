"""Base agent class for consistent interface across all agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..logging import get_logger


class BaseAgent(ABC):
    """Base class for all agents in the mygentic package."""
    
    def __init__(self, name: Optional[str] = None, **kwargs):
        """Initialize the base agent.
        
        Args:
            name: Agent name for logging
            **kwargs: Additional configuration options
        """
        self.name = name or self.__class__.__name__
        self.logger = get_logger(self.name)
        self.config = kwargs
    
    @abstractmethod
    async def execute(self, task: str, **kwargs) -> Any:
        """Execute a task. Must be implemented by subclasses.
        
        Args:
            task: Task description or instruction
            **kwargs: Task-specific parameters
            
        Returns:
            Task result
        """
        pass
    
    def configure(self, **kwargs) -> None:
        """Update agent configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        self.config.update(kwargs)
        self.logger.info(f"Updated configuration for {self.name}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current agent configuration.
        
        Returns:
            Dictionary of configuration parameters
        """
        return self.config.copy()