# python packages
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
# our local packages
from models import helpers

# configurations - if error occurs, create a folder manually
UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = {'txt'}

# flask instance
app = Flask(__name__)
# destination folder when saving a flie
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# the maximum size of the file in bytes
# app.config['MAX_CONTENT-PATH']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SECRET_KEY'] = 'supersecretkey'

# helper instance
helper = helpers


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Routes:

    @app.route("/", methods=['GET', 'POST'])
    @app.route("/index", methods=['GET', 'POST'])
    def index():
        """
            # Index function in route ('/')
            - is the first page that the user will see
            - user can enter their name and the script for their speech
        """

        # use validation and error class from helper
        valid = helper.Validation

        # this is the containers of string that we will use later
        text = upload = user_name = ""

        # check if the request method use if Post
        if request.method == "POST":

            # get the request from the input file
            user_name = request.form['username']
            text = request.form['text_script']

            # check if the post request has the file part
            if 'file_script' in request.files:
                upload = request.files['file_script']

            """
                if the text and upload file is empty return as it is
                - good for starting the index file without anything on the input
            """
            if user_name == "" and text == "" and upload.filename == '':
                return {"error": "username and script text are not found. try again"}

            # if user_name is not empty but it is not valid return error message
            if not user_name == "" and not valid.name(user_name):
                return {"error": "username error. try again"}

            # we have our user_name now but no text file or text found
            if text == "" and upload.filename == '':
                return {"error": "no script text found. try again"}

            # our user_name is empty but we have something in our text fild or upload field
            if user_name == "" and (text != "" or not upload.filename != ""):
                return {"error": "no username found. try again"}

            """
                if text is empty but we have upload file
                check the file path and file exist
                if true proceed uploading it to our local storage
                - generate filname
                - and save as text
                else return with error
            """
            if text == "" and not upload.filename == "":

                # if the file uploaded is a file but not the allowed one (txt file only here)
                if upload and not allowed_file(upload.filename):
                    return {"error": "invalid file type. try again"}

                # save to path
                upload.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), app.config['UPLOAD_FOLDER'], secure_filename(upload.filename)))
                # generate filename
                filename = app.config['UPLOAD_FOLDER'] + \
                    "/" + secure_filename(upload.filename)

                # if the file does not exist
                if not os.path.isfile(filename):
                    return {"error": "file does not exist. try again"}

                # read the contents of file and set them on text variable
                with open(filename) as f:
                    text = f.read()

                if not valid.text(text):
                    return {"error": "text is too short. try again"}

            # if text is not empty but it is not valid return error message
            if not text == "" and not valid.text(text):
                return {"error": "script text is too short. try again"}

        # proceed with no error messages
        # redirect to a page together with these dictionary
        return {
            "user_name": user_name,
            "text_script": text
        }

    @ app.route("/show", methods=['POST'])
    def show():
        """
            # Show function with route ('/show')
            - get the name and the input text to display in the browswer
        """
        return 0

    @ app.route("/store", methods=['POST'])
    def store():
        """
            # Store function with route ('/store')
            - get the recorded file and store for processing
        """
        return 0

    @ app.route("/feedback", methods=['GET'])
    def feedback():
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

    @ app.route("/destroy", methods=['POST'])
    def destroy():
        return 0


if __name__ == "__main__":

    """
        port=8080 is important for us; when connecting to the client's frontent we will
        configure package.json and set the to "proxy": "http://127.0.0.1:8080" since we use
        8080 else just put the "proxy": "http://127.0.0.1:5000" since it is the default proxy
    """

    app.run(debug=True, threaded=True, host='localhost', port=8080)

    """
    try -> jsonify(__var)
    someday
    """
