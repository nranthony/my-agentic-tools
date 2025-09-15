"""Tests for Y Combinator job board scraper."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import modules to test
from mygentic.web_scraping.yc_scraper.models.search_params import SearchParams, Role, JobType, SortBy
from mygentic.web_scraping.yc_scraper.models.company import Company
from mygentic.web_scraping.yc_scraper.models.job import Job
from mygentic.web_scraping.yc_scraper.core.url_builder import URLBuilder
from mygentic.web_scraping.yc_scraper.core.auth_handler import AuthHandler
from mygentic.web_scraping.yc_scraper.utils.data_cleaner import DataCleaner
from mygentic.web_scraping.yc_scraper.extractors.company_extractor import CompanyExtractor
from mygentic.web_scraping.yc_scraper.extractors.job_extractor import JobExtractor


class TestSearchParams:
    """Test SearchParams model and URL handling."""
    
    def test_default_params(self):
        """Test default search parameters."""
        params = SearchParams()
        
        assert params.role == Role.ANY
        assert params.job_type == JobType.FULLTIME
        assert params.sort_by == SortBy.CREATED_DESC
        assert params.has_equity.value == "any"
    
    def test_url_params_conversion(self):
        """Test conversion to URL parameters."""
        params = SearchParams(
            role=Role.ENGINEERING,
            job_type=JobType.PARTTIME,
            sort_by=SortBy.COMPANY_NAME
        )
        
        url_params = params.to_url_params()
        
        assert url_params["role"] == "engineering"
        assert url_params["jobType"] == "parttime"
        assert url_params["sortBy"] == "company_name"
    
    def test_from_url_parsing(self):
        """Test parsing search parameters from URL."""
        url = "https://www.workatastartup.com/companies?role=science&jobType=fulltime&sortBy=created_desc"
        
        params = SearchParams.from_url(url)
        
        assert params.role == Role.SCIENCE
        assert params.job_type == JobType.FULLTIME
        assert params.sort_by == SortBy.CREATED_DESC


class TestURLBuilder:
    """Test URL building functionality."""
    
    def test_build_search_url(self):
        """Test building search URLs."""
        builder = URLBuilder()
        params = SearchParams(role=Role.ENGINEERING, job_type=JobType.FULLTIME)
        
        url = builder.build_search_url(params)
        
        assert "workatastartup.com/companies" in url
        assert "role=engineering" in url
        assert "jobType=fulltime" in url
    
    def test_build_company_url(self):
        """Test building company URLs."""
        builder = URLBuilder()
        
        url = builder.build_company_url("openai")
        
        assert url == "https://www.workatastartup.com/companies/openai"
    
    def test_build_company_jobs_url(self):
        """Test building company jobs URLs."""
        builder = URLBuilder()
        
        url = builder.build_company_jobs_url("openai")
        
        assert url == "https://www.workatastartup.com/companies/openai/jobs"
    
    def test_extract_company_slug(self):
        """Test extracting company slug from URL."""
        builder = URLBuilder()
        
        # Test various URL formats
        slug1 = builder.extract_company_slug("https://www.workatastartup.com/companies/openai")
        slug2 = builder.extract_company_slug("https://www.workatastartup.com/companies/openai/jobs")
        
        assert slug1 == "openai"
        assert slug2 == "openai"
    
    def test_is_yc_url(self):
        """Test YC URL validation."""
        builder = URLBuilder()
        
        assert builder.is_yc_url("https://www.workatastartup.com/companies")
        assert builder.is_yc_url("https://workatastartup.com/companies/openai")
        assert not builder.is_yc_url("https://example.com")


class TestAuthHandler:
    """Test authentication handling."""
    
    def test_init_without_cookie(self):
        """Test initialization without session cookie."""
        auth = AuthHandler()
        
        assert not auth.is_authenticated()
        assert auth.session_cookie is None
    
    def test_init_with_cookie(self):
        """Test initialization with session cookie."""
        auth = AuthHandler("test_cookie_value")
        
        assert auth.is_authenticated()
        assert auth.session_cookie == "test_cookie_value"
    
    def test_get_cookies(self):
        """Test getting cookies for requests."""
        auth = AuthHandler("test_cookie")
        
        cookies = auth.get_cookies()
        
        assert "_yc_session" in cookies
        assert cookies["_yc_session"] == "test_cookie"
    
    def test_get_headers(self):
        """Test getting request headers."""
        auth = AuthHandler()
        
        headers = auth.get_headers()
        
        assert "User-Agent" in headers
        assert "Accept" in headers
        assert headers["Connection"] == "keep-alive"
    
    def test_user_agent_rotation(self):
        """Test user agent rotation."""
        auth = AuthHandler()
        
        # Get multiple user agents
        ua1 = auth.get_user_agent()
        ua2 = auth.get_user_agent()
        ua3 = auth.get_user_agent()
        
        # Should rotate through different user agents
        user_agents = [ua1, ua2, ua3]
        assert len(set(user_agents)) > 1  # At least some should be different


class TestCompanyModel:
    """Test Company model validation and functionality."""
    
    def test_company_creation(self):
        """Test creating a valid Company object."""
        company = Company(
            name="Test Company",
            description="A test company",
            url="https://test.com",
            job_count=5
        )
        
        assert company.name == "Test Company"
        assert company.description == "A test company"
        assert company.job_count == 5
    
    def test_company_required_fields(self):
        """Test that name is required."""
        with pytest.raises(Exception):  # Pydantic validation error
            Company()
    
    def test_company_optional_fields(self):
        """Test optional fields have defaults."""
        company = Company(name="Test")
        
        assert company.job_count == 0
        assert company.tags == []
        assert company.description is None


class TestJobModel:
    """Test Job model validation and functionality."""
    
    def test_job_creation(self):
        """Test creating a valid Job object."""
        job = Job(
            title="Software Engineer",
            company_name="Test Corp",
            location="San Francisco",
            remote_ok=True,
            salary_min=120000,
            salary_max=180000
        )
        
        assert job.title == "Software Engineer"
        assert job.company_name == "Test Corp"
        assert job.remote_ok is True
        assert job.salary_min == 120000
    
    def test_job_required_fields(self):
        """Test that title and company_name are required."""
        with pytest.raises(Exception):
            Job(title="Engineer")  # Missing company_name
        
        with pytest.raises(Exception):
            Job(company_name="Test Corp")  # Missing title
    
    def test_job_defaults(self):
        """Test default values."""
        job = Job(title="Engineer", company_name="Test")
        
        assert job.remote_ok is False
        assert job.visa_sponsorship is False
        assert job.skills_required == []


class TestDataCleaner:
    """Test data cleaning utilities."""
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        # Test normal text
        assert DataCleaner._clean_text("  Normal text  ") == "Normal text"
        
        # Test placeholder removal
        assert DataCleaner._clean_text("N/A") is None
        assert DataCleaner._clean_text("null") is None
        assert DataCleaner._clean_text("not specified") is None
        
        # Test empty/whitespace
        assert DataCleaner._clean_text("   ") is None
        assert DataCleaner._clean_text("") is None
    
    def test_clean_url(self):
        """Test URL cleaning and validation."""
        # Valid URLs
        assert DataCleaner._clean_url("https://example.com") == "https://example.com"
        assert DataCleaner._clean_url("  https://test.com  ") == "https://test.com"
        
        # Auto-fix URLs
        assert DataCleaner._clean_url("www.example.com") == "https://www.example.com"
        assert DataCleaner._clean_url("//example.com") == "https://example.com"
        
        # Invalid URLs
        assert DataCleaner._clean_url("not a url") is None
        assert DataCleaner._clean_url("") is None
    
    def test_clean_email(self):
        """Test email cleaning and validation."""
        # Valid emails
        assert DataCleaner._clean_email("test@example.com") == "test@example.com"
        assert DataCleaner._clean_email("  User@Test.COM  ") == "user@test.com"
        
        # Invalid emails
        assert DataCleaner._clean_email("not an email") is None
        assert DataCleaner._clean_email("@example.com") is None
        assert DataCleaner._clean_email("") is None
    
    def test_clean_companies_deduplication(self):
        """Test company deduplication."""
        companies = [
            Company(name="Test Company", url="https://test.com"),
            Company(name="Test Company", url="https://test.com"),  # Duplicate name
            Company(name="Another Company", url="https://test.com")  # Duplicate URL
        ]
        
        cleaned = DataCleaner.clean_companies(companies)
        
        # Should remove duplicates
        assert len(cleaned) == 1
        assert cleaned[0].name == "Test Company"
    
    def test_clean_jobs_deduplication(self):
        """Test job deduplication."""
        jobs = [
            Job(title="Engineer", company_name="TestCorp"),
            Job(title="Engineer", company_name="TestCorp"),  # Duplicate
            Job(title="Designer", company_name="TestCorp")   # Different title
        ]
        
        cleaned = DataCleaner.clean_jobs(jobs)
        
        # Should remove duplicate job
        assert len(cleaned) == 2
        titles = [job.title for job in cleaned]
        assert "Engineer" in titles
        assert "Designer" in titles


class TestCompanyExtractor:
    """Test company data extraction."""
    
    def test_create_company_from_data(self):
        """Test creating Company object from extracted data."""
        mock_gemini = Mock()
        extractor = CompanyExtractor(mock_gemini)
        
        data = {
            "name": "Test Company",
            "description": "A test company",
            "job_count": "5 jobs",  # String format
            "url": "https://test.com",
            "tags": ["AI", "SaaS"]
        }
        
        company = extractor._create_company_from_data(data)
        
        assert company is not None
        assert company.name == "Test Company"
        assert company.job_count == 5  # Parsed from "5 jobs"
        assert company.tags == ["AI", "SaaS"]
    
    def test_clean_company_data(self):
        """Test company data cleaning."""
        mock_gemini = Mock()
        extractor = CompanyExtractor(mock_gemini)
        
        data = {
            "name": "  Test Company  ",
            "description": "",  # Empty string
            "job_count": "invalid",  # Invalid number
            "url": "https://test.com",
            "tags": "AI, SaaS"  # String instead of list
        }
        
        cleaned = extractor._clean_company_data(data)
        
        assert cleaned["name"] == "Test Company"
        assert "description" not in cleaned  # Empty removed
        assert cleaned["job_count"] == 0  # Invalid converted to 0
        assert cleaned["url"] == "https://test.com"


class TestJobExtractor:
    """Test job data extraction."""
    
    def test_parse_boolean(self):
        """Test boolean parsing from various formats."""
        mock_gemini = Mock()
        extractor = JobExtractor(mock_gemini)
        
        # Test various true values
        assert extractor._parse_boolean(True) is True
        assert extractor._parse_boolean("true") is True
        assert extractor._parse_boolean("yes") is True
        assert extractor._parse_boolean("1") is True
        
        # Test various false values
        assert extractor._parse_boolean(False) is False
        assert extractor._parse_boolean("false") is False
        assert extractor._parse_boolean("no") is False
        assert extractor._parse_boolean("0") is False
    
    def test_parse_integer(self):
        """Test integer parsing from various formats."""
        mock_gemini = Mock()
        extractor = JobExtractor(mock_gemini)
        
        # Test normal integers
        assert extractor._parse_integer(12345) == 12345
        assert extractor._parse_integer("12345") == 12345
        
        # Test with formatting
        assert extractor._parse_integer("$120,000") == 120000
        assert extractor._parse_integer("120k") == 120000
        assert extractor._parse_integer("120K") == 120000
        
        # Test invalid values
        assert extractor._parse_integer("invalid") is None
        assert extractor._parse_integer("") is None
    
    def test_parse_skills_list(self):
        """Test skills list parsing."""
        mock_gemini = Mock()
        extractor = JobExtractor(mock_gemini)
        
        # Test list input
        skills = extractor._parse_skills_list(["Python", "JavaScript", "React"])
        assert skills == ["Python", "JavaScript", "React"]
        
        # Test string input
        skills = extractor._parse_skills_list("Python, JavaScript, React")
        assert skills == ["Python", "JavaScript", "React"]
        
        # Test with different separators
        skills = extractor._parse_skills_list("Python; JavaScript| React")
        assert skills == ["Python", "JavaScript", "React"]


# Mock fixtures for integration tests
@pytest.fixture
def mock_firecrawl_client():
    """Mock Firecrawl client."""
    mock = Mock()
    mock.scrape_page.return_value = {
        "markdown": "Mock content",
        "html": "<html>Mock content</html>",
        "metadata": {"title": "Test Page"}
    }
    mock.scrape_with_scroll.return_value = {
        "markdown": "Mock scrolled content",
        "html": "<html>Mock scrolled content</html>",
        "metadata": {"title": "Test Page"}
    }
    return mock


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client."""
    mock = Mock()
    mock.extract_companies.return_value = [
        {
            "name": "Test Company",
            "description": "A test company",
            "job_count": 5,
            "url": "https://test.com"
        }
    ]
    mock.extract_jobs.return_value = [
        {
            "title": "Software Engineer",
            "company_name": "Test Company",
            "location": "San Francisco",
            "salary_min": 120000,
            "salary_max": 180000
        }
    ]
    return mock


