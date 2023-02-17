__version__ = "0.3"
__docformat__ = "restructuredtext en"

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
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db_name = 'records.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# routes here
from project import routes

UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = '../app/temp_data/text'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkeysecretkey'

from flask_login import UserMixin
