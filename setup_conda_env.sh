#!/bin/bash

# MyGentic Conda Environment Setup Script
# This script creates and sets up the mygentic conda environment from scratch
# Usage: ./setup_conda_env.sh [--update]

set -e  # Exit on any error

# ------------------------------------------------------------------
# INITIALIZE CONDA - This makes 'conda activate/deactivate' work
source "$(conda info --base)/etc/profile.d/conda.sh"
# ------------------------------------------------------------------

# Parse command line arguments
UPDATE_MODE=false
if [[ "$1" == "--update" ]]; then
    UPDATE_MODE=true
fi

echo "======================================================"
if [[ "$UPDATE_MODE" == true ]]; then
    echo "🔄 MyGentic Conda Environment Update"
else
    echo "🚀 MyGentic Conda Environment Setup"
fi
echo "======================================================"

# Check if mamba is available, fallback to conda
if command -v mamba &> /dev/null; then
    CONDA_CMD="mamba"
    echo "✓ Using mamba for faster package resolution"
else
    CONDA_CMD="conda"
    echo "✓ Using conda"
fi

# Handle existing environment
echo ""
if conda env list | grep -q "^mygentic "; then
    if [[ "$UPDATE_MODE" == true ]]; then
        echo "🔄 Updating existing mygentic environment..."
        # Check if mygentic is currently active and deactivate if so
        if [[ "$CONDA_DEFAULT_ENV" == "mygentic" ]]; then
            echo "Deactivating currently active 'mygentic' environment..."
            conda deactivate
        fi
        echo "Updating environment with --prune flag..."
        $CONDA_CMD env update -n mygentic -f environment.yml --prune -y
        echo "✅ Environment updated successfully!"
    else
        echo "🧹 Cleaning up existing environment..."
        # Check if mygentic is currently active and deactivate if so
        if [[ "$CONDA_DEFAULT_ENV" == "mygentic" ]]; then
            echo "Deactivating currently active 'mygentic' environment..."
            conda deactivate
        fi
        echo "Removing existing 'mygentic' environment..."
        conda env remove -n mygentic -y
        echo "✓ Existing environment removed"

        # Create new environment from environment.yml
        echo ""
        echo "🔨 Creating new conda environment..."
        $CONDA_CMD env create -f environment.yml -y
        echo "✅ Environment created successfully!"
    fi
else
    if [[ "$UPDATE_MODE" == true ]]; then
        echo "⚠️  No existing environment found. Creating new environment instead..."
    else
        echo "✓ No existing environment to remove"
    fi

    # Create new environment from environment.yml
    echo ""
    echo "🔨 Creating new conda environment..."
    $CONDA_CMD env create -f environment.yml -y
    echo "✅ Environment created successfully!"
fi

# Step 1: Activate environment (source it for this script)
echo ""
echo "1️⃣ Activating mygentic environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate mygentic
echo "✓ Environment activated"
    
# Step 2: Install project in development mode
echo ""
echo "2️⃣ Installing project in development mode..."
pip install -e .
echo "✓ Project installed in development mode"

echo ""
echo "======================================================"
echo "🎉 Complete Setup Finished!"
echo "======================================================"
echo "Happy coding! 🚀"