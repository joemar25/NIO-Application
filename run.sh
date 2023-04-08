#!/bin/bash
echo "Mar-Automation..."

# Upgrading pip
echo "Upgrading pip..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install FFmpeg
# sudo apt update && sudo add-apt-repository universe && sudo apt update && sudo apt install ffmpeg -y

# Install required Python packages
echo "Installing Python packages..."
pip install -r requirements.txt

# Change to the project directory
cd project

# Run the postcss command
echo "Running npm..."
npm install

# Install required Python packages
echo "Installing Python packages..."
pip install gunicorn

cd ..
