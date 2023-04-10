import os, urllib, tempfile, io, platform

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
from project.scripts.emotion import emotion_detector, emotion_label
from project.scripts.fluency import fluency_detector

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
        scores = Score.query.filter_by(user_id=current_user.id).all()
        data = { 'form': form, 'scores': scores }
        return render_template("main.html", **data)

    @app.route('/upload', methods=['POST'])
    def upload():
        # file config
        file_name = request.files['audio'].filename

        # convert audio file to WAV format
        audio = AudioSegment.from_file(request.files['audio'], format="webm")
        audio = audio.set_frame_rate(44000) # 16000 -> 44000 sample rate
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
                emotion_labels="",
                emotion_scores=""
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

            t_text = to_text(audio_file_path, use_temp_folder=False)
            ct_text = grammar().correct(t_text)

            rate = rate_score(audio=audio_file_path, text=t_text, use_temp_folder=False)
            fluency_score = fluency_detector.filler_score(audio_file_path)
            grammar_score_val = grammar_score(t_text, ct_text)
            emo = emotion_detector.predict(audio=audio_file_path, use_temp_folder=False)
            emo_label = emotion_label(emo)
            
            if rate is None:
                flash("Error processing rate score", category='danger')
                return redirect(url_for("feedback"))

            emo_str = f"{emo_label['emotion1']},{emo_label['emotion2']},{emo_label['emotion3']}"
            emo_score_str = f"{emo_label['score1']},{emo_label['score2']},{emo_label['score3']}"

            current_score.rate = round(rate['score'], 1)
            current_score.grammar = round(grammar_score_val, 1)
            current_score.fluency = round(fluency_score, 1)

            current_audio.transcribed = t_text
            current_audio.ctranscribed = ct_text
            current_audio.emotion_labels = emo_str
            current_audio.emotion_scores = emo_score_str

            db.session.commit()
            os.remove(audio_file_path)
            flash("Result successfully updated", category='success')
            return redirect(url_for("feedback"))

        except Exception as e:
            flash(f"Error updating score. Error message: {str(e)}", category='danger')
            return redirect(url_for("feedback"))


    @app.route('/process_audio_fail', methods=['GET'])
    def process_audio_fail():
        flash("Error sending audio recording to server", category='danger')
        return redirect(url_for("main"))

    @app.route("/feedback", methods=['GET'])
    def feedback():
        try:
            score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
            audio = Audio.query.filter_by(score_id=score.id).order_by(Audio.id.desc()).first()

            emo_label = audio.emotion_labels
            emo_scores = audio.emotion_scores
            
            emotion_labels = emo_label.split(",")
            emotion_scores = emo_scores.split(",")
            
            data = {
                'rate': score.rate,
                'fluency': score.fluency,
                'grammar': score.grammar,
                'fluency': score.fluency,
                'average': round((score.rate + score.fluency + score.grammar) / 3, 1),
                'transcribed': audio.transcribed,
                'ctranscribed': audio.ctranscribed,
                'emo_label_1': emotion_labels[0],
                'emo_label_2': emotion_labels[1],
                'emo_label_3': emotion_labels[2],
                'emo_score_1': emotion_scores[0],
                'emo_score_2': emotion_scores[1],
                'emo_score_3': emotion_scores[2]
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
