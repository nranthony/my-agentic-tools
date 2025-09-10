#!/usr/bin/env python3
"""
Environment and API key validation script.
"""
import os
import sys
from pathlib import Path
import importlib.util
from typing import Dict, List, Tuple

try:
    import httpx
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "httpx", "rich"])
    import httpx
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print

console = Console()


def check_python_packages() -> Dict[str, bool]:
    """Check if key Python packages are installed."""
    packages = {
        "requests": "requests",
        "pydantic": "pydantic", 
        "python-dotenv": "dotenv",
        "structlog": "structlog",
        "typer": "typer",
        "jupyter": "jupyter",
        "openai": "openai",
        "anthropic": "anthropic",
        "langchain": "langchain",
        "langgraph": "langgraph",
        "crewai": "crewai",
        "beautifulsoup4": "bs4",
        "selenium": "selenium",
    }
    
    results = {}
    for package_name, import_name in packages.items():
        try:
            spec = importlib.util.find_spec(import_name)
            results[package_name] = spec is not None
        except ImportError:
            results[package_name] = False
    
    return results


def check_environment_variables() -> Dict[str, Tuple[bool, str]]:
    """Check if environment variables are set."""
    env_vars = {
        "OPENAI_API_KEY": "OpenAI API access",
        "ANTHROPIC_API_KEY": "Anthropic Claude API access", 
        "LANGSMITH_API_KEY": "LangSmith tracing (optional)",
        "TAVILY_API_KEY": "Tavily search API (optional)",
        "FIRECRAWL_API_KEY": "Firecrawl web scraping (optional)",
        "NOTION_API_KEY": "Notion integration (optional)",
        "NEWS_API_KEY": "News API access (optional)",
    }
    
    results = {}
    for var_name, description in env_vars.items():
        value = os.getenv(var_name)
        is_set = value is not None and value.strip() != "" and not value.startswith("your_")
        results[var_name] = (is_set, description)
    
    return results


async def test_api_connections() -> Dict[str, Tuple[bool, str]]:
    """Test actual API connections."""
    results = {}
    
    # Test OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and not openai_key.startswith("your_"):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {openai_key}"},
                    timeout=10
                )
                results["OpenAI API"] = (response.status_code == 200, "Connection successful")
        except Exception as e:
            results["OpenAI API"] = (False, f"Connection failed: {str(e)[:50]}")
    else:
        results["OpenAI API"] = (False, "API key not configured")
    
    # Test Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and not anthropic_key.startswith("your_"):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "max_tokens": 1,
                        "messages": [{"role": "user", "content": "Hi"}]
                    },
                    timeout=10
                )
                results["Anthropic API"] = (response.status_code == 200, "Connection successful")
        except Exception as e:
            results["Anthropic API"] = (False, f"Connection failed: {str(e)[:50]}")
    else:
        results["Anthropic API"] = (False, "API key not configured")
    
    return results


def check_project_structure() -> Dict[str, bool]:
    """Check if project structure is correct."""
    expected_dirs = [
        "web-scraping",
        "document-generation",
        "langgraph-agents", 
        "crewai-workflows",
        "mcp-tools",
        "api-integrations",
        "shared",
        "notebooks",
        "scripts"
    ]
    
    results = {}
    for dir_name in expected_dirs:
        dir_path = Path(dir_name)
        results[dir_name] = dir_path.exists() and dir_path.is_dir()
    
    return results


def print_results_table(title: str, results: Dict, status_col: str = "Status"):
    """Print results in a formatted table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Item", style="cyan", no_wrap=True)
    table.add_column(status_col, style="green")
    if isinstance(list(results.values())[0], tuple):
        table.add_column("Details", style="dim")
    
    for item, result in results.items():
        if isinstance(result, tuple):
            is_ok, details = result
            status = "✅ OK" if is_ok else "❌ FAIL"
            table.add_row(item, status, details)
        else:
            status = "✅ OK" if result else "❌ MISSING"
            table.add_row(item, status)
    
    console.print(table)
    console.print()


async def main():
    """Main environment checking function."""
    console.print(Panel.fit("🔍 Environment Check for my-agentic-tools", 
                           style="bold blue"))
    console.print()
    
    # Check Python packages
    console.print("[bold yellow]Checking Python packages...[/bold yellow]")
    package_results = check_python_packages()
    print_results_table("Python Packages", package_results)
    
    # Check project structure
    console.print("[bold yellow]Checking project structure...[/bold yellow]")
    structure_results = check_project_structure()
    print_results_table("Project Structure", structure_results)
    
    # Check environment variables
    console.print("[bold yellow]Checking environment variables...[/bold yellow]")
    env_results = check_environment_variables()
    print_results_table("Environment Variables", env_results, "Configured")
    
    # Test API connections
    console.print("[bold yellow]Testing API connections...[/bold yellow]")
    api_results = await test_api_connections()
    print_results_table("API Connections", api_results, "Connection")
    
    # Summary
    total_packages = len(package_results)
    ok_packages = sum(package_results.values())
    
    total_structure = len(structure_results)
    ok_structure = sum(structure_results.values())
    
    total_env = len(env_results)
    ok_env = sum(1 for is_set, _ in env_results.values() if is_set)
    
    total_apis = len(api_results)
    ok_apis = sum(1 for is_ok, _ in api_results.values() if is_ok)
    
    console.print(Panel.fit(f"""
📊 Summary:
• Python Packages: {ok_packages}/{total_packages} OK
• Project Structure: {ok_structure}/{total_structure} OK  
• Environment Variables: {ok_env}/{total_env} configured
• API Connections: {ok_apis}/{total_apis} working

🚀 Ready to go: {ok_packages == total_packages and ok_structure == total_structure and ok_apis > 0}
    """, style="bold green" if (ok_packages == total_packages and ok_structure == total_structure) else "bold yellow"))
    
    if ok_env == 0:
        console.print(Panel.fit(
            "⚠️  No API keys configured!\nEdit the .env file to add your API keys.",
            style="bold red"
        ))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())