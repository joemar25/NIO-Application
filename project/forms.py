"""
This code defines two classes `EntryForm` and `RecordForm` that inherit from `FlaskForm` and are used to create forms for user input. 
The `EntryForm` class has three fields: `username`, `text_script`, and `file_script`, and a submit button `submit`. The `username` field is a string field that requires a value between 3 and 20 characters. The `text_script` field is a text area field that allows the user to enter a text script. The `file_script` field is a file field that allows the user to upload a script file.
The `RecordForm` class has only one field: `record`, which is a submit button. This class is likely used to trigger a function to record the user's voice or screen.
This code uses the `wtforms` library for form creation and `flask_wtf` for Flask integration. The `ValidationError` class is used to handle validation errors.
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
            "placeholder": "Username'",
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
