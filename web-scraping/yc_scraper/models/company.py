"""Company data model."""

from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class Company(BaseModel):
    """Y Combinator company data model."""
    
    name: str = Field(..., description="Company name")
    description: Optional[str] = Field(None, description="Company description/tagline")
    url: Optional[HttpUrl] = Field(None, description="Company website URL")
    yc_profile_url: Optional[str] = Field(None, description="Y Combinator profile URL")
    
    # Job-related info
    job_count: int = Field(default=0, description="Number of open jobs")
    jobs_url: Optional[str] = Field(None, description="'See all jobs' URL")
    
    # Company details
    industry: Optional[str] = Field(None, description="Company industry")
    location: Optional[str] = Field(None, description="Company location")
    team_size: Optional[str] = Field(None, description="Team size range")
    batch: Optional[str] = Field(None, description="Y Combinator batch (e.g., S21)")
    
    # Additional metadata
    logo_url: Optional[str] = Field(None, description="Company logo URL")
    founded_year: Optional[int] = Field(None, description="Year founded")
    tags: List[str] = Field(default_factory=list, description="Company tags/categories")
    
    class Config:
        """Pydantic config."""
        str_strip_whitespace = True
        validate_assignment = True