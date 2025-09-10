"""Company data extraction from Y Combinator job board listings."""

from typing import List, Optional, Dict, Any
import re
from ..models.company import Company
from ..clients.gemini_client import GeminiClient
import logging

logger = logging.getLogger(__name__)


class CompanyExtractor:
    """Extracts company information from Y Combinator job board content."""
    
    def __init__(self, gemini_client: GeminiClient):
        """Initialize company extractor.
        
        Args:
            gemini_client: Initialized Gemini client for AI extraction
        """
        self.gemini_client = gemini_client
    
    def extract_companies(
        self, 
        content: str, 
        max_companies: Optional[int] = None
    ) -> List[Company]:
        """Extract company information from job board content.
        
        Args:
            content: HTML or markdown content from the job board
            max_companies: Optional limit on number of companies to extract
            
        Returns:
            List of Company objects
        """
        logger.info(f"Extracting companies from content (max: {max_companies})")
        
        try:
            # Use Gemini to extract structured company data
            companies_data = self.gemini_client.extract_companies(content, max_companies)
            
            # Convert to Company objects
            companies = []
            for company_data in companies_data:
                try:
                    company = self._create_company_from_data(company_data)
                    if company:
                        companies.append(company)
                except Exception as e:
                    logger.warning(f"Failed to create company from data {company_data}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(companies)} companies")
            return companies
            
        except Exception as e:
            logger.error(f"Failed to extract companies: {e}")
            return []
    
    def extract_company_from_page(self, content: str, company_url: str) -> Optional[Company]:
        """Extract detailed company information from a company's individual page.
        
        Args:
            content: HTML or markdown content from the company page
            company_url: URL of the company page
            
        Returns:
            Company object with detailed information or None if extraction failed
        """
        logger.info(f"Extracting detailed company info from page: {company_url}")
        
        try:
            # Use Gemini with a more specific prompt for individual company pages
            company_data = self.gemini_client.extract_structured_data(
                content, 
                Company,
                f"Extract detailed company information from this company profile page. The company URL is: {company_url}"
            )
            
            if company_data:
                # Ensure the URL is set
                if not company_data.yc_profile_url:
                    company_data.yc_profile_url = company_url
                    
                logger.info(f"Successfully extracted detailed company info: {company_data.name}")
                return company_data
            
        except Exception as e:
            logger.error(f"Failed to extract detailed company info: {e}")
        
        return None
    
    def _create_company_from_data(self, data: Dict[str, Any]) -> Optional[Company]:
        """Create Company object from extracted data dictionary.
        
        Args:
            data: Dictionary with company data
            
        Returns:
            Company object or None if creation failed
        """
        try:
            # Clean and validate data
            cleaned_data = self._clean_company_data(data)
            
            # Create Company object with validation
            company = Company(**cleaned_data)
            return company
            
        except Exception as e:
            logger.warning(f"Failed to create Company object: {e}")
            return None
    
    def _clean_company_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize company data.
        
        Args:
            data: Raw company data dictionary
            
        Returns:
            Cleaned data dictionary
        """
        cleaned = {}
        
        # Required field: name
        if 'name' in data and data['name']:
            cleaned['name'] = str(data['name']).strip()
        else:
            raise ValueError("Company name is required")
        
        # Optional string fields
        string_fields = ['description', 'industry', 'location', 'team_size', 'batch']
        for field in string_fields:
            if field in data and data[field]:
                value = str(data[field]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a']:
                    cleaned[field] = value
        
        # URL fields
        url_fields = ['url', 'yc_profile_url', 'jobs_url', 'logo_url']
        for field in url_fields:
            if field in data and data[field]:
                url = str(data[field]).strip()
                if url and url.startswith(('http://', 'https://')):
                    cleaned[field] = url
        
        # Job count (integer)
        if 'job_count' in data:
            try:
                job_count = int(data['job_count'])
                cleaned['job_count'] = max(0, job_count)  # Ensure non-negative
            except (ValueError, TypeError):
                # Try to parse from text like "5 jobs"
                if isinstance(data['job_count'], str):
                    match = re.search(r'(\d+)', data['job_count'])
                    if match:
                        cleaned['job_count'] = int(match.group(1))
                    else:
                        cleaned['job_count'] = 0
                else:
                    cleaned['job_count'] = 0
        
        # Founded year (integer)
        if 'founded_year' in data and data['founded_year']:
            try:
                year = int(data['founded_year'])
                if 1800 <= year <= 2030:  # Reasonable year range
                    cleaned['founded_year'] = year
            except (ValueError, TypeError):
                pass
        
        # Tags (list of strings)
        if 'tags' in data and data['tags']:
            if isinstance(data['tags'], list):
                tags = [str(tag).strip() for tag in data['tags'] if tag]
                cleaned['tags'] = [tag for tag in tags if tag]  # Remove empty strings
            elif isinstance(data['tags'], str):
                # Split string into tags
                tags = [tag.strip() for tag in str(data['tags']).split(',')]
                cleaned['tags'] = [tag for tag in tags if tag]
        
        return cleaned
    
    def extract_job_links(self, content: str) -> List[str]:
        """Extract job listing links from company page content.
        
        Args:
            content: HTML or markdown content from company page
            
        Returns:
            List of job listing URLs
        """
        job_links = []
        
        try:
            # Common patterns for job links on Y Combinator
            patterns = [
                r'href="([^"]*jobs[^"]*)"',  # Links containing "jobs"
                r'href="([^"]*\/companies\/[^"]*\/jobs[^"]*)"',  # YC job URLs
                r'"(https://www\.workatastartup\.com/companies/[^"]*jobs[^"]*)"'  # Full YC job URLs
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if match not in job_links:
                        job_links.append(match)
            
            logger.info(f"Extracted {len(job_links)} job links")
            
        except Exception as e:
            logger.warning(f"Failed to extract job links: {e}")
        
        return job_links
    
    def extract_see_all_jobs_link(self, content: str) -> Optional[str]:
        """Extract 'See all X jobs >' link from company listing.
        
        Args:
            content: HTML or markdown content
            
        Returns:
            URL for "See all jobs" page or None if not found
        """
        try:
            # Pattern for "See all X jobs" links
            patterns = [
                r'href="([^"]*)"[^>]*>.*?See all \d+ jobs?',
                r'href="([^"]*)"[^>]*>.*?View all jobs',
                r'href="([^"]*)"[^>]*>.*?\d+ jobs?.*?>',
                r'"(https://www\.workatastartup\.com/companies/[^"]*jobs[^"]*)"'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    link = matches[0]
                    logger.debug(f"Found 'See all jobs' link: {link}")
                    return link
            
        except Exception as e:
            logger.warning(f"Failed to extract 'See all jobs' link: {e}")
        
        return None