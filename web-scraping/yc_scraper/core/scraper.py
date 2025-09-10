"""Main Y Combinator job board scraper orchestrator."""

import os
from typing import List, Dict, Any, Optional, Tuple
import logging
from urllib.parse import urljoin

from ..models.company import Company
from ..models.job import Job
from ..models.search_params import SearchParams
from ..clients.firecrawl_client import FirecrawlClient
from ..clients.gemini_client import GeminiClient
from ..core.auth_handler import AuthHandler
from ..core.url_builder import URLBuilder
from ..extractors.company_extractor import CompanyExtractor
from ..extractors.job_extractor import JobExtractor
from ..extractors.pagination_handler import PaginationHandler
from ..utils.data_cleaner import DataCleaner
from ..utils.exporters import DataExporter

logger = logging.getLogger(__name__)


class YCJobScraper:
    """Main scraper for Y Combinator job board."""
    
    def __init__(
        self,
        firecrawl_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        session_cookie: Optional[str] = None,
        output_dir: Optional[str] = None
    ):
        """Initialize the Y Combinator job scraper.
        
        Args:
            firecrawl_api_key: Firecrawl API key (uses env var if None)
            gemini_api_key: Gemini API key (uses env var if None)
            session_cookie: YC session cookie (uses env var if None)
            output_dir: Output directory for exports (uses env var if None)
        """
        # Initialize clients
        self.firecrawl_client = FirecrawlClient(firecrawl_api_key)
        self.gemini_client = GeminiClient(gemini_api_key)
        self.auth_handler = AuthHandler(session_cookie)
        self.url_builder = URLBuilder()
        
        # Initialize extractors
        self.company_extractor = CompanyExtractor(self.gemini_client)
        self.job_extractor = JobExtractor(self.gemini_client)
        self.pagination_handler = PaginationHandler(self.firecrawl_client)
        
        # Initialize utilities
        self.data_exporter = DataExporter(output_dir)
        
        logger.info("Y Combinator scraper initialized")
    
    def scrape_search(
        self,
        search_params: SearchParams,
        max_companies: Optional[int] = None,
        include_jobs: bool = True,
        max_scrolls: int = 15
    ) -> Tuple[List[Company], List[Job]]:
        """Scrape companies and jobs based on search parameters.
        
        Args:
            search_params: Search criteria
            max_companies: Maximum number of companies to process
            include_jobs: Whether to scrape job details for each company
            max_scrolls: Maximum scroll attempts for pagination
            
        Returns:
            Tuple of (companies_list, jobs_list)
        """
        logger.info(f"Starting search scrape with params: {search_params}")
        
        # Build search URL
        search_url = self.url_builder.build_search_url(search_params)
        logger.info(f"Search URL: {search_url}")
        
        # Scrape search results with pagination
        try:
            cookies = self.auth_handler.get_cookies()
            
            # Use infinite scroll for comprehensive results
            result = self.pagination_handler.scrape_with_infinite_scroll(
                search_url,
                cookies=cookies,
                max_scrolls=max_scrolls
            )
            
            content = result.get('markdown', '')
            if not content:
                logger.error("No content retrieved from search page")
                return [], []
            
            logger.info(f"Retrieved {len(content)} characters of content")
            
            # Extract companies from search results
            companies = self.company_extractor.extract_companies(content, max_companies)
            logger.info(f"Extracted {len(companies)} companies from search")
            
            if not companies:
                logger.warning("No companies found in search results")
                return [], []
            
            # Clean company data
            companies = DataCleaner.clean_companies(companies)
            
            # Scrape jobs if requested
            jobs = []
            if include_jobs:
                jobs = self._scrape_jobs_for_companies(companies)
                jobs = DataCleaner.clean_jobs(jobs)
            
            logger.info(f"Scraping complete: {len(companies)} companies, {len(jobs)} jobs")
            return companies, jobs
            
        except Exception as e:
            logger.error(f"Failed to scrape search results: {e}")
            return [], []
    
    def scrape_from_url(
        self,
        url: str,
        max_companies: Optional[int] = None,
        include_jobs: bool = True,
        max_scrolls: int = 15
    ) -> Tuple[List[Company], List[Job]]:
        """Scrape companies and jobs from a Y Combinator URL.
        
        Args:
            url: Y Combinator job board URL
            max_companies: Maximum number of companies to process
            include_jobs: Whether to scrape job details
            max_scrolls: Maximum scroll attempts
            
        Returns:
            Tuple of (companies_list, jobs_list)
        """
        logger.info(f"Scraping from URL: {url}")
        
        # Parse search parameters from URL
        try:
            search_params = self.url_builder.parse_search_url(url)
            return self.scrape_search(search_params, max_companies, include_jobs, max_scrolls)
        except Exception as e:
            logger.error(f"Failed to parse URL {url}: {e}")
            return [], []
    
    def scrape_company(self, company_slug: str) -> Tuple[Optional[Company], List[Job]]:
        """Scrape detailed information for a specific company.
        
        Args:
            company_slug: Company slug (e.g., 'openai')
            
        Returns:
            Tuple of (company_info, jobs_list)
        """
        logger.info(f"Scraping company: {company_slug}")
        
        try:
            # Build company URL
            company_url = self.url_builder.build_company_url(company_slug)
            cookies = self.auth_handler.get_cookies()
            
            # Scrape company page
            result = self.firecrawl_client.scrape_page(company_url, cookies)
            content = result.get('markdown', '')
            
            if not content:
                logger.error(f"No content retrieved for company: {company_slug}")
                return None, []
            
            # Extract detailed company information
            company = self.company_extractor.extract_company_from_page(content, company_url)
            
            # Scrape jobs for this company
            jobs = []
            if company:
                # Look for jobs URL in company page or build it
                jobs_url = company.jobs_url
                if not jobs_url:
                    jobs_url = self.url_builder.build_company_jobs_url(company_slug)
                
                # Scrape jobs
                jobs_result = self.firecrawl_client.scrape_page(jobs_url, cookies)
                jobs_content = jobs_result.get('markdown', '')
                
                if jobs_content:
                    jobs = self.job_extractor.extract_jobs(jobs_content, company.name)
                    jobs = DataCleaner.clean_jobs(jobs)
            
            logger.info(f"Company scrape complete: {company.name if company else 'None'}, {len(jobs)} jobs")
            return company, jobs
            
        except Exception as e:
            logger.error(f"Failed to scrape company {company_slug}: {e}")
            return None, []
    
    def _scrape_jobs_for_companies(self, companies: List[Company]) -> List[Job]:
        """Scrape job details for a list of companies.
        
        Args:
            companies: List of companies to scrape jobs for
            
        Returns:
            List of all jobs found
        """
        all_jobs = []
        cookies = self.auth_handler.get_cookies()
        
        for i, company in enumerate(companies, 1):
            logger.info(f"Scraping jobs for company {i}/{len(companies)}: {company.name}")
            
            try:
                # Skip companies with no jobs
                if company.job_count == 0:
                    logger.debug(f"Skipping {company.name} - no jobs listed")
                    continue
                
                # Determine jobs URL
                jobs_url = company.jobs_url
                
                if not jobs_url:
                    # Try to extract company slug and build jobs URL
                    if company.yc_profile_url:
                        company_slug = self.url_builder.extract_company_slug(company.yc_profile_url)
                        if company_slug:
                            jobs_url = self.url_builder.build_company_jobs_url(company_slug)
                
                if not jobs_url:
                    logger.warning(f"No jobs URL found for {company.name}")
                    continue
                
                # Scrape jobs page
                result = self.firecrawl_client.scrape_page(jobs_url, cookies, wait_time=2.0)
                content = result.get('markdown', '')
                
                if content:
                    # Extract jobs for this company
                    company_jobs = self.job_extractor.extract_jobs(content, company.name)
                    
                    # Add company context to jobs
                    for job in company_jobs:
                        if not job.company_url:
                            job.company_url = company.url
                        if not job.company_description:
                            job.company_description = company.description
                        if not job.company_industry:
                            job.company_industry = company.industry
                        if not job.company_size:
                            job.company_size = company.team_size
                    
                    all_jobs.extend(company_jobs)
                    logger.info(f"Found {len(company_jobs)} jobs for {company.name}")
                else:
                    logger.warning(f"No content retrieved for {company.name} jobs")
                
            except Exception as e:
                logger.error(f"Failed to scrape jobs for {company.name}: {e}")
                continue
            
            # Brief pause between company requests
            import time
            time.sleep(0.5)
        
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        return all_jobs
    
    def export_results(
        self,
        companies: List[Company],
        jobs: List[Job],
        format: str = "json",
        filename: Optional[str] = None
    ) -> Dict[str, str]:
        """Export scraping results to files.
        
        Args:
            companies: List of companies to export
            jobs: List of jobs to export
            format: Export format ('json', 'csv')
            filename: Base filename (timestamp will be added if None)
            
        Returns:
            Dict with paths to exported files
        """
        logger.info(f"Exporting {len(companies)} companies and {len(jobs)} jobs in {format} format")
        
        exported_files = {}
        
        try:
            # Export companies
            if companies:
                companies_file = self.data_exporter.export_companies(companies, format, f"{filename}_companies" if filename else None)
                exported_files['companies'] = companies_file
            
            # Export jobs
            if jobs:
                jobs_file = self.data_exporter.export_jobs(jobs, format, f"{filename}_jobs" if filename else None)
                exported_files['jobs'] = jobs_file
            
            # Export combined if both present
            if companies and jobs:
                combined_file = self.data_exporter.export_combined(companies, jobs, "json", f"{filename}_combined" if filename else None)
                exported_files['combined'] = combined_file
            
            logger.info(f"Export complete. Files: {list(exported_files.keys())}")
            return exported_files
            
        except Exception as e:
            logger.error(f"Failed to export results: {e}")
            return {}
    
    def get_auth_instructions(self) -> str:
        """Get instructions for setting up authentication."""
        return self.auth_handler.get_cookie_instructions()
    
    def is_authenticated(self) -> bool:
        """Check if scraper has authentication credentials."""
        return self.auth_handler.is_authenticated()
    
    def set_session_cookie(self, cookie: str) -> None:
        """Update session cookie for authentication."""
        self.auth_handler.set_session_cookie(cookie)