"""
This program defines two classes, EntryForm and RecordForm, which are used to create forms for user input in a Flask application.
The EntryForm class represents a form with fields for username, text_script, and file_script, along with a submit button.
The RecordForm class represents a form with a single field, record, which is likely used to trigger a function for recording user voice or screen.
These classes inherit from FlaskForm, indicating their integration with the Flask web framework.
The program utilizes the wtforms library for form creation and flask_wtf for Flask integration.
The validation logic is implemented using custom validation methods and the ValidationError class from wtforms.validators.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import ValidationError


class EntryForm(FlaskForm):
    def validate_username(self, input) -> bool:
        """
        Validate that the username field is not empty and is between 3 and 20 characters long.
        """
        username = input.data
        input = username.replace(" ", "")
        n = len(input)
        if not (n > 2 and n < 21):
            raise ValidationError(
                'Username must be between 3 and 20 characters long.')
        return

    username = StringField(
        label="Username",
        render_kw={
            "placeholder": "Username",
            "id": "username-input",
            "maxlength": "10"
        }
    )

    text_script = TextAreaField(
        label="Text Script",
        render_kw={
            "placeholder": "Speech Here"
        }
    )

    file_script = FileField(
        label="File Script"
    )

    submit = SubmitField(
        label="Proceed"
    )


class RecordForm(FlaskForm):
    record = SubmitField()
