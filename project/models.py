# Define the User, Score, and Audio models to store user data, scores, and audio information.
# The User model inherits from the UserMixin class to ensure compatibility with Flask-Login's
# required properties. The models define columns for various data types and relationships
# between tables. The code checks if a specific table exists in the database using SQLAlchemy's
# inspect() method and creates it using db.create_all() if it doesn't exist within the app context.

from project import app, db
from sqlalchemy import inspect
from flask_login import UserMixin
from datetime import datetime

# Define the User model to store user information, inheriting from the UserMixin class to
# ensure compatibility with Flask-Login's required properties. The model has columns for
# the user's ID, username, script, creation date, and a relationship to Score objects.
# The init method sets the username, script, and optional created_date if provided.


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    script = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    scores = db.relationship('Score', backref='user', lazy=True)

    def __init__(self, username, script=None, created_date=None):
        self.username = username
        self.script = script
        if created_date is None:
            created_date = datetime.utcnow()
        self.created_date = created_date

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grammar = db.Column(db.Float)
    fluency = db.Column(db.Float)
    rate = db.Column(db.Float)
    audio = db.relationship('Audio', uselist=False, backref='score')

    def __init__(self, user_id, grammar=None, fluency=None, rate=None):
        self.user_id = user_id
        self.grammar = grammar
        self.fluency = fluency
        self.rate = rate

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'), nullable=False)
    audio_name = db.Column(db.String(255), nullable=False)
    transcribed = db.Column(db.String(255))
    ctranscribed = db.Column(db.String(255))
    emotion_labels = db.Column(db.String(255))
    emotion_scores = db.Column(db.String(255))

    def __init__(self, score_id, audio_name, transcribed=None, ctranscribed=None, emotion_labels=None, emotion_scores=None):
        self.score_id = score_id
        self.audio_name = audio_name
        self.transcribed = transcribed
        self.ctranscribed = ctranscribed
        self.emotion_labels = emotion_labels
        self.emotion_scores = emotion_scores


# Check if the 'table_name' table already exists in the database using SQLAlchemy's
# inspect() method. If it doesn't exist, create it using db.create_all() within the
# app context to ensure proper database connection.

with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table('table_name'):
        db.create_all()
