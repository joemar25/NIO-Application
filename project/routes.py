import os
import io
import urllib
import tempfile
import json
import re

from functools import lru_cache
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from project import app, db, storage, mode
from project.models import User, Score, Audio
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation
from project.scripts.transcribe import to_text
from project.scripts.rate import rate
from project.scripts.emotion import emotion_detector, emotion_label
from project.scripts.grammar import grammar, grammar_score
from project.scripts.fluency import fluency_detector
from project.scripts.feedback import feedback

ALLOWED_EXTENSIONS = {'txt'}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@lru_cache(maxsize=None)
def get_user(user_id):
    return User.query.get_or_404(int(user_id))


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.context_processor
def inject_current_page():
    return dict(current_page=request.path)


def read_file(file):
    CHUNK_SIZE = 4096
    text_chunks = []
    while True:
        chunk = file.read(CHUNK_SIZE)
        if not chunk:
            break
        text_chunks.append(chunk)
    text = b''.join(text_chunks).decode('utf-8')
    if not is_safe_text(text):
        return ""
    return text


def is_safe_text(text):
    # Use regular expressions to check for potential malicious patterns
    patterns = [
        r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',
        r'<(?!\/?[\w\s"\':=\/\-])(?:[^>"\']|"(?:[^"]|\\")*"|\'(?:[^\']|\\\')*\')*>'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Routes:

    @app.route("/")
    @app.route("/index")
    def index():
        return redirect(url_for("getstarted"))

    @app.route("/welcome")
    def getstarted():
        return render_template("getstarted.html")

    @app.route("/home", methods=['GET', 'POST'])
    def login():
        logout_user()
        entry_form = EntryForm()

        if request.method != "POST":
            return render_template("home.html", form=entry_form)

        username = entry_form.username.data
        text = entry_form.text_script.data
        file = request.files.get('file_script')

        if not bool(text) and file and allowed_file(file.filename):
            text = read_file(file)
        else:
            flash(f'Please select a valid .txt file.', category='danger')
            return render_template("home.html", form=entry_form)

        if not Validation.is_valid_username(username):
            flash(f'Username must be at least 3 characters long.', category='danger')
            return render_template("home.html", form=entry_form)

        if not is_safe_text(text):
            flash(f'Invalid input detected.', category='danger')
            return render_template("home.html", form=entry_form)

        try:
            user = User(username=username, script=text)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("main"))

        except IntegrityError:
            flash(f'Username already exists.', category='danger')
            return render_template("home.html", form=entry_form)

    @app.route("/main", methods=['GET', 'POST'])
    @login_required
    def main():
        form = RecordForm()
        scores = Score.query.filter_by(user_id=current_user.id).all()

        # Perform a join operation to retrieve all audio entries and their associated scores
        audio_scores = db.session.query(Audio, Score).join(Score, Audio.score_id == Score.id).\
            filter(Audio.score_id.in_(
                [score.id for score in scores])).all()

        emotion_data = []
        attempt_count = 0

        for audio, score in audio_scores:
            # Calculate the overall score using the grammar, fluency, and rate attributes of the score
            overall_score = (
                score.grammar + score.fluency + score.rate) / 3

            # Split the emotion labels and scores from the current audio entry
            emo_labels = audio.emotion_labels.split(",")
            emo_scores = audio.emotion_scores.split(",")

            attempt_count += 1
            emotion_dict = {
                'overall_score': round(overall_score, 1),
                'attempts': attempt_count,
                'labels': emo_labels,
                'scores': emo_scores
            }
            emotion_data.append(emotion_dict)

        count = 0
        attempts_str = [0]
        rate_scores = [0]
        grammar_scores = [0]
        fluency_scores = [0]

        for score in scores:
            count += 1
            grammar_scores.append(score.grammar)
            fluency_scores.append(score.fluency)
            rate_scores.append(score.rate)
            attempts_str.append(f"Attempt {count}")

        chart_data = {
            "labels": attempts_str,
            "datasets": [
                {
                    "label": "Grammar",
                    "data": grammar_scores,
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1,
                    "color": "#FF6384",
                },
                {
                    "label": "Rate",
                    "data": rate_scores,
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1,
                    "color": "#36A2EB",
                    "hidden": "true"
                },
                {
                    "label": "Fluency",
                    "data": fluency_scores,
                    "backgroundColor": "rgba(255, 206, 86, 0.2)",
                    "borderColor": "rgba(255, 206, 86, 1)",
                    "borderWidth": 1,
                    "color": "#FFCE56",
                    "hidden": "true"
                }
            ]
        }

        chart_data_json = json.dumps(chart_data)
        return render_template("main.html", form=form, chart_data=chart_data_json, emotion_data=emotion_data)

    @app.route('/upload', methods=['POST'])
    def upload():
        # file config
        file_name = request.files['audio'].filename

        # convert audio file to WAV format
        audio = AudioSegment.from_file(request.files['audio'], format="webm")
        audio = audio.set_frame_rate(44000)
        audio = audio.set_channels(1)

        # write audio to a buffer
        with io.BytesIO() as buffer:
            audio.export(buffer, format="wav")
            buffer.seek(0)
            # store the audio file in Firebase Storage
            storage.child("recorded_audio/" + file_name).put(buffer.read())

        try:
            score_obj = Score(user_id=current_user.id)
            db.session.add(score_obj)
            db.session.commit()

            score = Score.query.order_by(Score.id.desc()).first()
            s_id = score.id if score else 1

            audio_obj = Audio(score_id=s_id, audio_name=file_name)
            db.session.add(audio_obj)
            db.session.commit()
        except Exception as e:
            return jsonify({"success": False}), 500
        return jsonify({"success": True})

    @app.route('/process_audio', methods=['GET'])
    def process_audio():
        try:
            current_score = Score.query.filter_by(
                user_id=current_user.id).order_by(Score.id.desc()).first()
            if current_score is None:
                flash(
                    "Failed to load score table in database for current user", category='danger')
                return redirect(url_for("main"))

            current_audio = current_score.audio
            if current_audio is None:
                flash(
                    "Failed to load audio table in database for current score", category='danger')
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

            rate_score_val = rate.rate_score(
                audio=audio_file_path, text=t_text, use_temp_folder=False)
            fluency_score = fluency_detector.filler_score(audio_file_path)
            grammar_score_val = grammar_score(t_text, ct_text)
            emo = emotion_detector.predict(
                audio=audio_file_path, use_temp_folder=False)
            emo_label = emotion_label(emo)

            if rate is None:
                flash("Error processing rate score", category='danger')
                return redirect(url_for("feedback"))

            emo_str = f"{emo_label['emotion1']},{emo_label['emotion2']},{emo_label['emotion3']}"
            emo_score_str = f"{emo_label['score1']},{emo_label['score2']},{emo_label['score3']}"

            current_score.rate = round(rate_score_val['score'], 1)
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
            # flash(f"Error updating score. Error message: {str(e)}", category='danger')
            return redirect(url_for("feedback"))

    @app.route('/process_audio_fail', methods=['GET'])
    def process_audio_fail():
        flash("Error sending audio recording to server", category='danger')
        return redirect(url_for("main"))

    @app.route("/feedback", methods=['GET'])
    def feedback():
        try:
            score = Score.query.filter_by(
                user_id=current_user.id).order_by(Score.id.desc()).first()
            audio = Audio.query.filter_by(
                score_id=score.id).order_by(Audio.id.desc()).first()

            emo_label = audio.emotion_labels
            emo_scores = audio.emotion_scores

            emotion_labels = emo_label.split(",")
            emotion_scores = emo_scores.split(",")

            # for feedback
            feedback.rate = score.rate
            feedback.fluency = score.fluency
            feedback.grammar = score.grammar

            scores = Score.query.filter_by(user_id=current_user.id).all()

            count = 0
            attempts_str = [0]
            rate_scores = [0]
            grammar_scores = [0]
            fluency_scores = [0]

            for s in scores:
                count += 1
                grammar_scores.append(s.grammar)
                fluency_scores.append(s.fluency)
                rate_scores.append(s.rate)
                attempts_str.append(f"Attempt {count}")

            chart_data = {
                "labels": attempts_str,
                "datasets": [
                    {
                        "label": "Grammar",
                        "data": grammar_scores,
                        "backgroundColor": "rgba(255, 99, 132, 0.2)",
                        "borderColor": "rgba(255, 99, 132, 1)",
                        "borderWidth": 1,
                        "color": "#FF6384",
                    },
                    {
                        "label": "Rate",
                        "data": rate_scores,
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 1,
                        "color": "#36A2EB",
                        "hidden": "true"
                    },
                    {
                        "label": "Fluency",
                        "data": fluency_scores,
                        "backgroundColor": "rgba(255, 206, 86, 0.2)",
                        "borderColor": "rgba(255, 206, 86, 1)",
                        "borderWidth": 1,
                        "color": "#FFCE56",
                        "hidden": "true"
                    }
                ]
            }

            # chart data
            chart_data_json = json.dumps(chart_data)

            # average and comment
            average = round(
                (score.rate + score.fluency + score.grammar) / 3, 1)
            if average >= 75:
                comment_on_average = "Excellent"
            elif average >= 50:
                comment_on_average = "Satisfactory"
            elif average > 25:
                comment_on_average = "Needs improvement"
            else:
                comment_on_average = "Poor"

            data = {
                'rate': score.rate,
                'fluency': score.fluency,
                'grammar': score.grammar,
                'fluency': score.fluency,
                'average': average,
                'comment_on_average': comment_on_average,
                'transcribed': audio.transcribed,
                'ctranscribed': audio.ctranscribed,
                'emo_label_1': emotion_labels[0],
                'emo_label_2': emotion_labels[1],
                'emo_label_3': emotion_labels[2],
                'emo_score_1': emotion_scores[0],
                'emo_score_2': emotion_scores[1],
                'emo_score_3': emotion_scores[2],
                'feedback_msg': feedback.feedback(),
                'chart_data': chart_data_json
            }

            # Perform a join operation to retrieve all audio entries and their associated scores
            audio_scores = db.session.query(Audio, Score).join(Score, Audio.score_id == Score.id).\
                filter(Audio.score_id.in_(
                    [score.id for score in scores])).all()

            emotion_data = []
            attempt_count = 0

            for audio, score in audio_scores:
                # Calculate the overall score using the grammar, fluency, and rate attributes of the score
                overall_score = (
                    score.grammar + score.fluency + score.rate) / 3

                # Split the emotion labels and scores from the current audio entry
                emo_labels = audio.emotion_labels.split(",")
                emo_scores = audio.emotion_scores.split(",")

                attempt_count += 1
                emotion_dict = {
                    'overall_score': round(overall_score, 1),
                    'attempts': attempt_count,
                    'labels': emo_labels,
                    'scores': emo_scores
                }
                emotion_data.append(emotion_dict)

            return render_template("feedback.html", **data, emotion_data=emotion_data)
        except Exception as e:
            # flash(f"Error getting feedback: {e}", category='danger')
            flash(f"Audio must be clear and must be at least 5 seconds.",
                  category='danger')
            return redirect(url_for("main"))

    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route("/help")
    def help():
        return render_template("help.html")

    @app.route("/test")
    def test():
        return render_template("temp.html")

    @app.route("/destroy", methods=['POST'])
    def destroy():
        logout_user()
        return redirect(url_for("index"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
