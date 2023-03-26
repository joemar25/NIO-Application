#!/bin/bash

echo "Mar-Automation..."

# Check if virtual environment exists
if [ ! -d .venv ]; then
  echo "Creating a new virtual environment..."
  python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install required Python packages
echo "Installing Python packages..."
pip install --upgrade --no-deps -r requirements.txt

# Change directory to the project folder
cd "$(dirname "$0")/../NIO-APPLICATION/project"

# Run the postcss command
echo "Running npm..."
npm install &
