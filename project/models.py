"""

    MODELS
    - Contains all the Entities of our Database
    - All fields must be specified base on needs
    - Has relationship (ONE:User -> MANY:Score)
    - No need for dummy rows,
        since all will just be created automatically once
        the proceed with the correct information inside 'home'
    - the creation of database migration is automatically once
        we navigate through 'home' page
    - this Model uses db from '__init__'
    - this Model would be used inside the 'routes'

"""

from project import db
from datetime import datetime


class User(db.Model):
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True
    )
    user_name = db.Column(
        'user_name',
        db.String(length=21),
        unique=False,
        nullable=False
    )
    text = db.Column(
        'text',
        db.Text,
        nullable=False
    )
    audio = db.Column(
        'audio',
        db.Text,
        nullable=True,
        default=None
    )
    datetime = db.Column(
        'timestamp',
        db.DateTime,
        default=datetime.utcnow
    )

    # lazy means if not specified it then the sql alchemy will not
    # grab all the object of items in one shot
    scores = db.relationship("Score", backref="user", lazy=True)

    # def __repr__(self):
    # return '<User %r>' % self.username

    # str representation of the model
    def __repr__(self):
        return f"User: {self.user_name}\tText: {self.text}\tAudio: {self.audio}"


class Score(db.Model):
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True
    )

    # foreign key, using id of the user
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    rate = db.Column(
        'rate',
        db.Float(),
        unique=False,
        nullable=False
    )
    grammar = db.Column(
        'grammar',
        db.Float(),
        unique=False,
        nullable=False
    )
    fluency = db.Column(
        'fluency',
        db.Float(),
        unique=False,
        nullable=False
    )

    # str representation of the model
    def __repr__(self):
        return f"{self.rate} {self.grammar} {self.fluency}"
