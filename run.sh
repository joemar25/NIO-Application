#!/bin/bash

# Check if Python 3 is installed
if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: Python 3 is not installed.' >&2
  exit 1
fi

# Check if pip is installed
if ! [ -x "$(command -v pip3)" ]; then
  echo 'Error: pip is not installed.' >&2
  exit 1
fi

# Check if virtualenv is installed
if ! [ -x "$(command -v virtualenv)" ]; then
  echo 'virtualenv is not installed. Installing virtualenv...'
  pip3 install virtualenv
fi

# Create a virtual environment and activate it
if [ ! -d venv ]; then
  echo 'Creating a new virtual environment...'
  virtualenv venv
fi
source venv/bin/activate

# Install required Python packages
echo 'Installing Python packages...'
pip3 install -r others/requirements.txt

# Start the Flask app
echo 'Starting Flask app...'
flask run
