"""
This script sets up a Flask application with a SQLite database, secure sessions, and a Firebase configuration.
The script also creates the necessary directories and loads environment variables from the .env file.

Dependencies:
    - Flask, Flask_SQLAlchemy, firebase, dotenv

Author: NioAppTeam
Date: April 12, 2023
"""

import os
import firebase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv as env_load

# Load environment variables
env_load()

# Disable AVX and AVX2 instructions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize Flask app
app = Flask(__name__)

# Set up paths for storing database and audio files
# rc_path = os.path.join(os.getcwd(), "project", "temp_data") -> comment for now

# Create directories if they don't exist
# os.makedirs(rc_path, exist_ok=True) -> make dir comment for now

# Set up database configuration
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get Secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Firebase configuration
config = {
    'apiKey': os.getenv('apiKey'),
    'authDomain': os.getenv('authDomain'),
    "databaseURL": os.getenv('databaseURL'),
    'projectId': os.getenv('projectId'),
    'storageBucket': os.getenv('storageBucket'),
    'messagingSenderId': os.getenv('messagingSenderId'),
    'appId': os.getenv('appId'),
    'measurementId': os.getenv('measurementId')
}

config = firebase.initialize_app(config)
storage = config.storage()

# Mode of the application
mode = "dev"

# Import routes
from project import routes
