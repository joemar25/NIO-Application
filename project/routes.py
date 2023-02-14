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
from project.scripts.rules import Validation

# for file upload
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Validation.ALLOWED_EXTENSIONS
class Routes:
    @app.route("/")
    def index():
        return redirect(url_for("home"))

    @app.route("/home", methods=['GET', 'POST'])
    def home():
        # if database not exist then create
        if not exists('./instance/' + db_name):
            db.create_all()

        # form instance
        form = EntryForm()
        
        # if request is not post, just render page
        if request.method != "POST":
            return render_template("home.html", form=form)

        # get all data in form
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

        # Use trained data to determine the sentence is ok for the text
        
        # add to database
        user = User(user_name=user_name, text=text)
        db.session.add(user)
        db.session.commit()
        
        # redirect to main page
        # return render_template("home.html", form=form, username=user_name, text=text)
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    def main():
        query = User.query.order_by(-User.id).first()
        username = query.user_name
        text = query.text

        # grammar checking on text
        # ready for recording
        
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
