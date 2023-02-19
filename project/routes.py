"""

    ROUTES
    - Contains all possible web url for our website
    - Provides error handling if url fails
    - Responsible for Query, Get, Request, and Data Manipulation 
    
    SESSION
        note: is great, since they were temporary.
              they're are stored in the web server
              and simple there for quick access of information
              of all diffirent pages of our website
        
        while user is in the website, they will use their own information
        to have their scores updated and gain more scores better and better
        
        but when they were about to change user or logout. their session
        will also end and the application is open for new user for new session

"""

from flask import render_template, redirect, url_for, flash, request, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from os.path import exists
from project import app, db_file, db
from project.models import User, Score
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar.gingerit import Grammar as grammar
from pydub import AudioSegment
import os

"""
todo, In Flask, is there a way to hide a @app.route from everyone but the app itself. My database can be seen from a url in JSON format
https://stackoverflow.com/questions/57173318/in-flask-is-there-a-way-to-hide-a-app-route-from-everyone-but-the-app-itself
dl punkt manually, and no need to download everytime we run -> run.app
"""

# session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# absolute path for export of the temporary data
temp_dir = os.path.abspath(os.getcwd()+"/project/temp_data/")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Routes:

    @app.route("/")
    def index():
        """
        This is the index function where we only redirect to home page if called.

        Args:
            None.

        Returns:
            __template__: 'home' for '/home'
        """
        return redirect(url_for("login"))

    @app.route("/home", methods=['GET', 'POST'])
    def login():
        """
        Where the home page of the users will see.

        Args:
            None.

        Returns:
            __template__: 'home' for '/home'

        Function:
            Manage form and it's validation to be put inside the db
        """
        # logout user if this page is accessed
        logout_user()

        # form instance is created for forms to render on page
        form = EntryForm()

        # if request is not post, just render page
        if request.method != "POST":
            return render_template("home.html", form=form)

        # [GET] all data in form is submit button is clicked
        user_name = form.username.data
        text = form.text_script.data

        """
        check if text script has no strings in it
            
        - if true; check file data then read text
        
        note: this statement will get the file and read it
                by decoding it using 'utf-8' for us to get the
                text data
        """

        if not text:
            file = form.file_script.data
            text = file.read().decode('utf-8')

        # add the text error if text is empty
        if not text:
            flash(f'{"no text script. try again"}', category='danger')

        # if true return all errors related to forms
        if not form.validate_on_submit():
            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(f'{err_msg}', category='danger')
            return render_template("home.html", form=form)

        # Validate text if passed or not
        if not Validation.is_valid_sentence(text):
            if text:
                flash(f'{"invalid script text. try again"}', category='danger')
            return render_template("home.html", form=form)

        corrected_text = ""
        try:
            # correcting the grammar
            corrected = grammar(text)
            corrected_text = corrected.checkGrammar()
        except Exception:
            flash(f'{"invalid script. try again"}', category='danger')
            return render_template("home.html", form=form)

        # db management
        user = User(
            user_name=user_name,
            text=text,
            ctext=corrected_text
        )
        db.session.add(user)
        db.session.commit()

        # login the current user to the session
        user = User.query.order_by(-User.id).first()
        login_user(user)

        # redirect to main page
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    @login_required
    def main():
        form = RecordForm()
        return render_template("main.html", form=form)

    @app.route('/upload', methods=['POST'])
    def upload():
        dir = "project/temp_data"
        if not os.path.exists(dir):
            os.makedirs(dir)

        temp_dir = os.getcwd() + "/project/temp_data/"
        file_name = File.name() + '.wav'

        audio = request.files['audio']
        audio = AudioSegment.from_file(audio, format="webm")

        # Convert the audio to WAV format
        # Set the frame rate to 16000 Hz (optional)
        audio = audio.set_frame_rate(16000)
        # Set the number of channels to 1 (optional)
        audio = audio.set_channels(1)

        # export audio file to our absolute path (temp_data)
        audio.export(os.path.join(temp_dir, file_name), format="wav")

        # db management
        audio_query = Score(
            user_id=current_user.id,
            audio=file_name,
            transcribed="No transciption yet."
        )
        db.session.add(audio_query)
        db.session.commit()

        return "Upload successful"

    @app.route("/feedback", methods=['GET'])
    def feedback():
        # no login required but has error message if user access this page with no login credentials
        return render_template("feedback.html")

    @app.route("/loading")
    def loading():
        return render_template('loading.html')

    @app.route("/help")
    def help():
        return render_template("help.html")

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
