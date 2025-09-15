"""Gemini AI client for structured data extraction."""

import os
import json
import time
from typing import Dict, List, Any, Optional, Type, TypeVar
import google.generativeai as genai
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class GeminiClient:
    """Gemini AI client for extracting structured data from web content."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        """Initialize Gemini client.
        
        Args:
            api_key: Gemini API key. If None, uses GEMINI_API_KEY env var.
            model_name: Gemini model to use for generation.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable or api_key parameter required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
    
    def extract_companies(self, content: str, max_companies: Optional[int] = None) -> List[Dict[str, Any]]:
        """Extract company information from Y Combinator job board content.
        
        Args:
            content: HTML or markdown content from the job board
            max_companies: Optional limit on number of companies to extract
            
        Returns:
            List of company dictionaries with extracted data
        """
        logger.info("Extracting companies from content")
        
        prompt = self._build_company_extraction_prompt(content, max_companies)
        
        try:
            result = self._generate_with_retries(prompt)
            companies_data = self._parse_json_response(result)
            
            if isinstance(companies_data, dict) and "companies" in companies_data:
                companies_data = companies_data["companies"]
            
            if not isinstance(companies_data, list):
                logger.warning("Expected list of companies, got different format")
                return []
                
            logger.info(f"Extracted {len(companies_data)} companies")
            return companies_data
            
        except Exception as e:
            logger.error(f"Failed to extract companies: {str(e)}")
            return []
    
    def extract_jobs(self, content: str, company_name: str) -> List[Dict[str, Any]]:
        """Extract job information from company job listings page.
        
        Args:
            content: HTML or markdown content from company job listings
            company_name: Name of the company for context
            
        Returns:
            List of job dictionaries with extracted data
        """
        logger.info(f"Extracting jobs for company: {company_name}")
        
        prompt = self._build_job_extraction_prompt(content, company_name)
        
        try:
            result = self._generate_with_retries(prompt)
            jobs_data = self._parse_json_response(result)
            
            if isinstance(jobs_data, dict) and "jobs" in jobs_data:
                jobs_data = jobs_data["jobs"]
            
            if not isinstance(jobs_data, list):
                logger.warning("Expected list of jobs, got different format")
                return []
                
            logger.info(f"Extracted {len(jobs_data)} jobs for {company_name}")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Failed to extract jobs for {company_name}: {str(e)}")
            return []
    
    def extract_structured_data(
        self, 
        content: str, 
        schema: Type[T], 
        context: str = ""
    ) -> Optional[T]:
        """Extract structured data using a Pydantic model schema.
        
        Args:
            content: Content to extract from
            schema: Pydantic model class defining the structure
            context: Additional context for extraction
            
        Returns:
            Instance of the schema model or None if extraction failed
        """
        logger.info(f"Extracting structured data using schema: {schema.__name__}")
        
        # Get the JSON schema from the Pydantic model
        json_schema = schema.model_json_schema()
        
        prompt = f"""
        Extract structured data from the following content using this JSON schema:
        
        JSON Schema:
        {json.dumps(json_schema, indent=2)}
        
        {context}
        
        Content to extract from:
        {content[:10000]}  # Limit content length
        
        Return ONLY a valid JSON object that matches the schema. Do not include any explanation or additional text.
        """
        
        try:
            result = self._generate_with_retries(prompt)
            data = self._parse_json_response(result)
            
            # Validate and create Pydantic model instance
            return schema.model_validate(data)
            
        except Exception as e:
            logger.error(f"Failed to extract structured data: {str(e)}")
            return None
    
    def _build_company_extraction_prompt(self, content: str, max_companies: Optional[int]) -> str:
        """Build prompt for company extraction."""
        limit_text = f" Extract up to {max_companies} companies." if max_companies else ""
        
        return f"""
        Extract company information from this Y Combinator job board content.{limit_text}
        
        For each company, extract:
        - name: Company name
        - description: Company description/tagline
        - url: Company website URL (if available)
        - yc_profile_url: Y Combinator profile URL (if available)
        - job_count: Number of open jobs (parse from "X jobs" text)
        - jobs_url: "See all jobs" link URL (if available)
        - industry: Company industry/category
        - location: Company location
        - team_size: Team size (if mentioned)
        - batch: Y Combinator batch (e.g., S21, W22)
        - logo_url: Company logo URL (if available)
        - tags: Array of relevant tags/categories
        
        Content:
        {content[:15000]}  # Limit content length to avoid token limits
        
        Return a JSON object with this structure:
        {{
          "companies": [
            {{
              "name": "Company Name",
              "description": "What the company does",
              "url": "https://company.com",
              "yc_profile_url": "https://workatastartup.com/companies/company-name",
              "job_count": 5,
              "jobs_url": "https://workatastartup.com/companies/company-name/jobs",
              "industry": "Technology",
              "location": "San Francisco, CA",
              "team_size": "11-50",
              "batch": "S21",
              "logo_url": "https://logo.url",
              "tags": ["AI", "SaaS"]
            }}
          ]
        }}
        
        Return ONLY the JSON object. Do not include explanations or additional text.
        """
    
    def _build_job_extraction_prompt(self, content: str, company_name: str) -> str:
        """Build prompt for job extraction."""
        return f"""
        Extract job information from this job listings page for {company_name}.
        
        For each job, extract:
        - title: Job title
        - company_name: Company name (use "{company_name}")
        - description: Job description
        - location: Job location
        - remote_ok: Whether remote work is allowed (boolean)
        - location_type: "Remote", "On-site", or "Hybrid"
        - salary_min/salary_max: Salary range (numbers only)
        - salary_currency: Currency (USD, EUR, etc.)
        - equity_min/equity_max: Equity range (percentages)
        - job_type: "Full-time", "Part-time", "Contract", "Internship"
        - experience_level: "Junior", "Senior", "Lead", etc.
        - department: "Engineering", "Product", "Marketing", etc.
        - skills_required: Array of required skills
        - application_url: Application URL
        - visa_sponsorship: Whether visa sponsorship is available (boolean)
        
        Content:
        {content[:15000]}
        
        Return a JSON object with this structure:
        {{
          "jobs": [
            {{
              "title": "Software Engineer",
              "company_name": "{company_name}",
              "description": "Job description text",
              "location": "San Francisco, CA",
              "remote_ok": true,
              "location_type": "Hybrid",
              "salary_min": 120000,
              "salary_max": 180000,
              "salary_currency": "USD",
              "equity_min": 0.1,
              "equity_max": 0.5,
              "job_type": "Full-time",
              "experience_level": "Mid-level",
              "department": "Engineering",
              "skills_required": ["Python", "React", "AWS"],
              "application_url": "https://apply.url",
              "visa_sponsorship": true
            }}
          ]
        }}
        
        Return ONLY the JSON object. Do not include explanations or additional text.
        """
    
    def _generate_with_retries(self, prompt: str) -> str:
        """Generate content with retry logic."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini")
                    
            except Exception as e:
                logger.warning(f"Gemini generation attempt {attempt + 1} failed: {str(e)}")
                last_error = e
                
                if attempt < self.max_retries - 1:
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
        
        raise Exception(f"Failed to generate after {self.max_retries} attempts: {last_error}")
    
    def _parse_json_response(self, response: str) -> Any:
        """Parse JSON response, handling common formatting issues."""
        # Clean up response - remove markdown code blocks if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response[:500]}...")
            raise Exception(f"Invalid JSON response: {e}")