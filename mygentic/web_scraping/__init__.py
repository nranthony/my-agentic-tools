"""Web Scraping Tools

A collection of web scraping tools including Y Combinator job board scraper,
using Firecrawl, Gemini AI, and various extraction utilities.
"""

# Core scraping functionality
from .yc_scraper.core.scraper import YCJobScraper
from .yc_scraper.models.company import Company
from .yc_scraper.models.job import Job
from .yc_scraper.models.search_params import SearchParams

# Import submodules for namespace access
from . import yc_scraper
from . import examples
from . import tests

__version__ = "0.1.0"
__all__ = [
    # Main exports
    "YCJobScraper", 
    "Company", 
    "Job", 
    "SearchParams",
    
    # Submodules
    "yc_scraper",
    "examples",
    "tests",
]