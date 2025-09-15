#!/bin/bash

# MyGentic Conda Environment Setup Script
# This script creates and sets up the mygentic conda environment from scratch

set -e  # Exit on any error

echo "======================================================"
echo "🚀 MyGentic Conda Environment Setup"
echo "======================================================"

# Check if mamba is available, fallback to conda
if command -v mamba &> /dev/null; then
    CONDA_CMD="mamba"
    echo "✓ Using mamba for faster package resolution"
else
    CONDA_CMD="conda"
    echo "✓ Using conda"
fi

# Remove existing environment if it exists
echo ""
echo "🧹 Cleaning up existing environment..."
if conda env list | grep -q "^mygentic "; then
    echo "Removing existing 'mygentic' environment..."
    conda env remove -n mygentic -y
    echo "✓ Existing environment removed"
else
    echo "✓ No existing environment to remove"
fi

# Create new environment from environment.yml
echo ""
echo "🔨 Creating new conda environment..."
$CONDA_CMD env create -f environment.yml

echo ""
echo "✅ Environment created successfully!"

# Provide activation instructions
echo ""
echo "======================================================"
echo "🎉 Setup Complete!"
echo "======================================================"
echo ""
echo "Next steps:"
echo "1. Activate the environment:"
echo "   conda activate mygentic"
echo ""
echo "2. Install the project in development mode:"
echo "   cd mygentic && pip install -e ."
echo ""
echo "3. Run the development setup:"
echo "   python dev_setup.py"
echo ""
echo "4. Test the installation:"
echo "   python scripts/env_checker.py"
echo ""
echo "Happy coding! 🚀"