from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import ValidationError

class EntryForm(FlaskForm):
    """
    A form used to enter a username and a text script or upload a script file
    """

    # custom validation - to upgrade
    def validate_username(self, input) -> bool:
        """
        Validate that the username field is not empty and is between 3 and 20 characters long.
        """
        username = input.data
        input = username.replace(" ", "")
        n = len(input)
        if not (n > 2 and n < 21):
            raise ValidationError('Username must be between 3 and 20 characters long.')
        return

    def validate_file_script(self, input) -> bool:
        """
        Add validation for the file_script field if needed.
        """
        text = input.data
        return
    
    # fields
    username = StringField(
        label="Username",
        render_kw={"placeholder": "Enter your Username"}
    )

    text_script = TextAreaField(
        label="Text Script",
        render_kw={"placeholder": "Speech Here"}
    )
    
    file_script = FileField(
        label="File Script"
    )
    
    submit = SubmitField(
        label="Proceed",
        render_kw={"data-tooltip-target":"tooltip-animation"}
    )


class RecordForm(FlaskForm):
    """
    A form used to record or stop recording audio.
    """
    record = SubmitField(
        label="Record"
    )