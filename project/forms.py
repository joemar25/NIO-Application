from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import Length, ValidationError
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
    
    def validate_text_script(self, input) -> bool:
        """
        splitting result in world by world counting
        putting it to n  and  analyze
        n must be greater than 3
        and must be less than 5000
        """
        text = input.data
        split = text.split()
        n = len(split)
        if not (n > 3 and n < 5000):
            raise ValidationError('not a valid sentence for speech. try again')
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
        label="Script",
        validators=[
            Length(min=1),
        ]
    )
    file_script = FileField()
    submit = SubmitField(
        label="Proceed"
    )


class RecordForm(FlaskForm):
    pass
