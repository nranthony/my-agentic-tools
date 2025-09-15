# Y Combinator Job Board Scraper

A comprehensive, modular scraper for Y Combinator's "Work at a Startup" job board using Firecrawl, Gemini AI, and cookie-based authentication.

## Features

- **Modular Architecture**: Easy to swap components (AI models, scraping backends)
- **Infinite Scroll Support**: Handles dynamic content loading with intelligent pagination
- **AI-Powered Extraction**: Uses Gemini AI for structured data extraction
- **Cookie Authentication**: Access authenticated content with session cookies  
- **Data Cleaning**: Automatic deduplication and normalization
- **Multiple Export Formats**: JSON, CSV export with metadata
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Type Safety**: Full Pydantic models with validation

## Quick Start

### 1. Setup Environment

```bash
# Create .env file with your API keys
cp .env.example .env

# Edit .env with your keys:
# GEMINI_API_KEY=your_gemini_key
# FIRECRAWL_API_KEY=your_firecrawl_key
# YC_SESSION_COOKIE=your_session_cookie  # Optional but recommended
```

### 2. Basic Usage

```python
from yc_scraper import YCJobScraper, SearchParams
from yc_scraper.models.search_params import Role, JobType

# Initialize scraper
scraper = YCJobScraper()

# Create search parameters
search_params = SearchParams(
    role=Role.ENGINEERING,
    job_type=JobType.FULLTIME
)

# Scrape companies and jobs
companies, jobs = scraper.scrape_search(
    search_params=search_params,
    max_companies=50,
    include_jobs=True
)

# Export results
scraper.export_results(companies, jobs, format="json")
```

### 3. Scrape from URL

```python
# Scrape directly from Y Combinator URL
url = "https://www.workatastartup.com/companies?role=science&jobType=fulltime"
companies, jobs = scraper.scrape_from_url(url, max_companies=20)
```

## Architecture

```
yc_scraper/
├── core/           # Main orchestration
│   ├── scraper.py      # YCJobScraper main class
│   ├── auth_handler.py # Cookie/session management
│   └── url_builder.py  # URL parameter handling
├── clients/        # External API clients
│   ├── firecrawl_client.py  # Firecrawl API wrapper
│   └── gemini_client.py     # Gemini AI client
├── extractors/     # Data extraction logic
│   ├── company_extractor.py  # Company data parsing
│   ├── job_extractor.py      # Job data parsing
│   └── pagination_handler.py # Infinite scroll handling
├── models/         # Data models
│   ├── company.py     # Company data model
│   ├── job.py         # Job data model
│   └── search_params.py # Search parameters
└── utils/          # Utilities
    ├── data_cleaner.py  # Data cleaning/deduplication
    └── exporters.py     # Export to various formats
```

## Key Components

### Authentication

The scraper supports cookie-based authentication for accessing more comprehensive data:

```python
# Get your session cookie from browser dev tools
scraper.set_session_cookie("your_session_cookie_here")

# Check authentication status
if scraper.is_authenticated():
    print("Ready to access authenticated content")
else:
    print("Using public access only")
    print(scraper.get_auth_instructions())
```

### Search Parameters

Flexible search configuration:

```python
from yc_scraper.models.search_params import *

params = SearchParams(
    role=Role.PRODUCT,              # Product roles
    job_type=JobType.FULLTIME,      # Full-time only
    sort_by=SortBy.CREATED_DESC,    # Newest first
    location="San Francisco",       # Location filter
    has_equity=YesNoAny.YES        # Must offer equity
)
```

### Data Models

Type-safe data models with validation:

```python
# Company model
company = Company(
    name="Acme Corp",
    description="Building the future",
    url="https://acme.com",
    job_count=15,
    industry="AI/ML",
    location="San Francisco",
    batch="S23"
)

# Job model  
job = Job(
    title="Senior Engineer",
    company_name="Acme Corp",
    location="SF/Remote",
    salary_min=150000,
    salary_max=200000,
    equity_min=0.1,
    equity_max=0.5,
    skills_required=["Python", "React", "AWS"]
)
```

### Infinite Scroll Handling

Intelligent pagination for complete data collection:

