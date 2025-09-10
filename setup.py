#!/usr/bin/env python3
"""
Development environment setup script for my-agentic-tools.
"""
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None, check=True):
    """Run a shell command and print the output."""
    print(f"Running: {command}")
    if cwd:
        print(f"  in directory: {cwd}")
    
    result = subprocess.run(
        command, 
        shell=True, 
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result


def check_python_version():
    """Ensure Python 3.9+ is being used."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("Error: Python 3.9 or higher is required")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")


def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv .venv")
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")


def install_base_dependencies():
    """Install the main project with core dependencies."""
    print("Installing base project with core dependencies...")
    run_command("pip install -e .")
    print("✓ Base dependencies installed")


def install_project_dependencies():
    """Install each project's dependencies."""
    projects = [
        "web-scraping",
        "document-generation", 
        "langgraph-agents",
        "crewai-workflows",
        "mcp-tools",
        "api-integrations",
        "shared"
    ]
    
    for project in projects:
        project_path = Path(project)
        if project_path.exists():
            print(f"Installing {project}...")
            run_command("pip install -e .", cwd=project_path)
            print(f"✓ {project} installed")


def install_development_tools():
    """Install development and testing tools."""
    print("Installing development tools...")
    run_command("pip install -e .[dev]")
    print("✓ Development tools installed")


def create_env_file():
    """Create a template .env file if it doesn't exist."""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# API Keys for Agentic Tools
# Copy this file and add your actual API keys

# Core AI APIs
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# LangChain/LangSmith
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=my-agentic-tools

# Search APIs
TAVILY_API_KEY=your_tavily_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_cse_id_here

# Document Services
FIRECRAWL_API_KEY=your_firecrawl_key_here

# Social Media APIs
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
LINKEDIN_CLIENT_ID=your_linkedin_client_id_here

# Productivity APIs
NOTION_API_KEY=your_notion_api_key_here
SLACK_BOT_TOKEN=your_slack_bot_token_here

# Data APIs
NEWS_API_KEY=your_news_api_key_here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here

# Development Settings
LOG_LEVEL=INFO
DEBUG=false
"""
        env_file.write_text(env_content)
        print("✓ Template .env file created - add your API keys!")
    else:
        print("✓ .env file already exists")


def setup_git_hooks():
    """Set up git hooks for code quality."""
    hooks_dir = Path(".git/hooks")
    if hooks_dir.exists():
        pre_commit_hook = hooks_dir / "pre-commit"
        if not pre_commit_hook.exists():
            hook_content = """#!/bin/sh
# Pre-commit hook to run code quality checks
python scripts/lint_and_format.py --check
if [ $? -ne 0 ]; then
    echo "Code quality checks failed. Run 'python scripts/lint_and_format.py' to fix."
    exit 1
fi
"""
            pre_commit_hook.write_text(hook_content)
            os.chmod(pre_commit_hook, 0o755)
            print("✓ Git pre-commit hook installed")
        else:
            print("✓ Git pre-commit hook already exists")


def print_next_steps():
    """Print instructions for getting started."""
    print("\n" + "="*50)
    print("🎉 Setup completed successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    print("   source .venv/bin/activate  # Linux/Mac")
    print("   .venv\\Scripts\\activate     # Windows")
    print("\n2. Edit the .env file and add your API keys")
    print("\n3. Run a quick test:")
    print("   python scripts/env_checker.py")
    print("\n4. Explore the notebooks:")
    print("   jupyter lab")
    print("\n5. Check out the project READMEs for specific usage instructions")
    print("\nHappy coding! 🚀")


def main():
    """Main setup function."""
    print("Setting up my-agentic-tools development environment...")
    print("="*50)
    
    check_python_version()
    create_virtual_environment()
    install_base_dependencies() 
    install_project_dependencies()
    install_development_tools()
    create_env_file()
    setup_git_hooks()
    print_next_steps()


if __name__ == "__main__":
    main()