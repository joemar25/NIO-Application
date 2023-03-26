#!/bin/bash

echo "Mar-Automation..."

# Check if virtual environment exists
if [ ! -d .venv ]; then
  echo "Creating a new virtual environment..."
  python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrading pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install FFmpeg
apt update && add-apt-repository universe && apt update && apt install ffmpeg -y

# Install required Python packages
echo "Installing Python packages..."
pip install -r requirements.txt


# Change to the project directory
cd project

# Run the postcss command
echo "Running npm..."
npm install

# Run dev and bfy commands
npm run dev &
npm run bfy &

cd ..

# Install gunicorn if not already installed
if ! pip list | grep -q gunicorn; then
  echo "Installing gunicorn..."
  pip install gunicorn
fi