```python
# The scraper automatically handles infinite scroll
companies, jobs = scraper.scrape_search(
    search_params,
    max_scrolls=20,          # Maximum scroll attempts
    include_jobs=True        # Get detailed job info
)
```

## Advanced Usage

### Custom Export Options

```python
# Export to different formats
files = scraper.export_results(
    companies, jobs,
    format="csv",           # or "json"
    filename="my_scrape"    # Custom filename
)

print(f"Exported to: {files}")
# Output: {'companies': 'path/to/companies.csv', 'jobs': 'path/to/jobs.csv'}
```

### Company-Specific Scraping

```python
# Scrape specific company by slug
company, jobs = scraper.scrape_company("openai")

print(f"Found {len(jobs)} jobs at {company.name}")
```

### Data Cleaning

```python
from yc_scraper.utils.data_cleaner import DataCleaner

# Clean and deduplicate data
clean_companies = DataCleaner.clean_companies(raw_companies)
clean_jobs = DataCleaner.clean_jobs(raw_jobs)
```

## Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key

# Optional Authentication
YC_SESSION_COOKIE=your_session_cookie

# Optional Configuration
SCRAPE_DELAY=1.0          # Delay between requests
MAX_RETRIES=3             # Retry attempts
REQUEST_TIMEOUT=30        # Request timeout
OUTPUT_FORMAT=json        # Default export format
OUTPUT_DIR=./output       # Export directory
LOG_LEVEL=INFO           # Logging level
```

### Getting Session Cookie

1. Open browser and go to https://www.workatastartup.com/
2. Log in to your Y Combinator account  
3. Open Developer Tools (F12)
4. Go to Application/Storage → Cookies → workatastartup.com
5. Find cookie like `_yc_session` or `waas_session`
6. Copy the value and set as `YC_SESSION_COOKIE`

## Error Handling

The scraper includes comprehensive error handling:

```python
import logging

# Enable detailed logging
logging.basicConfig(level=logging.INFO)

try:
    companies, jobs = scraper.scrape_search(params)
except Exception as e:
    logger.error(f"Scraping failed: {e}")
    # Scraper will attempt retries and graceful degradation
```

## Limitations & Considerations

- **Rate Limiting**: Built-in delays and retry logic
- **Content Changes**: Y Combinator may update their site structure
- **Authentication**: Session cookies expire and need periodic renewal
- **API Costs**: Firecrawl and Gemini API calls incur costs
- **Legal**: Respect robots.txt and terms of service

## Testing

```bash
# Run tests
python -m pytest web-scraping/tests/test_yc_scraper.py -v

# Test with coverage
python -m pytest web-scraping/tests/ --cov=yc_scraper --cov-report=html
```

## Example Output

### Companies Data
```json
{
  "export_info": {
    "timestamp": "2024-01-15T10:30:00",
    "total_companies": 25,
    "source": "Y Combinator Job Board"
  },
  "companies": [
    {
      "name": "Acme AI",
      "description": "Building AI for everyone",
      "url": "https://acme-ai.com",
      "yc_profile_url": "https://workatastartup.com/companies/acme-ai",
      "job_count": 8,
      "industry": "Artificial Intelligence",
      "location": "San Francisco, CA",
      "batch": "S23",
      "tags": ["AI", "B2B", "SaaS"]
    }
  ]
}
```

### Jobs Data
```json
{
  "jobs": [
    {
      "title": "Senior Software Engineer",
      "company_name": "Acme AI",
      "location": "San Francisco / Remote",
      "remote_ok": true,
      "salary_min": 160000,
      "salary_max": 220000,
      "salary_currency": "USD",
      "equity_min": 0.1,
      "equity_max": 0.5,
      "job_type": "Full-time",
      "department": "Engineering",
      "skills_required": ["Python", "React", "AWS", "Machine Learning"],
      "application_url": "https://jobs.acme-ai.com/senior-engineer"
    }
  ]
}
```

## Contributing

The modular architecture makes it easy to extend:

- **New AI Models**: Implement new clients in `clients/`
- **Additional Scrapers**: Add extractors in `extractors/`  
- **Export Formats**: Extend `utils/exporters.py`
- **Data Models**: Add fields to models in `models/`

## License

MIT License - see LICENSE file for details.