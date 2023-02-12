from flask import render_template, redirect, url_for, request, jsonify
from os.path import exists
from project import app, db_name, db
from project.models import User
from project.scripts.helper import Validation


class Routes:
    @app.route("/")
    def _():
        return redirect(url_for("home"))

    @app.route("/home")
    def home():
        return render_template("home.html")

    @app.route("/validate", methods=['GET', 'POST'])
    def validate():
        # if database not exist then create
        if not exists('./instance/' + db_name):
            db.create_all()

        # if not post request just return a page
        if request.method != "POST":
            return redirect(url_for("home"))

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
        validate = Validation

        if not validate.name(user_name):
            return render_template("home.html", error="not valid username. try again")

        if not validate.text(text):
            return render_template("home.html", error="not valid text. try again")

        # save to database
        query_user = User(
            user_name=user_name,
            text=text,
            audio=None
        )
        db.session.add(query_user)
        db.session.commit()

        # query
        id = User.query.order_by(-User.id).first().id

        # return to main/id
        return redirect(url_for("main", id=id))

    @app.route("/main/<int:id>", methods=['GET', 'POST'])
    def main(id: int):
        query = User.query.order_by(-User.id).first()
        username = query.user_name
        text = query.text

        # return a template holding data
        return render_template("main.html", username=username, text=text)

    @app.route("/feedback", methods=['GET'])
    def feedback():
        return render_template("feedback.html")

    @app.route("/loading")
    def loading():
        return render_template('loading.html')

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
