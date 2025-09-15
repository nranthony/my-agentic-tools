#!/usr/bin/env python3
"""Test Firecrawl API access with YC job board."""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

print("🔥 Testing Firecrawl API Access")
print("=" * 40)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️  python-dotenv not available, using system env vars")

# Test 1: Basic Firecrawl connection
print("\n1. Testing Firecrawl initialization...")
try:
    from mygentic.web_scraping.yc_scraper.clients.firecrawl_client import FirecrawlClient
    
    client = FirecrawlClient()
    print("✅ Firecrawl client initialized successfully")
    
    # Test 2: Simple scrape test
    print("\n2. Testing basic scrape functionality...")
    test_url = "https://www.workatastartup.com/companies"
    
    try:
        print(f"   Scraping: {test_url}")
        result = client.app.scrape(test_url, 
            formats=["markdown"],
            timeout=10000  # 10 seconds for quick test
        )
        
        # Handle both v1 and v2 API response formats
        if hasattr(result, 'markdown'):
            # v2 API - result is a Document object
            content = getattr(result, 'markdown', '')
            print(f"✅ Basic scrape successful - got {len(content)} characters")
        elif result and result.get('success'):
            # v1 API - result is a dict
            content = result.get('markdown', '')
            print(f"✅ Basic scrape successful - got {len(content)} characters")
        else:
            print(f"❌ Scrape failed: {result}")
            content = ""
        
        if content:
            # Look for YC-specific content
            if "Y Combinator" in content or "startup" in content.lower():
                print("✅ YC content detected in scraped data")
            else:
                print("⚠️  No obvious YC content found (might be behind auth)")
            
    except Exception as e:
        print(f"❌ Basic scrape failed: {e}")
    
    # Test 3: Test with cookies (session cookie)
    print("\n3. Testing authentication with session cookie...")
    session_cookie = os.getenv("YC_SESSION_COOKIE")
    
    if session_cookie:
        print("   Session cookie found, testing authenticated access...")
        try:
            # Test with cookies
            cookies = {"_ycombinator_session": session_cookie}
            
            auth_result = client.scrape_with_scroll(
                url="https://www.workatastartup.com/companies?role=engineering",
                cookies=cookies,
                max_scrolls=1  # Just test one scroll
            )
            
            if auth_result and auth_result.get('success'):
                content = auth_result.get('markdown', '')
                print(f"✅ Authenticated scrape successful - got {len(content)} characters")
                
                # Look for more detailed content that requires auth
                if "Apply" in content or "jobs" in content.lower():
                    print("✅ Authenticated content detected")
                else:
                    print("⚠️  Basic content only (auth might not be working)")
            else:
                print(f"❌ Authenticated scrape failed: {auth_result}")
                
        except Exception as e:
            print(f"❌ Authenticated scrape error: {e}")
    else:
        print("   No session cookie found - skipping auth test")
        print("   Add YC_SESSION_COOKIE to .env file for authenticated access")
    
except Exception as e:
    print(f"❌ Firecrawl client initialization failed: {e}")

print("\n✨ Firecrawl tests completed!")
print("\n💡 Next steps if working:")
print("   - Test Gemini AI extraction")
print("   - Run full scraping workflow")
print("   - Validate data quality")