import os
from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from pydub import AudioSegment
from project import app, db
from project.models import User, Score
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar import Grammar as grammar
from project.scripts.grammar import grammar_score
from project.scripts.transcribe import to_text
from project.scripts.rate import rate_score

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

        if not bool(text):
            flash(f'no text script. try again', category='danger')

        if not entry_form.validate_on_submit():
            error_messages = ', '.join([str(x) for x in entry_form.errors.values()])
            flash(f'{error_messages}', category='danger')
            return render_template("home.html", form=entry_form)

        if not Validation.is_valid_sentence(text):
            if text:
                flash(f'invalid script text. try again', category='danger')
            return render_template("home.html", form=entry_form)

        try:
            corrected_text = grammar(text).checkGrammar()
        except Exception:
            flash(f'invalid script. try again', category='danger')
            return render_template("home.html", form=entry_form)

        user = User(
            user_name=username,
            text=text,
            ctext=corrected_text
        )
        db.session.add(user)
        db.session.commit()

        user = User.query.order_by(-User.id).first()
        login_user(user)
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    @login_required
    def main():
        form = RecordForm()
        user_id = current_user.id

        # all_score = Score.query.filter_by(user_id=user_id)
        all_score = {"rate": 93, "grammar": 66, "fluency": 55}

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
        
        try:
            audio_query = Score(
                user_id=current_user.id,
                audio=file_name,
                transcribed=to_text(file_name)
            )
            db.session.add(audio_query)
            db.session.commit()
        except:
            return jsonify({"success": False}), 500

        return jsonify({"success": True}) 

    @app.route('/process_audio', methods=['GET'])
    def process_audio():
        current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
        rate = rate_score(current_score.audio, current_score.transcribed)
        grammar = grammar_score(current_score.transcribed, current_user.ctext)
        fluency = 85

        current_score.rate = round(rate['score'], 1)
        current_score.grammar = round(grammar, 1)
        current_score.fluency = round(fluency, 1)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("error updating score: {}".format(str(e)), category='danger')
            return redirect(url_for("main"))
        finally:
            db.session.close()

        return redirect(url_for("feedback"))

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

    @app.route("/destroy", methods=['POST'])
    def destroy():
        logout_user() # log the user out
        return redirect(url_for("index"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
