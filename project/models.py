from flask_login import UserMixin
from project import app, db
from datetime import datetime
from sqlalchemy import inspect

# The UserMixin class provides the implementation for Flask-Login's required properties
# for user models, so we inherit from it to ensure our User model is compatible.
class User(db.Model, UserMixin):
    # Define the columns for the User table.
    id = db.Column('id', db.Integer, primary_key=True)
    user_name = db.Column('user_name', db.String(length=21), unique=False, nullable=False)
    text = db.Column('text', db.Text, nullable=False)
    ctext = db.Column('ctext', db.Text, nullable=True)
    datetime = db.Column('timestamp', db.DateTime, default=datetime.utcnow)

    # Define the one-to-many relationship between User and Score. The lazy='dynamic'
    # option is used to ensure that the related objects are not loaded until explicitly requested.
    scores = db.relationship('Score', backref='user', lazy='dynamic')

# Define the Score model to represent a user's score for a specific task.
class Score(db.Model):
    # Define the columns for the Score table.
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    audio = db.Column('audio', db.Text, unique=True, nullable=False, default=None)
    transcribed = db.Column('transcribed', db.Text, unique=False, nullable=False, default="no transcription")
    rate = db.Column('rate', db.Float(), unique=False, nullable=False, default=0)
    grammar = db.Column('grammar', db.Float(), unique=False, nullable=False, default=0)
    fluency = db.Column('fluency', db.Float(), unique=False, nullable=False, default=0)

# Use the SQLAlchemy inspect() method to check if the table already exists in the database.
# If it does not exist, create it using db.create_all().
with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table('table_name'):
        db.create_all()