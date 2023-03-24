import os
from pydub import AudioSegment
from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project import app, db
from project.models import User, Score, Audio
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar import Grammar as grammar
from project.scripts.grammar import grammar_score
from project.scripts.transcribe import to_text
from project.scripts.rate import rate_score
from project.scripts.emotion import emotion_detector

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Routes:

    @app.route("/")
    def index():
        return redirect(url_for("login"))

    @app.route("/home", methods=['GET', 'POST'])
    def login():
        logout_user()
        entry_form = EntryForm()

        if request.method != "POST":
            return render_template("home.html", form=entry_form)

        username = entry_form.username.data
        text = entry_form.text_script.data

        if not bool(text):
            file = entry_form.file_script.data
            text = file.read().decode('utf-8')
            
        if not Validation.is_valid_username(username):
            if username:
                flash(f'invalid username. try again', category='danger')
            return render_template("home.html", form=entry_form)

        user = User(
            username=username,
            script=text,
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("main"))


    @app.route("/main", methods=['GET', 'POST'])
    @login_required
    def main():
        form = RecordForm()
        user_id = current_user.id

        all_score = Score.query.filter_by(user_id=user_id)

        return render_template("main.html", form=form, score=all_score)

    @app.route('/upload', methods=['POST'])
    def upload():
        temp_folder = "/project/temp_data/"
        temp_dir = os.getcwd() + temp_folder
        file_name = File.name() + '.wav'
        audio = request.files['audio']
        audio = AudioSegment.from_file(audio, format="webm")
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio.export(os.path.join(temp_dir, file_name), format="wav")

        t_text = to_text(file_name)
        ct_text = grammar().correct(t_text)

        try:
            audio_obj = Audio(
                audio_name=file_name,
                transcribed=t_text,
                ctranscribed=ct_text,
                emotion_labels="sad,happy,ok",
                emotion_scores="26.9,55.9,11.9"
            )
            score_obj = Score(
                user_id=current_user.id,
                rate=0,
                grammar=0,
                fluency=0,
                audio=audio_obj
            )

            db.session.add(audio_obj)
            db.session.add(score_obj)
            db.session.commit()
        except:
            return jsonify({"success": False}), 500
        return jsonify({"success": True})

    @app.route('/process_audio', methods=['GET'])
    def process_audio():
        try:
            current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()

            if current_score is None:
                flash("Failed to load score table in database for current user", category='danger')
                return redirect(url_for("main"))

            audio = current_score.audio
            if audio is None:
                flash("Failed to load audio table in database for current score", category='danger')
                return redirect(url_for("main"))

            rate = rate_score(audio=audio.audio_name, text=audio.transcribed, use_temp_folder=True)
            grammar = grammar_score(audio.transcribed, audio.ctranscribed)
            fluency = 85

            if rate is None:
                flash("Error processing rate score", category='danger')
                return redirect(url_for("feedback"))
            if grammar is None:
                flash("Error processing grammar score", category='danger')
                return redirect(url_for("feedback"))

            current_score.rate = round(rate['score'], 1)
            current_score.grammar = round(grammar, 1)
            current_score.fluency = round(fluency, 1)

            db.session.commit()
            flash("Score updated successfully", category='success')
            return redirect(url_for("feedback"))

        except Exception as e:
            db.session.rollback()
            flash("Error updating score: {}".format(str(e)), category='danger')
            return redirect(url_for("main"))

    @app.route('/process_audio_fail', methods=['GET'])
    def process_audio_fail():
        flash("Error sending audio recording to server. Please try again.", category='danger')
        return redirect(url_for("main"))

    @app.route("/feedback", methods=['GET'])
    def feedback():
        try:
            current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
            average = round((current_score.rate + current_score.fluency + current_score.grammar) / 3, 1)
            return render_template("feedback.html", score=current_score, average=average)
        except Exception as e:
            flash(f"Error getting feedback: {e}", category='danger')
            return redirect(url_for("main"))

    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route("/help")
    def help():
        return render_template("help.html")

    @app.route("/test")
    def test():
        return render_template("test_home.html")

    @app.route("/destroy", methods=['POST'])
    def destroy():
        logout_user() # log the user out
        return redirect(url_for("index"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
