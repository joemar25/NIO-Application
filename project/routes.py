from project import app, db_name, db
from flask import render_template, redirect, url_for, request, jsonify
from os.path import exists
from project.models import User


class Routes:
    @app.route("/")
    def _():
        return redirect(url_for("home"))

    @app.route("/home", methods=['GET', 'POST'])
    def home():
        """
        ### home function, route('/home')
        - if request method is not post then just return a plain home.html
        - else redirect to the recording phrase
        Returns:
            _type_: _template_
        """

        # if database not exist then create
        if not exists('./instance/' + db_name):
            db.create_all()

        # if not post request just return a page
        if request.method != "POST":
            return render_template("home.html")

        # else get the username if exist else return error
        if request.form['username']:
            user_name = request.form['username']
        else:
            return render_template("home.html", error="username error. try again")

        # text validation --> assigning if one of them exist
        if request.form['text_script']:
            text = request.form['text_script']
        else:
            text = request.files['file_script']

        # if text empty then return error
        if not text:
            return render_template("home.html", error="no script text found. try again")

        # all fields are filled, we can now validate
        # !!!!!!!!!! todo VALIDATION
        # data is for jsonification
        data = {
            'user_name': user_name,
            'text': text
        }

        # save to database
        query_user = User(
            user_name=data['user_name'], text=data['text'], audio=None)
        db.session.add(query_user)
        db.session.commit()

        return jsonify(data)

    @app.route("/validate", methods=['GET', 'POST'])
    def validate():
        # return jsonify(data)
        return redirect(url_for("main"))

    @app.route("/main/<username>", methods=['GET', 'POST'])
    def main(username):
        return render_template("main.html", username=username, text="")

    @app.route("/feedback", methods=['GET'])
    def feedback():
        return render_template("feedback.html")

    @app.route("/loading")
    def loading():
        return render_template('loading.html')

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0
