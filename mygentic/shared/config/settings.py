"""Centralized settings management with environment variables."""

import os
from pathlib import Path
from typing import Optional, Union
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Centralized configuration settings loaded from environment variables."""
    
    # Core AI APIs
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    google_api_key: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    
    # LangChain/LangSmith
    langsmith_api_key: Optional[str] = Field(None, env="LANGSMITH_API_KEY")
    langsmith_tracing: bool = Field(False, env="LANGSMITH_TRACING")
    
    # Web scraping
    firecrawl_api_key: Optional[str] = Field(None, env="FIRECRAWL_API_KEY")
    yc_session_cookie: Optional[str] = Field(None, env="YC_SESSION_COOKIE")
    
    # Search and data
    tavily_api_key: Optional[str] = Field(None, env="TAVILY_API_KEY")
    news_api_key: Optional[str] = Field(None, env="NEWS_API_KEY")
    
    # Scraping configuration
    scrape_delay: float = Field(1.0, env="SCRAPE_DELAY")
    max_retries: int = Field(3, env="MAX_RETRIES")
    request_timeout: int = Field(30, env="REQUEST_TIMEOUT")
    
    # Output settings
    output_dir: str = Field("output", env="OUTPUT_DIR")
    output_format: str = Field("json", env="OUTPUT_FORMAT")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"  # Allow extra fields
    
    def __init__(self, **kwargs):
        """Initialize settings and create output directory if needed."""
        super().__init__(**kwargs)
        
        # Create output directory if it doesn't exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.openai_api_key)
    
    @property
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is available."""
        return bool(self.anthropic_api_key)
    
    @property
    def has_gemini_key(self) -> bool:
        """Check if Gemini API key is available."""
        return bool(self.gemini_api_key or self.google_api_key)
    
    @property
    def has_firecrawl_key(self) -> bool:
        """Check if Firecrawl API key is available."""
        return bool(self.firecrawl_api_key)
    
    @property
    def effective_gemini_key(self) -> Optional[str]:
        """Get the effective Gemini API key (prefer GEMINI_API_KEY over GOOGLE_API_KEY)."""
        return self.gemini_api_key or self.google_api_key


# Global settings instance
settings = Settings()