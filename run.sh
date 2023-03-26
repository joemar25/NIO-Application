#!/bin/bash

echo "Mar-Automation..."

# Upgrading pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install libries
pip install flask
pip install Flask-WTF
pip install Flask-Login
pip install Flask-SQLAlchemy
pip install Werkzeug
pip install Flask-SQLAlchemy
pip install pytz
pip install psycopg2-binary
pip install gunicorn
pip install nltk
pip install librosa
pip install pydub
pip install openai-whisper
pip install tensorflow
pip install keras

# Install FFmpeg
# sudo apt update && sudo add-apt-repository universe && sudo apt update && sudo apt install ffmpeg -y

# Install gunicorn if not already installed
if ! pip list | grep -q gunicorn; then
  echo "Installing gunicorn..."
  pip install gunicorn
fi

# Change to the project directory
cd project

# Run the postcss command
echo "Running npm..."
npm install

cd ..