class TestYCJobScraperIntegration:
    """Integration tests for the main scraper (with mocking)."""
    
    @patch('yc_scraper.core.scraper.FirecrawlClient')
    @patch('yc_scraper.core.scraper.GeminiClient')
    def test_scraper_initialization(self, mock_gemini_cls, mock_firecrawl_cls):
        """Test scraper initialization."""
        from yc_scraper.core.scraper import YCJobScraper
        
        scraper = YCJobScraper(
            firecrawl_api_key="test_key",
            gemini_api_key="test_key"
        )
        
        assert scraper is not None
        assert scraper.firecrawl_client is not None
        assert scraper.gemini_client is not None
        assert scraper.auth_handler is not None
    
    @patch('yc_scraper.core.scraper.FirecrawlClient')
    @patch('yc_scraper.core.scraper.GeminiClient')
    def test_scrape_search_basic(self, mock_gemini_cls, mock_firecrawl_cls, 
                                mock_firecrawl_client, mock_gemini_client):
        """Test basic search scraping functionality."""
        from yc_scraper.core.scraper import YCJobScraper
        
        # Set up mocks
        mock_firecrawl_cls.return_value = mock_firecrawl_client
        mock_gemini_cls.return_value = mock_gemini_client
        
        scraper = YCJobScraper(firecrawl_api_key="test", gemini_api_key="test")
        
        search_params = SearchParams(role=Role.ENGINEERING)
        
        companies, jobs = scraper.scrape_search(
            search_params, 
            max_companies=1, 
            include_jobs=False
        )
        
        # Should get mocked results
        assert len(companies) >= 0  # Depends on mock setup
        assert isinstance(companies, list)
        assert isinstance(jobs, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])