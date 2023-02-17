"""

    ROUTES
    - Contains all possible web url for our website
    - Provides error handling if url fails
    - Responsible for Query, Get, Request, and Data Manipulation 
    
    SESSION
        note: is great, since they were temporary.
              they're are stored in the web server
              and simple there for quick access of information
              of all diffirent pages of our website
        
        while user is in the website, they will use their own information
        to have their scores updated and gain more scores better and better
        
        but when they were about to change user or logout. their session
        will also end and the application is open for new user for new session

"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from os.path import exists
from project import app, db_name, db
from project.models import User
from project.forms import EntryForm, RecordForm
from project.scripts.rules import Validation
from project.scripts.grammar.gingerit_class import Grammar as grammar

# session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        return redirect(url_for("login"))

    @app.route("/home", methods=['GET', 'POST'])
    def login():
        """
        Where the home page of the users will see.

        Args:
            None.

        Returns:
            __template__: 'home' for '/home'
        
        Function:
            Manage form and it's validation to be put inside the db
        """
        
        # logout user if this page is accessed
        logout_user()
        
        # form instance is created for forms to render on page
        form = EntryForm()
        
        # if request is not post, just render page
        if request.method != "POST":
            return render_template("home.html", form=form)
        
        # if database not exist then create
        if not exists('./instance/' + db_name):
            db.create_all()

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
        
        # login the current user to the session
        user = User.query.order_by(-User.id).first()
        login_user(user)
        
        # redirect to main page
        return redirect(url_for("main"))

    @app.route("/main", methods=['GET', 'POST'])
    @login_required
    def main():
        form = RecordForm()

        # grammar check and correct
        text = grammar(current_user.text)
        cgrammar = text.checkGrammar()
        return render_template("main.html", text=cgrammar, form=form)

    @app.route("/rec_handler", methods=['POST'])
    @login_required
    def rec_handler():
        if request.method != "POST":
            return
        
        if request.form["status"] == "finished":
            rec_audio_path = request.form["rec_audio_path"]
        
        return ('', 204)
    
    @app.route("/feedback", methods=['GET'])
    def feedback():
        # no login required but has error message if user access this page with no login credentials
        return render_template("feedback.html")

    @app.route("/loading")
    def loading():
        return render_template('loading.html')

    @app.route("/help")
    def help():
        return render_template("help.html")

    @app.route("/destroy", methods=['POST'])
    def destroy():
        return 0
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
