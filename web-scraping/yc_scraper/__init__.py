"""Y Combinator Job Board Scraper

A modular scraper for Y Combinator's "Work at a Startup" job board
using Firecrawl, Gemini AI, and cookie-based authentication.
"""

from .core.scraper import YCJobScraper
from .models.company import Company
from .models.job import Job
from .models.search_params import SearchParams

__version__ = "0.1.0"
__all__ = ["YCJobScraper", "Company", "Job", "SearchParams"]