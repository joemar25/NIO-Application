# our local packages
from models import generator
from models import helpers
import os
from os.path import exists
# default
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


# flask instance
app = Flask(__name__)

# configurations - database
db_name = 'records.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


# configurations - file storage
UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = '../app/temp_data/text'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SECRET_KEY'] = os.urandom(24)

# instances
helper = helpers
file = generator.File


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _emptydir(directory: str):
    ''''
        used for chcking if directory exist or not
        - if not exist, then create one
        - else do nothing
    '''
    if not (directory and not directory.isspace()):
        return

    _path = ''
    for dir in directory.split('/'):
        _path += dir+'/'
        if os.path.isdir(_path) == False:
            os.mkdir(_path)


# classes/models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.Text, nullable=False)
    audio = db.Column(db.Text, nullable=True)

    scores = db.relationship("Score", backref="user")

    def __repr__(self):
        return '<User %r>' % self.username

    # str representation of the model
    def __str__(self):
        return f"{self.user_name} {self.text}"


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # foreign key, using id of the user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    rate = db.Column(db.Float(), unique=False, nullable=False)
    grammar = db.Column(db.Float(), unique=False, nullable=False)
    fluency = db.Column(db.Float(), unique=False, nullable=False)


class DB():
    @app.route('/test_db')
    def test_db():
        try:
            db.session.query(text('1')).from_statement(text('SELECT 1')).all()
            return '<h1>It works.</h1>'
        except Exception as e:
            # e holds description of the error
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is broken.</h1>'
            return hed + error_text


class Routes:

    @app.route("/")
    def _():
        return redirect(url_for("home"))

    @app.route("/home", methods=['GET', 'POST'])
    def home():
        """
        ### home function, route('/home')
        - if request method is not post then just return a plain home.html
        - else redirect to the recording phrase
        Returns:
            _type_: _template_
        """

        # if database not exist then create
        if not exists('./instance/'+db_name):
            db.create_all()

        # if not post request just return a page
        if request.method != "POST":
            return render_template("home.html")

        # else get the username if exist else return error
        if request.form['username']:
            user_name = request.form['username']
        else:
            return render_template("home.html", error="username error. try again")

        # text validation --> assigning if one of them exist
        if request.form['text_script']:
            text = request.form['text_script']
        else:
            text = request.files['file_script']

        # if text empty then return error
        if not text:
            return render_template("home.html", error="no script text found. try again")

        # all fields are filled, we can now validate
        data = {
            'user_name': user_name,
            'text': text
        }
        return jsonify(data)

    @app.route("/validate", methods=['GET', 'POST'])
    def validate():
        # return jsonify(data)
        return redirect(url_for("main"))

    @app.route("/main/<username>", methods=['GET', 'POST'])
    def main(username):
        return render_template("main.html", username=username, text="")

    @app.route("/feedback", methods=['GET'])
    def feedback():
        return render_template("feedback.html")

    @app.route("/loading")
    def loading():
        return render_template('loading.html')

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0


if __name__ == "__main__":

    """
        port=8080 is important for us; when connecting to the client's frontent we will
        configure package.json and set the to "proxy": "http://127.0.0.1:8080" since we use
        8080 else just put the "proxy": "http://127.0.0.1:5000" since it is the default proxy
    """
    # run app
    app.run(debug=True, threaded=True, host='localhost', port=8080)
    # clear screen
    os.system('cls')
