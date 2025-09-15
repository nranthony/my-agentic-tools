#!/usr/bin/env python3
"""Simple test script for YC scraper functionality."""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

print("🚀 Testing Y Combinator Job Board Scraper")
print("=" * 50)

# Test 1: Basic imports
print("\n1. Testing imports...")
try:
    from mygentic.shared import get_logger, settings
    print("✅ Shared utilities imported successfully")
    
    from mygentic.web_scraping.yc_scraper.core.scraper import YCJobScraper
    from mygentic.web_scraping.yc_scraper.models.search_params import SearchParams
    print("✅ YC scraper imported successfully")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check logger setup
print("\n2. Testing logger...")
try:
    logger = get_logger("test_scraper")
    logger.info("Logger working correctly")
    print("✅ Loguru logger working")
except Exception as e:
    print(f"❌ Logger failed: {e}")

# Test 3: Check settings
print("\n3. Testing settings...")
try:
    print(f"   Firecrawl key available: {settings.has_firecrawl_key}")
    print(f"   Gemini key available: {settings.has_gemini_key}")
    print(f"   Output directory: {settings.output_dir}")
    print("✅ Settings working")
except Exception as e:
    print(f"❌ Settings failed: {e}")

# Test 4: Check scraper initialization
print("\n4. Testing scraper initialization...")
try:
    scraper = YCJobScraper()
    print("✅ Scraper initialized successfully")
    
    # Check if we have API keys
    if not settings.has_firecrawl_key:
        print("⚠️  FIRECRAWL_API_KEY not found - add to .env file")
    
    if not settings.has_gemini_key:
        print("⚠️  GEMINI_API_KEY not found - add to .env file")
    
    if settings.has_firecrawl_key and settings.has_gemini_key:
        print("✅ All required API keys found")
        
        # Test 5: Try a minimal scrape
        print("\n5. Testing basic functionality...")
        try:
            # Just test that we can create the search URL
            from mygentic.web_scraping.yc_scraper.models.search_params import JobType, Role, SortBy
            
            search_params = SearchParams(
                role=Role.ENGINEERING,
                job_type=JobType.FULLTIME,
                sort_by=SortBy.CREATED_DESC
            )
            
            search_url = scraper.url_builder.build_search_url(search_params)
            print(f"   Search URL: {search_url}")
            print("✅ URL building working")
            
            # Test authentication check
            is_authenticated = hasattr(scraper, 'is_authenticated') and callable(scraper.is_authenticated)
            print(f"   Authentication method available: {is_authenticated}")
            
        except Exception as e:
            print(f"❌ Basic functionality test failed: {e}")
    
    else:
        print("⚠️  Skipping API tests - missing keys")
        
except Exception as e:
    print(f"❌ Scraper initialization failed: {e}")

print("\n✨ Basic tests completed!")
print("\n💡 Next steps:")
print("   1. Add FIRECRAWL_API_KEY and GEMINI_API_KEY to .env file")
print("   2. Add YC_SESSION_COOKIE for premium content access (optional)")
print("   3. Run a real scraping test with API calls")