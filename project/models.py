from flask_login import UserMixin
from project import app, db
from datetime import datetime
from sqlalchemy import inspect

# The UserMixin class provides the implementation for Flask-Login's required properties
# for user models, so we inherit from it to ensure our User model is compatible
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    script = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    scores = db.relationship('Score', backref='user', lazy=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grammar = db.Column(db.Float, nullable=False)
    fluency = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    audio = db.relationship('Audio', uselist=False, backref='score')

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'), nullable=False)
    audio_name = db.Column(db.String(255), nullable=False)
    transcribed = db.Column(db.String(255))
    ctranscribed = db.Column(db.String(255))
    emotion_labels = db.Column(db.String(255))
    emotion_scores = db.Column(db.String(255))

# Use the SQLAlchemy inspect() method to check if the table already exists in the database.
# If it does not exist, create it using db.create_all().
with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table('table_name'):
        db.create_all()