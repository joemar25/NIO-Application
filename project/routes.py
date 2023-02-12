"""

    ROUTES
    - Contains all possible web url for our website
    - Provides error handling if url fails
    - Responsible for Query, Get, Request, and Data Manipulation 

"""

from flask import render_template, redirect, url_for, request, jsonify, flash
from os.path import exists
from project import app, db_name, db
from project.models import User
from project.forms import EntryForm
from project.scripts.helper import Validation
import re

class Routes:
    @app.route("/")
    def _():
        return redirect(url_for("home"))

    @app.route("/home", methods=['GET', 'POST'])
    def home():
        # if database not exist then create
        if not exists('./instance/' + db_name):
            db.create_all()

        # form instance
        form = EntryForm()

        # else get the username if exist else return error
        if form.validate_on_submit():
            user_name = form.username.data

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'{err_msg}', category='danger')

        return render_template("home.html", form=form)
        # return redirect(url_for("main", id=id))

    # @app.route("/main/<int:id>", methods=['GET', 'POST'])
    # def main(id: int):
    #     query = User.query.order_by(-User.id).first()
    #     username = query.user_name
    #     text = query.text

    #     # return a template holding data
    #     return render_template("main.html", username=username, text=text)

    @app.route("/main", methods=['GET', 'POST'])
    def main():
        # return a template holding data
        return render_template("main.html", username="a", text="b")

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
