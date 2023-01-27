# for default configuration
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

# for forms
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Specify the destination folder
# app.config[‘MAX_CONTENT-PATH‘] Specifies the maximum size of the file in bytes
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SECRET_KEY'] = 'supersecretkey'


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")


class Routes:

    @app.route("/hello", methods=['GET', 'POST'])
    def hello():
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            return "File has been uploaded."
        return render_template("hello.html", form=form)

    @app.route("/", methods=['GET', 'POST'])
    @app.route("/index", methods=['GET', 'POST'])
    def index():
        """
            #### Index function in route ('/')
            - is the first page that the user will see
            - user can enter their name and the script for their speech
        """
        text = ""
        user_name = ""
        upload = ""

        if request.method == "POST":
            user_name = request.form['username']
            """
                - create a validation tester for:
                  text is too short
                  uploaded file texts is too short or token
            """
            text = request.form['text_script']
            upload = request.files['file_script']

            if text == "" and upload.filename != '':
                # upload.save(UPLOAD_FOLDER, secure_filename(upload.filename))
                upload.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), app.config['UPLOAD_FOLDER'], secure_filename(upload.filename)))
            else:
                return render_template("index.html", user_name=user_name, text_script=text)
        return render_template("index.html", user_name=user_name, text_script=text)

    @app.route("/store", methods=['POST'])
    def store():
        """
            #### Store function with route ('/store')
            - get the recorded file and store for processing
        """
        return 0

    @app.route("/feedback", methods=['GET'])
    def show():
        rate = 80
        grammar = 81
        fluency = 85
        emotion = "Joyful"
        feedback = "this is a sample feedback"

        return {
            "rate": rate,
            "grammar": grammar,
            "fluency": fluency,
            "emotion": emotion,
            "feedback": feedback
        }

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0


if __name__ == "__main__":
    # we are in development mode
    app.run(debug=True, threaded=True, host='localhost', port=8080)
