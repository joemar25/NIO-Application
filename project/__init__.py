import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize a Flask app instance
app = Flask(__name__)

# Set the path to the database directory, name of the database file, and create the full path to the database file
db_path = os.getcwd() + "/project/database/"
db_name = 'records.db'
db_file = db_path + db_name

# temp data file path
temp_path = os.getcwd() + "/project/temp_data/"

# Create the database directory if it does not exist
if not os.path.exists(db_path):
    os.makedirs(db_path)
    
# create temp folder
if not os.path.exists(temp_path):
    os.makedirs(temp_path)

# Set the configuration options for the app, including the location of the database file and whether to track modifications to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize the SQLAlchemy database object with the app instance
db = SQLAlchemy(app)

# Import the routes for the app
# NOTE: This import statement must be put after the initialization of the db object, or at the end of the file
from project import routes

# Set the configuration options for file uploads
UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = '../app/temp_data/text'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkeysecretkey'

# Import the UserMixin class from Flask-Login
from flask_login import UserMixin
