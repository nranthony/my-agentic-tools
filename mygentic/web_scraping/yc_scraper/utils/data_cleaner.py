"""Data cleaning and normalization utilities."""

import re
from typing import List, Dict, Any, Optional
from ..models.company import Company
from ..models.job import Job
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Utilities for cleaning and normalizing scraped data."""
    
    @staticmethod
    def clean_companies(companies: List[Company]) -> List[Company]:
        """Clean and deduplicate list of companies.
        
        Args:
            companies: List of Company objects
            
        Returns:
            Cleaned list of companies
        """
        logger.info(f"Cleaning {len(companies)} companies")
        
        cleaned = []
        seen_names = set()
        seen_urls = set()
        
        for company in companies:
            try:
                # Skip if we've seen this company name (case-insensitive)
                name_key = company.name.lower().strip()
                if name_key in seen_names:
                    logger.debug(f"Skipping duplicate company: {company.name}")
                    continue
                
                # Skip if we've seen this URL
                if company.yc_profile_url and company.yc_profile_url in seen_urls:
                    logger.debug(f"Skipping company with duplicate URL: {company.yc_profile_url}")
                    continue
                
                # Clean the company data
                cleaned_company = DataCleaner._clean_company(company)
                
                if cleaned_company:
                    cleaned.append(cleaned_company)
                    seen_names.add(name_key)
                    if cleaned_company.yc_profile_url:
                        seen_urls.add(cleaned_company.yc_profile_url)
                
            except Exception as e:
                logger.warning(f"Error cleaning company {company.name}: {e}")
                continue
        
        logger.info(f"Cleaned companies: {len(companies)} -> {len(cleaned)}")
        return cleaned
    
    @staticmethod
    def clean_jobs(jobs: List[Job]) -> List[Job]:
        """Clean and deduplicate list of jobs.
        
        Args:
            jobs: List of Job objects
            
        Returns:
            Cleaned list of jobs
        """
        logger.info(f"Cleaning {len(jobs)} jobs")
        
        cleaned = []
        seen_jobs = set()
        
        for job in jobs:
            try:
                # Create unique key for job (company + title)
                job_key = f"{job.company_name.lower().strip()}:{job.title.lower().strip()}"
                
                if job_key in seen_jobs:
                    logger.debug(f"Skipping duplicate job: {job.title} at {job.company_name}")
                    continue
                
                # Clean the job data
                cleaned_job = DataCleaner._clean_job(job)
                
                if cleaned_job:
                    cleaned.append(cleaned_job)
                    seen_jobs.add(job_key)
                
            except Exception as e:
                logger.warning(f"Error cleaning job {job.title}: {e}")
                continue
        
        logger.info(f"Cleaned jobs: {len(jobs)} -> {len(cleaned)}")
        return cleaned
    
    @staticmethod
    def _clean_company(company: Company) -> Optional[Company]:
        """Clean individual company data.
        
        Args:
            company: Company object to clean
            
        Returns:
            Cleaned Company object or None if invalid
        """
        try:
            # Create dict for cleaned data
            data = company.model_dump()
            
            # Clean name (required field)
            if not data.get('name'):
                return None
            
            data['name'] = DataCleaner._clean_text(data['name'])
            if not data['name']:
                return None
            
            # Clean optional text fields
            text_fields = ['description', 'industry', 'location', 'team_size', 'batch']
            for field in text_fields:
                if data.get(field):
                    cleaned_text = DataCleaner._clean_text(data[field])
                    data[field] = cleaned_text if cleaned_text else None
            
            # Clean URLs
            url_fields = ['url', 'yc_profile_url', 'jobs_url', 'logo_url']
            for field in url_fields:
                if data.get(field):
                    cleaned_url = DataCleaner._clean_url(data[field])
                    data[field] = cleaned_url if cleaned_url else None
            
            # Validate job count
            if data.get('job_count') is not None:
                try:
                    job_count = int(data['job_count'])
                    data['job_count'] = max(0, job_count)  # Ensure non-negative
                except (ValueError, TypeError):
                    data['job_count'] = 0
            
            # Clean tags list
            if data.get('tags'):
                cleaned_tags = DataCleaner._clean_tags_list(data['tags'])
                data['tags'] = cleaned_tags
            
            # Create new Company object with cleaned data
            return Company(**data)
            
        except Exception as e:
            logger.warning(f"Failed to clean company: {e}")
            return None
    
    @staticmethod
    def _clean_job(job: Job) -> Optional[Job]:
        """Clean individual job data.
        
        Args:
            job: Job object to clean
            
        Returns:
            Cleaned Job object or None if invalid
        """
        try:
            # Create dict for cleaned data
            data = job.model_dump()
            
            # Clean required fields
            if not data.get('title') or not data.get('company_name'):
                return None
            
            data['title'] = DataCleaner._clean_text(data['title'])
            data['company_name'] = DataCleaner._clean_text(data['company_name'])
            
            if not data['title'] or not data['company_name']:
                return None
            
            # Clean optional text fields
            text_fields = [
                'description', 'location', 'location_type', 'salary_currency',
                'job_type', 'experience_level', 'department', 'education_required',
                'company_description', 'company_industry', 'company_size'
            ]
            
            for field in text_fields:
                if data.get(field):
                    cleaned_text = DataCleaner._clean_text(data[field])
                    data[field] = cleaned_text if cleaned_text else None
            
            # Clean URLs/emails
            url_fields = ['application_url', 'company_url']
            for field in url_fields:
                if data.get(field):
                    cleaned_url = DataCleaner._clean_url(data[field])
                    data[field] = cleaned_url if cleaned_url else None
            
            if data.get('application_email'):
                cleaned_email = DataCleaner._clean_email(data['application_email'])
                data['application_email'] = cleaned_email if cleaned_email else None
            
            # Validate numeric fields
            numeric_fields = ['salary_min', 'salary_max', 'years_experience']
            for field in numeric_fields:
                if data.get(field) is not None:
                    try:
                        value = int(data[field])
                        data[field] = max(0, value) if value >= 0 else None
                    except (ValueError, TypeError):
                        data[field] = None
            
            # Validate equity fields
            equity_fields = ['equity_min', 'equity_max']
            for field in equity_fields:
                if data.get(field) is not None:
                    try:
                        value = float(data[field])
                        if 0 <= value <= 100:  # Reasonable equity range
                            data[field] = value
                        else:
                            data[field] = None
                    except (ValueError, TypeError):
                        data[field] = None
            
            # Clean skills list
            if data.get('skills_required'):
                cleaned_skills = DataCleaner._clean_skills_list(data['skills_required'])
                data['skills_required'] = cleaned_skills
            
            # Create new Job object with cleaned data
            return Job(**data)
            
        except Exception as e:
            logger.warning(f"Failed to clean job: {e}")
            return None
    
    @staticmethod
    def _clean_text(text: str) -> Optional[str]:
        """Clean and normalize text content.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text or None if empty
        """
        if not text:
            return None
        
        # Convert to string and strip
        text = str(text).strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common placeholder text
        placeholder_patterns = [
            r'^\s*n/?a\s*$',
            r'^\s*null\s*$',
            r'^\s*none\s*$',
            r'^\s*not specified\s*$',
            r'^\s*tbd\s*$',
            r'^\s*-\s*$'
        ]
        
        for pattern in placeholder_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return None
        
        # Return cleaned text if it has content
        return text if text else None
    
    @staticmethod
    def _clean_url(url: str) -> Optional[str]:
        """Clean and validate URL.
        
        Args:
            url: URL to clean
            
        Returns:
            Cleaned URL or None if invalid
        """
        if not url:
            return None
        
        url = str(url).strip()
        
        # Must start with http/https
        if not url.startswith(('http://', 'https://')):
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('www.'):
                url = 'https://' + url
            else:
                return None
        
        # Basic URL validation
        if len(url) < 10 or ' ' in url:
            return None
        
        return url
    
    @staticmethod
    def _clean_email(email: str) -> Optional[str]:
        """Clean and validate email address.
        
        Args:
            email: Email to clean
            
        Returns:
            Cleaned email or None if invalid
        """
        if not email:
            return None
        
        email = str(email).strip().lower()
        
        # Basic email pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_pattern, email):
            return email
        
        return None
    
    @staticmethod
    def _clean_tags_list(tags: List[str]) -> List[str]:
        """Clean list of tags.
        
        Args:
            tags: List of tag strings
            
        Returns:
            Cleaned list of tags
        """
        if not tags:
            return []
        
        cleaned = []
        seen = set()
        
        for tag in tags:
            if not tag:
                continue
            
            # Clean individual tag
            tag = str(tag).strip()
            
            # Skip if empty or too short
            if len(tag) < 2:
                continue
            
            # Convert to title case and deduplicate
            tag = tag.title()
            
            if tag.lower() not in seen:
                cleaned.append(tag)
                seen.add(tag.lower())
        
        return cleaned[:10]  # Limit to 10 tags
    
    @staticmethod
    def _clean_skills_list(skills: List[str]) -> List[str]:
        """Clean list of skills.
        
        Args:
            skills: List of skill strings
            
        Returns:
            Cleaned list of skills
        """
        if not skills:
            return []
        
        cleaned = []
        seen = set()
        
        for skill in skills:
            if not skill:
                continue
            
            # Clean individual skill
            skill = str(skill).strip()
            
            # Skip if empty or too short
            if len(skill) < 2:
                continue
            
            # Normalize common tech skills
            skill = DataCleaner._normalize_skill(skill)
            
            if skill.lower() not in seen:
                cleaned.append(skill)
                seen.add(skill.lower())
        
        return cleaned[:20]  # Limit to 20 skills
    
    @staticmethod
    def _normalize_skill(skill: str) -> str:
        """Normalize skill name (e.g., standardize capitalization).
        
        Args:
            skill: Skill name to normalize
            
        Returns:
            Normalized skill name
        """
        # Common skill normalizations
        skill_mapping = {
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'python': 'Python',
            'java': 'Java',
            'c++': 'C++',
            'c#': 'C#',
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'node': 'Node.js',
            'nodejs': 'Node.js',
            'aws': 'AWS',
            'gcp': 'Google Cloud',
            'azure': 'Azure',
            'docker': 'Docker',
            'kubernetes': 'Kubernetes',
            'sql': 'SQL',
            'postgresql': 'PostgreSQL',
            'mysql': 'MySQL',
            'mongodb': 'MongoDB',
            'redis': 'Redis',
            'git': 'Git',
            'github': 'GitHub',
            'gitlab': 'GitLab'
        }
        
        skill_lower = skill.lower()
        return skill_mapping.get(skill_lower, skill)