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
    # Check if mygentic is currently active and deactivate if so
    if [[ "$CONDA_DEFAULT_ENV" == "mygentic" ]]; then
        echo "Deactivating currently active 'mygentic' environment..."
        conda deactivate
    fi
    echo "Removing existing 'mygentic' environment..."
    conda env remove -n mygentic -y
    echo "✓ Existing environment removed"
else
    echo "✓ No existing environment to remove"
fi

# Create new environment from environment.yml
echo ""
echo "🔨 Creating new conda environment..."
$CONDA_CMD env create -f environment.yml -y

echo ""
echo "✅ Environment created successfully!"

# Provide activation instructions and offer to continue setup
echo ""
echo "======================================================"
echo "🎉 Environment Created Successfully!"
echo "======================================================"
echo ""
echo "Would you like to continue with the development setup? (Y/n)"
read -r response
if [[ -z "$response" || "$response" == "y" || "$response" == "Y" || "$response" == "yes" || "$response" == "YES" ]]; then
    echo ""
    echo "🔧 Continuing with development setup..."
    
    # Step 1: Activate environment (source it for this script)
    echo ""
    echo "1️⃣ Activating mygentic environment..."
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate mygentic
    echo "✓ Environment activated"
    
    # Step 2: Install project in development mode
    echo ""
    echo "2️⃣ Installing project in development mode..."
    pip install -e ./mygentic
    echo "✓ Project installed in development mode"
    
    # Step 3: Run development setup
    echo ""
    echo "3️⃣ Running development setup..."
    python dev_setup.py
    
    # Step 4: Test installation
    echo ""
    echo "Would you like to test the installation? (Y/n)"
    read -r test_response
    if [[ -z "$test_response" || "$test_response" == "y" || "$test_response" == "Y" || "$test_response" == "yes" || "$test_response" == "YES" ]]; then
        echo ""
        echo "4️⃣ Testing installation..."
        python scripts/env_checker.py
    else
        echo "✓ Skipping installation test"
        echo ""
        echo "To test later, run: python scripts/env_checker.py"
    fi
    
    echo ""
    echo "======================================================"
    echo "🎉 Complete Setup Finished!"
    echo "======================================================"
    echo "Happy coding! 🚀"
else
    echo ""
    echo "✓ Environment created. Manual setup steps:"
    echo "1. Activate the environment:"
    echo "   conda activate mygentic"
    echo ""
    echo "2. Install the project in development mode:"
    echo "   pip install -e ./mygentic"
    echo ""
    echo "3. Run the development setup:"
    echo "   python dev_setup.py"
    echo ""
    echo "4. Test the installation:"
    echo "   python scripts/env_checker.py"
    echo ""
    echo "Happy coding! 🚀"
fi