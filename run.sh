#!/bin/bash

echo "Mar-Automation..."

# Check if virtual environment exists
if [ ! -d .venv ]; then
  echo "Creating a new virtual environment..."
  python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install FFmpeg
sudo apt update && sudo add-apt-repository universe && sudo apt update && sudo apt install ffmpeg -y

# Install required Python packages
echo "Installing Python packages..."
pip install --upgrade --no-deps -r others/requirements.txt

# Change to the parent directory of the script
cd /workspaces/NIO-Application/project

# Run the postcss command
echo "Running npm..."
npm install &