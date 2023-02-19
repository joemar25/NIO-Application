from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from os.path import exists
from project import app, db_file, db
from project.models import User, Score
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar.gingerit import Grammar as grammar
from pydub import AudioSegment
import os

# session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Routes:

    @app.route("/")
    def index():
        # Redirect to the login page when someone accesses the root URL.
        return redirect(url_for("login"))

    @app.route("/home", methods=['GET', 'POST'])
    def login():
        # If the user is already logged in, log them out before logging in again.
        logout_user()
        form = EntryForm()

        # If the request method is not POST, render the login page.
        if request.method != "POST":
            return render_template("home.html", form=form)

        # Get the username and text script from the form.
        user_name = form.username.data
        text = form.text_script.data

        # If the text field is empty, try to read the text script from a file.
        if not text:
            file = form.file_script.data
            text = file.read().decode('utf-8')

        # If there is still no text script, show an error message.
        if not text:
            flash(f'{"no text script. try again"}', category='danger')

        # If the form did not pass validation, show error messages.
        if not form.validate_on_submit():
            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(f'{err_msg}', category='danger')
            return render_template("home.html", form=form)

        # If the script is invalid, show an error message.
        if not Validation.is_valid_sentence(text):
            if text:
                flash(f'{"invalid script text. try again"}', category='danger')
            return render_template("home.html", form=form)

        # Correct the script with gingerit.
        corrected_text = ""
        try:
            corrected = grammar(text)
            corrected_text = corrected.checkGrammar()
        except Exception:
            flash(f'{"invalid script. try again"}', category='danger')
            return render_template("home.html", form=form)

        # Add the user and their script to the database.
        user = User(
            user_name=user_name,
            text=text,
            ctext=corrected_text
        )
        db.session.add(user)
        db.session.commit()

        # Log in the user and redirect to the main page.
        user = User.query.order_by(-User.id).first()
        login_user(user)
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    @login_required
    def main():
        # Render the main page.
        form = RecordForm()
        return render_template("main.html", form=form)

    @app.route('/upload', methods=['POST'])
    def upload():
        # Get the name of the uploaded file and save it to the temp data directory.
        temp_dir = os.getcwd() + "/project/temp_data/"
        file_name = File.name() + '.wav'

        # Convert the uploaded file to a WAV file and save it to the temp data directory.
        audio = request.files['audio']
        audio = AudioSegment.from_file(audio, format="webm")
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio.export(os.path.join(temp_dir, file_name), format="wav")

        # Add the audio query to the database.
        audio_query = Score(
            user_id=current_user.id,
            audio=file_name,
            transcribed="No transcription yet."
        )
        db.session.add(audio_query)
        db.session.commit()

        return "Upload successful"

    @app.route("/feedback", methods=['GET'])
    def feedback():
        """
        Displays the feedback page.
        """
        return render_template("feedback.html")


    @app.route("/loading")
    def loading():
        """
        Displays the loading page.
        """
        return render_template('loading.html')


    @app.route("/help")
    def help():
        """
        Displays the help page.
        """
        return render_template("help.html")


    @app.route("/destroy", methods=['POST'])
    def destroy():
        """
        Destroys the user session and returns 0.
        """
        logout_user() # log the user out
        return redirect(url_for("index"))


    @app.errorhandler(404)
    def page_not_found(e):
        """
        Displays the 404 error page when a page is not found.
        """
        return render_template('404.html'), 404
