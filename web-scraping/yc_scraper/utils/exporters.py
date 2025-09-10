"""Data export utilities for various formats."""

import json
import csv
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from ..models.company import Company
from ..models.job import Job
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Utilities for exporting scraped data to various formats."""
    
    def __init__(self, output_dir: Optional[str] = None):
        """Initialize data exporter.
        
        Args:
            output_dir: Output directory. If None, uses OUTPUT_DIR env var or ./output
        """
        self.output_dir = Path(output_dir or os.getenv("OUTPUT_DIR", "./output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Data exporter initialized with output dir: {self.output_dir}")
    
    def export_companies(
        self, 
        companies: List[Company], 
        format: str = "json",
        filename: Optional[str] = None
    ) -> str:
        """Export companies to specified format.
        
        Args:
            companies: List of Company objects to export
            format: Export format ('json', 'csv')
            filename: Custom filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"yc_companies_{timestamp}"
        
        if format.lower() == "json":
            return self._export_companies_json(companies, filename)
        elif format.lower() == "csv":
            return self._export_companies_csv(companies, filename)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def export_jobs(
        self, 
        jobs: List[Job], 
        format: str = "json",
        filename: Optional[str] = None
    ) -> str:
        """Export jobs to specified format.
        
        Args:
            jobs: List of Job objects to export
            format: Export format ('json', 'csv')
            filename: Custom filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"yc_jobs_{timestamp}"
        
        if format.lower() == "json":
            return self._export_jobs_json(jobs, filename)
        elif format.lower() == "csv":
            return self._export_jobs_csv(jobs, filename)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def export_combined(
        self,
        companies: List[Company],
        jobs: List[Job],
        format: str = "json",
        filename: Optional[str] = None
    ) -> str:
        """Export companies and jobs together.
        
        Args:
            companies: List of Company objects
            jobs: List of Job objects
            format: Export format ('json')
            filename: Custom filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"yc_scrape_results_{timestamp}"
        
        if format.lower() == "json":
            return self._export_combined_json(companies, jobs, filename)
        else:
            raise ValueError(f"Combined export only supports JSON format")
    
    def _export_companies_json(self, companies: List[Company], filename: str) -> str:
        """Export companies to JSON format."""
        filepath = self.output_dir / f"{filename}.json"
        
        # Convert to serializable format
        companies_data = []
        for company in companies:
            company_dict = company.model_dump()
            # Convert datetime objects to ISO format if any
            company_dict = self._serialize_datetime(company_dict)
            companies_data.append(company_dict)
        
        data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "total_companies": len(companies),
                "source": "Y Combinator Job Board"
            },
            "companies": companies_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(companies)} companies to {filepath}")
        return str(filepath)
    
    def _export_companies_csv(self, companies: List[Company], filename: str) -> str:
        """Export companies to CSV format."""
        filepath = self.output_dir / f"{filename}.csv"
        
        if not companies:
            # Create empty CSV with headers
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self._get_company_csv_headers())
            return str(filepath)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers
            headers = self._get_company_csv_headers()
            writer.writerow(headers)
            
            # Write company data
            for company in companies:
                row = self._company_to_csv_row(company)
                writer.writerow(row)
        
        logger.info(f"Exported {len(companies)} companies to {filepath}")
        return str(filepath)
    
    def _export_jobs_json(self, jobs: List[Job], filename: str) -> str:
        """Export jobs to JSON format."""
        filepath = self.output_dir / f"{filename}.json"
        
        # Convert to serializable format
        jobs_data = []
        for job in jobs:
            job_dict = job.model_dump()
            # Convert datetime objects to ISO format
            job_dict = self._serialize_datetime(job_dict)
            jobs_data.append(job_dict)
        
        data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "total_jobs": len(jobs),
                "source": "Y Combinator Job Board"
            },
            "jobs": jobs_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(jobs)} jobs to {filepath}")
        return str(filepath)
    
    def _export_jobs_csv(self, jobs: List[Job], filename: str) -> str:
        """Export jobs to CSV format."""
        filepath = self.output_dir / f"{filename}.csv"
        
        if not jobs:
            # Create empty CSV with headers
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self._get_job_csv_headers())
            return str(filepath)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers
            headers = self._get_job_csv_headers()
            writer.writerow(headers)
            
            # Write job data
            for job in jobs:
                row = self._job_to_csv_row(job)
                writer.writerow(row)
        
        logger.info(f"Exported {len(jobs)} jobs to {filepath}")
        return str(filepath)
    
    def _export_combined_json(self, companies: List[Company], jobs: List[Job], filename: str) -> str:
        """Export companies and jobs together in JSON format."""
        filepath = self.output_dir / f"{filename}.json"
        
        # Convert to serializable format
        companies_data = [self._serialize_datetime(c.model_dump()) for c in companies]
        jobs_data = [self._serialize_datetime(j.model_dump()) for j in jobs]
        
        data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "total_companies": len(companies),
                "total_jobs": len(jobs),
                "source": "Y Combinator Job Board"
            },
            "companies": companies_data,
            "jobs": jobs_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(companies)} companies and {len(jobs)} jobs to {filepath}")
        return str(filepath)
    
    def _get_company_csv_headers(self) -> List[str]:
        """Get CSV headers for company export."""
        return [
            "name", "description", "url", "yc_profile_url", "job_count",
            "jobs_url", "industry", "location", "team_size", "batch",
            "logo_url", "founded_year", "tags"
        ]
    
    def _get_job_csv_headers(self) -> List[str]:
        """Get CSV headers for job export."""
        return [
            "title", "company_name", "description", "location", "remote_ok",
            "location_type", "salary_min", "salary_max", "salary_currency",
            "equity_min", "equity_max", "job_type", "experience_level",
            "department", "skills_required", "education_required",
            "years_experience", "application_url", "application_email",
            "posted_date", "company_url", "company_description",
            "company_industry", "company_size", "visa_sponsorship"
        ]
    
    def _company_to_csv_row(self, company: Company) -> List[str]:
        """Convert Company object to CSV row."""
        return [
            company.name or "",
            company.description or "",
            company.url or "",
            company.yc_profile_url or "",
            str(company.job_count) if company.job_count is not None else "0",
            company.jobs_url or "",
            company.industry or "",
            company.location or "",
            company.team_size or "",
            company.batch or "",
            company.logo_url or "",
            str(company.founded_year) if company.founded_year else "",
            "|".join(company.tags) if company.tags else ""
        ]
    
    def _job_to_csv_row(self, job: Job) -> List[str]:
        """Convert Job object to CSV row."""
        return [
            job.title or "",
            job.company_name or "",
            job.description or "",
            job.location or "",
            str(job.remote_ok) if job.remote_ok is not None else "",
            job.location_type or "",
            str(job.salary_min) if job.salary_min is not None else "",
            str(job.salary_max) if job.salary_max is not None else "",
            job.salary_currency or "",
            str(job.equity_min) if job.equity_min is not None else "",
            str(job.equity_max) if job.equity_max is not None else "",
            job.job_type or "",
            job.experience_level or "",
            job.department or "",
            "|".join(job.skills_required) if job.skills_required else "",
            job.education_required or "",
            str(job.years_experience) if job.years_experience is not None else "",
            job.application_url or "",
            job.application_email or "",
            job.posted_date.isoformat() if job.posted_date else "",
            job.company_url or "",
            job.company_description or "",
            job.company_industry or "",
            job.company_size or "",
            str(job.visa_sponsorship) if job.visa_sponsorship is not None else ""
        ]
    
    def _serialize_datetime(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert datetime objects to ISO format strings."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    data[key] = self._serialize_datetime(value)
        return data
    
    def get_export_summary(self, filepath: str) -> Dict[str, Any]:
        """Get summary information about an exported file.
        
        Args:
            filepath: Path to exported file
            
        Returns:
            Dictionary with file information
        """
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return {"error": "File not found"}
            
            file_size = file_path.stat().st_size
            
            summary = {
                "filepath": str(file_path),
                "filename": file_path.name,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
            
            # Try to get record count for JSON files
            if file_path.suffix == '.json':
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'companies' in data:
                            summary['companies_count'] = len(data['companies'])
                        if 'jobs' in data:
                            summary['jobs_count'] = len(data['jobs'])
                except Exception as e:
                    summary['content_error'] = str(e)
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get export summary: {e}")
            return {"error": str(e)}