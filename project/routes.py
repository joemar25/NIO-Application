import os, urllib, tempfile, io, platform # platform to know what system

from pydub import AudioSegment
from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project import app, db, storage, mode
from project.models import User, Score, Audio
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar import grammar_score, Grammar as grammar
from project.scripts.transcribe import to_text
from project.scripts.rate import rate_score
from project.scripts.emotion import emotion_detector

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(int(user_id))

@app.context_processor
def inject_current_page():
    return dict(current_page=request.path)

class Routes:

    @app.route("/")
    @app.route("/index")
    def index():
        return redirect(url_for("login"))

    @app.route("/home", methods=['GET', 'POST'])
    def login():
        print("in home....")
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
        print("main....")
        form = RecordForm()
        scores = Score.query.filter_by(user_id=current_user.id).all()
        data = { 'form': form, 'scores': scores }
        return render_template("main.html", **data)

    @app.route('/upload', methods=['POST'])
    def upload():
        print("uploading....")
        # file config
        file_name = request.files['audio'].filename

        # convert audio file to WAV format
        audio = AudioSegment.from_file(request.files['audio'], format="webm")
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)

        # write audio to a buffer
        with io.BytesIO() as buffer:
            audio.export(buffer, format="wav")
            buffer.seek(0)
            # store the audio file in Firebase Storage
            storage.child("recorded_audio/" + file_name).put(buffer.read())
        
        try:
            audio_obj = Audio(
                audio_name=file_name,
                transcribed="",
                ctranscribed="",
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
        print("processing audio....")
        try:
            current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
            if current_score is None:
                flash("Failed to load score table in database for current user", category='danger')
                return redirect(url_for("main"))

            current_audio = current_score.audio
            if current_audio is None:
                flash("Failed to load audio table in database for current score", category='danger')
                return redirect(url_for("main"))

            # retrieve audio
            cloud_path = 'recorded_audio/' + current_audio.audio_name
            url = storage.child(cloud_path).get_url(None)
            response = urllib.request.urlopen(url)
            audio_data = response.read()

            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(audio_data)
                audio_file_path = f.name

            # t_text = to_text(audio_file_path, use_temp_folder=False)
            # ct_text = grammar().correct(t_text)
            
            t_text = to_text(audio_file_path, use_temp_folder=False)
            ct_text = "sample correct"

            rate = rate_score(audio=audio_file_path, text=t_text, use_temp_folder=False)
            fluency_score = 85.0
            grammar_score_val = grammar_score(t_text, ct_text)
            
            print("transcribed text is =", t_text)
            # print("corrected transcribed text is =", ct_text)
            
            if rate is None:
                flash("Error processing rate score", category='danger')
                return redirect(url_for("feedback"))

            current_score.rate = round(rate['score'], 1)
            current_score.grammar = round(grammar_score_val, 1)
            current_score.fluency = round(fluency_score, 1)

            current_audio.transcribed = t_text
            current_audio.ctranscribed = ct_text

            db.session.commit()

            os.remove(audio_file_path)
            flash("Result successfully updated", category='success')
            return redirect(url_for("feedback"))

        except Exception as e:
            flash(f"Error updating score. Error message: {str(e)}", category='danger')
            return redirect(url_for("feedback"))


    @app.route('/process_audio_fail', methods=['GET'])
    def process_audio_fail():
        print("in processing audio fail....")
        flash("Error sending audio recording to server", category='danger')
        return redirect(url_for("main"))

    @app.route("/feedback", methods=['GET'])
    def feedback():
        print("in feedback....")
        try:
            score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
            audio = Audio.query.filter_by(score_id=score.id).order_by(Audio.id.desc()).first()

            data = {
                'rate': score.rate,
                'fluency': score.fluency,
                'grammar': score.grammar,
                'average': round((score.rate + score.fluency + score.grammar) / 3, 1),
                'transcribed': audio.transcribed,
                'ctranscribed': audio.ctranscribed
            }

            return render_template("feedback.html", **data)
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
        logout_user()
        return redirect(url_for("index"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
