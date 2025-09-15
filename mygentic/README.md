# MyGentic

A comprehensive toolkit for agentic AI systems including web scraping, document generation, API integrations, and workflow orchestration.

## Installation

```bash
cd mygentic && pip install -e .[web-scraping]
```

## Usage

```python
from mygentic.web_scraping import YCJobScraper

scraper = YCJobScraper()
companies, jobs = scraper.scrape_search()
```