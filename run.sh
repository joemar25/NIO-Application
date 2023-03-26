#!/bin/bash
echo "Mar-Automation..."

# Upgrading pip
echo "Upgrading pip..."
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

cd ..
