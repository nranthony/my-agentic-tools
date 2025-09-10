"""Pagination and infinite scroll handling for Y Combinator job board."""

import time
from typing import Dict, List, Any, Optional
from ..clients.firecrawl_client import FirecrawlClient
import logging

logger = logging.getLogger(__name__)


class PaginationHandler:
    """Handles infinite scroll pagination on Y Combinator job board."""
    
    def __init__(self, firecrawl_client: FirecrawlClient):
        """Initialize pagination handler.
        
        Args:
            firecrawl_client: Initialized Firecrawl client
        """
        self.firecrawl_client = firecrawl_client
    
    def scrape_with_infinite_scroll(
        self,
        url: str,
        cookies: Optional[Dict[str, str]] = None,
        max_scrolls: int = 15,
        scroll_pause: float = 3.0,
        content_check_interval: int = 3,
        min_new_content_threshold: int = 100
    ) -> Dict[str, Any]:
        """Scrape page with intelligent infinite scroll handling.
        
        Args:
            url: URL to scrape
            cookies: Authentication cookies
            max_scrolls: Maximum number of scroll attempts
            scroll_pause: Seconds to wait between scrolls
            content_check_interval: Check for new content every N scrolls
            min_new_content_threshold: Minimum characters for "new content"
            
        Returns:
            Dict with final scraped content and metadata
        """
        logger.info(f"Starting infinite scroll scrape of: {url}")
        
        try:
            # Initial scrape to get baseline content
            result = self.firecrawl_client.scrape_page(url, cookies, wait_time=3.0)
            initial_content = result.get('markdown', '')
            initial_length = len(initial_content)
            
            logger.info(f"Initial content length: {initial_length} characters")
            
            if initial_length == 0:
                logger.warning("No initial content found")
                return result
            
            # Perform scrolling with content monitoring
            last_content = initial_content
            last_length = initial_length
            no_change_count = 0
            
            for scroll_num in range(1, max_scrolls + 1):
                logger.info(f"Performing scroll {scroll_num}/{max_scrolls}")
                
                # Scrape with scrolling
                result = self.firecrawl_client.scrape_with_scroll(
                    url, 
                    cookies, 
                    max_scrolls=1,  # One scroll at a time for monitoring
                    scroll_pause=scroll_pause,
                    wait_for_content=scroll_pause
                )
                
                current_content = result.get('markdown', '')
                current_length = len(current_content)
                
                # Check if we have significant new content
                length_increase = current_length - last_length
                logger.debug(f"Content length change: +{length_increase} characters")
                
                if scroll_num % content_check_interval == 0:
                    # Detailed content comparison every few scrolls
                    if self._has_significant_new_content(
                        last_content, 
                        current_content, 
                        min_new_content_threshold
                    ):
                        logger.info(f"New content detected at scroll {scroll_num}")
                        no_change_count = 0
                        last_content = current_content
                        last_length = current_length
                    else:
                        no_change_count += 1
                        logger.info(f"No significant new content (count: {no_change_count})")
                        
                        # If no new content for several checks, we may have reached the end
                        if no_change_count >= 2:
                            logger.info("No new content detected for multiple checks - stopping")
                            break
                else:
                    # Simple length-based check for other scrolls
                    if length_increase > min_new_content_threshold:
                        no_change_count = 0
                    elif length_increase < 10:  # Very little change
                        no_change_count += 0.5  # Partial increment
                
                # Stop if content hasn't grown significantly
                if length_increase < 10 and scroll_num > 5:
                    logger.info(f"Minimal content growth - may have reached end")
                    no_change_count += 1
                    
                    if no_change_count >= 3:
                        logger.info("Stopping due to lack of content growth")
                        break
                
                # Small delay between scrolls
                time.sleep(0.5)
            
            logger.info(f"Infinite scroll completed. Final content length: {len(current_content)}")
            return result
            
        except Exception as e:
            logger.error(f"Failed during infinite scroll: {e}")
            # Return whatever we managed to get
            return result if 'result' in locals() else {}
    
    def _has_significant_new_content(
        self, 
        old_content: str, 
        new_content: str, 
        min_threshold: int
    ) -> bool:
        """Check if new content has significant additions.
        
        Args:
            old_content: Previous content
            new_content: Current content
            min_threshold: Minimum characters for significant change
            
        Returns:
            True if significant new content is detected
        """
        if len(new_content) <= len(old_content):
            return False
        
        # Simple heuristic: check if the new part contains job/company indicators
        new_part = new_content[len(old_content):]
        
        if len(new_part) < min_threshold:
            return False
        
        # Look for indicators of new job/company listings
        job_indicators = [
            'job', 'position', 'role', 'hiring', 'engineer', 'developer',
            'manager', 'designer', 'analyst', 'specialist', 'coordinator'
        ]
        
        company_indicators = [
            'company', 'startup', 'founded', 'team size', 'batch', 'industry'
        ]
        
        new_part_lower = new_part.lower()
        
        # Count indicators in new content
        indicator_count = 0
        for indicator in job_indicators + company_indicators:
            indicator_count += new_part_lower.count(indicator)
        
        # If we have multiple indicators, likely new content
        has_indicators = indicator_count >= 3
        
        logger.debug(f"New content analysis: {len(new_part)} chars, {indicator_count} indicators")
        
        return has_indicators
    
    def estimate_total_results(self, initial_content: str) -> Optional[int]:
        """Estimate total number of results from initial page load.
        
        Args:
            initial_content: Initial page content
            
        Returns:
            Estimated total results or None if cannot determine
        """
        try:
            import re
            
            # Look for result count indicators
            patterns = [
                r'(\d+)\s+companies?',
                r'(\d+)\s+results?',
                r'showing\s+(\d+)',
                r'(\d+)\s+total'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, initial_content, re.IGNORECASE)
                if matches:
                    try:
                        count = int(matches[0])
                        logger.info(f"Estimated total results: {count}")
                        return count
                    except ValueError:
                        continue
            
            # Fallback: count company/job entries in initial content
            company_patterns = [
                r'class="[^"]*company[^"]*"',
                r'data-company-id',
                r'href="[^"]*companies/[^"]*"'
            ]
            
            total_matches = 0
            for pattern in company_patterns:
                matches = re.findall(pattern, initial_content, re.IGNORECASE)
                total_matches += len(matches)
            
            if total_matches > 0:
                # Rough estimate: if we found N companies in initial load,
                # there might be more with scrolling
                estimate = min(total_matches * 3, 1000)  # Cap at reasonable number
                logger.info(f"Estimated results from pattern matching: {estimate}")
                return estimate
            
        except Exception as e:
            logger.warning(f"Failed to estimate total results: {e}")
        
        return None
    
    def should_continue_scrolling(
        self, 
        scroll_count: int, 
        content_changes: List[int], 
        max_scrolls: int
    ) -> bool:
        """Determine if scrolling should continue based on patterns.
        
        Args:
            scroll_count: Current scroll count
            content_changes: List of content length changes from recent scrolls
            max_scrolls: Maximum allowed scrolls
            
        Returns:
            True if scrolling should continue
        """
        if scroll_count >= max_scrolls:
            return False
        
        if len(content_changes) < 3:
            return True  # Keep going if we don't have enough data
        
        # Check recent changes
        recent_changes = content_changes[-3:]
        
        # If all recent changes are very small, probably reached the end
        if all(change < 50 for change in recent_changes):
            logger.info("Stopping - consistent small content changes")
            return False
        
        # If we have at least one decent change recently, continue
        if any(change > 100 for change in recent_changes):
            return True
        
        # Default: continue unless we've been getting tiny changes
        avg_recent_change = sum(recent_changes) / len(recent_changes)
        return avg_recent_change > 20