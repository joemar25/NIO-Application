"""
    REMEMBER!
        the line - from project import routes
        must be put after db = SQLAlchemy(app)
        or end of the line in this __init__ file

        reason: for the api.py to run
        
    the imports
        os is used in randomizing our secret key
        flask sql alchemy is for database
        flask is used as framework
        
        upload folder contains the area where we upload file/save file
        
"""
from flask_login import UserMixin
from project import routes
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db_path = os.getcwd() + "/project/database/"
db_name = 'records.db'
db_file = db_path + db_name

if not os.path.exists(db_path):
    os.makedirs(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# routes here

UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = '../app/temp_data/text'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkeysecretkey'
