import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv as env_load

# .env
env_load()

# disable the AVX and AVX2 instructions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Set up app
app = Flask(__name__)
# Set up paths (database and recorded audio)
rc_path = os.path.join(os.getcwd(), "project", "temp_data")
# create directories if they don't exist
os.makedirs(rc_path, exist_ok=True)
# configuration of database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# set up notification if modification is on set to false
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# set up secret key for secure sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

mode = "dev" # dev or prod

# Import routes
from project import routes