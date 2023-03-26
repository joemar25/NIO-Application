#!/bin/bash

echo "Mar-Automation..."

# Upgrading pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install flask
pip install flask

# Install FFmpeg
sudo apt update && sudo add-apt-repository universe && sudo apt update && sudo apt install ffmpeg -y

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
