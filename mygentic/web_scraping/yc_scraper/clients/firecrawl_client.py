"""Firecrawl client for web scraping with infinite scroll support."""

import os
import time
from typing import Dict, List, Any, Optional
from firecrawl import FirecrawlApp
import logging

logger = logging.getLogger(__name__)


class FirecrawlClient:
    """Firecrawl API client with scroll and pagination support."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Firecrawl client.
        
        Args:
            api_key: Firecrawl API key. If None, uses FIRECRAWL_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable or api_key parameter required")
        
        self.app = FirecrawlApp(api_key=self.api_key)
        self.scrape_delay = float(os.getenv("SCRAPE_DELAY", "1.0"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    def scrape_with_scroll(
        self, 
        url: str, 
        cookies: Optional[Dict[str, str]] = None,
        max_scrolls: int = 10,
        scroll_pause: float = 2.0,
        wait_for_content: float = 3.0
    ) -> Dict[str, Any]:
        """Scrape a page with infinite scroll support.
        
        Args:
            url: URL to scrape
            cookies: Browser cookies for authentication
            max_scrolls: Maximum number of scroll attempts
            scroll_pause: Seconds to wait between scrolls
            wait_for_content: Seconds to wait for content to load after scroll
            
        Returns:
            Dict with scraped content and metadata
        """
        logger.info(f"Scraping URL with scroll: {url}")
        
        # Build actions for infinite scroll
        actions = []
        
        # Wait for initial content to load
        actions.append({"type": "wait", "milliseconds": int(wait_for_content * 1000)})
        
        # Perform scrolling to load more content
        for i in range(max_scrolls):
            # Scroll to bottom
            actions.append({"type": "scroll", "direction": "down", "amount": "page"})
            
            # Wait for content to load
            actions.append({"type": "wait", "milliseconds": int(scroll_pause * 1000)})
            
            # Check if we've reached the end (this is a heuristic)
            if i > 0 and i % 3 == 0:
                # Every few scrolls, wait a bit longer to see if more content loads
                actions.append({"type": "wait", "milliseconds": int(wait_for_content * 1000)})
        
        # Final wait to ensure all content is loaded
        actions.append({"type": "wait", "milliseconds": int(wait_for_content * 1000)})
        
        return self._scrape_with_retries(url, cookies, actions)
    
    def scrape_page(
        self, 
        url: str, 
        cookies: Optional[Dict[str, str]] = None,
        wait_time: float = 2.0
    ) -> Dict[str, Any]:
        """Scrape a single page without scrolling.
        
        Args:
            url: URL to scrape
            cookies: Browser cookies for authentication
            wait_time: Seconds to wait for page to load
            
        Returns:
            Dict with scraped content and metadata
        """
        logger.info(f"Scraping single page: {url}")
        
        actions = [{"type": "wait", "milliseconds": int(wait_time * 1000)}]
        return self._scrape_with_retries(url, cookies, actions)
    
    def _scrape_with_retries(
        self, 
        url: str, 
        cookies: Optional[Dict[str, str]] = None,
        actions: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Scrape with retry logic.
        
        Args:
            url: URL to scrape
            cookies: Browser cookies
            actions: List of Firecrawl actions to perform
            
        Returns:
            Dict with scraped content and metadata
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Prepare scrape options
                kwargs = {
                    "formats": ["markdown", "html"],
                    "timeout": self.timeout * 1000,  # Convert to milliseconds
                }
                
                # Add cookies if provided
                if cookies:
                    # Convert cookies dict to cookie string format
                    cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
                    kwargs["headers"] = {"Cookie": cookie_string}
                
                # Add actions if provided
                if actions:
                    kwargs["actions"] = actions
                
                # Perform scrape
                result = self.app.scrape(url, **kwargs)
                
                # Handle new Firecrawl API v2 response format
                if hasattr(result, 'data') and hasattr(result, 'success'):
                    # v2 API returns a Document object
                    if result.success:
                        logger.info(f"Successfully scraped {url}")
                        return {
                            "success": True,
                            "markdown": getattr(result.data, 'markdown', ''),
                            "html": getattr(result.data, 'html', ''),
                            "metadata": getattr(result.data, 'metadata', {}),
                        }
                    else:
                        error_msg = getattr(result, 'error', 'Unknown error')
                        logger.warning(f"Scrape attempt {attempt + 1} failed: {error_msg}")
                        last_error = Exception(f"Firecrawl scrape failed: {error_msg}")
                elif result and hasattr(result, '__dict__'):
                    # Fallback: treat as object with attributes
                    logger.info(f"Successfully scraped {url}")
                    result_dict = result.__dict__
                    return {
                        "success": True,
                        "markdown": result_dict.get('markdown', ''),
                        "html": result_dict.get('html', ''),
                        "metadata": result_dict.get('metadata', {}),
                    }
                else:
                    # Legacy v1 API format or error
                    if result and result.get("success", False):
                        logger.info(f"Successfully scraped {url}")
                        return result
                    else:
                        error_msg = result.get("error", "Unknown error") if result else "No result returned"
                        logger.warning(f"Scrape attempt {attempt + 1} failed: {error_msg}")
                        last_error = Exception(f"Firecrawl scrape failed: {error_msg}")
                    
            except Exception as e:
                logger.warning(f"Scrape attempt {attempt + 1} failed with exception: {str(e)}")
                last_error = e
            
            # Wait before retry (except on last attempt)
            if attempt < self.max_retries - 1:
                time.sleep(self.scrape_delay * (attempt + 1))  # Exponential backoff
        
        # All retries failed
        error_msg = f"Failed to scrape {url} after {self.max_retries} attempts"
        logger.error(f"{error_msg}. Last error: {last_error}")
        raise Exception(f"{error_msg}: {last_error}")
    
    def extract_content_sections(self, result: Dict[str, Any]) -> Dict[str, str]:
        """Extract different content formats from Firecrawl result.
        
        Args:
            result: Firecrawl scrape result
            
        Returns:
            Dict with markdown, html, and metadata
        """
        return {
            "markdown": result.get("markdown", ""),
            "html": result.get("html", ""),
            "title": result.get("metadata", {}).get("title", ""),
            "description": result.get("metadata", {}).get("description", ""),
            "url": result.get("metadata", {}).get("sourceURL", ""),
        }