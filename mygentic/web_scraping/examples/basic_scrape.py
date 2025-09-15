#!/usr/bin/env python3
"""
Basic example of using the Y Combinator Job Board Scraper.

This example demonstrates:
1. Setting up the scraper with API keys
2. Creating search parameters
3. Scraping companies and jobs
4. Exporting results to files

Before running, make sure you have:
1. Set up your .env file with API keys (see .env.example)
2. Installed dependencies: pip install -e .
"""

import os
import sys
from pathlib import Path

# Import from the mygentic package
from mygentic.web_scraping import YCJobScraper, SearchParams
from mygentic.web_scraping.yc_scraper.models.search_params import JobType, Role, SortBy
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main example function."""
    print("🚀 Y Combinator Job Board Scraper Example")
    print("=" * 50)
    
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed. Make sure to set environment variables manually.")
    
    # Check for required API keys
    if not os.getenv("FIRECRAWL_API_KEY"):
        print("❌ FIRECRAWL_API_KEY not found in environment variables")
        print("   Please set it in your .env file or environment")
        return
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("   Please set it in your .env file or environment")
        return
    
    # Initialize the scraper
    print("\n📡 Initializing scraper...")
    try:
        scraper = YCJobScraper()
        print("✅ Scraper initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize scraper: {e}")
        return
    
    # Check authentication
    if scraper.is_authenticated():
        print("🔐 Authentication: Session cookie found")
    else:
        print("⚠️  Authentication: No session cookie found")
        print("   Public content only - some data may be limited")
        print("\n" + "=" * 60)
        print("📋 To get your session cookie:")
        print(scraper.get_auth_instructions())
        print("=" * 60)
    
    # Example 1: Scrape using SearchParams
    print("\n📋 Example 1: Scraping with SearchParams")
    print("-" * 40)
    
    # Create search parameters for science/data roles
    search_params = SearchParams(
        role=Role.SCIENCE,          # Science roles (data, ML, research)
        job_type=JobType.FULLTIME,  # Full-time positions
        sort_by=SortBy.CREATED_DESC # Newest first
    )
    
    print(f"Search parameters: {search_params.role.value} roles, {search_params.job_type.value}")
    
    try:
        # Scrape with pagination (limit to 10 companies for demo)
        print("🔍 Scraping companies and jobs...")
        companies, jobs = scraper.scrape_search(
            search_params=search_params,
            max_companies=10,        # Limit for demo
            include_jobs=True,       # Get job details too
            max_scrolls=5           # Limit scrolling for demo
        )
        
        print(f"✅ Found {len(companies)} companies and {len(jobs)} jobs")
        
        # Display some results
        if companies:
            print("\n🏢 Sample companies:")
            for i, company in enumerate(companies[:3], 1):
                print(f"  {i}. {company.name}")
                if company.description:
                    print(f"     Description: {company.description[:100]}...")
                if company.job_count:
                    print(f"     Jobs: {company.job_count}")
                print()
        
        if jobs:
            print("💼 Sample jobs:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"  {i}. {job.title} at {job.company_name}")
                if job.location:
                    print(f"     Location: {job.location}")
                if job.salary_min and job.salary_max:
                    print(f"     Salary: ${job.salary_min:,} - ${job.salary_max:,}")
                print()
        
        # Export results
        if companies or jobs:
            print("💾 Exporting results...")
            exported_files = scraper.export_results(
                companies=companies,
                jobs=jobs,
                format="json",
                filename="science_roles_demo"
            )
            
            for file_type, filepath in exported_files.items():
                print(f"   {file_type}: {filepath}")
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        logger.exception("Detailed error:")
    
    # Example 2: Scrape from URL
    print("\n📋 Example 2: Scraping from URL")
    print("-" * 40)
    
    # Example URL for engineering roles
    example_url = "https://www.workatastartup.com/companies?role=engineering&jobType=fulltime&sortBy=created_desc"
    print(f"URL: {example_url}")
    
    try:
        print("🔍 Scraping from URL...")
        companies, jobs = scraper.scrape_from_url(
            url=example_url,
            max_companies=5,        # Small limit for demo
            include_jobs=False,     # Just companies this time
            max_scrolls=3
        )
        
        print(f"✅ Found {len(companies)} companies")
        
        if companies:
            print("\n🏢 Engineering companies:")
            for i, company in enumerate(companies, 1):
                print(f"  {i}. {company.name} ({company.location or 'Location TBD'})")
                if company.industry:
                    print(f"     Industry: {company.industry}")
        
    except Exception as e:
        print(f"❌ URL scraping failed: {e}")
        logger.exception("Detailed error:")
    
    # Example 3: Scrape specific company
    print("\n📋 Example 3: Scraping specific company")
    print("-" * 40)
    
    try:
        # Note: Replace 'example-company' with an actual company slug
        # You can get company slugs from the search results above
        print("ℹ️  This example requires a specific company slug")
        print("   Company slugs can be found in the yc_profile_url of search results")
        print("   Format: https://www.workatastartup.com/companies/COMPANY_SLUG")
        
        # Uncomment and modify this to test with a real company:
        # company, jobs = scraper.scrape_company("openai")  # Example slug
        # print(f"Found company: {company.name if company else 'None'}")
        # print(f"Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"❌ Company scraping failed: {e}")
    
    print("\n✨ Examples completed!")
    print("💡 Tips:")
    print("   - Add your session cookie to access more data")
    print("   - Adjust max_companies and max_scrolls based on your needs")
    print("   - Check the output directory for exported files")
    print("   - Use different SearchParams to find specific roles/companies")


if __name__ == "__main__":
    main()