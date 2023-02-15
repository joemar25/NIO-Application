from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import ValidationError
from project.models import User

class EntryForm(FlaskForm):
    
    # custom validation - to upgrade
    def validate_username(self, input) -> bool:
        """
        name must be greater than 3
        and not longer than 20 characters

        need improvement incase, puro space nilagay
        """
        username = input.data
        input = username.replace(" ", "")
        n = len(input)
        if not (n > 2 and n < 21):
            raise ValidationError('username must be greater than 2 characters. try again')
        return

    def validate_file_script(self, input) -> bool:
        """
        """
        text = input.data
        return

    
    # fields
    username = StringField(
        label="Username"
    )

    text_script = TextAreaField(
        label="Text Script"
    )
    
    file_script = FileField(
        label="File Script"
    )
    
    submit = SubmitField(
        label="Proceed"
    )

class RecordForm(FlaskForm):
    record = SubmitField(
        label="Record"
    )
    
    stop = SubmitField(
        label="Stop"
    )

    script = TextAreaField(
        label="Script"
    )