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

from flask_login import UserMixin
from project import app, db
from datetime import datetime
# inspect import for out database if not exist on databse folder
from sqlalchemy import inspect

"""
Flask-login requires a User model with the following properties:

(1) has an is_authenticated() method that returns True if the user has provided valid credentials
(2) has an is_active() method that returns True if the user’s account is active
(3) has an is_anonymous() method that returns True if the current user is an anonymous user
(4) has a get_id() method which, given a User instance, returns the unique ID for that object

UserMixin class provides the implementation of this properties. Its the reason you can call for example
is_authenticated to check if login credentials provide is correct or not instead of having to write a
method to do that yourself.


We can use the fields here in 'current_user.field_name' to print or use the data in it.
"""


class User(db.Model, UserMixin):
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
    ctext = db.Column(
        'ctext',
        db.Text,
        nullable=True,
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

    audio = db.Column(
        'audio',
        db.Text,
        unique=True,
        nullable=False,
        default=None
    )

    transcribed = db.Column(
        'transcribed',
        db.Text,
        unique=False,
        nullable=False,
        default=None
    )

    rate = db.Column(
        'rate',
        db.Float(),
        unique=False,
        nullable=False,
        default=0
    )
    grammar = db.Column(
        'grammar',
        db.Float(),
        unique=False,
        nullable=False,
        default=0
    )
    fluency = db.Column(
        'fluency',
        db.Float(),
        unique=False,
        nullable=False,
        default=0
    )

    # str representation of the model
    def __repr__(self):
        return f"{self.rate} {self.grammar} {self.fluency}"


""""
use the inspect() method from SQLAlchemy's sqlalchemy.inspect module to check if a table exists in the database.

By doing this, you can avoid creating tables that already exist, which can prevent errors or data loss.
"""
with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table('table_name'):
        db.create_all()
