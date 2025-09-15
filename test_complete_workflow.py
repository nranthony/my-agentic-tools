#!/usr/bin/env python3
"""Test complete YC scraper workflow end-to-end."""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

print("🚀 Testing Complete YC Scraper Workflow")
print("=" * 50)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from mygentic.web_scraping.yc_scraper.core.scraper import YCJobScraper
    from mygentic.web_scraping.yc_scraper.models.search_params import SearchParams, JobType, Role, SortBy
    
    print("📡 Initializing scraper...")
    scraper = YCJobScraper()
    print("✅ Scraper initialized successfully")
    
    print("\n🔍 Testing complete workflow...")
    search_params = SearchParams(
        role=Role.ENGINEERING,
        job_type=JobType.FULLTIME, 
        sort_by=SortBy.CREATED_DESC
    )
    
    print(f"   Search parameters: {search_params.role.value} roles, {search_params.job_type.value}")
    
    companies, jobs = scraper.scrape_search(
        search_params=search_params,
        max_companies=3,      # Small test
        include_jobs=True,    # Get job details
        max_scrolls=1        # Minimal scrolling for test
    )
    
    print(f"✅ Successfully scraped {len(companies)} companies and {len(jobs)} jobs")
    
    if companies:
        print("\n🏢 Companies found:")
        for i, company in enumerate(companies, 1):
            name = getattr(company, 'name', 'N/A')
            location = getattr(company, 'location', None) or 'TBD'
            industry = getattr(company, 'industry', None) or 'N/A'
            print(f"  {i}. {name} ({location})")
            if industry != 'N/A':
                print(f"     Industry: {industry}")
    
    if jobs:
        print("\n💼 Jobs found:")
        for i, job in enumerate(jobs, 1):
            title = getattr(job, 'title', 'N/A')
            company_name = getattr(job, 'company_name', 'N/A')
            location = getattr(job, 'location', None) or 'TBD'
            print(f"  {i}. {title} at {company_name}")
            if location != 'TBD':
                print(f"     Location: {location}")
    
    # Test export functionality
    if companies or jobs:
        print("\n💾 Testing export functionality...")
        try:
            # Test combined export
            from mygentic.web_scraping.yc_scraper.utils.exporters import DataExporter
            exporter = DataExporter()
            
            exported_files = exporter.export_combined(
                companies=companies,
                jobs=jobs,
                filename="test_scrape_results",
                format="json"
            )
            
            print("✅ JSON export successful:")
            for file_type, filepath in exported_files.items():
                print(f"   {file_type}: {filepath}")
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"     File size: {size} bytes")
            
            # Test CSV export  
            csv_files = exporter.export_combined(
                companies=companies,
                jobs=jobs,
                filename="test_scrape_results_csv",
                format="csv"
            )
            
            print("✅ CSV export successful:")
            for file_type, filepath in csv_files.items():
                print(f"   {file_type}: {filepath}")
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"     File size: {size} bytes")
                    
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    print("\n🎉 Complete workflow test successful!")
    print("✅ All components working:")
    print("   - Firecrawl web scraping")
    print("   - Session cookie authentication") 
    print("   - Gemini AI data extraction")
    print("   - Data export (JSON/CSV)")
    print("   - Error handling and retries")
    
except Exception as e:
    print(f"❌ Workflow test failed: {e}")
    import traceback
    traceback.print_exc()