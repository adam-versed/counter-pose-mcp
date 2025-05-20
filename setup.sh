#!/bin/bash
# Setup script for Counter-Pose MCP Server

# Exit on error
set -e

echo "Setting up Counter-Pose MCP Server..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

# Make run scripts executable
chmod +x run_server.sh
chmod +x test_client.sh

echo "Setup complete! You can now run the server with ./run_server.sh"
