from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project import app, db
from project.models import User, Score
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar import Grammar as grammar
from project.scripts.transcribe import to_text
from project.scripts.rate import rate_score
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
        
        # Get the current user's ID
        user_id = current_user.id

        # score history
        # all_score = Score.query.filter_by(user_id=user_id)
        all_score = {
            "rate": 93,
            "grammar": 66,
            "fluency": 55
        }

        # if all_score.count() == 0:
        #     print("No scores found")
        # else:
        #     print("Scores found")

        """
        todo, the problem here is the delay of database update for score
        resulting to AttributeError: 'NoneType' object has no attribute 'rate'
        """
        
        return render_template("main.html", form=form, score=all_score)

    @app.route('/upload', methods=['POST'])
    def upload():
        # Get the name of the uploaded file and save it to the temp data directory.
        temp_folder = "/project/temp_data/"
        temp_dir = os.getcwd() + temp_folder
        file_name = File.name() + '.wav'

        # Convert the uploaded file to a WAV file and save it to the temp data directory.
        audio = request.files['audio']
        audio = AudioSegment.from_file(audio, format="webm")
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio.export(os.path.join(temp_dir, file_name), format="wav")
        
        try:
            # Add the audio query to the database.
            audio_query = Score(
                user_id=current_user.id,
                audio=file_name,
                transcribed=to_text(file_name)
            )
            db.session.add(audio_query)
            db.session.commit()
        except:
            return jsonify({"success": False}), 500  # indicate failure with a 500 error

        return jsonify({"success": True})  # indicate success with a 200 OK response

    @app.route('/process_audio', methods=['GET'])
    def process_audio():
        
        # get current score and update
        current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
        
        # process: getting scores [rate, fluency, grammar]
        rate = rate_score(current_score.audio, current_score.transcribed)
        fluency = 88 # constant for now
        grammar = 78 # constant for now
        
        # update the values of the current score
        current_score.rate = round(rate['score'], 1)
        current_score.fluency = round(fluency, 1)
        current_score.grammar = round(grammar, 1)
        
        try:
            db.session.commit()
            return redirect(url_for("feedback"))
        except Exception as e:
            db.session.rollback()
            flash("error updating score: {}".format(str(e)), category='danger')
            return redirect(url_for("main"))

    # if audio fails in the javascript
    @app.route('/process_audio_fail', methods=['GET'])
    def process_audio_fail():
        flash("error sending audio recording to server. please try again.", category='danger')
        return redirect(url_for("main"))
    
    @app.route("/feedback", methods=['GET'])
    def feedback():
        try:
            # Query the database to get the current user's score
            current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()

            # Get average
            average = (current_score.rate + current_score.fluency + current_score.grammar) / 3

            # Render the template with the score and response time
            return render_template("feedback.html", score=current_score, average=round(average, 1))
        except Exception as e:
            flash(f"{e}", category='danger')
            return redirect(url_for("main")) 

    @app.route("/about")
    def about():
        """
        Displays the about page.
        """
        return render_template('about.html')
    
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
