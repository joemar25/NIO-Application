from project import db
from datetime import datetime


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_name = db.Column('user_name', db.String(80),
                          unique=False, nullable=False)
    text = db.Column('text', db.Text, nullable=False)
    audio = db.Column('audio', db.Text, nullable=True, default=None)
    datetime = db.Column('timestamp', db.DateTime,
                         default=datetime.utcnow)

    scores = db.relationship("Score", backref="user")

    # def __repr__(self):
    # return '<User %r>' % self.username

    # str representation of the model
    def __repr__(self):
        return f"User: {self.user_name}\tText: {self.text}\tAudio: {self.audio}"


class Score(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)

    # foreign key, using id of the user
    user_id = db.Column('user_id', db.Integer,
                        db.ForeignKey("user.id"), nullable=False)

    rate = db.Column('rate', db.Float(), unique=False, nullable=False)
    grammar = db.Column('grammar', db.Float(), unique=False, nullable=False)
    fluency = db.Column('fluency', db.Float(), unique=False, nullable=False)

    # str representation of the model
    def __repr__(self):
        return f"{self.rate} {self.grammar} {self.fluency}"
