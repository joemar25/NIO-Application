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
from project.forms import EntryForm, RecordForm
from project.scripts.rules import Validation

class Routes:
        
    @app.route("/")
    def index():
        """
        This is the index function where we only redirect to home page if called.

        Args:
            None.

        Returns:
            __template__: 'home' for '/home'
        """
        return redirect(url_for("home"))

    @app.route("/home", methods=['GET', 'POST'])
    def home():
        """
        Where the home page of the users will see.

        Args:
            None.

        Returns:
            __template__: 'home' for '/home'
        
        Function:
            Manage form and it's validation to be put inside the db
        """
        
        # if database not exist then create
        if not exists('./instance/' + db_name):
            db.create_all()

        # form instance is created for forms to render on page
        form = EntryForm()
        
        # if request is not post, just render page
        if request.method != "POST":
            return render_template("home.html", form=form)

        # [GET] all data in form is submit button is clicked
        user_name = form.username.data
        text = form.text_script.data
        
        """
        check if text script has no strings in it
            
        - if true; check file data then read text
        
        note: this statement will get the file and read it
                by decoding it using 'utf-8' for us to get the
                text data
        """
        if not text:
            file = form.file_script.data
            text = file.read().decode('utf-8')
            
        # add the text error if text is empty
        if not text:
            flash(f'{"no text script. try again"}', category='danger')
        
        # if true return all errors related to forms
        if not form.validate_on_submit():
            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(f'{err_msg}', category='danger')
            return render_template("home.html", form=form)

        # Validate text if passed or not
        if not Validation.is_valid_sentence(text):
            if text:
                flash(f'{"invalid script text. try again"}', category='danger')
            return render_template("home.html", form=form)
        
        # db management
        user = User(
            user_name = user_name,
            text = text
        )
        db.session.add(user)
        db.session.commit()
        
        # redirect to main page
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    def main():
        """
        This is loaded after we get the correct data from home page though form.

        Args:
            None.

        Returns:
            __template__: 'home' for '/home'
            
        Function:
            Manage database and session of the user
        """
        query = User.query.order_by(-User.id).first()
        username = query.user_name
        text = query.text

        # (1) grammar checking on text
        
        # (2) do a validation for session
        
        # (3) ready for recording
        form = RecordForm()
        
        # if request is not post, just render page
        if request.method != "POST":
            return render_template("main.html", form=form)
        
        # return a template holding data
        return render_template("main.html", audio=audio_data)


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
