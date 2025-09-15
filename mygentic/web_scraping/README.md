# Web Scraping Tools

Collection of web scraping utilities using various frameworks and services.

## Tools Included

- **Firecrawl Integration**: Convert websites to LLM-ready markdown
- **BeautifulSoup**: HTML parsing and extraction
- **Selenium**: Browser automation for dynamic content
- **Scrapy**: High-performance web crawling framework
- **Playwright**: Modern browser automation

## Key Features

- Rate limiting and retry mechanisms
- Proxy rotation support
- Content extraction pipelines
- Data cleaning and normalization
- Export to multiple formats (JSON, CSV, markdown)

## Installation

```bash
# From root directory
pip install -e .[web-scraping]

# Or install individually
cd web-scraping && pip install -e .
```

## Quick Start

```python
from web_scraping.firecrawl_client import FirecrawlClient
from web_scraping.selenium_scraper import SeleniumScraper

# Firecrawl example
client = FirecrawlClient()
content = client.scrape_to_markdown("https://example.com")

# Selenium example  
scraper = SeleniumScraper()
data = scraper.extract_content("https://dynamic-site.com")
```

## Configuration

Set environment variables or create `.env` file:

```
FIRECRAWL_API_KEY=your_api_key_here
PROXY_LIST=proxy1:port,proxy2:port
USER_AGENT_LIST=agent1,agent2
```