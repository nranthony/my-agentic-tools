"""Job data extraction from Y Combinator job listings."""

from typing import List, Optional, Dict, Any
import re
from datetime import datetime
from ..models.job import Job
from ..clients.gemini_client import GeminiClient
import logging

logger = logging.getLogger(__name__)


class JobExtractor:
    """Extracts job information from Y Combinator job listings."""
    
    def __init__(self, gemini_client: GeminiClient):
        """Initialize job extractor.
        
        Args:
            gemini_client: Initialized Gemini client for AI extraction
        """
        self.gemini_client = gemini_client
    
    def extract_jobs(self, content: str, company_name: str) -> List[Job]:
        """Extract job information from company job listings page.
        
        Args:
            content: HTML or markdown content from job listings page
            company_name: Name of the company for context
            
        Returns:
            List of Job objects
        """
        logger.info(f"Extracting jobs for company: {company_name}")
        
        try:
            # Use Gemini to extract structured job data
            jobs_data = self.gemini_client.extract_jobs(content, company_name)
            
            # Convert to Job objects
            jobs = []
            for job_data in jobs_data:
                try:
                    job = self._create_job_from_data(job_data, company_name)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"Failed to create job from data {job_data}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(jobs)} jobs for {company_name}")
            return jobs
            
        except Exception as e:
            logger.error(f"Failed to extract jobs for {company_name}: {e}")
            return []
    
    def extract_job_from_page(
        self, 
        content: str, 
        company_name: str, 
        job_url: str
    ) -> Optional[Job]:
        """Extract detailed job information from individual job page.
        
        Args:
            content: HTML or markdown content from job page
            company_name: Name of the company
            job_url: URL of the job posting
            
        Returns:
            Job object with detailed information or None if extraction failed
        """
        logger.info(f"Extracting detailed job info from: {job_url}")
        
        try:
            # Use Gemini with specific context for job page
            job_data = self.gemini_client.extract_structured_data(
                content,
                Job,
                f"Extract detailed job information from this job posting page. Company: {company_name}, Job URL: {job_url}"
            )
            
            if job_data:
                # Ensure company name and application URL are set
                if not job_data.company_name:
                    job_data.company_name = company_name
                if not job_data.application_url:
                    job_data.application_url = job_url
                    
                logger.info(f"Successfully extracted job: {job_data.title} at {company_name}")
                return job_data
            
        except Exception as e:
            logger.error(f"Failed to extract job details: {e}")
        
        return None
    
    def _create_job_from_data(self, data: Dict[str, Any], company_name: str) -> Optional[Job]:
        """Create Job object from extracted data dictionary.
        
        Args:
            data: Dictionary with job data
            company_name: Company name for fallback
            
        Returns:
            Job object or None if creation failed
        """
        try:
            # Clean and validate data
            cleaned_data = self._clean_job_data(data, company_name)
            
            # Create Job object with validation
            job = Job(**cleaned_data)
            return job
            
        except Exception as e:
            logger.warning(f"Failed to create Job object: {e}")
            return None
    
    def _clean_job_data(self, data: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """Clean and normalize job data.
        
        Args:
            data: Raw job data dictionary
            company_name: Company name for fallback
            
        Returns:
            Cleaned data dictionary
        """
        cleaned = {}
        
        # Required fields
        if 'title' in data and data['title']:
            cleaned['title'] = str(data['title']).strip()
        else:
            raise ValueError("Job title is required")
        
        # Use provided company_name or from data
        cleaned['company_name'] = data.get('company_name', company_name) or company_name
        
        # Optional string fields
        string_fields = [
            'description', 'location', 'location_type', 'salary_currency',
            'job_type', 'experience_level', 'department', 'education_required',
            'application_url', 'application_email', 'company_url', 
            'company_description', 'company_industry', 'company_size'
        ]
        
        for field in string_fields:
            if field in data and data[field]:
                value = str(data[field]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', 'not specified']:
                    cleaned[field] = value
        
        # Boolean fields
        bool_fields = ['remote_ok', 'visa_sponsorship']
        for field in bool_fields:
            if field in data:
                cleaned[field] = self._parse_boolean(data[field])
        
        # Integer fields
        int_fields = ['salary_min', 'salary_max', 'years_experience']
        for field in int_fields:
            if field in data and data[field]:
                try:
                    value = self._parse_integer(data[field])
                    if value is not None and value >= 0:
                        cleaned[field] = value
                except (ValueError, TypeError):
                    pass
        
        # Float fields (equity percentages)
        float_fields = ['equity_min', 'equity_max']
        for field in float_fields:
            if field in data and data[field]:
                try:
                    value = self._parse_float(data[field])
                    if value is not None and 0 <= value <= 100:  # Reasonable equity range
                        cleaned[field] = value
                except (ValueError, TypeError):
                    pass
        
        # Skills list
        if 'skills_required' in data and data['skills_required']:
            skills = self._parse_skills_list(data['skills_required'])
            if skills:
                cleaned['skills_required'] = skills
        
        # Posted date
        if 'posted_date' in data and data['posted_date']:
            posted_date = self._parse_date(data['posted_date'])
            if posted_date:
                cleaned['posted_date'] = posted_date
        
        return cleaned
    
    def _parse_boolean(self, value: Any) -> bool:
        """Parse boolean value from various formats."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on', 'enabled']
        return bool(value)
    
    def _parse_integer(self, value: Any) -> Optional[int]:
        """Parse integer value from various formats."""
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            # Handle formats like "$120,000", "120K", etc.
            clean_value = re.sub(r'[^\d]', '', value)
            if clean_value:
                base_value = int(clean_value)
                # Handle K (thousands) multiplier
                if 'k' in value.lower():
                    base_value *= 1000
                return base_value
        return None
    
    def _parse_float(self, value: Any) -> Optional[float]:
        """Parse float value from various formats."""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Handle formats like "0.5%", "0.5", etc.
            clean_value = re.sub(r'[^\d.]', '', value)
            if clean_value:
                return float(clean_value)
        return None
    
    def _parse_skills_list(self, value: Any) -> List[str]:
        """Parse skills list from various formats."""
        if isinstance(value, list):
            return [str(skill).strip() for skill in value if skill]
        if isinstance(value, str):
            # Split on common delimiters
            skills = re.split(r'[,;|]', value)
            return [skill.strip() for skill in skills if skill.strip()]
        return []
    
    def _parse_date(self, value: Any) -> Optional[datetime]:
        """Parse date from various formats."""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            # Try common date formats
            date_formats = [
                '%Y-%m-%d',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%SZ',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%B %d, %Y',
                '%b %d, %Y'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except ValueError:
                    continue
        
        return None
    
    def extract_salary_range(self, content: str) -> tuple[Optional[int], Optional[int], Optional[str]]:
        """Extract salary range from job content.
        
        Args:
            content: Job content text
            
        Returns:
            Tuple of (min_salary, max_salary, currency)
        """
        try:
            # Common salary patterns
            patterns = [
                r'(\$|€|£)(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*-\s*(\$|€|£)?(\d{1,3}(?:,\d{3})*(?:k|K)?)',
                r'(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*-\s*(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*(USD|EUR|GBP|\$|€|£)',
                r'Salary[:\s]*(\$|€|£)(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*-\s*(\$|€|£)?(\d{1,3}(?:,\d{3})*(?:k|K)?)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    match = matches[0]
                    # Process the match based on pattern structure
                    # This is a simplified implementation - would need refinement
                    logger.debug(f"Found salary pattern: {match}")
                    break
            
        except Exception as e:
            logger.warning(f"Failed to extract salary range: {e}")
        
        return None, None, None
    
    def extract_equity_range(self, content: str) -> tuple[Optional[float], Optional[float]]:
        """Extract equity range from job content.
        
        Args:
            content: Job content text
            
        Returns:
            Tuple of (min_equity, max_equity) as percentages
        """
        try:
            # Common equity patterns
            patterns = [
                r'(\d+(?:\.\d+)?)\s*%?\s*-\s*(\d+(?:\.\d+)?)\s*%?\s*equity',
                r'equity[:\s]*(\d+(?:\.\d+)?)\s*%?\s*-\s*(\d+(?:\.\d+)?)\s*%?',
                r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*%\s*equity'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    match = matches[0]
                    min_equity = float(match[0])
                    max_equity = float(match[1])
                    logger.debug(f"Found equity range: {min_equity}% - {max_equity}%")
                    return min_equity, max_equity
            
        except Exception as e:
            logger.warning(f"Failed to extract equity range: {e}")
        
        return None, None