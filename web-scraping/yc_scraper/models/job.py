"""Job data model."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Job(BaseModel):
    """Y Combinator job posting data model."""
    
    title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Company name")
    description: Optional[str] = Field(None, description="Job description")
    
    # Location and work arrangement
    location: Optional[str] = Field(None, description="Job location")
    remote_ok: bool = Field(default=False, description="Remote work allowed")
    location_type: Optional[str] = Field(None, description="On-site/Remote/Hybrid")
    
    # Compensation
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")
    salary_currency: Optional[str] = Field(None, description="Salary currency (USD, EUR, etc.)")
    equity_min: Optional[float] = Field(None, description="Minimum equity percentage")
    equity_max: Optional[float] = Field(None, description="Maximum equity percentage")
    
    # Job details  
    job_type: Optional[str] = Field(None, description="Full-time/Part-time/Contract/Internship")
    experience_level: Optional[str] = Field(None, description="Junior/Senior/Lead/etc.")
    department: Optional[str] = Field(None, description="Engineering/Product/Marketing/etc.")
    
    # Requirements
    skills_required: List[str] = Field(default_factory=list, description="Required skills")
    education_required: Optional[str] = Field(None, description="Education requirements")
    years_experience: Optional[int] = Field(None, description="Years of experience required")
    
    # Application details
    application_url: Optional[str] = Field(None, description="Application URL")
    application_email: Optional[str] = Field(None, description="Application email")
    posted_date: Optional[datetime] = Field(None, description="Job posting date")
    
    # Company info (denormalized for convenience)
    company_url: Optional[str] = Field(None, description="Company website")
    company_description: Optional[str] = Field(None, description="Company description")
    company_industry: Optional[str] = Field(None, description="Company industry")
    company_size: Optional[str] = Field(None, description="Company team size")
    
    # Visa requirements
    visa_sponsorship: bool = Field(default=False, description="Visa sponsorship available")
    
    class Config:
        """Pydantic config."""
        str_strip_whitespace = True
        validate_assignment = True