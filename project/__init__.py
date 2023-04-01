import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv as ENV_LOAD

# .env
ENV_LOAD()

# disable the AVX and AVX2 instructions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Set up app
app = Flask(__name__)
# Set up paths (database and recorded audio)
rc_path = os.path.join(os.getcwd(), "project", "temp_data")
# create directories if they don't exist
os.makedirs(rc_path, exist_ok=True)
# configuration of database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nio_records_user:mgT1zN4ALO4KUwcRAbPzkiNDnjfFX2co@dpg-cgfe6g82qv28tc6ps14g-a.singapore-postgres.render.com/nio_records"
# set up notification if modification is on set to false
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# set up secret key for secure sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

# Import routes
from project import routes