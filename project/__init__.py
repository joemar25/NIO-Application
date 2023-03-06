import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set up app
app = Flask(__name__)

# Set up paths (database and recorded audio)
db_path = os.path.join(os.getcwd(), "project", "database", "records.db")
rc_path = os.path.join(os.getcwd(), "project", "temp_data")

# create directories if they don't exist
os.makedirs(os.path.dirname(db_path), exist_ok=True)
os.makedirs(rc_path, exist_ok=True)

# configuration of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up secret key for secure sessions
app.config['SECRET_KEY'] = "1A1q21u231z4d1a241sdA123Ja567s87daOEadM99a9da0Asd5Rop"

# Import routes
from project import routes
