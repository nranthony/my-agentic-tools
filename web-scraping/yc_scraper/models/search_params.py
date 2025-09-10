"""Search parameters model for Y Combinator job board."""

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class JobType(str, Enum):
    """Job type options."""
    FULLTIME = "fulltime"
    PARTTIME = "parttime"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    ANY = "any"


class Role(str, Enum):
    """Role type options."""
    ENGINEERING = "engineering"
    DESIGN = "design"
    PRODUCT = "product"
    SALES = "sales"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    FINANCE = "finance"
    LEGAL = "legal"
    SCIENCE = "science"
    ANY = "any"


class SortBy(str, Enum):
    """Sorting options."""
    CREATED_DESC = "created_desc"
    CREATED_ASC = "created_asc"
    COMPANY_NAME = "company_name"
    INDUSTRY = "industry"


class Layout(str, Enum):
    """Layout options."""
    LIST_COMPACT = "list-compact"
    LIST_DETAILED = "list-detailed"
    GRID = "grid"


class YesNoAny(str, Enum):
    """Yes/No/Any options."""
    YES = "yes"
    NO = "no"
    ANY = "any"


class SearchParams(BaseModel):
    """Y Combinator job board search parameters."""
    
    demographic: YesNoAny = Field(default=YesNoAny.ANY, description="Demographic filter")
    has_equity: YesNoAny = Field(default=YesNoAny.ANY, description="Equity availability")
    has_salary: YesNoAny = Field(default=YesNoAny.ANY, description="Salary availability") 
    industry: str = Field(default="any", description="Industry filter")
    interview_process: str = Field(default="any", description="Interview process type")
    job_type: JobType = Field(default=JobType.FULLTIME, description="Type of job")
    layout: Layout = Field(default=Layout.LIST_COMPACT, description="Display layout")
    role: Role = Field(default=Role.ANY, description="Job role category")
    sort_by: SortBy = Field(default=SortBy.CREATED_DESC, description="Sort order")
    tab: str = Field(default="any", description="Tab filter")
    us_visa_not_required: YesNoAny = Field(default=YesNoAny.ANY, description="US visa requirement")
    
    # Additional filters
    location: Optional[str] = Field(default=None, description="Location filter")
    company_size: Optional[str] = Field(default=None, description="Company size filter")
    
    def to_url_params(self) -> dict:
        """Convert to URL parameters dictionary."""
        params = {
            "demographic": self.demographic.value,
            "hasEquity": self.has_equity.value,
            "hasSalary": self.has_salary.value,
            "industry": self.industry,
            "interviewProcess": self.interview_process,
            "jobType": self.job_type.value,
            "layout": self.layout.value,
            "role": self.role.value,
            "sortBy": self.sort_by.value,
            "tab": self.tab,
            "usVisaNotRequired": self.us_visa_not_required.value,
        }
        
        # Add optional parameters if set
        if self.location:
            params["location"] = self.location
        if self.company_size:
            params["companySize"] = self.company_size
            
        return params
    
    @classmethod
    def from_url(cls, url: str) -> "SearchParams":
        """Create SearchParams from Y Combinator job board URL."""
        from urllib.parse import urlparse, parse_qs
        
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        # Extract parameters with defaults
        params = {}
        if "demographic" in query_params:
            params["demographic"] = query_params["demographic"][0]
        if "hasEquity" in query_params:
            params["has_equity"] = query_params["hasEquity"][0]
        if "hasSalary" in query_params:
            params["has_salary"] = query_params["hasSalary"][0]
        if "industry" in query_params:
            params["industry"] = query_params["industry"][0]
        if "interviewProcess" in query_params:
            params["interview_process"] = query_params["interviewProcess"][0]
        if "jobType" in query_params:
            params["job_type"] = query_params["jobType"][0]
        if "layout" in query_params:
            params["layout"] = query_params["layout"][0]
        if "role" in query_params:
            params["role"] = query_params["role"][0]
        if "sortBy" in query_params:
            params["sort_by"] = query_params["sortBy"][0]
        if "tab" in query_params:
            params["tab"] = query_params["tab"][0]
        if "usVisaNotRequired" in query_params:
            params["us_visa_not_required"] = query_params["usVisaNotRequired"][0]
        if "location" in query_params:
            params["location"] = query_params["location"][0]
        if "companySize" in query_params:
            params["company_size"] = query_params["companySize"][0]
        
        return cls(**params)