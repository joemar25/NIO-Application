# default
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
# our local packages
from models import helpers
from models import generator

# flask instance
app = Flask(__name__)

# configurations
UPLOAD_FOLDER = '../app/temp_data/text'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = '../app/temp_data/text'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SECRET_KEY'] = os.urandom(24)

# instances
helper = helpers
file = generator.File


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _emptydir(directory: str):
    ''''
        used for chcking if directory exist or not
        - if not exist, then create one
        - else do nothing
    '''
    if not (directory and not directory.isspace()):
        return

    _path = ''
    for dir in directory.split('/'):
        _path += dir+'/'
        if os.path.isdir(_path) == False:
            os.mkdir(_path)


class Routes:

    @app.route("/", methods=['GET', 'POST'])
    @app.route("/index", methods=['GET', 'POST'])
    def index():
        """
        ### index function, route('/index')
        - if request method is not post then just return a plain index.html
        - else redirect to the recording phrase
        Returns:
            _type_: _template_
        """

        """
        ### index function, route('/index')
        - if request method is not post then just return a plain index.html
        - else redirect to the recording phrase
        Returns:
            _type_: _template_
        """

        # if not post request just return a page
        if request.method != "POST":
            return render_template("index.html")

        # else get the username if exist else return error
        if request.form['username']:
            user_name = request.form['username']
        else:
            return render_template("index.html", error="username error. try again")

        # text validation --> assigning if one of them exist
        if request.form['text_script']:
            text = request.form['text_script']
        else:
            text = request.files['file_script']

        # if text empty then return error
        if not text:
            return render_template("index.html", error="no script text found. try again")

        # all fields are filled, we can now validate

        data = {
            'user_name': user_name,
            'text': text
        }
        return jsonify(data)

    @app.route("/validate", methods=['GET', 'POST'])
    def validate():
        # return jsonify(data)
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    def main():
        return render_template("main.html")

    @app.route("/feedback", methods=['GET'])
    def show():
        return 0

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0


if __name__ == "__main__":

    """
        port=8080 is important for us; when connecting to the client's frontent we will
        configure package.json and set the to "proxy": "http://127.0.0.1:8080" since we use
        8080 else just put the "proxy": "http://127.0.0.1:5000" since it is the default proxy
    """

    app.run(debug=True, threaded=True, host='localhost', port=8080)
    os.system('cls')
