#!/usr/bin/env python3
"""Test Gemini AI data extraction from YC content."""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

print("🧠 Testing Gemini AI Data Extraction")
print("=" * 40)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️  python-dotenv not available, using system env vars")

# Test 1: Initialize Gemini client
print("\n1. Testing Gemini client initialization...")
try:
    from mygentic.web_scraping.yc_scraper.clients.gemini_client import GeminiClient
    
    client = GeminiClient()
    print("✅ Gemini client initialized successfully")
    
    # Test 2: Simple extraction test with mock data
    print("\n2. Testing data extraction with sample content...")
    
    sample_markdown = """
    # Company: OpenAI
    
    **Industry:** Artificial Intelligence
    **Location:** San Francisco, CA
    **Employees:** 500+
    **Founded:** 2015
    
    OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence (AGI) benefits all of humanity.
    
    ## Open Positions:
    
    ### Senior Software Engineer - AI Safety
    - **Location:** San Francisco, CA / Remote
    - **Type:** Full-time
    - **Salary:** $200,000 - $300,000
    - **Experience:** 5+ years
    
    We're looking for experienced engineers to work on AI safety research and implementation.
    
    ### Machine Learning Research Scientist
    - **Location:** San Francisco, CA
    - **Type:** Full-time
    - **Salary:** $250,000 - $400,000
    - **Experience:** PhD preferred
    
    Join our research team working on cutting-edge ML models.
    """
    
    try:
        print("   Testing company extraction...")
        companies = client.extract_companies(sample_markdown, max_companies=5)
        
        if companies:
            print(f"✅ Successfully extracted {len(companies)} company")
            company = companies[0]
            print(f"   Name: {company.get('name', 'N/A')}")
            print(f"   Industry: {company.get('industry', 'N/A')}")
            print(f"   Location: {company.get('location', 'N/A')}")
            print(f"   Description length: {len(company.get('description', ''))}")
        else:
            print("❌ No companies extracted")
            
    except Exception as e:
        print(f"❌ Company extraction failed: {e}")
    
    try:
        print("\n   Testing job extraction...")
        jobs = client.extract_jobs(sample_markdown, "OpenAI")
        
        if jobs:
            print(f"✅ Successfully extracted {len(jobs)} jobs")
            for i, job in enumerate(jobs[:2], 1):  # Show first 2
                print(f"   Job {i}: {job.get('title', 'N/A')}")
                print(f"     Location: {job.get('location', 'N/A')}")
                print(f"     Type: {job.get('job_type', 'N/A')}")
                if job.get('salary_min') and job.get('salary_max'):
                    print(f"     Salary: ${job['salary_min']:,} - ${job['salary_max']:,}")
        else:
            print("❌ No jobs extracted")
            
    except Exception as e:
        print(f"❌ Job extraction failed: {e}")
    
    # Test 3: Full workflow with real scraped content
    print("\n3. Testing full workflow with scraped YC content...")
    try:
        from mygentic.web_scraping.yc_scraper.clients.firecrawl_client import FirecrawlClient
        
        # Get some real content
        firecrawl_client = FirecrawlClient()
        print("   Scraping YC companies page...")
        
        result = firecrawl_client.scrape_page("https://www.workatastartup.com/companies?role=engineering")
        
        if result and result.get('success'):
            markdown_content = result.get('markdown', '')
            print(f"   Got {len(markdown_content)} characters of content")
            
            # Extract companies
            print("   Extracting companies from real content...")
            companies = client.extract_companies(markdown_content, max_companies=5)
            
            if companies:
                print(f"✅ Extracted {len(companies)} companies from real data")
                
                # Show sample companies
                for i, company in enumerate(companies[:3], 1):
                    print(f"   Company {i}: {company.get('name', 'N/A')}")
                    if company.get('industry'):
                        print(f"     Industry: {company['industry']}")
                    if company.get('location'):
                        print(f"     Location: {company['location']}")
                    if company.get('description'):
                        print(f"     Description: {company['description'][:100]}...")
                    print()
            else:
                print("⚠️  No companies extracted from real content")
                print("   Content preview:")
                print(f"   {markdown_content[:300]}...")
        else:
            print("❌ Failed to scrape content for extraction test")
            
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")
        
except Exception as e:
    print(f"❌ Gemini client initialization failed: {e}")

print("\n✨ Gemini AI tests completed!")
print("\n💡 Next steps if working:")
print("   - Test full scraper workflow")
print("   - Export data to JSON/CSV")
print("   - Validate data quality and completeness")