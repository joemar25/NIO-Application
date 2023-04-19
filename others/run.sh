#!/bin/bash
echo "Mar-Automation..."

# Upgrading pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install FFmpeg
# sudo apt update && sudo add-apt-repository universe && sudo apt update && sudo apt install ffmpeg -y

# Install required Python packages
echo "Installing Python packages..."
# pip install -r req.txt
pip install future --use-pep517
pip install openai-whisper==20230117
pip install tensorflow==2.11.0
pip install firebase-rest-api
pip install flask
pip install Flask-WTF
pip install Flask-Login
pip install Flask-SQLAlchemy
pip install Werkzeug
pip install pydub
pip install pytz
pip install nltk
pip install librosa
pip install psycopg2-binary
pip install gunicorn
pip install python-dotenv
pip install my-voice-analysis
pip install protobuf==3.20.0

# Change to the project directory
cd project

# Run the postcss command
echo "Running npm..."
npm install

cd ..