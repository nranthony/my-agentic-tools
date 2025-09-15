"""URL building and parameter management for Y Combinator job board."""

from typing import Dict, Optional
from urllib.parse import urlencode, urlparse, parse_qs
from ..models.search_params import SearchParams
import logging

logger = logging.getLogger(__name__)


class URLBuilder:
    """Builds and manages URLs for Y Combinator job board searches."""
    
    BASE_URL = "https://www.workatastartup.com/companies"
    
    def __init__(self):
        """Initialize URL builder."""
        pass
    
    def build_search_url(self, search_params: SearchParams) -> str:
        """Build search URL from SearchParams.
        
        Args:
            search_params: SearchParams object with search criteria
            
        Returns:
            Full search URL
        """
        params = search_params.to_url_params()
        query_string = urlencode(params)
        url = f"{self.BASE_URL}?{query_string}"
        
        logger.info(f"Built search URL: {url}")
        return url
    
    def parse_search_url(self, url: str) -> SearchParams:
        """Parse search parameters from Y Combinator URL.
        
        Args:
            url: Y Combinator job board URL
            
        Returns:
            SearchParams object with parsed parameters
        """
        logger.info(f"Parsing search URL: {url}")
        return SearchParams.from_url(url)
    
    def build_company_url(self, company_slug: str) -> str:
        """Build URL for a specific company page.
        
        Args:
            company_slug: Company slug (e.g., "openai")
            
        Returns:
            Company page URL
        """
        url = f"{self.BASE_URL}/{company_slug}"
        logger.debug(f"Built company URL: {url}")
        return url
    
    def build_company_jobs_url(self, company_slug: str) -> str:
        """Build URL for a specific company's jobs page.
        
        Args:
            company_slug: Company slug (e.g., "openai")
            
        Returns:
            Company jobs page URL
        """
        url = f"{self.BASE_URL}/{company_slug}/jobs"
        logger.debug(f"Built company jobs URL: {url}")
        return url
    
    def extract_company_slug(self, company_url: str) -> Optional[str]:
        """Extract company slug from Y Combinator company URL.
        
        Args:
            company_url: Y Combinator company URL
            
        Returns:
            Company slug or None if extraction failed
        """
        try:
            parsed = urlparse(company_url)
            
            # Handle different URL formats:
            # https://www.workatastartup.com/companies/openai
            # https://www.workatastartup.com/companies/openai/jobs
            path_parts = [part for part in parsed.path.split('/') if part]
            
            if len(path_parts) >= 2 and path_parts[0] == 'companies':
                slug = path_parts[1]
                logger.debug(f"Extracted company slug: {slug}")
                return slug
            
        except Exception as e:
            logger.warning(f"Failed to extract company slug from {company_url}: {e}")
        
        return None
    
    def is_yc_url(self, url: str) -> bool:
        """Check if URL is a Y Combinator job board URL.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL is from Y Combinator job board
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower() in ['www.workatastartup.com', 'workatastartup.com']
        except:
            return False
    
    def normalize_url(self, url: str) -> str:
        """Normalize Y Combinator URL (remove fragments, sort params, etc.).
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL
        """
        try:
            parsed = urlparse(url)
            
            # Parse and sort query parameters
            params = parse_qs(parsed.query)
            # Convert single-item lists back to strings
            normalized_params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
            
            # Rebuild URL without fragment
            query_string = urlencode(sorted(normalized_params.items()))
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if query_string:
                normalized += f"?{query_string}"
            
            logger.debug(f"Normalized URL: {url} -> {normalized}")
            return normalized
            
        except Exception as e:
            logger.warning(f"Failed to normalize URL {url}: {e}")
            return url
    
    def get_pagination_url(self, base_url: str, page: int) -> str:
        """Get URL for a specific page (if pagination exists).
        
        Args:
            base_url: Base search URL
            page: Page number (1-based)
            
        Returns:
            URL with pagination parameters
        """
        # Note: Y Combinator uses infinite scroll, not traditional pagination
        # This method is provided for potential future use or alternative implementations
        try:
            parsed = urlparse(base_url)
            params = parse_qs(parsed.query)
            
            # Add/update page parameter
            params['page'] = [str(page)]
            
            query_string = urlencode({k: v[0] if len(v) == 1 else v for k, v in params.items()})
            paginated_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query_string}"
            
            logger.debug(f"Built pagination URL for page {page}: {paginated_url}")
            return paginated_url
            
        except Exception as e:
            logger.warning(f"Failed to build pagination URL: {e}")
            return base_url