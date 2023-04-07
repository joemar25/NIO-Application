import os, platform, firebase, urllib
from pydub import AudioSegment
from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project import app, db, mode
from project.models import User, Score, Audio
from project.forms import EntryForm, RecordForm
from project.scripts.helpers import Validation, File
from project.scripts.grammar import grammar_score, Grammar as grammar
from project.scripts.transcribe import to_text
from project.scripts.rate import rate_score
from project.scripts.emotion import emotion_detector

# firebase config
config = {
  'apiKey': "AIzaSyAAbWrX6aXoW5ykkFDEPDLl5BnqqMbBdKk",
  'authDomain': "nio-application.firebaseapp.com",
   "databaseURL": "gs://nio-application.appspot.com",
  'projectId': "nio-application",
  'storageBucket': "nio-application.appspot.com",
  'messagingSenderId': "738476225376",
  'appId': "1:738476225376:web:0e840888904b7891f4a405",
  'measurementId': "G-0PWN8WQ4CT"
}

config = firebase.initialize_app(config)
storage = config.storage()


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
        
        print("\n\n\n\nin home....\n\n\n\n")
        
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
        
        print("\n\n\n\nin main....\n\n\n\n")
        
        form = RecordForm()
        scores = Score.query.filter_by(user_id=current_user.id).all()
        data = { 'form': form, 'scores': scores }
        return render_template("main.html", **data)

    @app.route('/upload', methods=['POST'])
    def upload():

        print("\n\n\n\nin upload....\n\n\n\n")
        
        file_name = File.name() + '.wav'
        # Load audio from request and process it
        audio = request.files['audio']
        audio = AudioSegment.from_file(audio, format="webm")
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        cloud_path = 'recorded_audio/' + file_name
        audio_bytes = audio.raw_data
        storage.child(cloud_path).put(audio_bytes)
        
        t_text = to_text(cloud_path, use_temp_folder=False, use_cloud_storage=True)
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
        
        print("\n\n\n\nin processing audio....\n\n\n\n")
        
        try:
            current_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()

            if current_score is None:
                flash("Failed to load score table in database for current user", category='danger')
                return redirect(url_for("main"))

            audio = current_score.audio
            if audio is None:
                flash("Failed to load audio table in database for current score", category='danger')
                return redirect(url_for("main"))

            # read file
            cloud_path = 'recorded_audio/' + audio.audio_name
            audio_file = raw_file
            # need a validation for this file url if exist (filename check if same - integrity)
            url = storage.child(cloud_path).get_url(None)
            response = urllib.request.urlopen(url)
            audio = io.BytesIO(response.read())
            
            rate = rate_score(audio=audio, text=audio.transcribed, use_temp_folder=False, use_cloud_storage=True)
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
            flash("Result successfully updated", category='success')
            return redirect(url_for("feedback"))

        except Exception as e:
            
            print("\n\n\n\nin processing audio fail....\n\n\n\n")
            
            db.session.rollback()
            flash("Error updating score: {}".format(str(e)), category='danger')
            return redirect(url_for("main"))

    @app.route('/process_audio_fail', methods=['GET'])
    def process_audio_fail():
        
        print("\n\n\n\nin processing audio fail area....\n\n\n\n")
        
        flash("Error sending audio recording to server", category='danger')
        return redirect(url_for("main"))

    @app.route("/feedback", methods=['GET'])
    def feedback():
        
        print("\n\n\n\nin feedback....\n\n\n\n")
        
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
