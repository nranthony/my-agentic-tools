#!/usr/bin/env python3
"""
Code linting and formatting script.
"""
import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def run_command(command: List[str], check_only: bool = False) -> bool:
    """Run a command and return True if successful."""
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        success = result.returncode == 0
        if success:
            print(f"✅ {command[0]} passed")
        else:
            print(f"❌ {command[0]} failed")
        
        return success
    except FileNotFoundError:
        print(f"❌ {command[0]} not found - install with 'pip install {command[0]}'")
        return False


def get_python_files() -> List[str]:
    """Get list of Python files to process."""
    python_dirs = [
        "web-scraping",
        "document-generation", 
        "langgraph-agents",
        "crewai-workflows",
        "mcp-tools",
        "api-integrations",
        "shared",
        "scripts",
        "notebooks"
    ]
    
    files = ["setup.py"]
    
    for dir_name in python_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            # Add Python files from each directory
            files.extend(str(p) for p in dir_path.rglob("*.py"))
    
    return files


def run_black(files: List[str], check_only: bool = False) -> bool:
    """Run Black code formatter."""
    command = ["black"]
    if check_only:
        command.append("--check")
    command.extend(files)
    return run_command(command, check_only)


def run_isort(files: List[str], check_only: bool = False) -> bool:
    """Run isort import formatter.""" 
    command = ["isort"]
    if check_only:
        command.append("--check-only")
    command.extend(files)
    return run_command(command, check_only)


def run_flake8(files: List[str]) -> bool:
    """Run flake8 linter."""
    command = ["flake8"] + files
    return run_command(command, check_only=True)


def run_mypy() -> bool:
    """Run mypy type checker."""
    python_dirs = [
        "web-scraping",
        "document-generation",
        "langgraph-agents", 
        "crewai-workflows",
        "mcp-tools",
        "api-integrations",
        "shared"
    ]
    
    success = True
    for dir_name in python_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            command = ["mypy", str(dir_path)]
            success &= run_command(command, check_only=True)
    
    return success


def main():
    """Main linting and formatting function."""
    parser = argparse.ArgumentParser(description="Lint and format Python code")
    parser.add_argument("--check", action="store_true", 
                       help="Check only, don't modify files")
    parser.add_argument("--skip-mypy", action="store_true",
                       help="Skip mypy type checking")
    parser.add_argument("--files", nargs="*",
                       help="Specific files to process (default: all Python files)")
    
    args = parser.parse_args()
    
    # Get files to process
    if args.files:
        files = args.files
    else:
        files = get_python_files()
        if not files:
            print("No Python files found")
            return 0
    
    print(f"Processing {len(files)} Python files...")
    print("=" * 50)
    
    success = True
    
    # Run Black
    print("\n🖤 Running Black (code formatter)...")
    success &= run_black(files, args.check)
    
    # Run isort
    print("\n📋 Running isort (import formatter)...")
    success &= run_isort(files, args.check)
    
    # Run flake8
    print("\n🔍 Running flake8 (linter)...")
    success &= run_flake8(files)
    
    # Run mypy (optional)
    if not args.skip_mypy:
        print("\n🔬 Running mypy (type checker)...")
        success &= run_mypy()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All code quality checks passed!")
        return 0
    else:
        print("❌ Some code quality checks failed")
        if not args.check:
            print("Run this script again to fix formatting issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())